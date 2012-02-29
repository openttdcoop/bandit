from pixa import render as pixarender
from pixa import PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaMaskColour
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
        transform = PixaMaskColour(0)

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
    def __init__(self, colourset, cargo, connection_type):
        self.id = id
        self.spritesheets = []
        self.colourset = colourset
        self.cargo = cargo
        self.connection_type = connection_type

class Spritesheet:
    def __init__(self, floorplan, palette):
        # create the new spritesheet (empty at this stage)
        self.spritesheet_width = floorplan.size[0]
        self.spritesheet_height = SPRITEROW_HEIGHT * (len(load_states))
        self.sprites = Image.new('P', (self.spritesheet_width, self.spritesheet_height))
        self.sprites.putpalette(palette)
        # store the floorplan
        self.floorplan = floorplan
        return None
        
    def render(self, spriterows, render_passes):    
        for i, load_state in enumerate(spriterows):
            spriterow = self.floorplan.copy()
            for render_pass in render_passes:
                spriterow = pixarender(spriterow, render_pass[0], render_pass[1])                
            start_y = i * SPRITEROW_HEIGHT
            end_y = start_y + SPRITEROW_HEIGHT            
            self.sprites.paste(spriterow,(0, start_y, spriterow.size[0], end_y))    
        
    def save(self, output_path):
        self.sprites.save(output_path, optimize=True)


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + SPRITEROW_HEIGHT))
    # get a palette
    palette = Image.open('palette_key.png').palette
    variations = []
    for colourset in coloursets:
        for cargo in cargos:
            for connection_type in ('fifth_wheel','drawbar'):
                variation = Variation(colourset = colourset, cargo=cargo, connection_type='fifth_wheel')
                variation.spritesheets.append(Spritesheet(floorplan=floorplan, palette=palette))
                variations.append(variation)
                
    for variation in variations:                            
        for spritesheet in variation.spritesheets:
            print coloursets[variation.colourset]
            colourset = coloursets[variation.colourset]
            render_passes = [
                (hide_or_show_drawbar_dolly_wheels(variation.connection_type), colourset),
                (key_colour_mapping_pass_1, colourset),
                (key_colour_mapping_pass_2, colourset),
                (key_colour_mapping_pass_3, colourset),
                (key_colour_mapping_pass_4, colourset),
            ]
            spritesheet.render(spriterows=load_states, render_passes=render_passes)
            length = '7_8' # !! hard coded var until this is figured out
            output_path = 'results/' + length + '_flat_trailer_' + variation.connection_type + '_' + variation.colourset + '_' + variation.cargo + '.png' 
            print output_path
            spritesheet.save(output_path)