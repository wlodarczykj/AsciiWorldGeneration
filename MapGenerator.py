import random
import sys
from PIL import Image, ImageDraw, ImageFont

#Settings
PROB_DROP = 60
INITIAL_CORE = 25
MAX_MAP_SIZE = 100

#Image Settings
FONT_SIZE = 15
IMAGE_SIZE = 10 + MAX_MAP_SIZE*(FONT_SIZE)
COLOR_KEY ={
    '~' : (0,0,255,255),
    '.' : (0,255,0,255)
}

fullMap = [[0 for x in range(0,MAX_MAP_SIZE)] for y in range(0,MAX_MAP_SIZE)]
prettyMap = [[0 for x in range(0,MAX_MAP_SIZE)] for y in range(0,MAX_MAP_SIZE)]
trackerMap = [[0 for x in range(0,MAX_MAP_SIZE)] for y in range(0,MAX_MAP_SIZE)]

def prettyPrintMap(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ''.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))
    #print >> f1, '\n'.join(table)

def makeImage(matrix):
    txt = Image.new('RGBA', (IMAGE_SIZE,IMAGE_SIZE), (0,0,0,0))
    fnt = ImageFont.truetype('Font/Roboto-black.ttf', FONT_SIZE)
    d = ImageDraw.Draw(txt)
    for x in range(0, MAX_MAP_SIZE):
        for y in range(0, MAX_MAP_SIZE):
            # draw text, full opacity
            d.text((10 + y*(FONT_SIZE), 10 + x*(FONT_SIZE)), matrix[x][y], font=fnt, fill=COLOR_KEY[matrix[x][y]])

    txt.show()

def generateMap(core):
    startX = random.randint(0,MAX_MAP_SIZE-1)
    startY = random.randint(0,MAX_MAP_SIZE-1)

    #place the core
    fullMap[startX][startY] = core
    if startX + 1 < len(trackerMap) and trackerMap[startX + 1][startY] == 0:
        genMapRec(startX + 1, startY, core)
    if startX - 1 >= 0 and trackerMap[startX - 1][startY] == 0:
        genMapRec(startX - 1, startY, core)
    if startY + 1 < len(trackerMap[0]) and trackerMap[startX][startY + 1] == 0:
        genMapRec(startX, startY + 1, core)
    if startY - 1 >= 0 and trackerMap[startX][startY - 1] == 0:
        genMapRec(startX, startY - 1, core)

def genMapRec(newX, newY, prevVal):
    newVal = 0
    #If another iteration already occupied this slot.
    if newX >= len(fullMap) or newY >= len(fullMap[0]):
        return
    if fullMap[newX][newY] != 0:
        return

    trackerMap[newX][newY] = 1

    if random.randint(0,100) < PROB_DROP:
        newVal = prevVal - 1
    else:
        newVal = prevVal

    if newVal != 0:
        fullMap[newX][newY] = newVal
        if newX + 1 < len(fullMap):
            genMapRec(newX + 1, newY, newVal)
        if newX - 1 >= 0:
            genMapRec(newX - 1, newY, newVal)
        if newY + 1 < len(fullMap):
            genMapRec(newX, newY + 1, newVal)
        if newY - 1 >= 0:
            genMapRec(newX, newY - 1, newVal)
    else:
        return

sys.setrecursionlimit(5000)

result = generateMap(INITIAL_CORE)
i = 0
for x in fullMap:
    j = 0
    for y in x:
        if y > 0:
            prettyMap[i][j] = '.'
        else:
            prettyMap[i][j] = '~'
        j = j + 1
    i = i + 1

#prettyPrintMap(fullMap)
print("")
prettyPrintMap(prettyMap)
makeImage(prettyMap)
