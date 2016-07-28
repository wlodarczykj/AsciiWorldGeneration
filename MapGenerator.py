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
import constants as consts
import astar

fullMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
prettyMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]

islandList = []
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

def generateMap(core):
    startX = random.randint(10,consts.MAX_MAP_SIZE-10)
    startY = random.randint(10,consts.MAX_MAP_SIZE-10)

    islandList.append((startX, startY))
    debugNum = 0
    #Place the core of the landmass and add it to our work list
    fullMap[startX][startY] = core
    processList = [(startX - 1, startY, spreadLand(core)), (startX + 1, startY, spreadLand(core)), (startX, startY - 1, spreadLand(core)), (startX, startY + 1, spreadLand(core))]

    #Trick to avoid recursion, basically instead of the stack keeping track of the work to do, processList will.
    while(len(processList) > 0):
        debugNum = debugNum + 1
        #print(debugNum)

        #extract the info from the processList using meaningful names
        newX = processList[0][0]
        newY = processList[0][1]
        newVal = processList[0][2]

        if newVal > 0 and fullMap[newX][newY] == 0:
            fullMap[newX][newY] = newVal
            if newX + 1 < len(fullMap) and fullMap[newX + 1][newY] == 0:
                nextValue = spreadLand(newVal)
                if nextValue > 0 and fullMap[newX + 1][newY] == 0:
                    processList.append((newX + 1, newY, nextValue))
            if newX - 1 >= 0 and fullMap[newX - 1][newY] == 0:
                nextValue = spreadLand(newVal)
                if nextValue > 0 and fullMap[newX - 1][ newY] == 0:
                    processList.append((newX - 1, newY, nextValue))
            if newY + 1 < len(fullMap) and fullMap[newX ][newY + 1] == 0:
                nextValue = spreadLand(newVal)
                if nextValue > 0 and fullMap[newX][ newY + 1] == 0:
                    processList.append((newX, newY + 1, nextValue))
            if newY - 1 >= 0 and fullMap[newX][newY - 1] == 0:
                nextValue = spreadLand(newVal)
                if nextValue > 0 and fullMap[newX][ newY - 1] == 0:
                    processList.append((newX, newY - 1, nextValue))

        processList.pop(0)
    #generateRivers(1)

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

            if newX < 0 or newX >= len(fullMap) or newY < 0 or newY >= len(fullMap[0]):
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
    while numRivers > 0:
        searchX = random.randint(10,consts.MAX_MAP_SIZE-10)
        searchY = random.randint(10,consts.MAX_MAP_SIZE-10)

        #Found land, generally speaking rivers always move towards some greater body of water
        #For our purposes since we have no lakes, that greater body of water has to be the ocean
        #So we need to find the ocean.
        if(fullMap[searchX][searchY] != 0):
            tup = findNearestRiverMouth(searchX, searchY)
            prettyMap[tup[0]][tup[1]] = '@'
            numRivers = numRivers - 1




def spreadLand(oldVal):
    if random.randint(0,100) < consts.PROB_DROP:
        return oldVal - 1
    else:
        return oldVal

coreCounter = consts.INITIAL_CORE
while coreCounter > 0:
    if coreCounter <= 1:
        break

    #TODO REMOVE DEBUG
    newIsland = consts.INITIAL_CORE

    coreCounter = coreCounter - newIsland
    generateMap(newIsland)
    print(str(newIsland) + " | " + str(coreCounter))

print(islandList)

i = 0
for x in fullMap:
    j = 0
    for y in x:

        if y > 0 and prettyMap[i][j] != '@':
            prettyMap[i][j] = '~'
        elif prettyMap[i][j] != '@':
            prettyMap[i][j] = '_'
        j = j + 1
    i = i + 1

#prettyPrintMap(fullMap)
#print("")
#prettyPrintMap(prettyMap)
#makeImage(fullMap)
makeImage(prettyMap)
