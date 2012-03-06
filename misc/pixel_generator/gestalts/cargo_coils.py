from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader 
from pixa import make_cheatsheet as make_cheatsheet
import Image
import common
import os.path
currentdir = os.curdir

cargos = {
    'STEL': 0, 
    'PAPR': 5,
    'COPR': 111,
}


class LoadState:
    def __init__(self, name, foo):
        self.name = name
        self.foo = foo # reminder that arbitrary attributes can be added to hold load state props
        
# load states - values define drawing parameters for the cargo to represent loading / loaded states
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('load_1', 0),
    LoadState('load_2', 0),
    LoadState('load_3', 0),
    LoadState('load_4', 0),
]

# constants
FLOORPLAN_START_Y = 10

# points
cargo_loader = PixaImageLoader(mask=(0,255))
coil_path = os.path.join(currentdir, 'input', 'test_coil.png')
coil_load = cargo_loader.make_points(coil_path, origin=(2,4))
#coil_sprite = cargo_loader.get_image(coil_path)
#make_cheatsheet(coil_sprite, os.path.join(currentdir, 'cheatsheets', file_name), origin=(2,4))

# sequence collections
sc_mask_out_template_guides = PixaSequenceCollection(
    sequences = {
         66 : PixaSequence(points = [(0, 0, common.COL_MASK)]),
         85 : PixaSequence(points = [(0, 0, common.COL_MASK)]),
        140 : PixaSequence(points = [(0, 0, common.COL_MASK)]),
        151 : PixaSequence(points = [(0, 0, common.COL_MASK)]),
        182 : PixaSequence(points = [(0, 0, common.COL_MASK)]),    
    }
)


def get_load_sequence(cargo, load_state):
    colour_shift_amount = cargos[cargo]
    return PixaSequenceCollection(
        sequences = {
            190 : PixaSequence(points = coil_load, transforms = [PixaShiftColour(0, 255, colour_shift_amount)]),
        }
    )


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # get a palette
    palette = Image.open('palette_key.png').palette
    # create variations containing empty spritesheets
    variations = []
    for cargo in cargos:
        for i in range(0,8):
            length = 8 - i
            # coloursets for these cargos are derived from the cargo and don't need storing on the Variation
            variation = common.Variation(set_name=None, colourset=None, cargo=cargo, length=length, connection_type='')
            # slice out the floorplan needed for this variation
            start_y = FLOORPLAN_START_Y + (i * common.SPRITEROW_HEIGHT)
            variation.attach_floorplan(floorplan.copy().crop((0, start_y, floorplan.size[0], start_y + common.SPRITEROW_HEIGHT)))
            spritesheet = Spritesheet(
                width=variation.floorplan.size[0],
                height=common.SPRITEROW_HEIGHT * (len(load_states)),
                palette=palette
            )
            variation.spritesheets.append(spritesheet)
            variations.append(variation)

    # render stage
    for variation in variations:
        for spritesheet in variation.spritesheets:
            spriterows = []
            for load_state in load_states:
                # spriterow holds data needed to render the row
                spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : variation.floorplan}
                # add n render passes to the spriterow (list controls render order, index 0 = first pass)
                spriterow['render_passes'] = [
                    {'seq' : sc_mask_out_template_guides, 'colourset' : None},
                    {'seq' : get_load_sequence(variation.cargo, load_state), 'colourset' : None},
                    {'seq' : get_load_sequence(variation.cargo, load_state), 'colourset' : None},
                    {'seq' : get_load_sequence(variation.cargo, load_state), 'colourset' : None},
                    {'seq' : get_load_sequence(variation.cargo, load_state), 'colourset' : None},
                ]
                spriterows.append(spriterow)
            spritesheet.render(spriterows=spriterows)
            gestalt_id = 'cargo_coils' 
            output_path = common.get_output_path(common.construct_filename(gestalt_id, variation))
            print output_path
            spritesheet.save(output_path)