print "running"

import os.path
currentdir = os.curdir
import sys
sys.path.append(os.path.join('gestalts')) # add to the module search path

from gestalts import tipping_trailer_4px
from gestalts import flat_trailer
from gestalts import tank_trailer
input_image_path = 'test_input.png'

#tipping_trailer_4px.generate(input_image_path)
#flat_trailer.generate(input_image_path)
#tank_trailer.generate(input_image_path)

print "done"