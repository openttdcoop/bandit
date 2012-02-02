#!/usr/bin/env python

import sys
sys.path.append('sprites/nml') # add to the module search path

import os.path
currentdir = os.curdir

import codecs #used for writing files - more unicode friendly than standard open() module

from chameleon import PageTemplateLoader
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, "sprites/nml"), format='text')
lang_templates = PageTemplateLoader(os.path.join(currentdir, "lang"), format='text')
docs_templates = PageTemplateLoader(os.path.join(currentdir, "docs"), format='text')

from BANDIT_vehicles_config import vehicles_dict

# get the globals - however for using globals in templates, it's better for the template to use global_template.pt as a macro   
import global_constants # expose all constants for easy passing to templates
from global_constants import * #import all stuff from constants for easy reference in python scripts

# get args passed by makefile
if (len(sys.argv) > 1):
  repo_vars = {'repo_title' : sys.argv[1], 'repo_version' : sys.argv[2]}
else: # provide some defaults so templates don't explode when testing python script without command line args
  repo_vars = {'repo_title' : 'BANDIT - compiled without makefile', 'repo_version' : 1}
    
class Trailer:
    """Base class for trailers"""
    def __init__(self, i, truck):
      self.id = truck.id + '_trailer_' + str(i+1)
      self.properties = {
        'trailer_capacity' : int(truck.properties['trailer_capacities'][i]),
        'numeric_id'       : truck.properties['numeric_id'] + i + 1,
      }
    
    def render(self, truck):
      template = templates['trailer_template.tnml']
      return template(
        trailer = self, 
        truck = truck,
      )

class Truck:
    """Base class for all types of trucks"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties      

      #setup various properties that make use of global constants
      self.properties['refittable_classes'] = standard_class_refits['default']['allow']
      self.properties['non_refittable_classes'] = standard_class_refits['default']['disallow']
      self.properties['allowed_cargos'] = '' # ! unfinished
      self.properties['disallowed_cargos'] = '' # ! unfinished
      self.properties['truck_model_life'] = model_lives[properties['truck_model_life']]
      self.properties['truck_vehicle_life'] = vehicle_lives[properties['truck_vehicle_life']]
      self.properties['truck_type_as_num'] = truck_type_nums[properties['truck_type']]
      

      if self.properties['truck_type'] == "BANDIT_TRUCK_TYPE_FIFTH_WHEEL":
        self.modify_capacities_fifth_wheel_trucks()
      # add trailer objects - will only be added if needed
      # order of trailers here doesn't matter as we'll finally build them based on the vehicle id
      self.trailers = []
      for i in range(0, self.properties['truck_num_trailers']):
        self.trailers.append(Trailer(i = i, truck = self))

    def modify_capacities_fifth_wheel_trucks(self):
      # fifth wheel trucks split part of the capacity of first trailer onto the truck, for TE reasons
      # the ratio is controlled by a decimal fraction defined as a property of the truck
      trailer_capacity = self.properties['trailer_capacities'][0]
      self.properties['truck_capacity'] = truck_capacity = int(trailer_capacity * (self.properties['fifth_wheel_truck_capacity_fraction']))
      self.properties['trailer_capacities'][0] = trailer_capacity - truck_capacity
      
    def get_total_consist_capacity(self):
      # used for the purchase menu
      capacity = self.properties['truck_capacity']
      capacity = capacity + sum([i.properties['trailer_capacity'] for i in self.trailers]) 
      return capacity
        
    def render(self):
      template = templates['truck_template.tnml']
      return template(
        vehicle = self,
      )


#compose vehicle objects into a list; order is not significant as numeric identifiers used to build vehicles 
vehicles=[]
for i in vehicles_dict:
  vehicles.append(Truck(id=i,properties=vehicles_dict[i]))


#compile a single final nml file for the grf (currently c pre-processor is still available and used, so pnml file) 

master_template = templates['bandit.tnml']

bandit_nml = codecs.open('sprites/nml/bandit.pnml','w','utf8')
bandit_nml.write(master_template(vehicles=vehicles,repo_vars=repo_vars))
bandit_nml.close()


#compile strings to single lang file (english only at the moment, but i18n translation is possible)
lang_template = lang_templates['english.lng.in']

lang = codecs.open('lang/english.lng', 'w','utf8')
lang.write(lang_template(vehicles=vehicles,repo_vars=repo_vars))
lang.close()

#compile docs (english only at the moment, but i18n translation is possible)
docs_template = docs_templates['readme.ptxt']

docs = codecs.open('docs/readme.txt', 'w','utf8')
docs.write(docs_template(repo_vars=repo_vars))
docs.close()

