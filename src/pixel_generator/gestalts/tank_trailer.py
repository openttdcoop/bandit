from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet
import Image
import common

gestalt_id = 'tank_trailer'
input_image_path = common.INPUT_IMAGE_PATH

# constants
FLOORPLAN_START_Y = 50

# colour sets
coloursets = {
    'cc1': dict (tank_colour = common.CC1, stripe_colour = 21),
    'cc2': dict (tank_colour = common.CC2, stripe_colour = 21),
    'silver': dict (tank_colour = 20, stripe_colour = common.CC1),
    'black': dict (tank_colour = 4, stripe_colour = common.CC2),
}
# colours
pc_tank = PixaColour(name='tank_colour', default=common.CC1)
pc_stripe = PixaColour(name='stripe_colour', default=21)

# pixel sequences
# x,y,colour (or colour object with optional shift)
tank_far_end_sw_ne = [
    (0, -3, pc_tank(2)),
    (0, -2, pc_stripe(1)),
    (0, -1, pc_tank()),
    (0, -0, pc_tank(-1)),
]
tank_sw_ne = [
    (-3, -5, pc_tank()),
    (-2, -5, pc_tank(1)),
    (-1, -5, pc_tank(1)),
    (-1, -4, pc_tank(2)),
    (0, -4, pc_tank(3)),
    (0, -3, pc_tank(2)),
    (0, -2, pc_stripe(1)),
    (0, -1, pc_tank()),
    (0, -0, pc_tank(-1)),
]
tank_near_end_sw_ne = [
    (-4, -4, pc_tank(-2)),
    (-4, -3, pc_tank(-1)),
    (-4, -2, pc_tank(-3)),
    (-3, -5, pc_tank(-1)),
    (-3, -4, pc_tank(-2)),
    (-3, -3, pc_tank(-2)),
    (-3, -2, pc_tank(-2)),
    (-3, -1, pc_tank(-3)),
    (-2, -4, pc_tank(-1)),
    (-2, -3, pc_tank(-2)),
    (-2, -2, pc_tank(-2)),
    (-2, -1, pc_tank(-2)),
    (-1, -4, pc_tank(-1)),
    (-1, -3, pc_tank(-2)),
    (-1, -2, pc_tank(-2)),
    (-1, -1, pc_tank(-2)),
    (-1, 0, pc_tank(-2)),
    (0, -3, pc_tank(-1)),
    (0, -2, pc_tank(-1)),
    (0, -1, pc_tank(-1)),
    (0, -0, pc_tank(-1)),
]
tank_far_end_nw_se = [
    (0, -3, pc_tank(1)),
    (0, -2, pc_stripe()),
    (0, -1, pc_tank(-1)),
    (0, -0, pc_tank(-2)),
]
tank_nw_se = [
    (3, -5, pc_tank(-1)),
    (2, -5, pc_tank()),
    (1, -5, pc_tank()),
    (1, -4, pc_tank(1)),
    (0, -4, pc_tank(2)),
    (0, -3, pc_tank(1)),
    (0, -2, pc_stripe()),
    (0, -1, pc_tank(-1)),
    (0, 0, pc_tank(-2)),
]
tank_near_end_nw_se = [
    (4, -4, pc_tank(2)),
    (4, -3, pc_tank(2)),
    (4, -2, pc_tank(2)),
    (3, -5, pc_tank(1)),
    (3, -4, pc_tank(1)),
    (3, -3, pc_tank(3)),
    (3, -2, pc_tank(2)),
    (3, -1, pc_tank(1)),
    (2, -4, pc_tank(1)),
    (2, -3, pc_tank(3)),
    (2, -2, pc_tank(2)),
    (2, -1, pc_tank(1)),
    (1, -4, pc_tank(1)),
    (1, -3, pc_tank(2)),
    (1, -2, pc_tank(2)),
    (1, -1, pc_tank(2)),
    (1, 0, pc_tank(1)),
    (0, -3, pc_tank(1)),
    (0, -2, pc_tank(1)),
    (0, -1, pc_tank(1)),
    (0, 0, pc_tank(1)),
]
tank_w_e = [
    (0, -6, pc_tank(-1)),
    (0, -5, pc_tank(1)),
    (0, -4, pc_tank(2)),
    (0, -3, pc_tank(1)),
    (0, -2, pc_stripe()),
    (0, -1, pc_tank(-1)),
    (0, 0, pc_tank(-2)),
]
tank_n_s = [
    (7, -1, pc_stripe(2)),
    (6, -2, pc_tank(2)),
    (5, -2, pc_tank(1)),
    (4, -2, pc_tank()),
    (3, -2, pc_tank(-1)),
    (2, -2, pc_tank(-1)),
    (1, -2, pc_tank(-2)),
    (0, -1, pc_tank(-2)),
]

tank_end_n_s = [
    (6, -2, pc_tank(1)),
    (5, -2, pc_tank(2)),
    (4, -2, pc_tank(1)),
    (3, -2, pc_tank(1)),
    (2, -2, pc_tank()),
    (1, -2, pc_tank(-1)),
    (7, -1, pc_tank(1)),
    (6, -1, pc_tank(1)),
    (5, -1, pc_tank(1)),
    (4, -1, pc_tank(1)),
    (3, -1, pc_tank()),
    (2, -1, pc_tank()),
    (1, -1, pc_tank()),
    (0, -1, pc_tank(-1)),
    (6, 0, pc_tank()),
    (5, 0, pc_tank()),
    (4, 0, pc_tank()),
    (3, 0, pc_tank()),
    (2, 0, pc_tank()),
    (1, 0, pc_tank(-1)),
    (0, 0, 2),
]

# sequence collections
sc_pass_1 = PixaSequenceCollection(
    sequences = {
         47 : PixaSequence(points = tank_far_end_nw_se), #47-40 NW-SE
         45 : PixaSequence(points = tank_nw_se), #47-40 NW-SE
         44 : PixaSequence(points = tank_nw_se, transforms = [PixaShiftColour(0, 255, -1)]), #47-40 NW-SE
         40 : PixaSequence(points = tank_near_end_nw_se), #47-40 NW-SE
         92 : PixaSequence(points = tank_n_s, transforms = [PixaShiftColour(0, 255, -1)]), #88-95 N-S
         93 : PixaSequence(points = tank_n_s), #88-95 N-S
         94 : PixaSequence(points = tank_end_n_s), #88-95 N-S
        143 : PixaSequence(points = tank_far_end_sw_ne), #143-136 SW-NE
        141 : PixaSequence(points = tank_sw_ne), #143-136 SW-NE
        140 : PixaSequence(points = tank_sw_ne, transforms = [PixaShiftColour(0, 255, -1)]), #143-136 SW-NE
        136 : PixaSequence(points = tank_near_end_sw_ne), #143-136 SW-NE
        197 : PixaSequence(points = tank_w_e, transforms = [PixaShiftColour(0, 255, 1)]), #197-92 W-E
        195 : PixaSequence(points = tank_w_e), #197-92 W-E
        194 : PixaSequence(points = tank_w_e, transforms = [PixaShiftColour(0, 255, -1)]), #197-92 W-E
        192 : PixaSequence(points = tank_w_e, transforms = [PixaShiftColour(0, 255, -1)]), #197-92 W-E
    }
)

def generate(filename):
    gv = common.GestaltTrailerVariation(filename)
    floorplan = common.get_trailer_floorplan(gv, FLOORPLAN_START_Y)
    spritesheet = common.make_spritesheet(floorplan, row_count=1)

    spriterows = []
    # spriterow holds data needed to render the row
    # only one spriterow for tank trailers; only one load state needed
    spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
    # add n render passes to the spriterow (list controls render order, index 0 = first pass)
    colourset = coloursets[gv.colourset_id]
    spriterow['render_passes'] = [
        {'seq' : common.hide_or_show_drawbar_dolly_wheels(gv.connection_type), 'colourset' : colourset},
        {'seq' : sc_pass_1, 'colourset' : colourset},
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
        for connection_type in ('fifth_wheel','drawbar'):
            variation = common.Variation(set_name=set_name, colourset=colourset, cargo=None, length=length, connection_type=connection_type)
            spritesheet = Spritesheet(
                width=floorplan.size[0],
                height=common.SPRITEROW_HEIGHT,
                palette=common.DOS_PALETTE
            )
            variation.spritesheets.append(spritesheet)
            variations.append(variation)

    # render stage
    for variation in variations:
        for spritesheet in variation.spritesheets:
            spriterows = []
            # spriterow holds data needed to render the row
            spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
            # add n render passes to the spriterow (list controls render order, index 0 = first pass)
            spriterow['render_passes'] = [
                {'seq' : common.hide_or_show_drawbar_dolly_wheels(variation.connection_type), 'colourset' : variation.colourset},
                {'seq' : sc_pass_1, 'colourset' : variation.colourset},
            ]
            spriterows.append(spriterow)
            spritesheet.render(spriterows=spriterows)
            output_path = common.get_output_path(common.construct_filename(gestalt_id, variation))
            print output_path
            spritesheet.save(output_path)
            manifest_payload.append(output_path)
"""