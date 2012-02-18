from P import P
from pixa import render as render
import Image

# set palette index for lightest colour of cargo; range for rest will be calculated automatically 
# when defining a new cargo, worth looking at resulting sprites in case range overflowed into wrong colours
bulk_cargos = {
    'COAL' : 4,
    'IORE' : 77,
    'GRAI' : 67,
    'CLAY' : 117,
}  

# load states - values define y offset for drawing load (above floor)
load_states = {
    'load_1' : 0,
    'load_2' : 2,
    'load_3' : 4,
}

# colour onstants
BODY = 10
CC_A = 202

# pixel sequences
# each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
# if colour values etc need to change for different load states etc, sequence needs to be returned from a def
def bulk_load(cargo_colour,load_offset): 
    return [P(0, load_offset, cargo_colour)]

body_outer = [
    P(0, 0, BODY),
    P(0, 1, CC_A), 
    P(0, 2, BODY), 
    P(0, 3, BODY), 
    P(0, 4, 13),
]
body_end   = [
    P(0, 0, BODY), 
    P(0, 1, CC_A), 
    P(0, 2, BODY), 
    P(0, 3, BODY), 
    P(0, 4, 13),
]
body_inner = [
    P(0, 0, 16), 
    P(0, 1, 17), 
    P(0, 2, 18),
    P(0, 3, 19), 
    P(0, 4, 14),
]

def key_colour_mapping(cargo,load_offset):
    if cargo == 'empty':
        cargo_or_empty = [P(0, 0, 19)] 
    else:
        cargo_or_empty = bulk_load(cargo_colour=bulk_cargos[cargo],load_offset=load_offset)    
    return {
        209 : dict(seq = body_inner,  colour_shift =  0),
         90 : dict(seq = body_inner,  colour_shift =  1),
        238 : dict(seq = body_outer,  colour_shift =  0),
        243 : dict(seq = body_outer,  colour_shift = -1),
        244 : dict(seq = body_outer,  colour_shift =  2),
        240 : dict(seq = body_end,    colour_shift = -1),
        166 : dict(seq = body_end,    colour_shift =  1),
        138 : dict(seq = cargo_or_empty, colour_shift = -3),
        139 : dict(seq = cargo_or_empty, colour_shift = -2),
        140 : dict(seq = cargo_or_empty, colour_shift = -1),
        141 : dict(seq = cargo_or_empty, colour_shift =  0),
    }

def render_and_save(input_image_path, spritesheet, cargo, load_state, load_offset):
    output_image_path = 'results/' + input_image_path.split('.png')[0] + '_tipper_' + cargo + '_' + load_state + '.png'            
    newspritesheet = render(spritesheet.copy(), key_colour_mapping(cargo=cargo, load_offset=load_offset))
    newspritesheet.save(output_image_path, optimize=1)        

def generate(input_image_path):
    spritesheet = Image.open(input_image_path)
    for cargo in bulk_cargos:
        for load_state in load_states:
            load_offset = load_states[load_state]
            render_and_save(input_image_path, spritesheet, cargo, load_state, load_offset)
    cargo = 'empty'
    load_state = '0'
    load_offset = 0
    render_and_save(input_image_path, spritesheet, cargo, load_state, load_offset)
