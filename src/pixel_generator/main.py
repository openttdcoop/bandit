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

body_filenames = [
    'body_box-cc1-7_8.png',
    'body_box-cc2-7_8.png',
    'body_box-light_grey-7_8.png',
    'body_tipping_4px-cc1-7_8-bulk-corn_yellow.png',
    'body_tipping_4px-cc2-7_8-bulk-corn_yellow.png',
    'body_tipping_4px-light_grey-7_8-bulk-corn_yellow.png',
    'body_tank-cc1-7_8.png',
    'body_tank-silver-7_8.png',
    'body_flat-cc1-7_8-cargo_coils-grey_metal.png',
    'body_flat-cc2-7_8-cargo_coils-white.png',
    'body_flat-cc2-7_8-cargo_tarps-pinkish.png',
    'body_flat-cc2-7_8-cargo_tarps-greenish.png',
]

trailer_filenames = [
    'trailer_0_2-box-cc1-7_8.png',
    'trailer_0_2-tipping_4px-cc1-7_8-bulk-corn_yellow.png',
    'trailer_0_2-tipping_4px-cc2-7_8-bulk-corn_yellow.png',
    'trailer_0_2-tipping_4px-light_grey-7_8-bulk-corn_yellow.png',
    'trailer_2_2-tipping_4px-cc1-7_8-bulk-corn_yellow.png',
    'trailer_2_2-tipping_4px-cc2-7_8-bulk-corn_yellow.png',
    'trailer_2_2-tipping_4px-light_grey-7_8-bulk-corn_yellow.png',
    'trailer_0_2-tipping_4px-cc1-7_8-bulk-black.png',
    'trailer_0_2-tipping_4px-cc2-7_8-bulk-black.png',
    'trailer_0_2-tipping_4px-light_grey-7_8-bulk-black.png',
    'trailer_2_2-tipping_4px-cc1-7_8-bulk-black.png',
    'trailer_2_2-tipping_4px-cc2-7_8-bulk-black.png',
    'trailer_2_2-tipping_4px-light_grey-7_8-bulk-black.png',
    'trailer_0_2-tipping_4px-cc1-7_8-bulk-iron_ore.png',
    'trailer_0_2-tipping_4px-cc2-7_8-bulk-iron_ore.png',
    'trailer_0_2-tipping_4px-light_grey-7_8-bulk-iron_ore.png',
    'trailer_2_2-tipping_4px-cc1-7_8-bulk-iron_ore.png',
    'trailer_2_2-tipping_4px-cc2-7_8-bulk-iron_ore.png',
    'trailer_2_2-tipping_4px-light_grey-7_8-bulk-iron_ore.png',
    'trailer_0_2-tipping_4px-cc1-7_8-bulk-clay_pink.png',
    'trailer_0_2-tipping_4px-cc2-7_8-bulk-clay_pink.png',
    'trailer_0_2-tipping_4px-light_grey-7_8-bulk-clay_pink.png',
    'trailer_2_2-tipping_4px-cc1-7_8-bulk-clay_pink.png',
    'trailer_2_2-tipping_4px-cc2-7_8-bulk-clay_pink.png',
    'trailer_2_2-tipping_4px-light_grey-7_8-bulk-clay_pink.png',
    'trailer_0_2-tipping_4px-cc1-7_8-bulk-grey.png',
    'trailer_0_2-tipping_4px-cc2-7_8-bulk-grey.png',
    'trailer_0_2-tipping_4px-light_grey-7_8-bulk-grey.png',
    'trailer_2_2-tipping_4px-cc1-7_8-bulk-grey.png',
    'trailer_2_2-tipping_4px-cc2-7_8-bulk-grey.png',
    'trailer_2_2-tipping_4px-light_grey-7_8-bulk-grey.png',
    'trailer_2_2-tank-cc1-7_8.png',
    'trailer_0_2-tank-cc1-7_8.png',
    'trailer_2_2-tank-cc2-7_8.png',
    'trailer_0_2-tank-cc2-7_8.png',
    'trailer_2_2-tank-black-7_8.png',
    'trailer_0_2-tank-black-7_8.png',
    'trailer_2_2-tank-silver-7_8.png',
    'trailer_0_2-tank-silver-7_8.png',
    'trailer_2_2-flat-cc1-7_8-cargo_coils-grey_metal.png',
    'trailer_0_2-flat-cc1-7_8-cargo_coils-grey_metal.png',
    'trailer_2_2-flat-cc1-7_8-cargo_coils-grey_metal.png',
    'trailer_0_2-flat-cc1-7_8-cargo_coils-white.png',
    'trailer_2_2-flat-cc2-7_8-cargo_coils-grey_metal.png',
    'trailer_0_2-flat-cc2-7_8-cargo_coils-grey_metal.png',
    'trailer_0_2-flat-cc2-7_8-cargo_tarps-pinkish.png',
    'trailer_2_2-flat-cc2-7_8-cargo_tarps-pinkish.png',
    'trailer_0_2-flat-cc2-7_8-cargo_tarps-greenish.png',
    'trailer_2_2-flat-cc2-7_8-cargo_tarps-greenish.png',
    'trailer_0_2-flat-cc2-7_8-cargo_tarps-default.png',
    'trailer_2_2-flat-cc2-7_8-cargo_tarps-default.png',
    'trailer_0_2-flat-cc2-7_8-cargo_tarps-cc1.png',
    'trailer_2_2-flat-cc2-7_8-cargo_tarps-cc1.png',
    'trailer_0_2-flat-cc2-7_8-cargo_tarps-cc2.png',
    'trailer_2_2-flat-cc2-7_8-cargo_tarps-cc2.png',
]

def make_sprites(filenames):
    # check for __main__ because fork bombs are bad
    if __name__ == '__main__':
        for filename in filenames:
            Process(target=dispatcher.dispatch, args=(filename,)).start()

    # dirty way to wait until all processes are complete before moving on
    while True:
        time.sleep(0.027) # 0.027 because it's a reference to TTD ticks :P (blame Rubidium)
        if len(active_children()) == 0:
            break

make_sprites(cargo_filenames)
make_sprites(body_filenames)

print "done"
