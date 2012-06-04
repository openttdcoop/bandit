from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftXY, PixaShiftDY, PixaMaskColour, Spritesheet, PixaImageLoader
from pixa import make_cheatsheet as make_cheatsheet
import Image
import common
import os.path
currentdir = os.curdir

gestalt_id = 'truck'

# constants
FLOORPLAN_START_Y = 10

def make_cab_points(gv):
    cab_loader = PixaImageLoader(mask=(0,255))
    cab_sprites = {}
    for spritenum in ('1', '2', '3', '4', '5', '6', '7', '8'):
        filename = spritenum + '.png'
        cab_path = os.path.join(currentdir, 'input','cabs', gv.truck_model, filename)
        cab_sprites[spritenum] = cab_loader.make_points(cab_path, origin=(0,0))
    return cab_sprites

# sequence collections
def sc_chassis(chassis_floorplan_start_y):
    chassis_loader = PixaImageLoader(mask=(0, 226, 255))
    chassis_path = os.path.join(currentdir, 'input','trucks_chassis', 'tandem.png')

    crop_start_y = chassis_floorplan_start_y
    crop_end_y = chassis_floorplan_start_y + common.SPRITEROW_HEIGHT
    crop_box = (0, crop_start_y, common.BODY_SPRITE_WIDTH, crop_end_y)

    chassis = chassis_loader.make_points(chassis_path, crop_box, origin=(0, 0))
    return PixaSequenceCollection(
        sequences = {226: PixaSequence(points = chassis, transforms = [PixaShiftXY(0, -9)])}
    )

def sc_cab_farside(cab_sprites, truck_length):
    return PixaSequenceCollection(
        sequences = {
            191: PixaSequence(points = cab_sprites['1'], transforms = [PixaShiftXY(*common.get_cab_offsets(1, truck_length))]),
            190: PixaSequence(points = cab_sprites['2'], transforms = [PixaShiftXY(*common.get_cab_offsets(2, truck_length))]),
            189: PixaSequence(points = cab_sprites['3'], transforms = [PixaShiftXY(*common.get_cab_offsets(3, truck_length))]),
            185: PixaSequence(points = cab_sprites['7'], transforms = [PixaShiftXY(*common.get_cab_offsets(7, truck_length))]),
            184: PixaSequence(points = cab_sprites['8'], transforms = [PixaShiftXY(*common.get_cab_offsets(8, truck_length))]),
        }
    )

def sc_cab_nearside(cab_sprites, truck_length):
    return PixaSequenceCollection(
        sequences = {
            188: PixaSequence(points = cab_sprites['4'], transforms = [PixaShiftXY(*common.get_cab_offsets(4, truck_length))]),
            187: PixaSequence(points = cab_sprites['5'], transforms = [PixaShiftXY(*common.get_cab_offsets(5, truck_length))]),
            186: PixaSequence(points = cab_sprites['6'], transforms = [PixaShiftXY(*common.get_cab_offsets(6, truck_length))]),
        }
    )

def sc_body(body_path, row_num, truck_length):
    body_loader = PixaImageLoader(mask=(0,255))

    body_sprites = {}
    for spritenum in ('1', '2', '3', '4', '5', '6', '7', '8'):
        # crops out the body sprite for each angle, appropriate to the required load state
        crop_start_x = common.get_standard_crop(spritenum)[0][0]
        crop_end_x = common.get_standard_crop(spritenum)[1][0]
        row_offset_y = (row_num) * common.SPRITEROW_HEIGHT
        crop_start_y = row_offset_y + FLOORPLAN_START_Y + common.get_standard_crop(spritenum)[0][1]
        crop_end_y = row_offset_y + FLOORPLAN_START_Y + common.get_standard_crop(spritenum)[1][1]

        crop_box = (crop_start_x, crop_start_y, crop_end_x, crop_end_y)
        body_sprites[spritenum] = body_loader.make_points(body_path, crop_box, origin=(0, 0))

    if 'body_fifth_wheel_mask' in body_path:
        colour_shift = PixaShiftColour(244, 244, -244) # for masking out chassis on fifth wheel trucks
    else:
        colour_shift = None
    return PixaSequenceCollection(
        sequences = {
            191: PixaSequence(points = body_sprites['1'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(1, truck_length))]),
            190: PixaSequence(points = body_sprites['2'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(2, truck_length))]),
            189: PixaSequence(points = body_sprites['3'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(3, truck_length))]),
            188: PixaSequence(points = body_sprites['4'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(4, truck_length))]),
            187: PixaSequence(points = body_sprites['5'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(5, truck_length))]),
            186: PixaSequence(points = body_sprites['6'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(6, truck_length))]),
            185: PixaSequence(points = body_sprites['7'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(7, truck_length))]),
            184: PixaSequence(points = body_sprites['8'], transforms = [colour_shift, PixaShiftXY(*common.get_truck_body_offsets(8, truck_length))]),
        }
    )


def generate(filename):
    gv = common.GestaltTruckVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, gv.floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=gv.num_load_states)
    cab_sprites = make_cab_points(gv)

    spriterows = []
    #colourset = coloursets[gv.colourset_id] # coloursets not used; transforming cab colour would require additional render pass selectively replacing 1cc
    # spriterow holds data needed to render the row
    for row_num in range(gv.num_load_states):
        spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        spriterow['render_passes'] = [
            {'seq': sc_cab_farside(cab_sprites, gv.length), 'colourset' : None},
            {'seq': sc_body(gv.body_path, row_num, gv.length), 'colourset': None},
            {'seq': sc_cab_nearside(cab_sprites, gv.length), 'colourset' : None},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png')
    spritesheet.save(output_path)
