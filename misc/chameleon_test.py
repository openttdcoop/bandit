import os

path = os.getcwd()

from chameleon import PageTemplateLoader
templates = PageTemplateLoader(os.path.join(path, "templates"), format='text')

#from chameleon import PageTemplate


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
  
for i in objects:
  print i.output()

#master_template = templates['test_2.pt']
#print master_template(objects=objects)

#print {'a':'apple', 'b':'ball'}.items()
