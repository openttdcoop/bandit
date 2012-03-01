from pixa import PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaMaskColour, Spritesheet
import Image
import common

# set palette index for lightest colour of cargo; range for rest will be calculated automatically 
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
cargos = {
    'STEL' : 4,
}  

# load states - values define y offset for drawing load (above floor)
# order needs to be predictable, so a dict won't do here
load_states = [
    ('default', 0),
]

# constants
SPRITEROW_HEIGHT = 40
FLOORPLAN_START_Y = 50

# colour sets
coloursets = [   
    ('cc_1', dict (tank_colour = 202, stripe_colour = 21)),
    ('cc_2', dict (tank_colour = 84, stripe_colour = 21)),
    ('silver', dict (tank_colour = 20, stripe_colour = 202)),
    ('black', dict (tank_colour = 4, stripe_colour = 84)),
]
# pixel sequences
tank_far_end_sw_ne = [
        (0, 3, 'tank_colour', +2), 
        (0, 2, 'stripe_colour', +1), 
        (0, 1, 'tank_colour'), 
        (0, 0, 'tank_colour', -1), 
]
def tank_sw_ne(colour_set): 
    c = colour_set
    return [
        (-3, 5, 'tank_colour'), 
        (-2, 5, 'tank_colour', +1), 
        (-1, 5, 'tank_colour', +1), 
        (-1, 4, 'tank_colour', +2), 
        (0, 4, 'tank_colour', +3), 
        (0, 3, 'tank_colour', +2), 
        (0, 2, 'stripe_colour', +1), 
        (0, 1, 'tank_colour'), 
        (0, 0, 'tank_colour', -1), 
    ]
def tank_near_end_sw_ne(colour_set): 
    c = colour_set
    return [
        (-4, 4, 'tank_colour', -2), 
        (-4, 3, 'tank_colour', -3), 
        (-4, 2, 'tank_colour', -3), 
        (-3, 5, 'tank_colour', -1), 
        (-3, 4, 'tank_colour', -2), 
        (-3, 3, 'tank_colour', -2), 
        (-3, 2, 'tank_colour', -2), 
        (-3, 1, 'tank_colour', -3), 
        (-2, 4, 'tank_colour', -1), 
        (-2, 3, 'tank_colour', -2), 
        (-2, 2, 'tank_colour', -2), 
        (-2, 1, 'tank_colour', -2), 
        (-1, 4, 'tank_colour', -1), 
        (-1, 3, 'tank_colour', -2), 
        (-1, 2, 'tank_colour', -2), 
        (-1, 1, 'tank_colour', -2), 
        (-1, 0, 'tank_colour', -2), 
        (0, 3, 'tank_colour', -1), 
        (0, 2, 'tank_colour', -1), 
        (0, 1, 'tank_colour', -1), 
        (0, 0, 'tank_colour', -1), 
    ]
def tank_far_end_nw_se(colour_set): 
    c = colour_set
    return [
        (0, 3, 'tank_colour', +1), 
        (0, 2, 'stripe_colour'), 
        (0, 1, 'tank_colour', -1), 
        (0, 0, 'tank_colour', -2), 
    ]
def tank_nw_se(colour_set): 
    c = colour_set
    return [
        (3, 5, 'tank_colour']-1), 
        (2, 5, 'tank_colour']), 
        (1, 5, 'tank_colour']), 
        (1, 4, 'tank_colour']+1), 
        (0, 4, 'tank_colour']+2), 
        (0, 3, 'tank_colour']+1), 
        (0, 2, 'stripe_colour']), 
        (0, 1, 'tank_colour']-1), 
        (0, 0, 'tank_colour']-2), 
    ]
def tank_near_end_nw_se(colour_set): 
    c = colour_set
    return [
        (4, 4, 'tank_colour']+2), 
        (4, 3, 'tank_colour']+2), 
        (4, 2, 'tank_colour']+2), 
        (3, 5, 'tank_colour']+1), 
        (3, 4, 'tank_colour']+1), 
        (3, 3, 'tank_colour']+3), 
        (3, 2, 'tank_colour']+2), 
        (3, 1, 'tank_colour']+1), 
        (2, 4, 'tank_colour']+1), 
        (2, 3, 'tank_colour']+3), 
        (2, 2, 'tank_colour']+2), 
        (2, 1, 'tank_colour']+1), 
        (1, 4, 'tank_colour']+1), 
        (1, 3, 'tank_colour']+2), 
        (1, 2, 'tank_colour']+2), 
        (1, 1, 'tank_colour']+2), 
        (1, 0, 'tank_colour']+1), 
        (0, 3, 'tank_colour']+1), 
        (0, 2, 'tank_colour']+1), 
        (0, 1, 'tank_colour']+1), 
        (0, 0, 'tank_colour']+1), 
    ]
def tank_w_e(colour_set): 
    c = colour_set
    return [
        (0, 6, 'tank_colour']-1), 
        (0, 5, 'tank_colour']+1), 
        (0, 4, 'tank_colour']+2), 
        (0, 3, 'tank_colour']+1), 
        (0, 2, 'stripe_colour']), 
        (0, 1, 'tank_colour']-1), 
        (0, 0, 'tank_colour']-2), 
    ]
def tank_n_s(colour_set): 
    c = colour_set
    return [
        (7, 1, 'stripe_colour']+2), 
        (6, 2, 'tank_colour']+2), 
        (5, 2, 'tank_colour']+1), 
        (4, 2, 'tank_colour']), 
        (3, 2, 'tank_colour']-1), 
        (2, 2, 'tank_colour']-1), 
        (1, 2, 'tank_colour']-2), 
        (0, 1, 'tank_colour']-2), 
    ]
def tank_end_n_s(colour_set): 
    c = colour_set
    return [
        (6, 2, 'tank_colour']+1), 
        (5, 2, 'tank_colour']+2), 
        (4, 2, 'tank_colour']+1), 
        (3, 2, 'tank_colour']+1), 
        (2, 2, 'tank_colour']), 
        (1, 2, 'tank_colour']-1), 
        (7, 1, 'tank_colour']+1), 
        (6, 1, 'tank_colour']+1), 
        (5, 1, 'tank_colour']+1), 
        (4, 1, 'tank_colour']+1), 
        (3, 1, 'tank_colour']), 
        (2, 1, 'tank_colour']), 
        (1, 1, 'tank_colour']), 
        (0, 1, 'tank_colour']-1), 
        (6, 0, 'tank_colour']), 
        (5, 0, 'tank_colour']), 
        (4, 0, 'tank_colour']), 
        (3, 0, 'tank_colour']), 
        (2, 0, 'tank_colour']), 
        (1, 0, 'tank_colour']-1), 
        (0, 0, 2), 
    ]
def hide_or_show_drawbar_dolly_wheels(connection_type, colour, shift):
    if connection_type == 'drawbar':
        if colour in [49, 48]:
            return [P(0, 0, 19 + shift)]
        else:
            return [P(0, 0, 4 + shift)]
    else: 
        return [P(0, 0, 0)]

def key_colour_mapping(cargo, load_state, colourset, connection_type):
    return {
         47 : dict(seq = tank_far_end_nw_se(colourset), colour_shift = 0), #47-40 NW-SE
         45 : dict(seq = tank_nw_se(colourset), colour_shift = 0), #47-40 NW-SE
         44 : dict(seq = tank_nw_se(colourset), colour_shift = -1), #47-40 NW-SE
         40 : dict(seq = tank_near_end_nw_se(colourset), colour_shift = 0), #47-40 NW-SE
         92 : dict(seq = tank_n_s(colourset), colour_shift = -1), #88-95 N-S
         93 : dict(seq = tank_n_s(colourset), colour_shift = 0), #88-95 N-S
         94 : dict(seq = tank_end_n_s(colourset), colour_shift = 0), #88-95 N-S
        143 : dict(seq = tank_far_end_sw_ne(colourset), colour_shift = 0), #143-136 SW-NE
        141 : dict(seq = tank_sw_ne(colourset), colour_shift = 0), #143-136 SW-NE
        140 : dict(seq = tank_sw_ne(colourset), colour_shift = -1), #143-136 SW-NE
        136 : dict(seq = tank_near_end_sw_ne(colourset), colour_shift = 0), #143-136 SW-NE
        197 : dict(seq = tank_w_e(colourset), colour_shift = 1), #197-92 W-E
        195 : dict(seq = tank_w_e(colourset), colour_shift = 0), #197-92 W-E
        194 : dict(seq = tank_w_e(colourset), colour_shift = -1), #197-92 W-E
        192 : dict(seq = tank_w_e(colourset), colour_shift = -1), #197-92 W-E
        49 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 49, 0), colour_shift =  0),
        48 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 48, 0), colour_shift =  -1),
        230 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 230, 1), colour_shift =  0),
        229 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 229, 0), colour_shift =  0),
        228 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 228, -1), colour_shift =  0),
        227 : dict(seq = hide_or_show_drawbar_dolly_wheels(connection_type, 227, -2), colour_shift =  0),
    }

class Variation:
    def __init__(self,id):
        self.id = id
        self.spritesheets = []

colour_variations = [Variation(id=i) for i in coloursets]

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
        output_path = 'results/' + length + '_tank_trailer_' + self.connection_type + '_' + variation_id + '_' + self.cid + '.png' 
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