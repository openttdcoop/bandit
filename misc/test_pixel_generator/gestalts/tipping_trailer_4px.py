class P:
    """ simple class to hold the definition of a pixel that should be drawn """
    def __init__(self, dx, dy, colour):
        self.dx = dx
        self.dy = dy
        self.colour = colour

# global constants
BODY = 10
CC_A = 202
BULK_CARGO = 4  

#each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
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
bulk_load_1 = [
    P(0, 2, BULK_CARGO),
]

key_colour_mapping = {
    209 : dict(seq = body_inner,  colour_shift =  0),
     90 : dict(seq = body_inner,  colour_shift =  1),
    238 : dict(seq = body_outer,  colour_shift =  0),
    243 : dict(seq = body_outer,  colour_shift = -1),
    244 : dict(seq = body_outer,  colour_shift =  2),
    240 : dict(seq = body_end,    colour_shift = -1),
    166 : dict(seq = body_end,    colour_shift =  1),
    138 : dict(seq = bulk_load_1, colour_shift = -3),
    139 : dict(seq = bulk_load_1, colour_shift = -2),
    140 : dict(seq = bulk_load_1, colour_shift = -1),
    141 : dict(seq = bulk_load_1, colour_shift =  0),
}
