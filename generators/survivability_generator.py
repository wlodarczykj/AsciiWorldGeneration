#########
#
#   Survivability
#   Creates a new matrix to define survivability. This uses previous
#   This is where all the generation starts, since the rest need land to do anything.
#   This is also the beginning of defining a Race within our world.
#
#   Therefore, this will require a Race to do anything with since each race's survivability
#   depends on the area.
#
#   Author: Jakub Wlodarczyk
#
#   TODO:
#
#   NOTE:
#
#########

class survivability_generator:
    def __init__(self, biomeMap, race):
        self.biomeMap = biomeMap
        logging.info('Generating survivability map for the ' + race.name + ' race')

    def generate(self):

        return self.survMap
