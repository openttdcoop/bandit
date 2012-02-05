#!/usr/bin/env python

import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import codecs #used for writing files - more unicode friendly than standard open() module

from chameleon import PageTemplateLoader
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'), format='text')
lang_templates = PageTemplateLoader(os.path.join(currentdir, 'lang'), format='text')
docs_templates = PageTemplateLoader(os.path.join(currentdir,'docs'), format='text')


# the parser handles config file formats; provides a custom utility function for parsing to a list 
import ConfigParser

import re
pattern = re.compile('\\d+$') #regular expressions magic: pattern of digits
def config_option_to_list_of_ints(txt):
  result = [] # we always want at minimum an empty list here or other code will be sad
  for i in txt.split('|'):
    m = pattern.match(i)
    if m:
      result.append(int(i))
  return result

config = ConfigParser.RawConfigParser()
config.read(os.path.join(currentdir, 'src', 'BANDIT.cfg'))


# get the globals - however for using globals in templates, it's better for the template to use global_template.pt as a macro   
import global_constants # expose all constants for easy passing to templates

# get args passed by makefile
if len(sys.argv) > 1:
  repo_vars = {'repo_title' : sys.argv[1], 'repo_version' : sys.argv[2]}
else: # provide some defaults so templates don't explode when testing python script without command line args
  repo_vars = {'repo_title' : 'BANDIT - compiled without makefile', 'repo_version' : 1}
    
class Trailer(object):
  """Base class for trailers"""
  def __init__(self, i, truck):
    self.id = truck.id + '_trailer_' + str(i+1)
    self.trailer_capacity = int(truck.trailer_capacities[i])
    self.numeric_id = truck.numeric_id + i + 1
  
  def render(self, truck):
    template = templates['trailer_template.pynml']
    return template(trailer = self, truck = truck)

class Truck(object):
  """Base class for all types of trucks"""
  def __init__(self, id):
    self.id = id
    
    #setup properties for this vehicle
    self.refittable_classes = global_constants.standard_class_refits['default']['allow']
    self.non_refittable_classes = global_constants.standard_class_refits['default']['disallow']
    self.allowed_cargos = '' # ! unfinished
    self.disallowed_cargos = '' # ! unfinished
    self.truck_model_life = global_constants.model_lives[config.get(id, 'truck_model_life')]
    self.truck_vehicle_life = global_constants.vehicle_lives[config.get(id, 'truck_vehicle_life')]
    self.truck_type_as_num = global_constants.truck_type_nums[config.get(id, 'truck_type')]
    self.numeric_id = config.getint(id, 'numeric_id')
    self.truck_speed = config.getint(id, 'truck_speed')
    self.truck_buy_cost = config.getint(id, 'truck_buy_cost')
    self.truck_run_cost = config.getint(id, 'truck_run_cost')
    self.truck_power = config.getint(id, 'truck_power')
    self.trailer_graphics_files = config.get(id, 'trailer_graphics_files').split('|')
    self.truck_graphics_file = config.get(id, 'truck_graphics_file')
    self.title = config.get(id, 'title')
    self.fifth_wheel_truck_capacity_fraction = config.getfloat(id, 'fifth_wheel_truck_capacity_fraction')
    self.truck_weight = config.getint(id, 'truck_weight')
    self.truck_intro_date = config.getint(id, 'truck_intro_date')
    self.truck_type = config.get(id, 'truck_type')
    self.truck_num_trailers = config.getint(id, 'truck_num_trailers')
    self.truck_smoke_offset = config.getint(id, 'truck_smoke_offset')
    self.truck_capacity = config.getint(id, 'truck_capacity')  
    self.truck_length = config.getint(id, 'truck_length')
    self.trailer_capacities = config_option_to_list_of_ints(config.get(id, 'trailer_capacities'))

    if self.truck_type == 'fifth_wheel_truck':
      self.modify_capacities_fifth_wheel_trucks()
      
    # add trailer objects - will only be added if needed
    # order of trailers here doesn't matter as we'll finally build them based on the vehicle id
    self.trailers = []
    for i in range(0, self.truck_num_trailers):
      self.trailers.append(Trailer(i = i, truck = self))
      
    
  def modify_capacities_fifth_wheel_trucks(self):
    # fifth wheel trucks split part of the capacity of first trailer onto the truck, for TE reasons
    # the ratio is controlled by a decimal fraction defined as a property of the truck
    trailer_capacity = self.trailer_capacities[0]
    self.truck_capacity = truck_capacity = int(trailer_capacity * self.fifth_wheel_truck_capacity_fraction)
    self.trailer_capacities[0] = trailer_capacity - truck_capacity

    
  def get_total_consist_capacity(self):
    # used for the purchase menu
    capacity = self.truck_capacity
    capacity = capacity + sum([i.trailer_capacity for i in self.trailers])
    return capacity

  @classmethod
  def make_buy_menu_trailer_tree(cls,items):
    # this is a tree to recurse over an arbitrary number of trailers - used to set buy menu strings; thanks to Eddi for this   
    if len(items) == 0: # guard against zero length items which cause recursion to fail
      return "string(str_empty)"
    if len(items) == 1: 
      return "string(STR_BUY_MENU_TRAILER,%d,%d)"%items[0]
    return "string(STR_ONE_MORE_LINE,%s,%s)"%(cls.make_buy_menu_trailer_tree(items[:len(items)/2]), cls.make_buy_menu_trailer_tree(items[len(items)/2:]))
      
  def get_buy_menu_string(self):
    # this is an intricate function to set buy menu texts according to various truck properties :P
    from string import Template
    if self.truck_type == 'solo_truck': #this for testing only - needs additional property on trucks to set extra info strings  
      extra_type_info = 'express'
    else: 
      extra_type_info = 'heavy_duty'

    if self.truck_type == 'solo_truck':
      # for solo trucks, no need to calculate trailer capacites
      buy_menu_template = Template(
        "string(str_buy_menu_text, string(str_vehicle_type_${extra_type_info}), string(str_empty))"
      )
      return buy_menu_template.substitute(extra_type_info=extra_type_info)
    else:
      # for articulated trucks, we'll want the capacities
      trailer_details = []
      cumulative_capacity = 0
      # we get the capacities out of the config, not from the vehicle props (because fifth wheel trucks split capacity prop on first trailer with truck TE reasons)
      for i, x in enumerate (config_option_to_list_of_ints(config.get(self.id, 'trailer_capacities'))):
        cumulative_capacity = cumulative_capacity + x
        print self.id, i, cumulative_capacity
        trailer_details.append((cumulative_capacity, i+1))
      
      # for drawbar trucks we also show truck capacity with no trailers
      if self.truck_type == 'drawbar_truck':
        optional_truck_cap_info = 'string(STR_BUY_MENU_CAP_DRAWBAR_TRUCK,' + str(self.truck_capacity) + ')'
      else:
        optional_truck_cap_info = 'string(str_empty)'
      
      trailer_info = self.make_buy_menu_trailer_tree(trailer_details)
      buy_menu_template = Template(
        "string(str_buy_menu_text, string(str_vehicle_type_${extra_type_info}), string(str_buy_menu_consist_info,${optional_truck_cap_info},${trailer_info}))"
      )
      return buy_menu_template.substitute(
        extra_type_info=extra_type_info,
        optional_truck_cap_info = optional_truck_cap_info,
        trailer_info=trailer_info
      )


  def render(self):
    template = templates['truck_template.pynml']
    return template(
      vehicle = self,
    )


#compose vehicle objects into a list; order is not significant as numeric identifiers are used to build vehicles 
vehicles = [Truck(id=i) for i in config.sections()]


#compile a single final nml file for the grf 
master_template = templates['bandit.pynml']

bandit_nml = codecs.open(os.path.join('bandit.nml'),'w','utf8')
bandit_nml.write(master_template(vehicles=vehicles, repo_vars=repo_vars))
bandit_nml.close()


#compile strings to single lang file (english only at the moment, but i18n translation is possible)
lang_template = lang_templates['english.pylng']

lang = codecs.open(os.path.join('lang','english.lng'), 'w','utf8')
lang.write(lang_template(vehicles=vehicles, repo_vars=repo_vars))
lang.close()


#compile docs (english only at the moment, but i18n translation is possible)
docs_template = docs_templates['readme.pytxt']

docs = codecs.open(os.path.join('docs','readme.txt'), 'w','utf8')
docs.write(docs_template(repo_vars=repo_vars))
docs.close()