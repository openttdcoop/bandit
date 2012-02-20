from P import P
from pixa import render as pixarender
import Image

# set palette index for lightest colour of cargo; range for rest will be calculated automatically 
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
cargos = {
    'STEL' : 4,
}  

# load states - values define y offset for drawing load (above floor)
# order needs to be predictable, so a dict won't do here
load_states = [
    ('empty', 0),
    ('load_1', 0),
    ('load_2', 0),
]

# constants
SPRITEROW_HEIGHT = 40
FLOORPLAN_START_Y = 90

# colour sets
coloursets = {    
    'cc_1' : dict ( 
        deck_colour = 108,
        company_colour = 202,
    ),
    'cc_2' : dict ( 
        deck_colour = 108,
        company_colour = 202,
    ),
}
# pixel sequences
# each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
# if colour values etc need to change for different load states etc, sequence needs to be returned from a def
def flatbed_nw_se(colour_set): 
    c = colour_set
    return [
        P(6, 2, c['company_colour']), 
        P(4, 2, c['deck_colour']-1), 
        P(4, 1, c['deck_colour']), 
        P(2, 1, c['deck_colour']+1), 
        P(2, 0, c['deck_colour']), 
        P(0, 0, c['company_colour']), 
    ]
def end_nw_se(colour_set): 
    c = colour_set
    return [
        P(6, 2, c['company_colour']+1), 
        P(4, 2, c['deck_colour']-1), 
        P(4, 1, c['company_colour']+1), 
        P(2, 1, c['deck_colour']+1), 
        P(2, 0, c['company_colour']+1), 
        P(0, 0, c['company_colour']), 
    ]
def flatbed_sw_ne(colour_set): 
    c = colour_set
    return [
        P(-6, 2, c['company_colour']-1), 
        P(-4, 2, c['deck_colour']-1), 
        P(-4, 1, c['deck_colour']), 
        P(-2, 1, c['deck_colour']+1), 
        P(-2, 0, c['deck_colour']), 
        P(0, 0, c['company_colour']), 
    ]
def end_sw_ne(colour_set): 
    c = colour_set
    return [
        P(-6, 2, c['company_colour']-1), 
        P(-4, 2, c['deck_colour']-1), 
        P(-4, 1, c['company_colour']-1), 
        P(-2, 1, c['deck_colour']+1), 
        P(-2, 0, c['company_colour']-1), 
        P(0, 0, c['company_colour']), 
    ]
def hide_or_show_drawbar_dolly_wheels(connection_type, colour, shift):
    if connection_type == 'drawbar':
        if colour == 231:
            return [P(0, 0, 19)]
        else:
            return [P(0, 0, 4 + shift)]
    else: 
        return [P(0, 0, 0)]

def key_colour_mapping(cargo, load_state, colourset, connection_type):
    return {
        45 : dict(seq = flatbed_nw_se(colourset), colour_shift = 0), #47-40 NW-SE
        40 : dict(seq = end_nw_se(colourset), colour_shift = 0), #47-40 NW-SE
        141 : dict(seq = flatbed_sw_ne(colourset), colour_shift = 0), #143-136 SW-NE
        136 : dict(seq = end_sw_ne(colourset), colour_shift = 0), #143-136 SW-NE
        231 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 231, 0), colour_shift =  0),
        230 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 230, 1), colour_shift =  0),
        229 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 229, -1), colour_shift =  0),
        228 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 228, -2), colour_shift =  0),
        227 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 227, -3), colour_shift =  0),
    }

class Variation:
    def __init__(self,id):
        self.id = id
        self.spritesheets = []

colour_variations = [
    Variation(id='cc_1'),
    Variation(id='cc_2'),
]

class Spritesheet:
    def __init__(self,cid, floorplan, palette, connection_type):
        self.cid = cid # cargoid
        # create the new spritesheet (empty at this stage)
        self.spritesheet_width = floorplan.size[0]
        self.spritesheet_height = SPRITEROW_HEIGHT * (len(load_states))
        self.sprites = Image.new('P', (self.spritesheet_width, self.spritesheet_height))
        self.sprites.putpalette(palette)
        # store the floorplan
        self.floorplan = floorplan
        self.connection_type = connection_type
        return None
        
    def render(self, colourset):    
        for i, load_state in enumerate(load_states):
            row = self.floorplan.copy()
            row = pixarender(row, key_colour_mapping(cargo=self.cid, load_state=load_state, colourset=colourset, connection_type=self.connection_type))
            start_y = i * SPRITEROW_HEIGHT
            end_y = (i+1) * SPRITEROW_HEIGHT            
            self.sprites.paste(row,(0, start_y, row.size[0], end_y))    
        
    def save(self, variation_id):
        length = '7_8' # !! hard coded var until this is figured out
        output_path = 'results/' + length + '_flat_trailer_' + self.connection_type + '_' + variation_id + '_' + self.cid + '.png' 
        self.sprites.save(output_path, optimize=True)


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + SPRITEROW_HEIGHT))
    # get a palette
    palette = Image.open('palette_key.png').palette
    for variation in colour_variations:
        for cargo in cargos:
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette, connection_type='fifth_wheel'))
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette, connection_type='drawbar'))
            
        for spritesheet in variation.spritesheets:
            spritesheet.render(coloursets[variation.id])
            spritesheet.save(variation.id)