import os.path
currentdir = os.curdir

from chameleon import PageTemplateLoader
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir), format='text')

template = templates['example.pynml']
print template()
