from PIL import Image, ImageDraw, ImageFont

FONT = 20
IMAGE_X = FONT * 1500
IMAGE_Y = FONT * 9

def makeImage():
    txt = Image.new('RGBA', (10 + IMAGE_Y, 10 + IMAGE_X), (10,10,10,255))
    fnt = ImageFont.truetype('Font/DF_Mayday_16x16.ttf', FONT)
    d = ImageDraw.Draw(txt)
    for x in range(0, int(IMAGE_X/FONT)):
        d.text((10 + 1*(FONT), 10 + x*(FONT)), str(x), font=fnt, fill=(255,255,255,255))
        d.text((10 + 6*(FONT), 10 + x*(FONT)), "|", font=fnt, fill=(255,255,255,255))
        d.text((10 + 8*(FONT), 10 + x*(FONT)), chr(x), font=fnt, fill=(255,255,255,255))

    txt.show()
    txt.save("font.bmp")

makeImage()
