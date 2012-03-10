from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet
import Image
import common

gestalt_id = 'flat_trailer'
input_image_path = common.INPUT_IMAGE_PATH

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
]

# constants
FLOORPLAN_START_Y = 90

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
coil_load = [
    (-1, 0, 3),
    ( 0, 0, 4),
    ( 1, 0, 3),
    ( 2, 0, 3),
    (-2, -1, 3),
    (-1, -1, 4),
    ( 0, -1, 1),
    ( 1, -1, 6),
    ( 2, -1, 5),
    ( 3, -1, 6),
    (-2, -2, 5),
    (-1, -2, 9),
    ( 0, -2, 6),
    ( 1, -2, 8),
    ( 2, -2, 8),
    ( 3, -2, 10),
    (-2, -3, 6),
    (-1, -3, 7),
    ( 0, -3, 3),
    ( 1, -3, 1),
    ( 2, -3, 6),
    ( 3, -3, 10),
    (-1, -4, 6),
    ( 0, -4, 8),
    ( 1, -4, 10),
    ( 2, -4, 8),
]

# sequence collections
sc_pass_1 = PixaSequenceCollection(
    sequences = {
         94 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]),
         93 : PixaSequence(points = stakes),
        141 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 1)]), #143-136 flatbed
        140 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, 0)]), #143-136 flatbed
        139 : PixaSequence(points = flatbed, transforms = [PixaShiftColour(0, 255, -1)]), #143-136 flatbed
        165 : PixaSequence(points = [(0, 0, pc_cc1(-1))]),
    }
)
sc_pass_2 = PixaSequenceCollection(
    sequences = {
        190 : PixaSequence(points = coil_load),
    }
)
sc_pass_3 = PixaSequenceCollection(
    sequences = {
        191 : PixaSequence(points = coil_load),
    }
)
sc_pass_4 = PixaSequenceCollection(
    sequences = {
        195 : PixaSequence(points = [(0, 0, pc_cc1())]),
        197 : PixaSequence(points = stakes),
    }
)

def generate(filename):
    gv = common.GestaltVariation(filename)
    floorplan = common.get_floorplan(gv, FLOORPLAN_START_Y)
    spritesheet = common.make_spritesheet(floorplan, row_count=(len(load_states)))

    spriterows = []
    for load_state in load_states:
        # spriterow holds data needed to render the row
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        colourset = coloursets[gv.colourset_id]
        spriterow['render_passes'] = [
            {'seq': common.hide_or_show_drawbar_dolly_wheels(gv.connection_type), 'colourset': colourset},
            {'seq': sc_pass_1, 'colourset': colourset},
            {'seq': sc_pass_2, 'colourset': colourset},
            {'seq': sc_pass_3, 'colourset': colourset},
            {'seq': sc_pass_4, 'colourset': colourset},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png')
    spritesheet.save(output_path)

"""
def create_all_filenames(filename):
    length = '7' # !! hard coded var until this is figured out
    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + common.SPRITEROW_HEIGHT))
    # create variations containing empty spritesheets
    variations = []
    manifest_payload = []
    for set_name, colourset in coloursets:
        for cargo in cargos:
            for connection_type in ('fifth_wheel','drawbar'):
                variation = common.Variation(set_name=set_name, colourset=colourset, cargo=cargo, length=length, connection_type=connection_type)
                spritesheet = Spritesheet(
                    width=floorplan.size[0],
                    height=common.SPRITEROW_HEIGHT * (len(load_states)),
                    palette=common.DOS_PALETTE
                )
                variation.spritesheets.append(spritesheet)
                variations.append(variation)

    # render stage
    for variation in variations:
        for spritesheet in variation.spritesheets:
            spriterows = []
            for load_state in load_states:
                # spriterow holds data needed to render the row
                spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
                # add n render passes to the spriterow (list controls render order, index 0 = first pass)
                spriterow['render_passes'] = [
                    {'seq' : common.hide_or_show_drawbar_dolly_wheels(variation.connection_type), 'colourset' : variation.colourset},
                    {'seq' : sc_pass_1, 'colourset' : variation.colourset},
                    {'seq' : sc_pass_2, 'colourset' : variation.colourset},
                    {'seq' : sc_pass_3, 'colourset' : variation.colourset},
                    {'seq' : sc_pass_4, 'colourset' : variation.colourset},
                ]
                spriterows.append(spriterow)
            spritesheet.render(spriterows=spriterows)
            output_path = common.get_output_path(common.construct_filename(gestalt_id, variation))
            print output_path
            spritesheet.save(output_path)
            manifest_payload.append(output_path)
"""
