print "running"

import dispatcher
from multiprocessing import Process, active_children

filenames = [
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
]

for filename in filenames:
    print filename
    Process(target=dispatcher.dispatch, args=(filename,)).start()

# wait until all processes are complete before moving on
while True:
    if len(active_children()) == 0:
        break

print "done"
