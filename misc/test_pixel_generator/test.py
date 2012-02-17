import Image
import ImageDraw
from random import choice

spritesheet = Image.open('test_input.png')
spritesheetpx = spritesheet.load()
draw = ImageDraw.Draw(spritesheet)

# global constants
body_colour = 10
cc_colour = 202

#each sequence is a tuple containing lists in format: [(x-offset,y-offset), colour]
body_outer = ([(0, 0), body_colour], [(0, 1), cc_colour], [(0, 2), body_colour], [(0, 3), body_colour], [(0, 4), 13])
body_end   = ([(0, 0), body_colour], [(0, 1), cc_colour], [(0, 2), body_colour], [(0, 3), body_colour], [(0, 4), 13])
body_inner = ([(0, 0), 16], [(0, 1), 17], [(0, 2), 18], [(0, 3), 19], [(0, 4), 14])
bulk_load_1 = ([(0, 2), 4],)

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

def get_pixel_sequence(x, y, key_colour):
    key_map = key_colour_mapping[key_colour]
    raw_sequence = key_map['seq']
    pixel_sequence = []
    for (dx,dy), col in raw_sequence:
        pixel_sequence.append((x + dx, y - dy, col + key_map['colour_shift']))
    return pixel_sequence

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

spritesheet.save('a_test_trailer.png')

print colours # debug: what colours did we find in this spritesheet?