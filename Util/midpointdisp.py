import random
import logging
from util.astar import astar

def displace(point, pathLength, divisor):
    random.seed()

    xDisp = random.randint(int(pathLength/(-divisor)), int(pathLength/divisor) + 1)
    yDisp = random.randint(int(pathLength/(-divisor)), int(pathLength/divisor) + 1)

    logging.info("Displacing by X:" + str(xDisp) + " Y: " + str(yDisp))
    newPoint = (point[0] + xDisp, point[1] + yDisp)
    return newPoint


def midpointDisplacement(startPath, iterations, matrix):
    points = [startPath[0], startPath[len(startPath) - 1]]
    allPaths = [startPath]
    for i in range(0, iterations):
        newPointList = []
        newPointList.append(points[0])

        j = 1
        for path in allPaths:
            timeout = 0
            newPoint = (-1,-1)
            #Get the previous point so we can
            prevPoint = path[int(len(path) / 2) - 1]

            testPath = None

            while not isValid(prevPoint, newPoint, matrix) and timeout < 25:
                timeout = timeout + 1
                newPoint = displace(path[int(len(path) / 2)], len(path), timeout+1)

            if timeout >= 25:
                logging.info("Could not find a valid place to displace to in " + logging + " attempts.")

            newPointList.append(newPoint)
            newPointList.append(points[j])

            j += 1

        points = newPointList

        allPaths = []
        for i in range(0, len(points) - 1):
            allPaths.append(astar(points[i], points[i + 1], matrix))

    logging.info("AllPaths: " + str(allPaths))
    return consolidatePaths(allPaths)

def consolidatePaths(allPaths):
    retPath = []
    for path in allPaths:
        for point in path:
            retPath.append(point)

    return retPath

def isValid(prevPoint, point, matrix):
    x, y = point
    if x >= 0 and y >= 0 and x < len(matrix) and y < len(matrix[0]) and matrix[x][y] != 0:
        testPath = astar(prevPoint, point, matrix)
        if testPath:
            return True
        else:
            return False

    return False
