from P import P
from pixa import render as render

def generate(input_image_path, spritesheet, gestalt):
    output_image_path = 'results/' + input_image_path.split('.png')[0] + '_generated.png'
    spritesheet = render(spritesheet, gestalt)
    spritesheet.save(output_image_path, optimize=1)
    

# global constants
C_WALL = 20
C_ROOF = 6  
C_LIP = C_WALL + 2

#each sequence contains stubby objects which are constructed with params (x-offset, y-offset, colour to draw)
metabolist_1 = [
    P(0, 0, C_WALL),
    P(0, 1, C_WALL), 
    P(0, 2, C_WALL), 
    P(0, 3, C_WALL-2), 
    P(0, 4, C_LIP), 
    P(0, 5, C_WALL),
    P(0, 6, C_WALL), 
    P(0, 7, C_WALL), 
    P(0, 8, C_WALL-2), 
    P(0, 9, C_LIP), 
    P(0, 10, C_WALL),
    P(0, 11, C_WALL), 
    P(0, 12, C_WALL), 
    P(0, 13, C_WALL-2), 
    P(0, 13, C_LIP), 
    P(0, 14, C_WALL),
    P(0, 15, C_WALL), 
    P(0, 16, C_WALL), 
    P(0, 17, C_WALL), 
    P(0, 18, C_LIP), 
]
metabolist_2 = [
    P(0, 0, C_WALL),
    P(0, 1, C_WALL), 
    P(0, 2, C_WALL-2), 
    P(0, 3, C_LIP), 
    P(0, 4, C_WALL),
    P(0, 5, C_WALL), 
    P(0, 6, C_WALL), 
    P(0, 7, C_WALL), 
    P(0, 8, C_LIP), 
    P(0, 13, C_WALL-2),
    P(0, 14, C_WALL), 
    P(0, 15, C_WALL), 
    P(0, 16, C_WALL), 
    P(0, 17, C_LIP), 
]

wall_plain = [
    P(0, 0, C_WALL-1),
    P(0, 1, C_WALL), 
    P(0, 2, C_WALL), 
    P(0, 3, C_WALL), 
    P(0, 4, C_WALL), 
    P(0, 5, C_WALL), 
    P(0, 6, C_WALL), 
    P(0, 7, C_WALL), 
    P(0, 8, C_WALL), 
    P(0, 9, C_WALL-1), 
    P(0, 10, C_LIP),
    P(0, 11, C_WALL), 
    P(0, 12, C_WALL), 
    P(0, 13, C_WALL), 
    P(0, 14, C_WALL), 
    P(0, 15, C_WALL), 
    P(0, 16, C_WALL), 
    P(0, 17, C_WALL), 
    P(0, 18, C_WALL), 
    P(0, 19, C_WALL-1), 
    P(0, 20, C_LIP),
]
wall_windows = [
    P(0, 0, C_WALL-1),
    P(0, 1, C_WALL), 
    P(0, 2, C_WALL), 
    P(0, 3, 130), 
    P(0, 4, 131), 
    P(0, 5, 132), 
    P(0, 6, 130), 
    P(0, 7, 131), 
    P(0, 8, 132), 
    P(0, 9, C_WALL-1), 
    P(0, 10, C_LIP),
    P(0, 11, C_WALL), 
    P(0, 12, 130), 
    P(0, 13, 131), 
    P(0, 14, 132), 
    P(0, 15, 130), 
    P(0, 16, 131), 
    P(0, 17, 132), 
    P(0, 18, C_WALL), 
    P(0, 19, C_WALL-1), 
    P(0, 20, C_LIP),
]
roof = [
    P(0, 20, C_ROOF),
]

key_colour_mapping = {
     45 : dict(seq = metabolist_1,  colour_shift =  0),
     44 : dict(seq = metabolist_1,  colour_shift =  -1),
     43 : dict(seq = metabolist_1,  colour_shift =  -2),
     28 : dict(seq = metabolist_2,  colour_shift =  0),
     27 : dict(seq = metabolist_2,  colour_shift =  -1),
     26 : dict(seq = metabolist_2,  colour_shift =  -2),
    209 : dict(seq = wall_plain,  colour_shift =  1),
    208 : dict(seq = wall_plain,  colour_shift =  0),
    238 : dict(seq = wall_plain,  colour_shift =  -0),
    237 : dict(seq = wall_plain,  colour_shift =  -1),
    165 : dict(seq = wall_windows,  colour_shift =  1),
    163 : dict(seq = wall_windows,  colour_shift =  0),
    139 : dict(seq = roof, colour_shift = -2),
    140 : dict(seq = roof, colour_shift = -1),
    141 : dict(seq = roof, colour_shift =  0),
}