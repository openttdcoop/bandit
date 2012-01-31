#!/usr/bin/env python

import sys
sys.path.append('sprites/nml') # add to the module search path

import os.path

currentdir = os.curdir

from chameleon import PageTemplateLoader
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, "sprites/nml"), format='text')
lang_templates = PageTemplateLoader(os.path.join(currentdir, "lang"), format='text')


from BANDIT_vehicles_config import vehicles_dict

from template_globals import template_globals, standard_class_refits
#print template_globals


class Trailer:
    """Base class for trailers"""
    def __init__(self, i, truck):
      self.id = truck.id + '_trailer_' + str(i+1)
      self.properties = {
        'trailer_capacity' : int(truck.properties['trailer_capacities'][i]),
        'numeric_id' : truck.properties['numeric_id'] + i + 1,
      }
    
    def render(self, truck):
      template = templates['trailer_template.tnml']
      return template(trailer=self, truck=truck)

class Truck:
    """Base class for all types of trucks"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties      

      #setup refits
      self.properties['refittable_classes'] = standard_class_refits['default']['allow']
      self.properties['non_refittable_classes'] = standard_class_refits['default']['disallow']

      if self.properties['truck_type'] == "GLOBAL_TRUCK_TYPE_FIFTH_WHEEL":
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
      return template(vehicle=self)


#compose vehicle objects into a list; order is not significant as numeric identifiers used to build vehicles 
vehicles=[]
for i in vehicles_dict:
  vehicles.append(Truck(id=i,properties=vehicles_dict[i]))


#compile a single final nml file for the grf (currently c pre-processor is still available and used, so pnml file) 

master_template = templates['bandit.tnml']

bandit_nml = open('sprites/nml/bandit.pnml','w')
bandit_nml.write(master_template(vehicles=vehicles,))
bandit_nml.close()


#compile strings to single lang file (english only at the moment, but i18n translation is possible)
lang_template = lang_templates['english.lng.in']

lang = open('lang/english.lng', 'w')
lang.write(lang_template(vehicles=vehicles))
lang.close()