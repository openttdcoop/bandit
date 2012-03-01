import psdparser
import Image

psd = psdparser.PSDParser("test.psd")
psd.parse()

for i, image in enumerate(psd.images):
    image.save(str(i) + ".png")