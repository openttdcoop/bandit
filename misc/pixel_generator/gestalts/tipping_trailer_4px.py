from P import P
from pixa import render as pixarender
import Image

# set palette index for lightest colour of cargo; range for rest will be calculated automatically 
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
bulk_cargos = {
    'COAL' : 4,
    'IORE' : 77,
    'GRAI' : 67,
    'CLAY' : 117,
}  

# load states - values define y offset for drawing load (above floor)
# order needs to be predictable, so a dict won't do here
load_states = [
    ('empty', 0),
    ('load_1', 0),
    ('load_2', 2),
    ('load_3', 4),
]

# constants
SPRITEROW_HEIGHT = 40
FLOORPLAN_START_Y = 10

# colour sets
coloursets = {    
    'cc_1' : dict ( 
        body_colour = 10,
        company_colour = 202,
    ),
    'cc_2' : dict ( 
        body_colour = 84,
        company_colour = 202,
    ),
}
# pixel sequences
# each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
# if colour values etc need to change for different load states etc, sequence needs to be returned from a def
def bulk_load(cargo_colour,load_offset): 
    return [P(0, load_offset, cargo_colour)]

def body_outer(colour_set):
    c = colour_set
    return [
        P(0, 0, c['body_colour']),
        P(0, 1, c['company_colour']), 
        P(0, 2, c['body_colour']), 
        P(0, 3, c['body_colour']), 
        P(0, 4, 13),
    ]
def body_end(colour_set):
    c = colour_set
    return [
        P(0, 0, c['body_colour']), 
        P(0, 1, c['company_colour']), 
        P(0, 2, c['body_colour']), 
        P(0, 3, c['body_colour']), 
        P(0, 4, 13),
    ]
def body_inner(colour_set):
    c = colour_set
    return [
        P(0, 0, 16), 
        P(0, 1, 17), 
        P(0, 2, 18),
        P(0, 3, 19), 
        P(0, 4, 14),
    ]

def key_colour_mapping(cargo,load_state, colourset):
    if load_state[0] == 'empty':
        cargo_or_empty = [P(0, 0, 19)] 
    else:
        cargo_or_empty = bulk_load(cargo_colour=bulk_cargos[cargo],load_offset=load_state[1])    
    return {
        209 : dict(seq = body_inner(colourset),  colour_shift =  0),
         90 : dict(seq = body_inner(colourset),  colour_shift =  1),
        238 : dict(seq = body_outer(colourset),  colour_shift =  0),
        243 : dict(seq = body_outer(colourset),  colour_shift = -1),
        244 : dict(seq = body_outer(colourset),  colour_shift =  2),
        240 : dict(seq = body_end(colourset),    colour_shift = -1),
        166 : dict(seq = body_end(colourset),    colour_shift =  1),
        138 : dict(seq = cargo_or_empty, colour_shift = -3),
        139 : dict(seq = cargo_or_empty, colour_shift = -2),
        140 : dict(seq = cargo_or_empty, colour_shift = -1),
        141 : dict(seq = cargo_or_empty, colour_shift =  0),
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
    def __init__(self,cid, floorplan, palette):
        self.cid = cid # cargoid
        # create the new spritesheet (empty at this stage)
        self.spritesheet_width = floorplan.size[0]
        self.spritesheet_height = SPRITEROW_HEIGHT * (len(load_states))
        self.sprites = Image.new('P', (self.spritesheet_width, self.spritesheet_height))
        self.sprites.putpalette(palette)
        # store the floorplan
        self.floorplan = floorplan
        return None
        
    def render(self, colourset):    
        for i, load_state in enumerate(load_states):
            row = self.floorplan.copy()
            row = pixarender(row, key_colour_mapping(cargo=self.cid, load_state=load_state, colourset=colourset))
            start_y = i * SPRITEROW_HEIGHT
            end_y = (i+1) * SPRITEROW_HEIGHT            
            self.sprites.paste(row,(0, start_y, row.size[0], end_y))    
        
    def save(self, variation_id):
        length = '7_8' # !! hard coded var until this is figured out
        connection_type = 'fifth_wheel'
        output_path = 'results/' + length + '_tipping_trailer_' + connection_type + '_' + variation_id + '_' + self.cid + '.png' 
        self.sprites.save(output_path, optimize=True)


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + SPRITEROW_HEIGHT))
    # get a palette
    palette = Image.open('palette_key.png').palette
    for variation in colour_variations:
        for cargo in bulk_cargos:
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette))
            
        for spritesheet in variation.spritesheets:
            spritesheet.render(coloursets[variation.id])
            spritesheet.save(variation.id)