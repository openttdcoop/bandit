import Image
import ImageDraw
from copy import deepcopy

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
            self.add_points(points)
        if transforms is not None:
            for i in transforms:
                self.add_transform(i)

    def add_points(self, points):
        """ pass in a list containing tuples of (x, y, colour) """
        # ? could check here and print a warning if more than one point has same x,y ? 
        for i in points:
            self.points.append(Point(dx = i[0], dy = i[1], colour = i[2]))

    def add_transform(self, transform):
        """ pass in an object for the transform """
        """ 
        ? this could be used by authors to add transforms at arbitrary points in their pipeline ? 
        that would let authors add transforms using variables which might not be in scope earlier in the pipeline
        however...order of transforms matter.  How would they control order when adding a transform? 
        """        
        self.transforms.append(transform)

    def get_recolouring(self, x, y, colourset=None):
        """ 
        Give points to be painted by the caller.
        Colourset is required if points use vars for colours.  Colourset not required if all colours are specified as numbers.
        If transforms are defined in this sequence, they willl be applied after the colourset and before returning points.
        """
        # create a copy of points, just used when returning to the caller
        # don't want to modify the actual point values stored in this sequence
        temp_points = deepcopy(self.points) # use deepcopy because we need to copy the objects in the list, not just the list
        
        for point in temp_points:            
            # is it a var for the colour?
            if point.colour in colourset:
                point.colour = colourset[point.colour]
            try:
                point.colour + 1
            except:
                print "! Error: '"+colour+"' is not a valid colour value. (perhaps it's missing from current colourset?)"
                raise # colour is not an int; possibly the colour is a var that is missing from current colourset
        
        if self.transforms is not None:
            for t in self.transforms:
                if t is not None:
                    temp_points = t.convert(temp_points)
        
        for point in temp_points:
            yield (x + point.dx, y - point.dy, point.colour)
        

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
                result.append(Point(p.dx, p.dy, p.colour + self.shift))
            else:
                result.append(p)
        return result

class PixaMaskColour(PixaMixer):
    """
    Mask out all colours for an entire sequence (mask colour user-defined to allow for palette variations).
    """
    def __init__(self, mask_colour):
        self.mask_colour = mask_colour

    def convert(self, seq):
        return [Point(p.dx, p.dy, self.mask_colour) for p in seq]


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