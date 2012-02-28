from pixa import render as pixarender
from pixa import PixaSequence, PixaSequenceCollection, PixaShiftColour
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
        deck_colour = 115,
        company_colour = 202,
    ),
    'cc_2' : dict ( 
        deck_colour = 75,
        company_colour = 84,
    ),
}
# pixel sequences
flatbed = [
    (0, 0, 'deck_colour'),      
]
stakes = [
    (0, 0, 133),      
    (0, 1, 21),      
]
coil_load = [
    (-1, 0, 3),          
    (0, 0, 4),          
    (1, 0, 3),          
    (2, 0, 3),
    (-2, 1, 3),
    (-1, 1, 4),
    (0 , 1, 1),
    (1, 1, 6),
    (2, 1, 5),
    (3, 1, 6),
    (-2, 2, 5),
    (-1, 2, 9),
    (0 , 2, 6),
    (1, 2, 8),
    (2, 2, 8),
    (3, 2, 10),
    (-2, 3, 6),
    (-1, 3, 7),
    (0 , 3, 3),
    (1, 3, 1),
    (2, 3, 6),
    (3, 3, 10),
    (-1, 4, 6),          
    (0, 4, 8),          
    (1, 4, 10),          
    (2, 4, 8),
]


key_colour_mapping_pass_1 = PixaSequenceCollection(
    sequences = {
         94 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]),
         93 : PixaSequence(points = stakes),
        141 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 1)]), #143-136 flatbed
        140 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 0)]), #143-136 flatbed
        139 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]), #143-136 flatbed
        165 : PixaSequence(points = [(0, 0, 'company_colour')], transforms = [PixaShiftColour(0, 255, -1)]),
    }
)
key_colour_mapping_pass_2 = PixaSequenceCollection(
    sequences = {
        190 : PixaSequence(points = coil_load),
    }
)
key_colour_mapping_pass_3 = PixaSequenceCollection(
    sequences = {
        191 : PixaSequence(points = coil_load),
    }
)
key_colour_mapping_pass_4 = PixaSequenceCollection(
    sequences = {
        195 : PixaSequence(points = [(0, 0, 'company_colour')]),
        197 : PixaSequence(points = stakes),
    }
)    
def hide_or_show_drawbar_dolly_wheels(connection_type):
    """ returns sequences to draw in dolly wheels for drawbar trailers, or mask them out with blue """
    if connection_type == 'drawbar':
        transform = None
    else:
        transform = PixaShiftColour(0, 255, -1)
        print 'not drawbar'        
    return PixaSequenceCollection(
        sequences = {
             49 : PixaSequence(points = [(0, 0, 19)], transforms = [transform]),
             48 : PixaSequence(points = [(0, 0, 18)], transforms = [transform]),
            230 : PixaSequence(points = [(0, 0, 5)], transforms = [transform]),
            229 : PixaSequence(points = [(0, 0, 4)], transforms = [transform]),
            228 : PixaSequence(points = [(0, 0, 3)], transforms = [transform]),
            227 : PixaSequence(points = [(0, 0, 2)], transforms = [transform]),
        }
    )
    

        
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
            row = pixarender(row, hide_or_show_drawbar_dolly_wheels(self.connection_type), colourset)
            row = pixarender(row, key_colour_mapping_pass_1, colourset)
            row = pixarender(row, key_colour_mapping_pass_2, colourset)
            row = pixarender(row, key_colour_mapping_pass_3, colourset)
            row = pixarender(row, key_colour_mapping_pass_4, colourset)
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
            print coloursets[variation.id]
            spritesheet.render(coloursets[variation.id])
            spritesheet.save(variation.id)