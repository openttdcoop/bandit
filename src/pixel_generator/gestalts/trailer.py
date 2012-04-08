from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour
from pixa import Spritesheet, PixaImageLoader
import Image
import common

gestalt_id = 'trailer'


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
    gv = common.GestaltTrailerVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, gv.floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=gv.num_load_states)

    spriterows = []
    for row_num in range(gv.num_load_states):
        # spriterow holds data needed to render the row
        spriterow = {'height': common.SPRITEROW_HEIGHT, 'floorplan': floorplan}
        # add n render passes to the spriterow (list controls render order, index 0 = first pass)
        spriterow['render_passes'] = [
            {'seq': get_body(gv.body_path, row_num), 'colourset': None},
        ]
        spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png')
    spritesheet.save(output_path)
