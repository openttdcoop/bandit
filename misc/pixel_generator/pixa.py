import Image
import ImageDraw

# common transforms
def colour_shift(point, shift_amount):
    point.colour + shift_amount
    return point

def replace_with_mask_colour(point, mask_colour):
    point.colour = mask_colour
    return point
# end common transforms

class Point:
    """ simple class to hold the definition of a pixel that should be drawn """
    def __init__(self, dx, dy, colour):
        self.dx = dx
        self.dy = dy
        self.colour = colour                

class PixaSequence:
    def __init__(self, points=None, transforms=None):
        """ pass on optional sequence, in format [(dx, dy, colour)...] """
        self.points = []
        self.transforms = []    
        if points is not None:
            for i in points:
                self.add_point(i)
        if transforms is not None:
            for i in transforms:
                self.add_transform(i)

    def add_point(self, point):
        """ pass in a tuple of x, y, colour """
        # ? could check here and print a warning if more than one point has same x,y ? 
        self.points.append(Point(dx = point[0], dy = point[1], colour = point[2]))

    def add_transform(self, transform):
        """ pass in an object for the transform """
        """ 
            ? this could be used by authors to add transforms at arbitrary points in their pipeline ? 
            that would let authors add transforms using variables which might not be in scope earlier in the pipeline
            however...order of transforms matter.  How would they control order when adding a transform? 
        """        
        self.transforms.append(transform)

    def get_sequence_values(self):
        """ Give sequence of pixels to the caller. """ 
        for dx, dy, col in self.sequence:
          yield dx, dy, col

    def get_recolouring(self, x, y, colourset=None):
        """ Give sequence of pixels to be painted by the caller. """ 
        for point in self.sequence:  #my my, that's ugly
            colour = point.colour
            # is it a var for the colour?
            if point.colour in colourset:
                colour = colourset[point.colour]
            try:
                colour + 1
            except:
                print "! Error: '"+colour+"' is not a valid colour value. (perhaps it's missing from current colourset?)"
                raise # colour is not an int; possibly the colour is a var that is missing from current colourset
            yield (x + point.dx, y - point.dy, colour)


class PixaSequenceCollection:
    def __init__(self, sequences):
        self.sequences = sequences
        
    def get_sequence_by_colour_index(self, colour):
        return self.sequences.get(colour)        



class PixaMixer(object):
    """
    Empty base class for modifying a sequence.
    """

    def convert(self, seq):
        """
        Convert the sequence.

        @param seq: Sequence of points.
        @type  seq: C{list} of L{Point}

        @return Converted sequence.
        @rtype: C{list} of L{Point}
        """
        raise NotImplementedError("Implement me in %r" % type(self))


class PixaShiftColour(PixaMixer):
    """
    Shift colours for an entire sequence by some value.
    """
    def __init__(self, lower, upper, shift):
        self.lower = lower
        self.upper = upper
        self.shift = shift

    def convert(self, seq):
        result = []
        for p in seq:
            if p.colour >= self.lower and p.colour <= self.upper:
                result.append((p.dx, p.dy, p.colour + self.shift))
            else:
                result.append(p)
        return result


class PixaShiftDY(PixaMixer):
    """
    Shift Y position.

    @ivar ddy: Change in dy.
    @type ddy: C{int}
    """
    def __init__(self, ddy):
        self.ddy = ddy

    def convert(self, seq):
        return [Point(p.dx, p.dy + self.ddy, p.colour) for p in seq]


class PixaMixerOld:
    def __init__(self, sequence, transform=None, transform_options=None):
        self.sequence = sequence
        self.transform = transform
        self.transform_options = transform_options
    
    def get_recolouring(self, x, y, colourset=None):
        """ Give sequence of pixels to be painted by the caller. """ 
        for point in self.sequence.points:  #my my, that's ugly
            colour = point.colour
            # is it a var for the colour?
            if point.colour in colourset:
                colour = colourset[point.colour]
            try:
                colour + 1
            except:
                print "! Error: '"+colour+"' is not a valid colour value. (perhaps it's missing from current colourset?)"
                raise # colour is not an int; possibly the colour is a var that is missing from current colourset
            if self.transform != None:
                point.colour = colour # !!! put the calculated colour back on the point object - might be better to create a new point obj locally ??
                point = self.transform(point=point)
            yield (x + point.dx, y - point.dy, colour)


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
            points = sequence.points
            #print sequence
            if sequence.transforms is not None:
                for t in sequence.transforms:
                    if t is not None:
                        print t.convert(points)                        
            """
            for sx, sy, scol in sequence.get_recolouring(x, y, colourset):
                draw.point([(sx, sy)], fill=scol)
            """  
    #print colours # debug: what colours did we find in this spritesheet?
    return image

def generate(input_image_path, key_colour_mapping, output_image_path):
    spritesheet = Image.open(input_image_path)
    draw = ImageDraw.Draw(spritesheet)
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)