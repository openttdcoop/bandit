from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader, pixamakeanifest
from pixa import make_cheatsheet as make_cheatsheet
import Image
import common
import os.path
currentdir = os.curdir

gestalt_id = 'cargo_tarps'

colourshifts = {
    'default': 0,
    'cc1': 52,
    'cc2': -66,
    'pinkish': -74,
    'greenish': -58,
}

class LoadState:
    def __init__(self, name, num_id):
         # reminder that arbitrary attributes can be added to hold load state props
        self.name = name
        self.num_id = num_id

# load states - values define drawing parameters for the cargo to represent loading / loaded states
# order needs to be predictable, so a dict won't do here
load_states = [
    LoadState('load_1',1),
    LoadState('load_2',2),
    LoadState('load_3',3),
    LoadState('load_4',4),
]

# constants
FLOORPLAN_START_Y = 10

# points
cargo_loader = PixaImageLoader(mask=(0,255))
load_sprites = {}
for spritename in ('large_tarp_1','large_tarp_2','large_tarp_3','large_tarp_4', 'small_tarp_1','small_tarp_2','small_tarp_3','small_tarp_4'):
    filename = spritename + '.png'
    tarp_path = os.path.join(currentdir, 'input', 'cargo_tarps', filename)
    load_sprites[spritename] = cargo_loader.make_points(tarp_path, origin=(2,4))
#tarp_sprite = cargo_loader.get_image(tarp_path)
#make_cheatsheet(tarp_sprite, os.path.join(currentdir, 'cheatsheets', filename), origin=(2,4))

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

def get_load_sequence(set_name, load_state):
    colour_shift_amount = colourshifts[set_name]
    magic_colours = {
        191: {'sprite':'large_tarp_1', 'load_states':(1,2,3,4)},
        190: {'sprite':'small_tarp_1', 'load_states':(3,4)},
        189: {'sprite':'large_tarp_2', 'load_states':(1,2,3,4)},
        188: {'sprite':'small_tarp_2', 'load_states':(3,4)},
        187: {'sprite':'large_tarp_3', 'load_states':(1,2,3,4)},
        186: {'sprite':'small_tarp_3', 'load_states':(3,4)},
        185: {'sprite':'large_tarp_4', 'load_states':(1,2,3,4)},
        184: {'sprite':'small_tarp_4', 'load_states':(3,4)},
    }
    sequences = {}
    for i in magic_colours:
        if load_state.num_id in magic_colours[i]['load_states']:
            points = load_sprites[magic_colours[i]['sprite']]
            sequences[i] = PixaSequence(points=points, transforms=[PixaShiftColour(147, 153, colour_shift_amount)])
        else:
            sequences[i] = PixaSequence(points=[(0, 0, common.COL_MASK)])
    return PixaSequenceCollection(
        sequences = sequences
    )


def generate(input_image_path):
    floorplan = Image.open(input_image_path)
    # get a palette
    palette = Image.open('palette_key.png').palette
    # create variations containing empty spritesheets
    variations = []
    manifest_payload = []
    for set_name in colourshifts:
        for i in range(7):
            length = 8 - i # don't bother generating 1/8 long cargo sprites
            variation = common.Variation(set_name=set_name, colourset=None, cargo=None, length=length, connection_type='')
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
                    #{'seq' : sc_mask_out_template_guides, 'colourset' : None},
                    {'seq' : get_load_sequence(variation.set_name, load_state), 'colourset' : None},
                ]
                spriterows.append(spriterow)
            spritesheet.render(spriterows=spriterows)
            output_path = common.get_output_path(common.construct_filename(gestalt_id, variation))
            print output_path
            spritesheet.save(output_path)
            manifest_payload.append(output_path)

    pixamakeanifest(gestalt_id, manifest_payload)
