from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader
import Image
import common
import os.path
currentdir = os.curdir


gestalt_id = 'flat_trailer'
floorplan_filename = 'flat_trailer_floorplan.png'

# set palette index for lightest colour of cargo; range for rest will be calculated automatically
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
cargos = {
    'STEL' : 4,
}

class LoadState:
    def __init__(self, name, foo):
        self.name = name
        self.foo = foo # reminder that arbitrary attributes can be added to hold load state props
# load states - values define drawing parameters for the cargo to represent loading / loaded states
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('empty', 0),
    LoadState('load_1', 0),
    LoadState('load_2', 0),
    LoadState('load_3', 0),
    LoadState('load_4', 0),
]

# colour sets
coloursets = {
    'cc1': dict(deck_colour = 115, company_colour_1 = common.CC1),
    'cc2': dict(deck_colour = 75,  company_colour_1 = common.CC2),
}
# colours
pc_deck = PixaColour(name='deck_colour', default=115)
pc_cc1 = PixaColour(name='company_colour_1', default=common.CC1)

# pixel sequences
# x,y,colour (or colour object with optional shift)
flatbed = [
    (0, 0, pc_deck()),
]
stakes = [
    (0, 0, 133),
    (0, -1, 21),
]

# sequence collections
sc_body_pass_1 = PixaSequenceCollection(
    sequences = {
         94 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]),
         93 : PixaSequence(points = stakes),
        141 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 1)]), #143-136 flatbed
        140 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 0)]), #143-136 flatbed
        139 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]), #143-136 flatbed
        165 : PixaSequence(points = [(0, 0, pc_cc1(-1))]),
    }
)
sc_body_pass_2 = PixaSequenceCollection(
    sequences = {
        195 : PixaSequence(points = [(0, 0, pc_cc1())]),
        197 : PixaSequence(points = stakes),
    }
)

def get_cargo_load(cargo_path, load_state, increment):
    if load_state.name == 'empty':
        return PixaSequenceCollection(sequences={})
    else:
        cargo_loader = PixaImageLoader(mask=(0,255))
        crop_start_y = (increment - 1) * common.SPRITEROW_HEIGHT
        crop_end_y = crop_start_y + common.SPRITEROW_HEIGHT
        crop_box = (0, crop_start_y, common.CARGO_SPRITE_WIDTH, crop_end_y)
        cargo_load = cargo_loader.make_points(cargo_path, crop_box, origin=(0, 9))
        return PixaSequenceCollection(
            sequences = {
                226 : PixaSequence(points = cargo_load),
            }
        )


def generate(filename):
    gv = common.GestaltTrailerVariation(filename)
    floorplan = common.get_trailer_floorplan(gv, floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=(len(load_states)))
    cargo_filename = gv.cargo + '-' + gv.cargo_colourset_id + '-' + gv.length + '.png'
    print cargo_filename
    cargo_path = os.path.join(common.INTERMEDIATES_PATH, cargo_filename)

    spriterows = []
    for i, load_state in enumerate(load_states):
        # spriterow holds data needed to render the row
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        colourset = coloursets[gv.colourset_id]
        spriterow['render_passes'] = [
            {'seq': common.hide_or_show_drawbar_dolly_wheels(gv.connection_type), 'colourset': colourset},
            {'seq': sc_body_pass_1, 'colourset': colourset},
            {'seq': get_cargo_load(cargo_path, load_state, i), 'colourset': None},
            {'seq': sc_body_pass_2, 'colourset': colourset},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png')
    spritesheet.save(output_path)
