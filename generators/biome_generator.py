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

#HUMIDITY MAP COLORING
COLOR = {
    0 : (255,0,0,255),
    1 : (255,125,0,255),
    2 : (255,255,0,255),
    3 : (125,255,0,255),
    4 : (0,255,0,255),
    5 : (0,255,255,255),
    6 : (0,100,255,255),
    7 : (0,0,255,255)
}

class biome_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.moisture_map = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
        self.height_map = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]

    def generate(self):
        self.build_moisture_map()
        self.build_height_map()


        return self.fullMap

    def build_moisture_map(self):
        size = len(self.fullMap)
        seed = random.randint(0,1000000)
        logging.info('Using seed = ' + str(seed) + ' for humidity map generation.')

        for y in range(size):
            for x in range(size):
                v = snoise3(x / 33.0, y / 33.0, seed, 10, 0.37, 4.0)
                v = (v + 1) * 4
                self.moisture_map[x][y] = v

    def build_height_map(self):
        size = len(self.fullMap)
        seed = random.randint(0,1000000)
        logging.info('Using seed = ' + str(seed) + ' for height map generation.')

        for y in range(size):
            for x in range(size):
                v = snoise3(x / 33.0, y / 33.0, seed, 10, 0.37, 4.0)
                v = (v + 1)/2.0
                self.height_map[x][y] = v * 255

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
