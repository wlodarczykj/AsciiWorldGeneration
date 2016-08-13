#Biome Dictionary
BIOMES = {
    0 : '~', #Ocean
    1 : chr(250), #Land
    2 : '^', #Peaks
    3 : 'X', #Rivers

    #High Elevation Biomes
    10 : 'A', #Snowy
    11 : 'B', #Tundra
    12 : 'C', #Bare
    13 : 'D', #Scorched

    #Med-High Biomes
    13 : 'E', #Taiga
    14 : 'F', #Shrubland
    15 : 'G', #Temperate Desert

    #Med-Low Biomes
    16 : 'H', #Temperate Rain Forest
    17 : 'I', #Temperate Deciduous
    18 : 'J', #Grassland
    19 : 'K', #Temperate Desert

    #Low Biomes
    20 : 'L', #Tropical Rainforest
    21 : 'M', #Tropcial Forest
    22 : 'N', #Grassland
    23 : 'O', #SubTropical Desert
}


#Color Key for drawing the map.
COLOR_KEY = {
    '~' : (0,0,255,255),
    chr(250) : (0,200,0,255),
    '@' : (255,0,0,255),
    '^' : (200,200,200,255),
    'X' : (175,175,0,255),
    '♣' : (255, 0, 0, 255),
    0 : (0,0,0,255)
}

#Land Settings
MAX_MAP_SIZE = 100
LACUNARITY = 5.0
PERSISTENCE = 0.35
SCALE = 15.0
OCTAVES = 12
LAND_THRESHOLD = 37
MOUNTAIN_THRESHOLD = 55

#River Settings
MIDPOINT_DISPLACE_ITERATIONS = 4

#Image Settings
FONT_SIZE = 22
IMAGE_SIZE = 10 + MAX_MAP_SIZE*(FONT_SIZE)
