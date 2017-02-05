#Biome Dictionary
BIOMES = {
    0 : '~', #Ocean
    1 : chr(250), #Land
    2 : '^', #Peaks
    3 : '≈', #Rivers

    #High Elevation Biomes
    10 : ':', #Snowy
    11 : '•', #Tundra
    12 : '∞', #Bare
    13 : '√', #Scorched

    #Med-High Biomes
    14 : '☼', #Taiga
    15 : '"', #Shrubland
    16 : 'Ö', #Temperate Desert
    17 : 'Ö',

    #Med-Low Biomes
    18 : '⌠', #Temperate Rain Forest
    19 : '♣', #Temperate Deciduous
    20 : chr(250), #Grassland
    21 : '~', #Temperate Desert

    #Low Biomes
    22 : '♠', #Tropical Rainforest
    23 : 'ô', #Tropical Forest
    24 : 'ú', #Grassland
    25 : '~', #SubTropical Desert
}


#Color Key for drawing the map.
COLOR_KEY = {
    0 : (0,0,255,255),
    1 : (0,200,0,255),
    '@' : (255,0,0,255),
    2 : (200,200,200,255),
    3 : (0,255,255,255),

    #High Elevation Biomes
    10 : (200, 200, 200, 255), #Snowy
    11 : (0, 139, 139, 255), #Tundra
    12 : (155, 155, 155, 255), #Bare
    13 : (145, 145, 34, 255), #Scorched

    #Med-High Biomes
    14 : (32,178,170), #Taiga
    15 : (0, 222, 0, 255), #Shrubland
    16 : (173,255,47), #Temperate Desert
    17 : (0, 128, 0, 255), #Temperate Desert♦♣☺☻♥♠

    #Med-Low Biomes
    18 : (0, 100, 0, 255), #Temperate Rain Forest
    19 : (34, 139, 34, 255), #Temperate Deciduous
    20 : (0, 128, 0, 255), #Grassland
    21 : (255, 255, 0, 255), #Temperate Desert

    #Low Biomes
    22 : (0, 100, 0, 255), #Tropical Rainforest
    23 : (54, 145, 54, 255), #Tropcial Forest
    24 : (50, 205, 50, 255), #Grassland
    25 : (150, 150, 0, 255) #SubTropical Desert
}

#Land Settings
MAX_MAP_SIZE = 100
LACUNARITY = 5.0
PERSISTENCE = 0.23
SCALE = 10.0
OCTAVES = 10
LAND_THRESHOLD = 37
MOUNTAIN_THRESHOLD = 60

#River Settings
MIDPOINT_DISPLACE_ITERATIONS = 4

#Image Settings
FONT_SIZE = 22
IMAGE_SIZE = 10 + MAX_MAP_SIZE*(FONT_SIZE)
