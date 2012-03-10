import os.path
currentdir = os.curdir
import sys
sys.path.append(os.path.join('gestalts')) # add to the module search path

from gestalts import cargo_coils
from gestalts import cargo_tarps

from gestalts import tipping_trailer
from gestalts import flat_trailer
from gestalts import tank_trailer

gestalt_patterns = {
    'tipping_trailer': tipping_trailer,
    'tank_trailer': tank_trailer,
    'flat_trailer': flat_trailer,
    'cargo_coils': cargo_coils,
    'cargo_tarps': cargo_tarps,
}

def dispatch(filename):
    print "dispatching", filename
    gestalt_full_id = filename.split('-',1)[0]
    for gestalt, module in gestalt_patterns.iteritems():
        if gestalt_full_id.startswith(gestalt):
            module.generate(filename)


"""
input_image_path = os.path.join(currentdir, 'input','cargo_tarps_floorplan.png')
cargo_tarps.generate(input_image_path)


input_image_path = os.path.join(currentdir, 'input','cargo_coils_floorplan.png')
cargo_coils.generate(input_image_path)
"""
