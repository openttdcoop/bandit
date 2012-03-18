from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet
import Image
import common

gestalt_id = 'box_trailer'
input_image_path = common.INPUT_IMAGE_PATH

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
roof = [
    (0, -4, pc_stripe())
]

# sequence collections
sc_pass_1 = PixaSequenceCollection(
    sequences = {
         94 : PixaSequence(points = body_inner),
         93 : PixaSequence(points = body_inner, transforms = [PixaShiftColour(0, 255, 1)]),
        141 : PixaSequence(points = roof, transforms = [PixaShiftColour(0, 255, 2)]),
        140 : PixaSequence(points = roof, transforms = [PixaShiftColour(0, 255, 2)]),
        139 : PixaSequence(points = roof, transforms = [PixaShiftColour(0, 255, 2)]),
        138 : PixaSequence(points = roof, transforms = [PixaShiftColour(0, 255, 2)]),
        197 : PixaSequence(points = body_outer, transforms = [PixaShiftColour(0, 255, 2)]),
        195 : PixaSequence(points = body_outer),
        194 : PixaSequence(points = body_outer, transforms = [PixaShiftColour(0, 255, -1)]),
        167 : PixaSequence(points = body_end, transforms = [PixaShiftColour(0, 255, 1)]),
        165 : PixaSequence(points = body_end, transforms = [PixaShiftColour(0, 255, -1)]),
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
