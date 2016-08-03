import constants as consts
from util.astar import astar
from util.midpointdisp import midpointDisplacement

class RiverGen:
    def findNearestRiverMouth(xPos, yPos):
        done = False
        searchOffset = 0

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
        midpointDisplacement(path, consts.MIDPOINT_DISPLACE_ITERATIONS, fullMap)
        for tup in path:
            x, y = tup
            prettyMap[x][y] = 'X'
