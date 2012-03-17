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
    'cargo_tarps-default-2_8.png',
    'cargo_tarps-default-3_8.png',
    'cargo_tarps-default-4_8.png',
    'cargo_tarps-default-5_8.png',
    'cargo_tarps-default-6_8.png',
    'cargo_tarps-default-7_8.png',
    'cargo_tarps-default-8_8.png',
    'cargo_tarps-cc1-2_8.png',
    'cargo_tarps-cc1-3_8.png',
    'cargo_tarps-cc1-4_8.png',
    'cargo_tarps-cc1-5_8.png',
    'cargo_tarps-cc1-6_8.png',
    'cargo_tarps-cc1-7_8.png',
    'cargo_tarps-cc1-8_8.png',
    'cargo_tarps-cc2-2_8.png',
    'cargo_tarps-cc2-3_8.png',
    'cargo_tarps-cc2-4_8.png',
    'cargo_tarps-cc2-5_8.png',
    'cargo_tarps-cc2-6_8.png',
    'cargo_tarps-cc2-7_8.png',
    'cargo_tarps-cc2-8_8.png',
    'cargo_tarps-pinkish-2_8.png',
    'cargo_tarps-pinkish-3_8.png',
    'cargo_tarps-pinkish-4_8.png',
    'cargo_tarps-pinkish-5_8.png',
    'cargo_tarps-pinkish-6_8.png',
    'cargo_tarps-pinkish-7_8.png',
    'cargo_tarps-pinkish-8_8.png',
    'cargo_tarps-greenish-2_8.png',
    'cargo_tarps-greenish-3_8.png',
    'cargo_tarps-greenish-4_8.png',
    'cargo_tarps-greenish-5_8.png',
    'cargo_tarps-greenish-6_8.png',
    'cargo_tarps-greenish-7_8.png',
    'cargo_tarps-greenish-8_8.png',
]

trailer_filenames = [
    'tipping_trailer_4px-0_2-cc1-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-0_2-cc2-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-0_2-light_grey-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-2_2-cc1-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-2_2-cc2-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-2_2-light_grey-7_8-bulk-corn_yellow.png',
    'tipping_trailer_4px-0_2-cc1-7_8-bulk-black.png',
    'tipping_trailer_4px-0_2-cc2-7_8-bulk-black.png',
    'tipping_trailer_4px-0_2-light_grey-7_8-bulk-black.png',
    'tipping_trailer_4px-2_2-cc1-7_8-bulk-black.png',
    'tipping_trailer_4px-2_2-cc2-7_8-bulk-black.png',
    'tipping_trailer_4px-2_2-light_grey-7_8-bulk-black.png',
    'tipping_trailer_4px-0_2-cc1-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-0_2-cc2-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-0_2-light_grey-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-2_2-cc1-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-2_2-cc2-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-2_2-light_grey-7_8-bulk-iron_ore.png',
    'tipping_trailer_4px-0_2-cc1-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-0_2-cc2-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-0_2-light_grey-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-2_2-cc1-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-2_2-cc2-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-2_2-light_grey-7_8-bulk-clay_pink.png',
    'tipping_trailer_4px-0_2-cc1-7_8-bulk-grey.png',
    'tipping_trailer_4px-0_2-cc2-7_8-bulk-grey.png',
    'tipping_trailer_4px-0_2-light_grey-7_8-bulk-grey.png',
    'tipping_trailer_4px-2_2-cc1-7_8-bulk-grey.png',
    'tipping_trailer_4px-2_2-cc2-7_8-bulk-grey.png',
    'tipping_trailer_4px-2_2-light_grey-7_8-bulk-grey.png',
    'tank_trailer-2_2-cc1-7_8.png',
    'tank_trailer-0_2-cc1-7_8.png',
    'tank_trailer-2_2-cc2-7_8.png',
    'tank_trailer-0_2-cc2-7_8.png',
    'tank_trailer-2_2-black-7_8.png',
    'tank_trailer-0_2-black-7_8.png',
    'tank_trailer-2_2-silver-7_8.png',
    'tank_trailer-0_2-silver-7_8.png',
    'flat_trailer-2_2-cc1-7_8-cargo_coils-grey_metal.png',
    'flat_trailer-0_2-cc1-7_8-cargo_coils-grey_metal.png',
    'flat_trailer-2_2-cc1-7_8-cargo_coils-grey_metal.png',
    'flat_trailer-0_2-cc1-7_8-cargo_coils-white.png',
    'flat_trailer-2_2-cc2-7_8-cargo_coils-grey_metal.png',
    'flat_trailer-0_2-cc2-7_8-cargo_coils-grey_metal.png',
    'flat_trailer-0_2-cc2-7_8-cargo_tarps-pinkish.png',
    'flat_trailer-2_2-cc2-7_8-cargo_tarps-pinkish.png',
    'flat_trailer-0_2-cc2-7_8-cargo_tarps-greenish.png',
    'flat_trailer-2_2-cc2-7_8-cargo_tarps-greenish.png',
    'flat_trailer-0_2-cc2-7_8-cargo_tarps-default.png',
    'flat_trailer-2_2-cc2-7_8-cargo_tarps-default.png',
    'flat_trailer-0_2-cc2-7_8-cargo_tarps-cc1.png',
    'flat_trailer-2_2-cc2-7_8-cargo_tarps-cc1.png',
    'flat_trailer-0_2-cc2-7_8-cargo_tarps-cc2.png',
    'flat_trailer-2_2-cc2-7_8-cargo_tarps-cc2.png',
]

filenames = trailer_filenames
#filenames.extend(cargo_filenames)

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