from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader
from pixa import make_cheatsheet as make_cheatsheet
import Image
import common
import os.path
currentdir = os.curdir

gestalt_id = 'cargo_coils'

cargos = {
    'grey_metal': 0,
    'white': 5,
    'copper_metal': 111,
}


class LoadState:
    def __init__(self, name, show):
         # reminder that arbitrary attributes can be added to hold load state props
        self.name = name
        self.show = show

# load states - values define drawing parameters for the cargo to represent loading / loaded states
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('load_1', show=[190]),
    LoadState('load_2', show=[190]),
    LoadState('load_3', show=[190, 191]),
    LoadState('load_4', show=[190, 191]),
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
         66: PixaSequence(points=[(0, 0, common.COL_MASK)]),
         85: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        140: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        151: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        182: PixaSequence(points=[(0, 0, common.COL_MASK)]),
    }
)

def get_load_sequence(cargo, load_state):
    colour_shift_amount = cargos[cargo]
    magic_colours = [190, 191]
    sequences = {}
    for i in magic_colours:
        if i in load_state.show:
            sequences[i] = PixaSequence(points=coil_load, transforms=[PixaShiftColour(0, 255, colour_shift_amount)])
        else:
            sequences[i] = PixaSequence(points=[(0, 0, common.COL_MASK)])

    return PixaSequenceCollection(
        sequences = sequences
    )

def generate(filename):
    gv = common.GestaltCargoVariation(filename)
    floorplan = common.get_cargo_floorplan(gv, 'cargo_coils_floorplan.png', FLOORPLAN_START_Y)
    spritesheet = common.make_spritesheet(floorplan, row_count=(len(load_states)))

    spriterows = []
    for load_state in load_states:
        # spriterow holds data needed to render the row
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        spriterow['render_passes'] = [
            {'seq' : sc_mask_out_template_guides, 'colourset' : None},
            {'seq' : get_load_sequence(gv.colourset_id, load_state), 'colourset' : None},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png', common.INTERMEDIATES_PATH)
    spritesheet.save(output_path)
