import math
from PIL import Image, ImageDraw, ImageFont

fullMap = [[0 for x in range(0,100)] for y in range(0,100)]
prettyMap = [['.' for x in range(0,100)] for y in range(0,100)]

def heuristic(first, second):
    x1, y1 = first
    x2, y2 = second
    return abs(x1 - x2) + abs(y1 - y2)

def astar(start, goal, matrix):
    closedSet = []
    print("Looking for path from " + str(start) + " to " + str(goal))
    cameFrom = {}
    fullmap = matrix

    gScore = {}#map with default value of Infinity
    fScore = {}#map with default value of Infinity

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            gScore[(i,j)] = float('inf')
            fScore[(i,j)] = float('inf')

    gScore[start] = 0
    fScore[start] = heuristic(start, goal)
    openSet = [(fScore[start], start)]

    #while there is stuff to evaluate
    counter = 0
    while openSet:
        counter = counter + 1
        openSet = sorted(openSet)
        #Get the current item, which is the first item in the list, and grab its
        #Value not the FScore
        current = openSet[0][1]

        if current == goal:
            return reconstruct_path(cameFrom, current)

        #Get rid of first elem
        openSet = openSet[1:]
        closedSet.append(current)
        neighbors = getNeighbors(current, matrix)

        for elem in neighbors:
            if elem in closedSet:
                continue

            tentative_gScore = gScore[current] + dist_between(current, elem)

            if tentative_gScore >= gScore[elem]:
                continue

            cameFrom[elem] = current
            gScore[elem] = tentative_gScore
            fScore[elem] = gScore[elem] + heuristic(elem, goal)
            if elem not in openSet:
                openSet.append((fScore[elem], elem))

    return []

def dist_between(first, second):
    x1, y1 = first
    x2, y2 = second

    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def getNeighbors(current, matrix):
    x, y = current
    retVal = []
    if x - 1 >= 0 and matrix[x - 1][y] != 100:
        retVal.append((x - 1, y))
        if y - 1 >= 0 and matrix[x - 1][y - 1] != 100:
            retVal.append((x - 1, y - 1))
        if y + 1 < len(matrix[0]) and matrix[x - 1][y + 1] != 100:
            retVal.append((x - 1, y + 1))
    if x + 1 < len(matrix) and matrix[x + 1][y] != 100:
        retVal.append((x + 1, y))
        if y - 1 >= 0  and matrix[x + 1][y - 1] != 100:
            retVal.append((x + 1, y - 1))
        if y + 1 < len(matrix[0]) and matrix[x + 1][y + 1] != 100:
            retVal.append((x + 1, y + 1))

    if y - 1 >= 0  and matrix[x][y - 1] != 100:
        retVal.append((x, y - 1))

    if y + 1 < len(matrix[0]) and matrix[x][y + 1] != 100:
        retVal.append((x, y + 1))


    return retVal

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def makeImage(matrix):
    txt = Image.new('RGBA', (100*15,100*15), (0,0,0,0))
    fnt = ImageFont.truetype('../Font/Roboto-black.ttf', 15)
    d = ImageDraw.Draw(txt)
    for x in range(0, 100):
        for y in range(0, 100):
            # draw text, full opacity
            if matrix[x][y] == 8:
                d.text((10 + y*(15), 10 + x*(15)), str(matrix[x][y]), font=fnt, fill=(100,100,255,255))
            else:
                d.text((10 + y*(15), 10 + x*(15)), str(matrix[x][y]), font=fnt, fill=(255,255,255,255))


    txt.show()
    txt.save("test.bmp")

pointA = (5,5)
pointB = (46, 80)
prettyMap[pointA[0]][pointA[1]] = 'S'
prettyMap[pointB[0]][pointB[1]] = 'E'

for i in range(0, len(fullMap) - 2):
    fullMap[i][50] = 100
    prettyMap[i][50] = '|'

path = astar(pointA, pointB, fullMap)


print("Path Length: " + str(len(path)))
for point in path:
    x, y = point
    prettyMap[x][y] = 8

makeImage(prettyMap)
