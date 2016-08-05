#########
#
#   This project is purely for training purposes, and use of it is free to anyone
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#       1. Need to refactor.
#       2. Need to Move this logic to a class and have a driver outside
#       3. Need to Move river generation logic out as well.
#       4. Find another better font for this purpose.
#       5. Cleanup debugging logic
#   NOTE:
#       1.A possible improvement is to use a low prob_drop (roughly 50 to 55%). Then fill in the small holes.
#       2.If I implement the above solution I will need to procedurally generate lakes and ponds. Gulfs should be safe
#
#
#
#
#########

import random
import sys
from PIL import Image, ImageDraw, ImageFont
from noise import pnoise3, snoise3
import constants as consts
from generators.river_generator import river_generator
from util.astar import astar
from util.midpointdisp import midpointDisplacement

fullMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
prettyMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]

islandList = {}
processList = []

def prettyPrintMap(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ''.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

def makeImage(matrix):
    txt = Image.new('RGBA', (consts.IMAGE_SIZE,consts.IMAGE_SIZE), (0,0,0,0))
    fnt = ImageFont.truetype('Font/Roboto-black.ttf', consts.FONT_SIZE)
    d = ImageDraw.Draw(txt)
    for x in range(0, consts.MAX_MAP_SIZE):
        for y in range(0, consts.MAX_MAP_SIZE):
            # draw text, full opacity

            d.text((10 + y*(consts.FONT_SIZE), 10 + x*(consts.FONT_SIZE)), str(matrix[x][y]), font=fnt, fill=consts.COLOR_KEY[matrix[x][y]])


    txt.show()
    txt.save("result.bmp")


def create_land():
    scale = 35.0
    size = len(fullMap)
    seed = random.randint(0,10000)

    for y in range(size):
        for x in range(size):
            v = pnoise3(x / scale, y / scale, seed, consts.OCTAVES, consts.PERSISTENCE, consts.LACUNARITY)
            v = (v+1)/2.0
            xScore = v * (size - abs(x - (size/2.0)))
            yScore = v * (size - abs(y - (size/2.0)))
            if xScore >= consts.MOUNTAIN_THRESHOLD and yScore >= consts.MOUNTAIN_THRESHOLD:
                fullMap[x][y] = 2
            elif xScore >= consts.LAND_THRESHOLD and yScore >= consts.LAND_THRESHOLD:
                fullMap[x][y] = 1
            else:
                fullMap[x][y] = 0
    return fullMap


create_land()
river_gen = river_generator(fullMap)
fullMap = river_gen.generateRivers(1)

for x in range(consts.MAX_MAP_SIZE):
    for y in range(consts.MAX_MAP_SIZE):
        if x <= 3 or x >= consts.MAX_MAP_SIZE - 3 or y <= 3 or y >= consts.MAX_MAP_SIZE - 3:
            prettyMap[x][y] = '~'
        elif fullMap[x][y] == 3:
            prettyMap[x][y] = 'X'
        elif fullMap[x][y] == 2:
            prettyMap[x][y] = '^'
        elif fullMap[x][y] == 1:
            prettyMap[x][y] = '_'
        else:
            prettyMap[x][y] = '~'

makeImage(prettyMap)
