from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour
from pixa import Spritesheet
import Image
import common

gestalt_id = 'tipping_trailer'
floorplan_filename = 'tipping_body_floorplan.png'

# set palette index for lightest colour of cargo; range for rest will be calculated automatically
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
cargo_colours = {
    'black': 4,
    'iron_ore': 77,
    'corn_yellow': 67,
    'clay_pink': 117,
    'grey': 22,
}

class LoadState:
    def __init__(self, name, yoffs):
        self.name = name
        self.yoffs = yoffs
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('empty', 0),
    LoadState('load_1', -1),
    LoadState('load_2', -2),
    LoadState('load_3', -3),
    LoadState('load_4', -4),
]

# colour sets
coloursets = {
    'light_grey': dict (body_colour = 10, stripe_colour = common.CC1),
    'cc1': dict (body_colour = common.CC1, stripe_colour = 10),
    'cc2': dict (body_colour = common.CC2, stripe_colour = 10),
}
# colours
pc_body = PixaColour(name='body_colour', default=10)
pc_stripe = PixaColour(name='stripe_colour', default=common.CC1)

# pixel sequences
# x,y,colour (or colour object with optional shift)
body_outer = [
    (0, 0, pc_body()),
    (0, -1, pc_stripe()),
    (0, -2, pc_body()),
    (0, -3, pc_body()),
    (0, -4, 13),
]
body_end = [
    (0, 0, pc_body()),
    (0, -1, pc_stripe()),
    (0, -2, pc_body()),
    (0, -3, pc_body()),
    (0, -4, 13),
]
body_inner = [
    (0, 0, 16),
    (0, -1, 17),
    (0, -2, 18),
    (0, -3, 19),
    (0, -4, 14),
]

# sequence collections
sc_pass_1 = PixaSequenceCollection(
    sequences = {
         94 : PixaSequence(points = body_inner),
         93 : PixaSequence(points = body_inner, transforms = [PixaShiftColour(0, 255, 1)]),
    }
)

def get_sc_cargo(cargo_colour_id, load_state):
    # returns sequences with correct y offset for current load state
    if load_state.name == 'empty':
        cargo_colour = 19
    else:
        cargo_colour = cargo_colours[cargo_colour_id]

    bulk_load = [
        (0, 0, cargo_colour)
    ]
    return  PixaSequenceCollection(
        sequences = {
            141 : PixaSequence(points = bulk_load, transforms = [ PixaShiftDY(load_state.yoffs)]),
            140 : PixaSequence(points = bulk_load, transforms = [PixaShiftColour(0, 255, -1), PixaShiftDY(load_state.yoffs)]),
            139 : PixaSequence(points = bulk_load, transforms = [PixaShiftColour(0, 255, -2), PixaShiftDY(load_state.yoffs)]),
            138 : PixaSequence(points = bulk_load, transforms = [PixaShiftColour(0, 255, -3), PixaShiftDY(load_state.yoffs)]),
        }
    )

sc_pass_3 = PixaSequenceCollection(
    sequences = {
        197 : PixaSequence(points = body_outer, transforms = [PixaShiftColour(0, 255, 2)]),
        195 : PixaSequence(points = body_outer),
        194 : PixaSequence(points = body_outer, transforms = [PixaShiftColour(0, 255, -1)]),
        167 : PixaSequence(points = body_end, transforms = [PixaShiftColour(0, 255, 1)]),
        165 : PixaSequence(points = body_end, transforms = [PixaShiftColour(0, 255, -1)]),
    }
)

def generate(filename):
    gv = common.GestaltBodyVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=(len(load_states)))

    spriterows = []
    for load_state in load_states:
        # spriterow holds data needed to render the row
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        colourset = coloursets[gv.colourset_id]
        spriterow['render_passes'] = [
            {'seq': sc_pass_1, 'colourset': colourset},
            {'seq': get_sc_cargo(gv.cargo_colourset_id, load_state), 'colourset': colourset},
            {'seq': sc_pass_3, 'colourset': colourset},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png', common.INTERMEDIATES_PATH)
    spritesheet.save(output_path)
