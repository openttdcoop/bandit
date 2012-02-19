from P import P
from pixa import render as render
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

SPRITEROW_HEIGHT = 40
SPRITEROW_START_Y = 10

# colour onstants
BODY = 10
CC_A = 202

# pixel sequences
# each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
# if colour values etc need to change for different load states etc, sequence needs to be returned from a def
def bulk_load(cargo_colour,load_offset): 
    return [P(0, load_offset, cargo_colour)]

body_outer = [
    P(0, 0, BODY),
    P(0, 1, CC_A), 
    P(0, 2, BODY), 
    P(0, 3, BODY), 
    P(0, 4, 13),
]
body_end   = [
    P(0, 0, BODY), 
    P(0, 1, CC_A), 
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

def key_colour_mapping(cargo,load_state):
    if load_state[0] == 'empty':
        cargo_or_empty = [P(0, 0, 19)] 
    else:
        cargo_or_empty = bulk_load(cargo_colour=bulk_cargos[cargo],load_offset=load_state[1])    
    return {
        209 : dict(seq = body_inner,  colour_shift =  0),
         90 : dict(seq = body_inner,  colour_shift =  1),
        238 : dict(seq = body_outer,  colour_shift =  0),
        243 : dict(seq = body_outer,  colour_shift = -1),
        244 : dict(seq = body_outer,  colour_shift =  2),
        240 : dict(seq = body_end,    colour_shift = -1),
        166 : dict(seq = body_end,    colour_shift =  1),
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
    Variation(id='cc1')
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
        
    def render(self):    
        for i, load_state in enumerate(load_states):
            row = self.floorplan.copy()
            row = render(row, key_colour_mapping(cargo=self.cid, load_state=load_state))
            start_y = i * SPRITEROW_HEIGHT
            end_y = (i+1) * SPRITEROW_HEIGHT            
            self.sprites.paste(row,(0, start_y, row.size[0], end_y))    
        
    def save(self, variation):
        length = '7_8' # !! hard coded var until this is figured out
        output_path = 'results/' + length + '_tipping_trailer_' + variation.id + '_' + self.cid + '.png' 
        self.sprites.save(output_path, optimize=True)


def render_and_save(input_image_path, spritesheet, cargo, load_state, load_offset):
    output_image_path = 'results/' + input_image_path.split('.png')[0] + '_tipper_' + cargo + '_' + load_state + '.png'            
    newspritesheet = render(spritesheet.copy(), key_colour_mapping(cargo=cargo, load_offset=load_offset))
    newspritesheet.save(output_image_path, optimize=1)        

def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, SPRITEROW_START_Y, floorplan.size[0], SPRITEROW_START_Y + SPRITEROW_HEIGHT))
    # get a palette
    palette = Image.open('palette_key.png').palette
    for variation in colour_variations:
        for cargo in bulk_cargos:
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette))
            
    for variation in colour_variations:
        for spritesheet in variation.spritesheets:
            spritesheet.render()
            spritesheet.save(variation)