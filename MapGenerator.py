#########
#
#   This project is purely for training purposes, and use of it is free to anyone
#   It generates a world, and tries to create as much detail as possible. There is one
#   visual output that combines every "map" inside "result.jpg".
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#       1. Code is getting bigger and slower, need to parallelize where possible.
#       2. Improve Rivers.
#       3. Add Civilization.
#   NOTE:
#
#########

import random
import sys
import constants as consts
import logging
from PIL import Image, ImageDraw, ImageFont
from noise import pnoise3, snoise3
from generators.river_generator import river_generator
from generators.biome_generator import biome_generator
from generators.land_generator import land_generator
from util.astar import astar
from util.midpointdisp import midpointDisplacement

#MAPS
fullMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
prettyMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]

#LOGGING
LOG_FILE = "logs/map_generation.log"
logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.DEBUG)

def prettyPrintMap(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ''.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

def makeImage(matrix, imageName, isText):
    if isText:
        image = Image.new('RGBA', (consts.IMAGE_SIZE, consts.IMAGE_SIZE), (10,10,10,255))
    else:
        newSize = int((consts.IMAGE_SIZE - 10)/consts.FONT_SIZE)
        image = Image.new('RGBA', (consts.IMAGE_SIZE, consts.IMAGE_SIZE), (10,10,10,255))

    fnt = ImageFont.truetype('Font/DF_Mayday_16x16.ttf', consts.FONT_SIZE)
    draw = ImageDraw.Draw(image)
    pixels = image.load()

    for x in range(0, consts.MAX_MAP_SIZE):
        for y in range(0, consts.MAX_MAP_SIZE):
            # draw text, full opacity
            if isText:
                draw.text((10 + y*(consts.FONT_SIZE), 10 + x*(consts.FONT_SIZE)), str(matrix[x][y]), font=fnt, fill=consts.COLOR_KEY[fullMap[x][y]])
            else:
                trunc = int(matrix[x][y])
                for i in range(0, consts.FONT_SIZE):
                    for j in range(0, consts.FONT_SIZE):
                        pixels[x*consts.FONT_SIZE + i, y*consts.FONT_SIZE + j] = (trunc, trunc, trunc, 255)

    image.show()
    image.save(imageName)

logging.info('Starting Map Generation...')

#Create Land
land_gen = land_generator(fullMap)
fullMap = land_gen.generateLand()

#Create Rivers
river_gen = river_generator(fullMap)
fullMap = river_gen.generateRivers(3)

#Create Biomes
biome_gen = biome_generator(fullMap)
fullMap = biome_gen.generate()
biome_gen.draw_moisture_map()

logging.info('Finished Map Generation...')

#Let's make it pretty to see what we have.
for x in range(consts.MAX_MAP_SIZE):
    for y in range(consts.MAX_MAP_SIZE):
        prettyMap[x][y] = consts.BIOMES[fullMap[x][y]]

makeImage(prettyMap, "result.jpg", True)
makeImage(biome_gen.height_map, "height.jpg", False)
