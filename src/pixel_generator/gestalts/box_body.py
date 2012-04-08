from pixa import PixaColour, PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaShiftDY, PixaMaskColour
from pixa import Spritesheet
import Image
import common

gestalt_id = 'box_body'
floorplan_filename = 'box_body_floorplan.png'

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
    (0, -4, pc_body(1)),
]
body_end = [
    (0, 0, pc_body()),
    (0, -1, pc_stripe()),
    (0, -2, pc_body()),
    (0, -3, pc_body()),
    (0, -4, pc_body(1)),
]
body_inner = [
    (0, 0, 16),
    (0, -1, 17),
    (0, -2, 18),
    (0, -3, 19),
    (0, -4, pc_body(1)),
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
    gv = common.GestaltBodyVariation(filename)
    floorplan = common.get_gestalt_floorplan(gv, floorplan_filename)
    spritesheet = common.make_spritesheet(floorplan, row_count=1)

    spriterows = []
    # spriterow holds data needed to render the row
    # only one spriterow for tank trailers; only one load state needed
    spriterow = {'height' : common.SPRITEROW_HEIGHT, 'floorplan' : floorplan}
    # add n render passes to the spriterow (list controls render order, index 0 = first pass)
    colourset = coloursets[gv.colourset_id]
    spriterow['render_passes'] = [
        {'seq' : sc_pass_1, 'colourset' : colourset},
    ]
    spriterows.append(spriterow)

    spritesheet.render(spriterows=spriterows)
    output_path = common.get_output_path(gv.filename + '.png', common.INTERMEDIATES_PATH)
    spritesheet.save(output_path)
