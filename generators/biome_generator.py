#########
#
#   Biome Generator
#   Creates two new matrices and modifies the map passed in and adds in other Biomes
#   At the moment it generates a humidity map, then based on temperature decides biomes
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
    0 : (0, 0, 255, 255),
    1 : (40, 125, 40, 255),
    2 : (255, 0, 0, 255),
}

biomeCounter = {}

class biome_generator:
    def __init__(self, mapMatrix):
        self.fullMap = mapMatrix
        self.moisture_map = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
        self.temperature_map = [[0 for x in range(0,consts.MAX_MAP_SIZE)] for y in range(0,consts.MAX_MAP_SIZE)]
        for i in range(10, 25):
            biomeCounter[i] = 0

    def generate(self):
        self.build_moisture_map()
        self.build_temperature_map()

        for x in range(0, consts.MAX_MAP_SIZE):
            for y in range(0, consts.MAX_MAP_SIZE):
                #Values range from [0,2]
                trunc_biome = int(self.moisture_map[x][y])
                humidity_biome_selector = trunc_biome

                #We need a value in the range of [0,4], so we need to manipulate our value.
                trunc_temperature = int(self.temperature_map[x][y] * (5.0/255.0) - 0.000001)
                temperature_biome_selector = trunc_temperature

                #Here we select the biome based on the consts Biome list.
                select = 10 + int(humidity_biome_selector + (3 * temperature_biome_selector))
                biomeCounter[select] += 1

                if self.fullMap[x][y] == 1:
                    self.fullMap[x][y] = select

        for i in range(10, 25):
            logging.info('Biome at ' + str(i) + ' used ' + str(biomeCounter[i]) + ' times.')

        return self.fullMap

    def build_moisture_map(self):
        size = len(self.fullMap)
        seed = random.randint(0,1000000)
        logging.info('Using seed = ' + str(seed) + ' for humidity map generation.')

        for y in range(size):
            for x in range(size):
                v = snoise3(x / 33.0, y / 33.0, seed, 3, 0.27, 4.0)
                #v is [-1, 1] so adding 1 makes it [0,2]
                #We need to select between 3 different humidities so we need to make it [0,3)
                #That is why we subtract 0.000001
                v = ((v + 1.0)* 3.0 / 2.0) - 0.000001
                self.moisture_map[x][y] = v

    def build_temperature_map(self):
        size = len(self.fullMap)
        seed = random.randint(0,1000000)
        logging.info('Using seed = ' + str(seed) + ' for temperature map generation.')

        for y in range(size):
            for x in range(size):
                v = snoise3(x / 15.0, y / 15.0, seed, 5, 0.25, 4.0)
                v = (v + 1)/2.0
                #The larger the value the closer it is to the middle of the map
                distanceFromCenterY = abs(y - (size/2.0))
                v = (v * 0.5) + 0.5

                yScore = (v) * (size*(3/5) - distanceFromCenterY)

                #Each square goes from [0,255] depending on temperature
                self.temperature_map[x][y] = yScore * 255.0/(size*(3/5))

    def draw_temperature_map(self):
        image = Image.new('RGBA', (consts.IMAGE_SIZE,consts.IMAGE_SIZE), (10,10,10,255))
        pixels = image.load()
        for x in range(0, consts.MAX_MAP_SIZE):
            for y in range(0, consts.MAX_MAP_SIZE):
                trunc = int(self.temperature_map[x][y])

                for i in range(0, consts.FONT_SIZE):
                    for j in range(0, consts.FONT_SIZE):
                        color = (int(self.temperature_map[x][y]), 0, 255 - int(self.temperature_map[x][y]), 255)
                        pixels[x*consts.FONT_SIZE + i, y*consts.FONT_SIZE + j] = color

        image.show()
        image.save("temperature.bmp")

    def draw_moisture_map(self):
        image = Image.new('RGBA', (consts.IMAGE_SIZE,consts.IMAGE_SIZE), (10,10,10,255))
        pixels = image.load()
        for x in range(0, consts.MAX_MAP_SIZE):
            for y in range(0, consts.MAX_MAP_SIZE):
                trunc = int(self.moisture_map[x][y])

                for i in range(0, consts.FONT_SIZE):
                    for j in range(0, consts.FONT_SIZE):
                        pixels[x*consts.FONT_SIZE + i, y*consts.FONT_SIZE + j] = COLOR[trunc]

#        image.show()
        image.save("moisture.bmp")
