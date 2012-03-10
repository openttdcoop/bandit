from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, pixamakeanifest
import Image
import common

gestalt_id = 'tipping_trailer'
input_image_path = common.INPUT_IMAGE_PATH

# set palette index for lightest colour of cargo; range for rest will be calculated automatically
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
cargos = {
    'COAL': 4,
    'IORE': 77,
    'GRAI': 67,
    'CLAY': 117,
    'GRVL': 22,
}

class LoadState:
    def __init__(self, name, yoffs):
        self.name = name
        self.yoffs = yoffs
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('empty', 0),
    LoadState('load_1', 0),
    LoadState('load_2', -2),
    LoadState('load_3', -4),
]

# constants
FLOORPLAN_START_Y = 10

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
def get_sc_cargo(cargo, load_state):
    # returns sequences with correct y offset for current load state
    bulk_load = [
        (0, 0, cargos[cargo])
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
    filename = filename.split('.png')[0]
    parts = filename.split('-')
    gestalt_full_id = parts[0]
    connection_type = parts[1]
    colourset = parts[2]
    length = parts[3]
    if len(parts) > 4:
        cargo = parts[4]
    else:
        cargo = None

    floorplan = Image.open(input_image_path)
    # slice out the floorplan needed for this gestalt
    floorplan = floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + common.SPRITEROW_HEIGHT))
    spritesheet = Spritesheet(
                    width=floorplan.size[0],
                    height=common.SPRITEROW_HEIGHT * (len(load_states)),
                    palette=common.DOS_PALETTE
                )

    spriterows = []
    for load_state in load_states:
        # spriterow holds data needed to render the row
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        spriterow['render_passes'] = [
            {'seq': common.hide_or_show_drawbar_dolly_wheels(connection_type), 'colourset': coloursets[colourset]},
            {'seq': sc_pass_1, 'colourset': coloursets[colourset]},
            {'seq': get_sc_cargo(cargo, load_state), 'colourset': coloursets[colourset]},
            {'seq': sc_pass_3, 'colourset': coloursets[colourset]},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(filename + '.png')
    spritesheet.save(output_path)
    print output_path


def create_all_filenames(filename):
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
                    {'seq' : get_sc_cargo(variation.cargo, load_state), 'colourset' : variation.colourset},
                    {'seq' : sc_pass_3, 'colourset' : variation.colourset},
                ]
                spriterows.append(spriterow)
            spritesheet.render(spriterows=spriterows)
            output_path = common.get_output_path(common.construct_filename(gestalt_id, variation))
            print output_path
            spritesheet.save(output_path)
            manifest_payload.append(output_path)

    pixamakeanifest(gestalt_id, manifest_payload)
