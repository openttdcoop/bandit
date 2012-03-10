# constants, classes, methods etc common to all gestalts in this project
from pixa import PixaSequence, PixaSequenceCollection, PixaShiftColour, PixaMaskColour, Spritesheet
import Image
import os.path
currentdir = os.curdir

def hide_or_show_drawbar_dolly_wheels(connection_type):
    """ returns sequences to draw in dolly wheels for drawbar trailers, or mask them out with blue """
    if connection_type == 'drawbar':
        transform = None
    else:
        transform = PixaMaskColour(0)

    return PixaSequenceCollection(
        sequences = {
             49 : PixaSequence(points = [(0, 0, 19)], transforms = [transform]),
             48 : PixaSequence(points = [(0, 0, 18)], transforms = [transform]),
            230 : PixaSequence(points = [(0, 0, 5)], transforms = [transform]),
            229 : PixaSequence(points = [(0, 0, 4)], transforms = [transform]),
            228 : PixaSequence(points = [(0, 0, 3)], transforms = [transform]),
            227 : PixaSequence(points = [(0, 0, 2)], transforms = [transform]),
        }
    )

class GestaltCargoVariation:
    def __init__(self, filename):
        self.filename = filename.split('.png')[0]
        self._parts = self.filename.split('-')
        self.gestalt_full_id = self._parts[0]
        self.colourset_id = self._parts[1]
        self.length = self._parts[2]


class GestaltTrailerVariation:
    def __init__(self, filename):
        self.filename = filename.split('.png')[0]
        self._parts = self.filename.split('-')
        self.gestalt_full_id = self._parts[0]
        self.connection_type = self._parts[1]
        self.colourset_id = self._parts[2]
        self.length = self._parts[3]
        if len(self._parts) > 4:
            self.cargo = self._parts[4]
        else:
            self.cargo = None


class Variation:
    def __init__(self, set_name, colourset, cargo, connection_type, length, body_subtype=''):
        self.spritesheets = []
        self.set_name = set_name
        self.colourset = colourset
        self.cargo = cargo
        self.connection_type = connection_type
        self.length = length
        self.body_subtype = body_subtype # optional, use for e.g. flatbeds with and w/o stakes

    def attach_floorplan(self, floorplan):
        self.floorplan = floorplan


def get_trailer_floorplan(gv, FLOORPLAN_START_Y):
    floorplan = Image.open(INPUT_IMAGE_PATH)
    # slice out the floorplan needed for this gestalt
    return floorplan.crop((0, FLOORPLAN_START_Y, floorplan.size[0], FLOORPLAN_START_Y + SPRITEROW_HEIGHT))


def get_cargo_floorplan(gv, floorplan_filename, floorplan_start_y):
    floorplan_image_path = os.path.join(currentdir, 'input', floorplan_filename)
    floorplan = Image.open(floorplan_image_path)

    start_y = floorplan_start_y + ((8 - int(gv.length.split('_')[0])) * SPRITEROW_HEIGHT)
    return floorplan.crop((0, start_y, floorplan.size[0], start_y + SPRITEROW_HEIGHT))


def make_spritesheet(floorplan, row_count):
    return Spritesheet(width=floorplan.size[0], height=SPRITEROW_HEIGHT * row_count, palette=DOS_PALETTE)


def construct_filename(gestalt_id, variation):
    """ Simple filename maker; will filter out attributes that have no meaningful value. """
    raw = [str(variation.length) + '_8', gestalt_id, variation.connection_type, variation.set_name, variation.cargo]
    clean = []
    for i in raw:
        if i is not None and i != '':
            clean.append(i)
    return '_'.join(clean) + '.png'


def get_output_path(filename):
    """ Simple path maker, to deal with OS path. Expects a filename.  Currently hard coded to use 'output' dir. """
    return os.path.join(currentdir, 'output', filename)

# constants
SPRITEROW_HEIGHT = 40
DOS_PALETTE = Image.open('palette_key.png').palette
INPUT_IMAGE_PATH = os.path.join(currentdir, 'input','test_input.png')

# colour defaults
CC1 = 202
CC2 = 84
COL_COAL = 4
COL_MASK = 0
