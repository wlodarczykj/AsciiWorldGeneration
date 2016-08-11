#########
#
#   This project is purely for training purposes, and use of it is free to anyone
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#       1. Need to refactor.
#       2. Add Logging.
#       3. Improve Rivers.
#       4. Add Biomes.
#       5. Add Civilization.
#   NOTE:
#       1. I wonder how I can make the map bigger and show off more stuff.
#
#########

import random
import sys
import constants as consts
import logging
from PIL import Image, ImageDraw, ImageFont
from noise import pnoise3, snoise3
from generators.river_generator import river_generator
from util.astar import astar
from util.midpointdisp import midpointDisplacement

#MAPS
fullMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
prettyMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
heightMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]

SEED = random.randint(0,10000)

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
        image = Image.new('RGBA', (newSize, newSize), (10,10,10,255))

    fnt = ImageFont.truetype('Font/DF_Mayday_16x16.ttf', consts.FONT_SIZE)
    draw = ImageDraw.Draw(image)
    pixels = image.load()

    for x in range(0, consts.MAX_MAP_SIZE):
        for y in range(0, consts.MAX_MAP_SIZE):
            # draw text, full opacity
            if isText:
                draw.text((10 + y*(consts.FONT_SIZE), 10 + x*(consts.FONT_SIZE)), str(matrix[x][y]), font=fnt, fill=consts.COLOR_KEY[matrix[x][y]])
            else:
                trunc = int(matrix[x][y])
                pixels[x,y] = (trunc, trunc, trunc, 255)

    image.show()
    image.save(imageName)


def create_land():
    scale = consts.SCALE
    size = len(fullMap)

    for y in range(size):
        for x in range(size):
            v = pnoise3(x / scale, y / scale, SEED, consts.OCTAVES, consts.PERSISTENCE, consts.LACUNARITY)
            v = (v+1)/2.0
            xScore = v * (size - abs(x - (size/2.0)))
            yScore = v * (size - abs(y - (size/2.0)))
            heightMap[x][y] = (xScore + yScore) * (255 / (4 * size))
            if xScore >= consts.MOUNTAIN_THRESHOLD and yScore >= consts.MOUNTAIN_THRESHOLD:
                fullMap[x][y] = 2
            elif xScore >= consts.LAND_THRESHOLD and yScore >= consts.LAND_THRESHOLD:
                fullMap[x][y] = 1
            else:
                fullMap[x][y] = 0
    return fullMap

def clear_edges():
    for x in range(0,4):
        for y in range(0,4):
            fullMap[x][y] = 0

logging.info('Starting Map Generation...')
create_land()
clear_edges()
river_gen = river_generator(fullMap)
fullMap = river_gen.generateRivers(1)
logging.info('Finished Map Generation...')

for x in range(consts.MAX_MAP_SIZE):
    for y in range(consts.MAX_MAP_SIZE):
        if fullMap[x][y] == 3:
            prettyMap[x][y] = 'X'
        elif fullMap[x][y] == 2:
            prettyMap[x][y] = '^'
        elif fullMap[x][y] == 1:
            prettyMap[x][y] = chr(250)
        else:
            prettyMap[x][y] = '~'

makeImage(prettyMap, "result.bmp", True)
makeImage(heightMap, "height.bmp", False)
