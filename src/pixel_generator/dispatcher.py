import os.path
currentdir = os.curdir
import sys

sys.path.append(os.path.join('gestalts')) # add to the module search path

from gestalts import cargo_coils
from gestalts import cargo_tarps

from gestalts import box_trailer
from gestalts import flat_trailer
from gestalts import tank_trailer
from gestalts import tipping_trailer

gestalt_patterns = {
    'cargo_coils': cargo_coils,
    'cargo_tarps': cargo_tarps,
    'box_trailer': box_trailer,
    'flat_trailer': flat_trailer,
    'tank_trailer': tank_trailer,
    'tipping_trailer': tipping_trailer,
}

def dispatch(filename):
    print "dispatching", filename
    gestalt_full_id = filename.split('-',1)[0]
    for gestalt, module in gestalt_patterns.iteritems():
        if gestalt_full_id.startswith(gestalt):
            module.generate(filename)
