#Biome Dictionary
#Biomes are seperated into chunks based on temperature.
#Each chunk has 4 possibilities based on humidities. Wet, damp, normal, and dry.
#For example 10, 11, 12, 13 are Cold. 10 is Cold and Wet, 11 is Cold and Damp etc...
BIOMES = {
    #Special Biomes
    0 : '~', #Ocean
    1 : chr(250), #Land
    2 : '^', #Peaks
    3 : '≈', #Rivers

    #Cold Biomes
    10 : '+', #Wet      - Snowy
    11 : '•', #Average  - Tundra
    12 : '∞', #Dry      - Bare

    #Chilly Biomes
    13 : '☼', #Wet      - Taiga
    14 : '•', #Average  - Tundra
    15 : '∞', #Dry      - Bare

    #Temperate Biomes
    16 : '♣', #Temperate Deciduous
    17 : '"', #Shrubland
    18 : "Ö", #Savanna

    #Warmer Biomes
    19 : '♠', #Tropical Rainforest
    20 : 'ú', #Grassland
    21 : '~', #Temperate Desert

    #Hot Biomes
    22 : 'ô', #Tropical Forest
    23 : '~', #SubTropical Desert
    24 : '√' #Scorched
}

#Color Key for drawing the map.
COLOR_KEY = {
    0 : (0,0,255,255),
    1 : (0,200,0,255),
    '@' : (255,0,0,255),
    2 : (200,200,200,255),
    3 : (0,255,255,255),

    #Cold Biomes
    10 : (200, 200, 200, 255), #Snowy
    11 : (0, 139, 139, 255), #Tundra
    12 : (100, 100, 215, 255), #Bare

    #Chilly Biomes
    13 : (32,178,170), #Taiga
    14 : (0, 139, 139, 255), #Tundra
    15 : (155, 155, 155, 255), #Bare

    #Temperate Biomes
    16 : (34, 124, 34, 255), #Temperate Deciduous
    17 : (0, 222, 0, 255), #Shrubland
    18 : (165, 80, 80, 255), #Savanna

    #Warm Biomes
    19 : (0, 100, 0, 255), #Tropical Rainforest
    20 : (50, 255, 50, 255), #Grassland
    21 : (173,173,47), #Temperate Desert

    #Hot Biomes
    22 : (54, 145, 54, 255), #Tropcial Forest
    23 : (150, 150, 0, 255), #SubTropical Desert
    24 : (145, 145, 34, 255) #Scorched



}

#Land Settings
MAX_MAP_SIZE = 100
LACUNARITY = 3.0
PERSISTENCE = 0.31
SCALE = 10.0
OCTAVES = 4
LAND_THRESHOLD = 37
MOUNTAIN_THRESHOLD = 60

#River Settings
MIDPOINT_DISPLACE_ITERATIONS = 2

#Image Settings
FONT_SIZE = 22
IMAGE_SIZE = 10 + MAX_MAP_SIZE*(FONT_SIZE)
