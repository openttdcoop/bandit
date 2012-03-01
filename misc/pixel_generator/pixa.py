import Image
import ImageDraw
from copy import deepcopy

class Point:
    """ simple class to hold the definition of a pixel that should be drawn """
    def __init__(self, dx, dy, colour):
        self.dx = dx
        self.dy = dy
        self._colour = colour # private storage of colour value or object
    
    def colour(self, colourset=None):
        """ get the actual colour via a method to hide the details from end user """
        if hasattr(self._colour, 'get_colour'):                
            # assume we have an object implementing a get_colour() method (ducktyped for ease of authors who want to provide their own colour object)
            return self._colour.get_colour(colourset)
        else:
            # assume we have a valid int, if it isn't render stage will likely fail anyway, which imo is good enough in this case 
            return self._colour

class PixaColour:
    """ 
    small factory-like class
    holds a variable for a colour index, for use in sequences
    creates instances of spot colour classes which optionally shift up or down the colour index from the parent class 
    """
    
    class PixaSpotColour: 
        def __init__(self, shift, parent):
            self.shift = shift
            self.parent = parent
            
        def get_colour(self, colourset):
            result = colourset.get(self.parent.name, self.parent.default)
            return result + self.shift
        
    def __init__(self, name, default):
        self.name = name
        self.default = default

    def __call__(self, shift=0):
        return self.PixaSpotColour(shift, self)
            
    
class PixaSequence:
    def __init__(self, points=None, transforms=None):
        """
        pass an optional sequence, in format [(dx, dy, colour)...]
        pass an optional list of transforms to use
        """
        self.points = []
        self.transforms = []
        if points is not None:
            self.add_points(points)
        if transforms is not None:
            self.add_transforms(transforms)

    def add_points(self, points):
        """ pass in a list containing tuples of (x, y, colour) """
        # ? could check here and print a warning if more than one point has same x,y ?
        for i in points:
            self.points.append(Point(dx = i[0], dy = i[1], colour = i[2]))

    def add_transforms(self, transforms):
        """ pass in an object for the transform """
        """
        ? this could be used by authors to add transforms at arbitrary points in their pipeline ?
        that would let authors add transforms using variables which might not be in scope earlier in the pipeline
        however...order of transforms matter.  How would they control order when adding a transform?
        """
        for transform in transforms:
            self.transforms.append(transform)

    def get_recolouring(self, x, y, colourset=None):
        """
        Give points to be painted by the caller.
        Colourset is required if points use vars for colours.  Colourset not required if all colours are specified as numbers.
        If transforms are defined in this sequence, they willl be applied after the colourset and before returning points.
        """

        # create a copy of points, just used when returning to the caller
        # don't want to modify the actual point values stored in the sequence definition
        # n.b. we need to copy the objects in the list, not just the list
        # we also apply a colourset at this point if available; if None, then default values will be used (if colour is provided by an object not int)
        temp_points = []
        for p in self.points:
            temp_points.append(Point(dx=p.dx, dy=p.dy, colour=p.colour(colourset)))            

        if self.transforms is not None:
            for t in self.transforms:
                if t is not None:
                    temp_points = t.convert(temp_points)

        for p in temp_points:
            yield (x + p.dx, y - p.dy, p.colour())


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
            if p.colour() >= self.lower and p.colour <= self.upper:
                result.append(Point(p.dx, p.dy, p.colour() + self.shift))
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
        return [Point(p.dx, p.dy + self.ddy, p.colour()) for p in seq]

class Spritesheet(object):
    """
    Class holding the sprite sheet.

    @ivar sprites: The sprite sheet.
    @type sprites: L{Image}
    """
    def __init__(self, width, height, palette):
        """
        Construct an empty sprite sheet.

        @param width: Width of the sprite sheet.
        @type  width: C{int}

        @param height: Height of the sprite sheet.
        @type  height: C{int}

        @param palette: Palette of the sprite sheet.
        @type  palette: C{list} of (256*3) C{int}
        """
        self.sprites = Image.new('P', (width, height))
        self.sprites.putpalette(palette)

    def render(self, spriterows):
        for i, spriterow in enumerate(spriterows):
            result = spriterow['floorplan'].copy() # need to copy the floorplan image to draw into (to avoid modifying the original image object)
            for render_pass in spriterow['render_passes']:
                result = pixarender(result, render_pass['seq'], render_pass['colourset'])
            crop_start_y = i * spriterow['height']
            crop_end_y = crop_start_y + spriterow['height']
            self.sprites.paste(result,(0, crop_start_y, result.size[0], crop_end_y))

    def save(self, output_path):
        self.sprites.save(output_path, optimize=True)

def pixarender(image, sequence_collection, colourset=None):
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
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)
