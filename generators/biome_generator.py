#########
#
#   Biome Generator
#   Creates two new matrices and modifies the map passed in and adds in other Biomes
#   At the moment it generates a humidity map, then based on height decides biomes
#   Temperature is not factored into this just yet.
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#       1. Need to add Temperature
#   NOTE:
#
#########

import random
import sys
import constants as consts
import logging
from PIL import Image, ImageDraw, ImageFont
from noise import pnoise3, snoise3

#SEED FOR PERLIN NOISE
random.seed()
SEED = random.randint(0,1000000)

#HUMIDITY MAP COLORING
COLOR = {
    0 : (255,0,0,255),
    1 : (255,125,0,255),
    2 : (255,255,0,255),
    3 : (125,255,0,255),
    4 : (0,255,0,255),
    5 : (0,255,255,255),
    6 : (0,100,255,255)
}

class biome_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.moisture_map = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
        logging.info('Using seed = ' + str(SEED) + ' for humidity map generation.')

    def generate(self):
        self.build_moisture_map()

        return self.fullMap

    def build_moisture_map(self):
        size = len(self.fullMap)

        for y in range(size):
            for x in range(size):
                v = snoise3(x / 17.0, y / 17.0, SEED, consts.OCTAVES, 0.05, 10.0)
                v = (v + 1) * 3.5
                self.moisture_map[x][y] = v

    def draw_moisture_map(self):
        image = Image.new('RGBA', (consts.IMAGE_SIZE,consts.IMAGE_SIZE), (10,10,10,255))
        pixels = image.load()
        for x in range(0, consts.MAX_MAP_SIZE):
            for y in range(0, consts.MAX_MAP_SIZE):
                trunc = int(self.moisture_map[x][y])
                for i in range(0, consts.FONT_SIZE):
                    for j in range(0, consts.FONT_SIZE):
                        pixels[x*consts.FONT_SIZE + i, y*consts.FONT_SIZE + j] = COLOR[trunc]

        image.show()
        image.save("moisture.bmp")
