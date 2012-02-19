import Image
import ImageDraw
import ImagePalette
spritesheet = Image.open('foo.png')

block_size = 30
palette_key = Image.new('P',(16*block_size,16*block_size))
draw = ImageDraw.Draw(palette_key)

print spritesheet.mode

palette_key.putpalette(spritesheet.palette)
x = 0
y = 0
for i in range (256):
  draw.rectangle([(x,y),(x+block_size,y+block_size)],fill=i)
  bg_size = draw.textsize(str(i))
  text_pos = (x+(block_size/4),y+(block_size/3))
  draw.rectangle([(text_pos[0]-1,text_pos[1]+1),(text_pos[0]+bg_size[0],text_pos[1]+bg_size[1]-2)],fill=255)
  draw.text((x+(block_size/4),y+(block_size/3)),str(i),fill=1)
  x = x+block_size
  if x == 16*block_size:
    x = 0
    y = y + block_size

palette_key.save('palette_key.png')
