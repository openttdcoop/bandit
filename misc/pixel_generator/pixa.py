import Image
import ImageDraw

def get_pixel_sequence(x, y, sequence):
    raw_sequence = sequence['seq']
    for P in raw_sequence:
        yield (x + P.dx, y - P.dy, P.colour + sequence['colour_shift'])

def render(image, sequence_collection):
    colours = set() #used for debug
    imagepx = image.load()
    draw = ImageDraw.Draw(image)
    for x in range(image.size[0]):
      for y in range(image.size[1]):
        colour = imagepx[x,y]
        if colour not in (0, 15, 255):
          colours.add(colour) #used for debug only
        sequence = sequence_collection.get(imagepx[x,y])
        if sequence is not None:
            for sx, sy, scol in get_pixel_sequence(x, y, sequence):
                draw.point([(sx, sy)], fill=scol)
    #print colours # debug: what colours did we find in this spritesheet?
    return image

def generate(input_image_path, key_colour_mapping, output_image_path):
    spritesheet = Image.open(input_image_path)
    draw = ImageDraw.Draw(spritesheet)
    spritesheet = render(spritesheet, key_colour_mapping)
    spritesheet.save(output_image_path, optimize=1)