import random
import astar

def displace(point, pathLength):
    random.seed()
    xDisp = random.randint(int(pathLength/-4), int(pathLength/4))
    yDisp = random.randint(int(pathLength/-4), int(pathLength/4))

    newPoint = (point[0] + xDisp, point[1] + yDisp)
    return newPoint


def midpointDisplacement(startPath, iterations):
    points = [startPath[0], startPath[len(path) - 1]]
    allPaths = [startPath]
    for i in range(0, iterations):
        newPointList = []
        newPointList.append(points[0])

        j = 1
        for path in allPaths:
            timeout = 0
            newPoint = (-1,-1)
            while not isValid(newPoint, fullMap) and timeout < 25:
                timeout = timeout + 1
                newPoint = displace(path[int(len(path) / 2)], len(path))

            newPointList.append(newPoint)
            newPointList.append(points[j])

            j = j + 1

        points = newPointList

        allPaths = []
        for i in range(0, len(points) - 1):
            allPaths.append(astar(points[i], points[i + 1], fullMap))
