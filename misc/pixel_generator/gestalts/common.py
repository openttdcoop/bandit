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

class Variation:
    def __init__(self, set_name, colourset, cargo, connection_type, body_subtype=''):
        self.spritesheets = []
        self.set_name = set_name
        self.colourset = colourset
        self.cargo = cargo
        self.connection_type = connection_type
        self.body_subtype = body_subtype # optional, use for e.g. flatbeds with and w/o stakes

def construct_filename(gestalt_id, length, variation):
    """ simple filename maker, not much to see here """
    return '_'.join([length, gestalt_id, variation.connection_type, variation.set_name, variation.cargo]) + '.png'

def get_output_path(filename):
    """ simple path maker, to deal with OS path. Expects a filename.  Currently hard coded to use 'output' dir """
    return os.path.join(currentdir, 'output', filename)
    
# constants
SPRITEROW_HEIGHT = 40
DOS_PALETTE = Image.open('palette_key.png').palette

# colour defaults
CC1 = 202
CC2 = 84
COL_COAL = 4