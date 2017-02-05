#########
#
#   Land Generator
#   Creates a two matrices, one being the height map and another being the land map
#   This is where all the generation starts, since the rest need land to do anything.
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#
#   NOTE:
#
#########

import constants as consts
import random
import logging
from noise import pnoise3, snoise3

SEED = random.randint(0,1000000)

class land_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.heightMap = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
        logging.info('Using seed = ' + str(SEED) + ' for land generation')

    def generateLand(self):
        scale = consts.SCALE
        size = len(self.fullMap)

        for y in range(size):
            for x in range(size):
                v = pnoise3(x / scale, y / scale, SEED, consts.OCTAVES, consts.PERSISTENCE, consts.LACUNARITY)
                #Normally the value is in the range [-1, 1] so we need to make it non-negative by adding 1 and dividing my 2.0
                v = (v+1)/2.0
                xScore = v * (size - abs(x - (size/2.0)))
                yScore = v * (size - abs(y - (size/2.0)))
                self.heightMap[x][y] = (xScore + yScore) * (255 / (4 * size))

                #Determine what is Land vs Mountainous vs Water
                if xScore >= consts.MOUNTAIN_THRESHOLD and yScore >= consts.MOUNTAIN_THRESHOLD:
                    self.fullMap[x][y] = 2
                elif xScore >= consts.LAND_THRESHOLD and yScore >= consts.LAND_THRESHOLD:
                    self.fullMap[x][y] = 1
                else:
                    self.fullMap[x][y] = 0
        return self.fullMap
