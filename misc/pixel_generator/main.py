print "running"

import dispatcher
import time
from multiprocessing import Process, active_children

cargo_filenames = [
    'cargo_coils-grey_metal-2_8.png',
    'cargo_coils-grey_metal-3_8.png',
    'cargo_coils-grey_metal-4_8.png',
    'cargo_coils-grey_metal-5_8.png',
    'cargo_coils-grey_metal-6_8.png',
    'cargo_coils-grey_metal-7_8.png',
    'cargo_coils-grey_metal-8_8.png',
    'cargo_coils-white-2_8.png',
    'cargo_coils-white-3_8.png',
    'cargo_coils-white-4_8.png',
    'cargo_coils-white-5_8.png',
    'cargo_coils-white-6_8.png',
    'cargo_coils-white-7_8.png',
    'cargo_coils-white-8_8.png',
    'cargo_coils-copper_metal-2_8.png',
    'cargo_coils-copper_metal-3_8.png',
    'cargo_coils-copper_metal-4_8.png',
    'cargo_coils-copper_metal-5_8.png',
    'cargo_coils-copper_metal-6_8.png',
    'cargo_coils-copper_metal-7_8.png',
    'cargo_coils-copper_metal-8_8.png',
]

trailer_filenames = [
    'tipping_trailer_4px-fifth_wheel-cc1-7_8-GRAI.png',
    'tipping_trailer_4px-fifth_wheel-cc2-7_8-GRAI.png',
    'tipping_trailer_4px-fifth_wheel-light_grey-7_8-GRAI.png',
    'tipping_trailer_4px-drawbar-cc1-7_8-GRAI.png',
    'tipping_trailer_4px-drawbar-cc2-7_8-GRAI.png',
    'tipping_trailer_4px-drawbar-light_grey-7_8-GRAI.png',
    'tipping_trailer_4px-fifth_wheel-cc1-7_8-COAL.png',
    'tipping_trailer_4px-fifth_wheel-cc2-7_8-COAL.png',
    'tipping_trailer_4px-fifth_wheel-light_grey-7_8-COAL.png',
    'tipping_trailer_4px-drawbar-cc1-7_8-COAL.png',
    'tipping_trailer_4px-drawbar-cc2-7_8-COAL.png',
    'tipping_trailer_4px-drawbar-light_grey-7_8-COAL.png',
    'tipping_trailer_4px-fifth_wheel-cc1-7_8-IORE.png',
    'tipping_trailer_4px-fifth_wheel-cc2-7_8-IORE.png',
    'tipping_trailer_4px-fifth_wheel-light_grey-7_8-IORE.png',
    'tipping_trailer_4px-drawbar-cc1-7_8-IORE.png',
    'tipping_trailer_4px-drawbar-cc2-7_8-IORE.png',
    'tipping_trailer_4px-drawbar-light_grey-7_8-IORE.png',
    'tipping_trailer_4px-fifth_wheel-cc1-7_8-CLAY.png',
    'tipping_trailer_4px-fifth_wheel-cc2-7_8-CLAY.png',
    'tipping_trailer_4px-fifth_wheel-light_grey-7_8-CLAY.png',
    'tipping_trailer_4px-drawbar-cc1-7_8-CLAY.png',
    'tipping_trailer_4px-drawbar-cc2-7_8-CLAY.png',
    'tipping_trailer_4px-drawbar-light_grey-7_8-CLAY.png',
    'tipping_trailer_4px-fifth_wheel-cc1-7_8-GRVL.png',
    'tipping_trailer_4px-fifth_wheel-cc2-7_8-GRVL.png',
    'tipping_trailer_4px-fifth_wheel-light_grey-7_8-GRVL.png',
    'tipping_trailer_4px-drawbar-cc1-7_8-GRVL.png',
    'tipping_trailer_4px-drawbar-cc2-7_8-GRVL.png',
    'tipping_trailer_4px-drawbar-light_grey-7_8-GRVL.png',
    'tank_trailer-drawbar-cc1-7_8.png',
    'tank_trailer-fifth_wheel-cc1-7_8.png',
    'tank_trailer-drawbar-cc2-7_8.png',
    'tank_trailer-fifth_wheel-cc2-7_8.png',
    'tank_trailer-drawbar-black-7_8.png',
    'tank_trailer-fifth_wheel-black-7_8.png',
    'tank_trailer-drawbar-silver-7_8.png',
    'tank_trailer-fifth_wheel-silver-7_8.png',
    'flat_trailer-drawbar-cc1-7_8_STEL.png',
    'flat_trailer-fifth_wheel-cc1-7_8_STEL.png',
    'flat_trailer-drawbar-cc2-7_8_STEL.png',
    'flat_trailer-fifth_wheel-cc2-7_8_STEL.png',
]

#filenames = trailer_filenames
filenames = cargo_filenames

# check for __main__ because fork bombs are bad
if __name__ == '__main__':
    for filename in filenames:
        Process(target=dispatcher.dispatch, args=(filename,)).start()

# dirty way to wait until all processes are complete before moving on
while True:
    time.sleep(0.027) # 0.027 because it's a reference to TTD ticks :P (blame Rubidium)
    if len(active_children()) == 0:
        break

print "done"
