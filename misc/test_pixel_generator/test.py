import Image
import ImageDraw
from random import choice

spritesheet = Image.open('test_input.png')
spritesheetpx = spritesheet.load()
draw = ImageDraw.Draw(spritesheet)


class P:
    """ simple class to hold the definition of a pixel that should be drawn """
    def __init__(self, dx, dy, colour):
        self.dx = dx
        self.dy = dy
        self.colour = colour

def get_pixel_sequence(x, y, key_colour):
    key_map = key_colour_mapping[key_colour]
    raw_sequence = key_map['seq']
    pixel_sequence = []
    for P in raw_sequence:
        pixel_sequence.append((x + P.dx, y - P.dy, P.colour + key_map['colour_shift']))
    return pixel_sequence



# global constants
BODY = 10
CC_A = 202
BULK_CARGO = 4  

#each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
body_outer = [
    P(0, 0, BODY),
    P(0, 1, CC_1), 
    P(0, 2, BODY), 
    P(0, 3, BODY), 
    P(0, 4, 13),
]
body_end   = [
    P(0, 0, BODY), 
    P(0, 1, CC_1), 
    P(0, 2, BODY), 
    P(0, 3, BODY), 
    P(0, 4, 13),
]
body_inner = [
    P(0, 0, 16), 
    P(0, 1, 17), 
    P(0, 2, 18),
    P(0, 3, 19), 
    P(0, 4, 14),
]
bulk_load_1 = [
    P(0, 2, BULK_CARGO),
]

key_colour_mapping = {
    209 : dict(seq = body_inner,  colour_shift =  0),
     90 : dict(seq = body_inner,  colour_shift =  1),
    238 : dict(seq = body_outer,  colour_shift =  0),
    243 : dict(seq = body_outer,  colour_shift = -1),
    244 : dict(seq = body_outer,  colour_shift =  2),
    240 : dict(seq = body_end,    colour_shift = -1),
    166 : dict(seq = body_end,    colour_shift =  1),
    138 : dict(seq = bulk_load_1, colour_shift = -3),
    139 : dict(seq = bulk_load_1, colour_shift = -2),
    140 : dict(seq = bulk_load_1, colour_shift = -1),
    141 : dict(seq = bulk_load_1, colour_shift =  0),
}

colours = {} #used for debug
for x in range(spritesheet.size[0]):
  for y in range(spritesheet.size[1]):
    colour = spritesheetpx[x,y]
    if colour not in (0, 15, 255):
      colours[colour] = ''
    if spritesheetpx[x,y] in key_colour_mapping.keys():
        seq = get_pixel_sequence(x, y, spritesheetpx[x,y])
        for sx, sy, scol in seq:
            draw.point([(sx, sy)], fill=scol)

spritesheet.save('a_test_trailer.png', optimize=1)

print colours # debug: what colours did we find in this spritesheet?