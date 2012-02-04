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

from BANDIT_vehicles_config import vehicles_dict

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
    template = templates['trailer_template.tnml']
    return template(trailer = self, truck = truck)

class Truck(object):
  """Base class for all types of trucks"""
  def __init__(self, id, properties):
    self.id = id

    #setup various properties that make use of global constants
    self.refittable_classes = global_constants.standard_class_refits['default']['allow']
    self.non_refittable_classes = global_constants.standard_class_refits['default']['disallow']
    self.allowed_cargos = '' # ! unfinished
    self.disallowed_cargos = '' # ! unfinished
    self.truck_model_life = global_constants.model_lives[properties['truck_model_life']]
    self.truck_vehicle_life = global_constants.vehicle_lives[properties['truck_vehicle_life']]
    self.truck_type_as_num = global_constants.truck_type_nums[properties['truck_type']]

    self.numeric_id = properties['numeric_id']
    self.trailer_capacities = properties['trailer_capacities']
    self.truck_speed = properties['truck_speed']
    self.truck_buy_cost = properties['truck_buy_cost']
    self.truck_run_cost = properties['truck_run_cost']
    self.truck_power = properties['truck_power']
    self.trailer_graphics_files = properties['trailer_graphics_files']
    self.truck_graphics_file = properties['truck_graphics_file']
    self.title = properties['title']
    self.fifth_wheel_truck_capacity_fraction = properties['fifth_wheel_truck_capacity_fraction']
    self.truck_weight = properties['truck_weight']
    self.truck_intro_date = properties['truck_intro_date']
    self.truck_type = properties['truck_type']
    self.truck_num_trailers = properties['truck_num_trailers']
    self.truck_smoke_offset = properties['truck_smoke_offset']
    self.truck_capacity = properties['truck_capacity']  
    self.truck_length = properties['truck_length']  
    

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
    self.truck_capacity = truck_capacity = int(trailer_capacity * (self.fifth_wheel_truck_capacity_fraction))
    self.trailer_capacities[0] = trailer_capacity - truck_capacity

    
  def get_total_consist_capacity(self):
    # used for the purchase menu
    capacity = self.truck_capacity
    capacity = capacity + sum([i.trailer_capacity for i in self.trailers])
    return capacity
      
  def render(self):
    template = templates['truck_template.tnml']
    return template(
      vehicle = self,
    )


#compose vehicle objects into a list; order is not significant as numeric identifiers used to build vehicles 
vehicles = [Truck(id=i,properties=j) for i,j in vehicles_dict.iteritems()]

#compile a single final nml file for the grf (currently c pre-processor is still available and used, so pnml file) 
master_template = templates['bandit.tnml']

bandit_nml = codecs.open(os.path.join('bandit.nml'),'w','utf8')
bandit_nml.write(master_template(vehicles=vehicles,repo_vars=repo_vars))
bandit_nml.close()

#compile strings to single lang file (english only at the moment, but i18n translation is possible)
lang_template = lang_templates['english.lng.in']

lang = codecs.open(os.path.join('lang','english.lng'), 'w','utf8')
lang.write(lang_template(vehicles=vehicles,repo_vars=repo_vars))
lang.close()

#compile docs (english only at the moment, but i18n translation is possible)
docs_template = docs_templates['readme.ptxt']

docs = codecs.open(os.path.join('docs','readme.txt'), 'w','utf8')
docs.write(docs_template(repo_vars=repo_vars))
docs.close()