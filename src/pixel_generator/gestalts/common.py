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

class GestaltBodyVariation:
    def __init__(self, filename):
        self.filename = filename.split('.png')[0]
        self._parts = self.filename.split('-')
        self.gestalt_full_id = self._parts[0]
        self.colourset_id = self._parts[1]
        self.length = self._parts[2]
        self.floorplan_start_y = floorplan_start_y_per_length[self.length]
        if len(self._parts) > 3:
            self.cargo = self._parts[3]
        else:
            self.cargo = None
        if len(self._parts) > 4:
            self.cargo_colourset_id = self._parts[4]
        else:
            self.cargo_colourset_id = None

    'trailer-0_2-body_box-cc1-7_8.png',

class GestaltTrailerVariation:
    def __init__(self, filename):
        self.filename = filename.split('.png')[0]
        self._parts = self.filename.split('-')
        self.chassis_type = self._parts[1]
        self.body_type = self._parts[2]
        self.length = self._parts[4]
        self.floorplan_start_y = floorplan_start_y_per_length[self.length]
        self.floorplan_filename = os.path.join('chassis', self.chassis_type + '.png')
        self.body_path = os.path.join(INTERMEDIATES_PATH, 'body_' + filename.split('body_')[1])

        # use partial matching as body_type strings can include extra gestalt subtype information
        for i in load_state_ranges:
            if i in self.body_type:
                self.num_load_states = load_state_ranges[i]

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


def get_gestalt_floorplan(gv, floorplan_filename):
    floorplan = Image.open(os.path.join(currentdir, 'input', floorplan_filename))
    # slice out the floorplan needed for this gestalt
    return floorplan.crop((0, gv.floorplan_start_y, floorplan.size[0], gv.floorplan_start_y + SPRITEROW_HEIGHT))


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


def get_output_path(filename, destination_dir='output'):
    """ Simple path maker, to deal with OS path. Expects a filename.
        Destination dir is optional, default will be used if not specified.
    """
    return os.path.join(currentdir, destination_dir, filename)

# constants
SPRITEROW_HEIGHT = 40
DOS_PALETTE = Image.open('palette_key.png').palette
INTERMEDIATES_PATH = os.path.join(currentdir, 'intermediates')
CARGO_SPRITE_WIDTH = 280
BODY_SPRITE_WIDTH = 280

# colour defaults
CC1 = 202
CC2 = 84
COL_COAL = 4
COL_MASK = 0

# could be calculated from sprite row height but 'meh', this is easy and obvious
floorplan_start_y_per_length = {
    '7_8': 50,
    '5_8': 130,
    '4_8': 170,
    '3_8': 210,
}


load_state_ranges = {
    'body_tipping':5,
    'body_flat':5,
    'body_box':1,
    'body_tank':1,
}


