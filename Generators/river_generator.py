from util.astar import astar
from util.midpointdisp import midpointDisplacement
import constants as consts
import random
import logging

class river_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.coastPoints = []

    def getCoast(self):
        for x in range(consts.MAX_MAP_SIZE):
            for y in range(consts.MAX_MAP_SIZE):
                if self.nearWater((x,y)):
                    self.coastPoints.append((x,y))
        logging.info('Successfully completed marking the coast. Coastal Points marked: ' + str(len(self.coastPoints)))

    def nearWater(self, point):
        x, y = point
        retVal = False

        if x + 1 >= len(self.fullMap) or y + 1 >= len(self.fullMap[0]) or x - 1 < 0 or y - 1 < 0:
            return False

        if self.fullMap[x][y] == 0 or (self.fullMap[x+1][y] == 0 and self.fullMap[x-1][y] == 0 and self.fullMap[x][y+1] == 0 and self.fullMap[x][y-1] == 0):
            return retVal

        for xChange in range(-1,2):
            for yChange in range(-1,2):
                retVal = retVal or (self.fullMap[x + xChange][y + yChange] == 0)
        return retVal

    def findDirectRiver(self):
        self.getCoast()
        secondPoint = None
        path = None
        processedSecondPoints = []

        firstPoint = random.randint(0, len(self.coastPoints)- 1)
        firstPoint = self.coastPoints[firstPoint]
        processedSecondPoints = []
        processedSecondPoints.append(firstPoint)
        while not path:
            while not secondPoint or secondPoint in processedSecondPoints:
                secondPoint = random.randint(0, len(self.coastPoints) - 1)
                secondPoint = self.coastPoints[secondPoint]

            path = astar(firstPoint, secondPoint, self.fullMap)
            processedSecondPoints.append(secondPoint)

        logging.info('Found direct river.')
        return path

    def generateRivers(self, numRivers):
        for riverNum in range(numRivers):
            logging.info('Starting to create river ' + str(riverNum))
            path = self.findDirectRiver()

            if path:
                path = midpointDisplacement(path, consts.MIDPOINT_DISPLACE_ITERATIONS, self.fullMap)
                for tup in path:
                    x, y = tup
                    self.fullMap[x][y] = 3
        return self.fullMap
