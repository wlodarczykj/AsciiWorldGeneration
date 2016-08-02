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

#TODO: Big todo here, Refactor this completely, need to move it to another file FOR SURE
def findNearestRiverMouth(xPos, yPos):
    done = False
    searchOffset = 0

    #TODO Implement ENUM instead of magic
    searchOrder = [0,1,2,3]
    random.shuffle(searchOrder)

    for order in searchOrder:
        searchOffset = 0
        done = False
        while not done:
            searchOffset = searchOffset + 1
            newX = xPos
            newY = yPos

            if newX - searchOffset < 0 or newX + searchOffset >= len(fullMap) or newY - searchOffset < 0 or newY + searchOffset >= len(fullMap[0]):
                done = True
            else:
                #+x
                if order == 0:
                    newX = xPos + searchOffset
                    if fullMap[newX][yPos] == 0:
                        return (newX - 1, yPos)
                #-x
                elif order == 1:
                    newX = xPos - searchOffset
                    if fullMap[newX][yPos] == 0:
                        return (newX + 1, yPos)

                #+y
                elif order == 2:
                    newY = yPos + searchOffset
                    if fullMap[xPos][newY] == 0:
                        return (xPos, newY - 1)

                #-y
                else:
                    newY = yPos - searchOffset
                    if fullMap[newX][yPos] == 0:
                        return (xPos, newY + 1)

def generateRivers(numRivers):
    riverPoints = []
    while len(riverPoints) < 2:
        searchX = random.randint(10,consts.MAX_MAP_SIZE-10)
        searchY = random.randint(10,consts.MAX_MAP_SIZE-10)

        #Found land, generally speaking rivers always move towards some greater body of water
        #For our purposes since we have no lakes, that greater body of water has to be the ocean
        #So we need to find the ocean.
        if(fullMap[searchX][searchY] != 0):
            riverPoints.append(findNearestRiverMouth(searchX, searchY))

    path = astar(riverPoints[0], riverPoints[1], fullMap)
    midpointDisplacement(path, 4, fullMap)
    for tup in path:
        x, y = tup
        prettyMap[x][y] = '@'

def create_land():
    scale = 15.0
    size = len(fullMap)
    seed = random.randint(0,10000)

    for y in range(size):
        for x in range(size):
            v = pnoise3(x / scale, y / scale, seed, consts.OCTAVES, consts.PERSISTENCE, consts.LACUNARITY)
            v = (v+1)/2.0
            score = v * (size*2 - abs(x - (size/2)) - abs(y - (size/2)))
            if score <= 80.0:
                fullMap[x][y] = 0
            else:
                fullMap[x][y] = round(score, 2)
    return fullMap

create_land()

i = 0
for x in fullMap:
    j = 0
    for y in x:

        if y > 0 and prettyMap[i][j] != '@':
            prettyMap[i][j] = '_'
        elif prettyMap[i][j] != '@':
            prettyMap[i][j] = '~'
        j = j + 1
    i = i + 1

#prettyPrintMap(fullMap)
#print("")
#prettyPrintMap(prettyMap)
#makeImage(fullMap)
makeImage(prettyMap)
