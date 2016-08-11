import random
import sys
import constants as consts
import logging
from PIL import Image, ImageDraw, ImageFont
from noise import pnoise3, snoise3
from generators.river_generator import river_generator
from util.astar import astar
from util.midpointdisp import midpointDisplacement

class biome_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix


    def generate(self):

        return self.fullMap

def makeImage(matrix):
    txt = Image.new('RGBA', (consts.IMAGE_SIZE,consts.IMAGE_SIZE), (10,10,10,255))
    d = ImageDraw.Draw(txt)
    for x in range(0, consts.MAX_MAP_SIZE):
        for y in range(0, consts.MAX_MAP_SIZE):
            # draw text, full opacity
            d.text((10 + y*(consts.FONT_SIZE), 10 + x*(consts.FONT_SIZE)), str(matrix[x][y]), font=fnt, fill=consts.COLOR_KEY[matrix[x][y]])

    txt.show()
    txt.save("result.bmp")
