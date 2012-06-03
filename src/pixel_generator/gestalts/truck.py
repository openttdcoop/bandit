from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader
from pixa import make_cheatsheet as make_cheatsheet
import Image
import common
import os.path
currentdir = os.curdir

gestalt_id = 'truck'
floorplan_filename = 'truck_2_8_cab_floorplan.png'

# constants
FLOORPLAN_START_Y = 10

# points
cargo_loader = PixaImageLoader(mask=(0,255))
load_sprites = {}
for spritename in ('1','2','3','4', '5','6','7','8'):
    filename = spritename + '.png'
    cab_path = os.path.join(currentdir, 'input','cabs', 'hackler_R', filename)
    load_sprites[spritename] = cargo_loader.make_points(cab_path, origin=(0,8))

# sequence collections
sc_mask_out_template_guides = PixaSequenceCollection(
    sequences = {
         85: PixaSequence(points=[(0, 0, common.COL_MASK)]),
    }
)

sc_pass_1 = PixaSequenceCollection(
    sequences = {
        191: PixaSequence(points = load_sprites['1']),
        190: PixaSequence(points = load_sprites['2']),
        189: PixaSequence(points = load_sprites['3']),
        188: PixaSequence(points = load_sprites['4']),
        187: PixaSequence(points = load_sprites['5']),
        186: PixaSequence(points = load_sprites['6']),
        185: PixaSequence(points = load_sprites['7']),
        184: PixaSequence(points = load_sprites['8']),
    }
)

# location points for cabs may be left behind due to transparent pixels in cab sequence; remove them if found
sc_mask_remnant_location_points = PixaSequenceCollection(
    sequences = {
        191: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        190: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        189: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        188: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        187: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        186: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        185: PixaSequence(points=[(0, 0, common.COL_MASK)]),
        184: PixaSequence(points=[(0, 0, common.COL_MASK)]),
    }
)


def get_body(body_path, row_num):
    body_loader = PixaImageLoader(mask=(0,255))

    crop_start_y = (row_num) * common.SPRITEROW_HEIGHT
    crop_end_y = crop_start_y + common.SPRITEROW_HEIGHT
    crop_box = (0, crop_start_y, common.BODY_SPRITE_WIDTH, crop_end_y)
    body = body_loader.make_points(body_path, crop_box, origin=(0, 9))

    return PixaSequenceCollection(
        sequences = {226: PixaSequence(points = body)}
    )


def generate(filename):
    gv = common.GestaltTruckVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=1)

    spriterows = []
    # spriterow holds data needed to render the row
    # only one spriterow for tank trailers; only one load state needed
    spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
    # add n render passes to the spriterow (list controls render order, index 0 = first pass)
    #colourset = coloursets[gv.colourset_id]
    spriterow['render_passes'] = [
        {'seq' : sc_mask_out_template_guides, 'colourset' : None},
        {'seq' : sc_pass_1, 'colourset' : None},
        {'seq' : sc_mask_remnant_location_points, 'colourset' : None},
        #{'seq': get_body(gv.body_path, row_num), 'colourset': None},
    ]
    spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png')
    spritesheet.save(output_path)
