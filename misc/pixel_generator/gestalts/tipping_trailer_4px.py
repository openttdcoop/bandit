from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaMaskColour, Spritesheet
import Image
import common

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
FLOORPLAN_START_Y = 10

# colour sets
coloursets = [   
    ('light_grey', dict (body_colour = 10, stripe_colour = common.CC1)),
    ('cc_1', dict (body_colour = common.CC1, stripe_colour = 10)),
    ('cc_2', dict (body_colour = common.CC2, stripe_colour = 10)),
]
# colours
pc_body = PixaColour(name='body_colour', default=10)
pc_stripe = PixaColour(name='stripe_colour', default=common.CC1)

# pixel sequences
# x,y,colour (or colour object with optional shift)
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
def hide_or_show_drawbar_dolly_wheels(connection_type, colour, shift):
    if connection_type == 'drawbar':
        if colour == 231:
            return [P(0, 0, 19)]
        else:
            return [P(0, 0, 4 + shift)]
    else: 
        return [P(0, 0, 0)]

def key_colour_mapping(cargo, load_state, colourset, connection_type):
    if load_state[0] == 'empty':
        cargo_or_empty = [P(0, 0, 19)] 
    else:
        cargo_or_empty = bulk_load(cargo_colour=bulk_cargos[cargo],load_offset=load_state[1])    
    return {
         94 : dict(seq = body_inner(colourset),  colour_shift =  0),
         93 : dict(seq = body_inner(colourset),  colour_shift =  1),
        197 : dict(seq = body_outer(colourset),  colour_shift =  2),
        195 : dict(seq = body_outer(colourset),  colour_shift =  0),
        194 : dict(seq = body_outer(colourset),  colour_shift = -1),
        167 : dict(seq = body_end(colourset),    colour_shift =  1),
        165 : dict(seq = body_end(colourset),    colour_shift = -1),
        141 : dict(seq = cargo_or_empty, colour_shift =  0),
        140 : dict(seq = cargo_or_empty, colour_shift = -1),
        139 : dict(seq = cargo_or_empty, colour_shift = -2),
        138 : dict(seq = cargo_or_empty, colour_shift = -3),
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
        output_path = 'results/' + length + '_tipping_trailer_' + self.connection_type + '_' + variation_id + '_' + self.cid + '.png' 
        self.sprites.save(output_path, optimize=True)


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + SPRITEROW_HEIGHT))
    # get a palette
    palette = Image.open('palette_key.png').palette
    for variation in colour_variations:
        for cargo in bulk_cargos:
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette, connection_type='fifth_wheel'))
            spritesheet = variation.spritesheets.append(Spritesheet(cid=cargo, floorplan=floorplan, palette=palette, connection_type='drawbar'))
            
        for spritesheet in variation.spritesheets:
            spritesheet.render(coloursets[variation.id])
            spritesheet.save(variation.id)