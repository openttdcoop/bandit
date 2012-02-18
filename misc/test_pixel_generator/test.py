import os.path
currentdir = os.curdir
import sys
sys.path.append(os.path.join('gestalts')) # add to the module search path

import Image
import ImageDraw
from P import P

from gestalts import building

#input_image_path = 'test_input.png'
input_image_path = 'test_input_building.png'

spritesheet = Image.open(input_image_path)
spritesheetpx = spritesheet.load()
draw = ImageDraw.Draw(spritesheet)

def get_pixel_sequence(x, y, key_colour):
    key_map = gestalt.key_colour_mapping[key_colour]
    raw_sequence = key_map['seq']
    pixel_sequence = []
    for P in raw_sequence:
        pixel_sequence.append((x + P.dx, y - P.dy, P.colour + key_map['colour_shift']))
    return pixel_sequence

gestalt = building

colours = {} #used for debug
for x in range(spritesheet.size[0]):
  for y in range(spritesheet.size[1]):
    colour = spritesheetpx[x,y]
    if colour not in (0, 15, 255):
      colours[colour] = ''
    if spritesheetpx[x,y] in gestalt.key_colour_mapping.keys():
        seq = get_pixel_sequence(x, y, spritesheetpx[x,y])
        for sx, sy, scol in seq:
            draw.point([(sx, sy)], fill=scol)

output_image_path = 'a_test_building.png'
spritesheet.save(output_image_path, optimize=1)

print colours # debug: what colours did we find in this spritesheet?