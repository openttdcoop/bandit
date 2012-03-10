import Image
import ImageDraw
import ImagePalette
import codecs #used for writing files - more unicode friendly than standard open() module
from copy import deepcopy
import os.path
currentdir = os.curdir


class Point:
    """ simple class to hold the definition of a pixel that should be drawn """
    def __init__(self, dx, dy, colour):
        self.dx = dx
        self.dy = dy
        self._colour = colour # private storage of colour value or object

    def colour(self, colourset=None):
        """
        for any given Point instance, colour value might be stored as a numeric value, or calculated by an object (and returned on demand)
        therefore get the actual colour via a method to hide implementation details from end user
        """
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
        self.colourset_cache = None
        self.temp_points_cache = None
        self.points = []
        self.transforms = []
        if points is not None:
            self.add_points(points)
        if transforms is not None:
            self.add_transforms(transforms)

    def add_points(self, points):
        """ pass in a list containing tuples of (x, y, colour) """
        # ? could check here and print a warning if more than one point has same x,y ?
        for dx, dy, col in points:
            self.points.append(Point(dx = dx, dy = dy, colour = col))

    def add_transforms(self, transforms):
        """ pass in an object for the transform """
        """
        ? this could be used by authors to add transforms at arbitrary points in their pipeline ?
        that would let authors add transforms using variables which might not be in scope earlier in the pipeline
        however...order of transforms matter.  How would they control order when adding a transform?
        """
        self.transforms.extend(transforms)

    def get_recolouring(self, x, y, colourset=None):
        """
        Give points to be painted by the caller.
        Colourset is required if points use vars for colours.  Colourset not required if all colours are specified as numbers.
        If transforms are defined in this sequence, they willl be applied after the colourset and before returning points.
        """

        if self.temp_points_cache is None or self.colourset_cache is None or self.colourset_cache != colourset:

            # create a copy of points, just used when returning to the caller
            # don't want to modify the actual point values stored in the sequence definition
            # n.b. we need to copy the objects in the list, not just the list
            # we also apply a colourset at this point if available; if None, then default values will be used (if colour is provided by an object not int)
            temp_points = []
            for p in self.points:
                temp_points.append(Point(dx=p.dx, dy=p.dy, colour=p.colour(colourset)))

            for t in self.transforms:
                if t is not None:
                    temp_points = t.convert(temp_points)

            self.temp_points_cache = temp_points
            self.colourset_cache = colourset

        for p in self.temp_points_cache:
            yield (x + p.dx, y + p.dy, p.colour())


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
            if p.colour() >= self.lower and p.colour() <= self.upper:
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
        self.sprites = Image.new('P', (width, height), 255)
        self.sprites.putpalette(palette)

    def render(self, spriterows):
        for i, spriterow in enumerate(spriterows):
            result = spriterow['floorplan'].copy() # need to copy the floorplan image to draw into (to avoid modifying the original image object)
            significant_pixels = pixascan(result)
            for render_pass in spriterow['render_passes']:
                result = pixarender(result, significant_pixels, render_pass['seq'], render_pass['colourset'])
            crop_start_y = i * spriterow['height']
            crop_end_y = crop_start_y + spriterow['height']
            self.sprites.paste(result,(0, crop_start_y, result.size[0], crop_end_y))

    def save(self, output_path):
        self.sprites.save(output_path, optimize=True)


class PixaImageLoader:
    """
    Loads images from disk and does various useful things with them.
    An instance of this class can store defaults for crops, masks etc, useful for working with imported spritesheets.
    Defaults can in certain cases be over-ridden when calling a method on this class.
    """
    def __init__(self, crop_box=None, mask=(), origin=(0,0)):
        self.crop_box = crop_box # an optional 4-tuple defining the left, upper, right, and lower pixel coordinate for crop
        self.mask = mask # a tuple of colour indexes that should be ignored when parsing this image
        self.origin = origin # a tuple of x,y to set origin when outputting sequnces of points

    class _Options:
        """ utility class to handle processing optional arguments """
        def __init__(self, parent, crop_box=None, mask=None, origin=None):
            # mask can't be None, use value from class instance (parent)
            if mask == None:
                self.mask = parent.mask
            else:
                self.mask = mask

            # crop_box can validly be None on call and class instance
            if crop_box != None:
                self.crop_box = crop_box
            elif parent.crop_box != None:
                self.crop_box = parent.crop_box
            else:
                self.crop_box = None

            # origin can't be None, use value from class instance (parent)
            if origin == None:
                self.origin = parent.origin
            else:
                self.origin = origin

    def get_image(self, image_file_path, crop_box=None):
        options = self._Options(self, crop_box)
        raw = Image.open(image_file_path)
        if options.crop_box != None:  # only crop if needed
            raw = raw.crop(options.crop_box)
        return raw

    def make_points(self, image_file_path, crop_box=None, mask=None, origin=None):
        """
        Turns an image file into a list of points (dx, dy, colour index) suitable for use with PixaSequence
        @param image_file_path: path to an image file to load

        @param origin: tuple (x,y), relative to top-left of file; dx, dy for points will be calculated relative to this origin
        """
        options = self._Options(self, crop_box, mask, origin)

        raw = Image.open(image_file_path)
        if options.crop_box != None:  # only crop if needed
            raw = raw.crop(options.crop_box)
        rawpx = raw.load()
        points = []
        for x in range(raw.size[0]):
          for y in range(raw.size[1]):
            colour = rawpx[x,y]
            if colour not in options.mask:
                dx = x - options.origin[0]
                dy = y - options.origin[1]
                points.append((dx, dy, colour))
        return points


def make_cheatsheet(image, output_path, origin=None):
    block_size = 30
    palette = deepcopy(image.palette)
    raw = image
    rawpx = raw.load()
    result = Image.new('P',(raw.size[0] * block_size, raw.size[1] * block_size))
    result.putpalette(palette)
    draw = ImageDraw.Draw(result)

    for x in range(raw.size[0]):
        for y in range(raw.size[1]):
            pen_x = x * block_size
            pen_y = y * block_size
            colour = rawpx[x,y]
            draw.rectangle([(pen_x,pen_y),(pen_x+block_size, pen_y+block_size)], fill=colour)
            if origin is not None and (x,y) == origin:
                # indicate origin; hacky, can't be bothered to learn to draw lines, so just draw more rects :P
                draw.rectangle([(pen_x,pen_y),(pen_x+(block_size), pen_y+(block_size))], fill=224)
                draw.rectangle([(pen_x+3,pen_y+3),(pen_x+(block_size-4), pen_y+(block_size-4))], fill=colour)
            bg_size = draw.textsize(str(colour))
            text_pos_x = (pen_x + (0.75 * block_size)) - bg_size[0]
            text_pos_y = pen_y+(block_size/3)
            draw.rectangle([(text_pos_x - 1, text_pos_y + 1), (text_pos_x + bg_size[0], text_pos_y + bg_size[1] -2)], fill=255)
            draw.text((text_pos_x, text_pos_y), str(colour), fill=1)

    result.save(output_path, optimize=True)


def pixascan(image):
    """ Optimisation method: scans an image from top left, rows first, and caches it into a list for reuse in multiple render passes """
    significant_pixels = []
    imagepx = image.load()
    for x in range(image.size[0]):
      for y in range(image.size[1]):
        colour = imagepx[x,y]
        if colour not in (0, 255): # don't store white, blue; assumes DOS palette
          significant_pixels.append((x,y,colour))
    return significant_pixels


def pixarender(image, significant_pixels, sequence_collection, colourset=None):
    """
    Draw pixels into an image from sequences.
    Expects a pre-assembled list of (x, y, colour) points to start drawing sequences at.
    """
    colours = set() #used for debug
    imagepx = image.load()
    for x, y, colour in significant_pixels:
        sequence = sequence_collection.get_sequence_by_colour_index(colour)
        if sequence is not None:
            for sx, sy, scol in sequence.get_recolouring(x, y, colourset):
                imagepx[sx,sy] = scol
    return image


def generate(input_image_path, key_colour_mapping, output_image_path):
    spritesheet = Image.open(input_image_path)
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)
