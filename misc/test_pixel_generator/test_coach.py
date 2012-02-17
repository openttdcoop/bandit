import Image
import ImageDraw
spritesheet = Image.open('test_input_coach.png')
spritesheetpx = spritesheet.load()
draw = ImageDraw.Draw(spritesheet)
colours = {}
for x in range(spritesheet.size[0]):
  for y in range(spritesheet.size[1]):
    colour = spritesheetpx[x,y]
    if colour != 255 and colour != 0 and colour != 15:
      colours[colour] = ''
    if spritesheetpx[x,y] == 240:
      if x%2 == 0:
        body_colour = 10
        cc_colour = 200
      else:
        body_colour = 11
        cc_colour = 201
      draw.point([(x,y)],fill=body_colour)
      draw.point([(x,y-1)],fill=cc_colour)
      draw.point([(x,y-2)],fill=body_colour)
      draw.point([(x,y-3)],fill=body_colour)
      draw.point([(x,y-4)],fill=19)
    if spritesheetpx[x,y] == 238:
      body_colour = 10
      cc_colour = 201
      draw.point([(x,y)],fill=body_colour)
      draw.point([(x,y-1)],fill=cc_colour)
      draw.point([(x,y-2)],fill=body_colour)
      draw.point([(x,y-3)],fill=body_colour)
      draw.point([(x,y-4)],fill=11)
    if spritesheetpx[x,y] == 209:
      draw.point([(x,y)],fill=20)
      draw.point([(x,y-1)],fill=19)
      draw.point([(x,y-2)],fill=18)
      draw.point([(x,y-3)],fill=17)
      draw.point([(x,y-4)],fill=16)
    if spritesheetpx[x,y] == 254:
      body_colour = 10
      cc_colour = 201
      draw.point([(x,y)],fill=body_colour)
      draw.point([(x,y-1)],fill=cc_colour)
      draw.point([(x,y-2)],fill=131)
      draw.point([(x,y-3)],fill=132)
      draw.point([(x,y-4)],fill=11)
spritesheet.save('a_test_coach.png')
print colours