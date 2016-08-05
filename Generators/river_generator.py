from util.astar import astar
from util.midpointdisp import midpointDisplacement
import constants as consts
import random

class river_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.coastPoints = []

    def getCoast(self):
        for x in range(consts.MAX_MAP_SIZE):
            for y in range(consts.MAX_MAP_SIZE):
                if self.nearWater((x,y)):
                    self.coastPoints.append((x,y))

    def nearWater(self, point):
        x, y = point
        retVal = False
        if self.fullMap[x][y] == 0:
            return retVal

        for xChange in range(-1,2):
            for yChange in range(-1,2):
                retVal = retVal or (self.fullMap[x + xChange][y + yChange] == 0)
        return retVal

    def findDirectRiver(self):
        done = False
        self.getCoast()
        firstPoint = None
        secondPoint = None
        path = None
        processedFirstPoints = []
        processedSecondPoints = []

        while not done:
            while not firstPoint or firstPoint in processedFirstPoints:
                firstPoint = random.randint(0, len(self.coastPoints)- 1)
                firstPoint = self.coastPoints[firstPoint]
            processedFirstPoints.append(firstPoint)
            if(len(self.coastPoints) == len(processedFirstPoints)):
                break
            processedSecondPoints = []
            processedSecondPoints.append(firstPoint)
            timeout = 0
            print(len(processedFirstPoints))
            while not path or timeout < 150:
                while not secondPoint or secondPoint in processedSecondPoints:
                    secondPoint = random.randint(0, len(self.coastPoints) - 1)
                    secondPoint = self.coastPoints[secondPoint]

                path = astar(firstPoint, secondPoint, self.fullMap)
                timeout += 1
            if timeout < 15:
                done = True

        print('Done! Found my path.')
        return path

    def generateRivers(self, numRivers):
        path = self.findDirectRiver()

        if path:
            #midpointDisplacement(path, consts.MIDPOINT_DISPLACE_ITERATIONS, self.fullMap)
            for tup in path:
                x, y = tup
                self.fullMap[x][y] = 3
            return self.fullMap
        else:
            return self.fullMap
