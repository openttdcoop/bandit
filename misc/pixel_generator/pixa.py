import Image
import ImageDraw


class PixaSequence:
    def __init__(self, sequence):
        self.sequence = sequence

    def get_sequence_values(self):
        """ Give sequence of pixels to the caller. """ 
        for dx, dy, col in self.sequence:
          yield dx, dy, col

class PixaSequenceCollection:
    def __init__(self, sequences):
        self.sequences = sequences
        
    def get_sequence_by_colour_index(self, colour):
        return self.sequences.get(colour)        

class PixaMixer:
    def __init__(self, sequence, colourset = None, transform = None, transform_options = None):
        self.sequence = sequence
        self.colourset = colourset
        self.transform = transform
        self.transform_options = transform_options
    
    def get_recolouring(self, x, y):
        """ Give sequence of pixels to be painted by the caller. """ 
        for P in self.sequence:
            colour = P.colour
            if self.colourset != None:
                colour = self.colourset[P.colour]
            if self.transform != None:
                colour = self.transform(P.colour, self.transform_options)
            yield (x + P.dx, y - P.dy, colour)

def render(image, sequence_collection):
    colours = set() #used for debug
    imagepx = image.load()
    draw = ImageDraw.Draw(image)
    for x in range(image.size[0]):
      for y in range(image.size[1]):
        colour = imagepx[x,y]
        if colour not in (0, 15, 255):
          colours.add(colour) #used for debug only
        sequence = sequence_collection.get_sequence_by_colour_index(imagepx[x,y])
        if sequence is not None:
            for sx, sy, scol in sequence.get_recolouring(x, y):
                draw.point([(sx, sy)], fill=scol)
    #print colours # debug: what colours did we find in this spritesheet?
    return image

def generate(input_image_path, key_colour_mapping, output_image_path):
    spritesheet = Image.open(input_image_path)
    draw = ImageDraw.Draw(spritesheet)
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)