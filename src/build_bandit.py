#!/usr/bin/env python

import os.path

#path = os.getcwd()
currentdir = os.curdir

from chameleon import PageTemplateLoader
templates = PageTemplateLoader(os.path.join(currentdir, "sprites/nml"), format='text')
lang_templates = PageTemplateLoader(os.path.join(currentdir, "lang"), format='text')


from dict_test import vehicles_dict
#print vehicles_dict

class Trailer:
    """Base class for trailers"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties
    
    def render(self, truck):
      template = templates['trailer_template.tnml']
      return template(trailer=self, truck=truck)

class Truck:
    """Base class for all types of trucks"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties

      # add trailer objects - will only be added if needed
      # order of trailers here doesn't matter as we'll finally build them using numeric identifiers based on the vehicle id
      self.trailers = []
      for i in properties['trailers_properties']:
        self.trailers.append(Trailer(id=i,properties=properties['trailers_properties'][i]))
        
    def getTotalConsistCapacity(self):
      # used for the purchase menu
      capacity = self.properties['truck_capacity']
      capacity = capacity + sum([i.properties['trailer_capacity'] for i in self.trailers]) 
      return capacity
        
    def render(self):
      template = templates['truck_template.tnml']
      return template(vehicle=self)


vehicles=[]


for i in vehicles_dict:
  vehicles.append(Truck(id=i,properties=vehicles_dict[i]))

"""  
for i in vehicles:
  print i.output()
"""


#compile a single final nml file for the grf (currently c pre-processor is still available and used, so pnml file) 
master_template = templates['bandit.tnml']

bandit_nml = open('sprites/nml/bandit.pnml','w')
bandit_nml.write(master_template(vehicles=vehicles))
bandit_nml.close()

#compile strings to single lang file (english only at the moment, but i18n translation is possible)
lang_template = lang_templates['english.lng.in']

lang = open('lang/english.lng', 'w')
lang.write(lang_template(vehicles=vehicles))
lang.close()