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
    
    def render(self):
      return self.id

class Truck:
    """Base class for all types of trucks"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties
      self.trailers = [] # note that order of trailers here doesn't matter as we'll finally build them using the identifiers 
      # !! this template assigning business might be redundant if one template serves for all trucks 
      if properties['truck_type'] == 'GLOBAL_TRUCK_TYPE_SOLO':
        pass # currently just part of error checking - no special stuff needed for solo trucks 
      elif properties['truck_type'] == 'GLOBAL_TRUCK_TYPE_FIFTH_WHEEL' or properties['truck_type'] == 'GLOBAL_TRUCK_TYPE_DRAWBAR':        
        for i in properties['trailers_properties']:
          self.trailers.append(Trailer(id=i,properties=properties['trailers_properties'][i]))
      else: 
        print "Error from " + os.path.basename(__file__)+ ": " + self.id + " has no valid value for truck_type"
        # ^ error handling truck_type might be over-engineering :P
        
    def render(self):
      self.template = templates['truck_template.tnml']
      return self.template(vehicle=self)


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