#!/usr/bin/env python

import os.path

#path = os.getcwd()
currentdir = os.curdir

from chameleon import PageTemplateLoader
templates = PageTemplateLoader(os.path.join(currentdir, "sprites/nml"), format='text')


from dict_test import vehicles_dict
#print vehicles_dict

class Truck:
    """Base class for all types of trucks"""
    def __init__(self, id, properties):
      self.id = id
      self.properties = properties
      
    def output(self):
      template = templates['test_1.pt']
      return template(vehicle=self)

objects=[]


for i in vehicles_dict:
  objects.append(Truck(id=i,properties=vehicles_dict[i]))

"""  
for i in objects:
  print i.properties['title']
"""

master_template = templates['bandit.tnml']

#compile a single final nml file for the grf (currently c pre-processor is still available and used, so pnml file) 
bandit_nml = open('sprites/nml/bandit.pnml','w')
bandit_nml.write(master_template())
bandit_nml.close()

#compile strings to single lang file (english only at the moment, but i8n translation is possible)
local_strings = open('lang/english.lng.in').read()
lang = open('lang/english.lng', 'w')
lang.write(local_strings)
lang.close()
