import math
from PIL import Image, ImageDraw, ImageFont
import random

fullMap = [[0 for x in range(0,100)] for y in range(0,100)]
prettyMap = [['.' for x in range(0,100)] for y in range(0,100)]

def heuristic(first, second):
    x1, y1 = first
    x2, y2 = second
    return abs(x1 - x2) + abs(y1 - y2)

def astar(start, goal, matrix):
    closedSet = []
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
    if x - 1 >= 0 and matrix[x - 1][y] != 0:
        retVal.append((x - 1, y))
        if y - 1 >= 0 and matrix[x - 1][y - 1] != 0:
            retVal.append((x - 1, y - 1))
        if y + 1 < len(matrix[0]) and matrix[x - 1][y + 1] != 0:
            retVal.append((x - 1, y + 1))
    if x + 1 < len(matrix) and matrix[x + 1][y] != 0:
        retVal.append((x + 1, y))
        if y - 1 >= 0  and matrix[x + 1][y - 1] != 0:
            retVal.append((x + 1, y - 1))
        if y + 1 < len(matrix[0]) and matrix[x + 1][y + 1] != 0:
            retVal.append((x + 1, y + 1))

    if y - 1 >= 0  and matrix[x][y - 1] != 0:
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

def isValid(point, matrix):
    x, y = point
    if x >= 0 and y >= 0 and x < len(matrix) and y < len(matrix[0]) and matrix[x][y] != 100:
        return True

    return False
