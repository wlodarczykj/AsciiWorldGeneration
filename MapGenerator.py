import random
import sys
from PIL import Image, ImageDraw, ImageFont

#Settings
PROB_DROP = 65
INITIAL_CORE = 5
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

processList = []

def prettyPrintMap(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ''.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

def makeImage(matrix):
    txt = Image.new('RGBA', (IMAGE_SIZE,IMAGE_SIZE), (0,0,0,0))
    fnt = ImageFont.truetype('Font/Roboto-black.ttf', FONT_SIZE)
    d = ImageDraw.Draw(txt)
    for x in range(0, MAX_MAP_SIZE):
        for y in range(0, MAX_MAP_SIZE):
            # draw text, full opacity
            d.text((10 + y*(FONT_SIZE), 10 + x*(FONT_SIZE)), matrix[x][y], font=fnt, fill=COLOR_KEY[matrix[x][y]])

    txt.show()
    txt.save("result.bmp")

def generateMap(core):
    startX = random.randint(10,MAX_MAP_SIZE-10)
    startY = random.randint(10,MAX_MAP_SIZE-10)

    debugNum = 0
    #Place the core of the landmass and add it to our work list
    fullMap[startX][startY] = core
    processList = [(startX - 1, startY, spreadLand(core)), (startX + 1, startY, spreadLand(core)), (startX, startY - 1, spreadLand(core)), (startX, startY + 1, spreadLand(core))]

    #Trick to avoid recursion, basically instead of the stack keeping track of the work to do, processList will.
    while(len(processList) > 0):
        newVal = 0
        debugNum = debugNum + 1
        #print(debugNum)

        #extract the info from the processList using meaningful names
        newX = processList[0][0]
        newY = processList[0][1]
        prevVal = processList[0][2]

        if random.randint(0,100) < PROB_DROP:
            newVal = prevVal - 1
        else:
            newVal = prevVal

        if newVal > 0:
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
        print (len(processList))

    print(debugNum)

def spreadLand(oldVal):
    if random.randint(0,100) < PROB_DROP:
        return oldVal - 1
    else:
        return oldVal

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
