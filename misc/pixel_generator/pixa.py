import Image
import ImageDraw


class PixaSequence:
    def __init__(self, sequence=None):
        self.sequence = []
        if sequence is not None:
            for i in sequence:
                self.set_point(i)

    class Point:
        """ simple class to hold the definition of a pixel that should be drawn """
        def __init__(self, dx, dy, colour):
            self.dx = dx
            self.dy = dy
            self.colour = colour
                
    def set_point(self, point_values):
        """ pass in a tuple of x, y, colour """
        point = self.Point(dx = point_values[0], dy = point_values[1], colour = point_values[2])
        # ? could check here and print a warning if more than one point has same x,y ? 
        self.sequence.append(point)

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
    def __init__(self, sequence, transform=None, transform_options=None):
        self.sequence = sequence
        self.transform = transform
        self.transform_options = transform_options
    
    def get_recolouring(self, x, y, colourset=None):
        """ Give sequence of pixels to be painted by the caller. """ 
        for P in self.sequence.sequence:  #my my, that's ugly
            colour = P.colour
            # is it a var for the colour?
            if P.colour in colourset:
                colour = colourset[P.colour]
            try:
                colour + 1
            except:
                print "! Error: '"+colour+"' is not a valid colour value. (perhaps it's missing from current colourset?)"
                raise # colour is not an int; possibly the colour is a var that is missing from current colourset
            if self.transform != None:
                colour = self.transform(colour, self.transform_options)
            yield (x + P.dx, y - P.dy, colour)

def render(image, sequence_collection, colourset=None):
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
            for sx, sy, scol in sequence.get_recolouring(x, y, colourset):
                draw.point([(sx, sy)], fill=scol)
    #print colours # debug: what colours did we find in this spritesheet?
    return image

def generate(input_image_path, key_colour_mapping, output_image_path):
    spritesheet = Image.open(input_image_path)
    draw = ImageDraw.Draw(spritesheet)
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)