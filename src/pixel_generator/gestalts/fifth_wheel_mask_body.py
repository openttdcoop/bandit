from pixa import PixaColour, PixaSequence, PixaSequenceCollection
from pixa import Spritesheet
import Image
import common

gestalt_id = 'fifth_wheel_mask_body'
floorplan_filename = 'fifth_wheel_mask_body_floorplan.png'

sc_passthrough = PixaSequenceCollection(
    sequences = {
        244 : PixaSequence(points = [(0, 0, 244),])
    }
)


def generate(filename):
    gv = common.GestaltBodyVariation('body_fifth_wheel_mask-blue_mask-5_8.png')
    #gv = common.GestaltBodyVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=1)

    spriterows = []
    # spriterow holds data needed to render the row
    # only one spriterow for tank trailers; only one load state needed
    spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
    # add n render passes to the spriterow (list controls render order, index 0 = first pass)
    spriterow['render_passes'] = [
        {'seq' : sc_passthrough, 'colourset' : None},
    ]
    spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png', common.INTERMEDIATES_PATH)
    spritesheet.save(output_path)
