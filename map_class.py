import pygame
from pytmx import load_pygame
from MAIN_CONFIG import TILE_SIZE, MAP_SIZE, BASIC_TILE, DISPLAY_WIDTH, DISPLAY_HEIGHT
from instances import gracz as player

MAIN_LEVEL = "mapa_2_00_placeholder.tmx"
UNDERGROUND_LEVEL = "mapa_2_00_podziemia_placeholder.tmx"
CHANGE_LEVEL_COORDINATES = ((66, 12), (14,20))


### MAP CLASS - REPRESENTS MAP OBJECT ##################################################################################
class Map:

    ### Initializer of instance ###
    def __init__(self):

        self.level = "main" # "main"/"underground"
        self.load_map()
        self.change_level_coordinates = CHANGE_LEVEL_COORDINATES
        self.get_center_coordinates()

    ### Function loads maps from files and creates scaled draw maps, movement/collision maps, water maps ###
    def load_map(self):

        # Loading maps from files #
        main_level = load_pygame(MAIN_LEVEL)
        underground_level = load_pygame(UNDERGROUND_LEVEL)

        # Function scales all layers of map #
        def map_scaling(num_of_layers, level):
            map_draw = [[] for _ in range(num_of_layers)]
            for i, map in enumerate(map_draw):
                for y in range(MAP_SIZE):
                    row = []
                    for x in range(MAP_SIZE):
                        image = level.get_tile_image(x, y, i)
                        if not image:
                            row.append(None)
                            continue
                        original_rect = image.get_rect()
                        expanded_image = pygame.transform.scale(image, (
                        original_rect.width * TILE_SIZE / BASIC_TILE, original_rect.height * TILE_SIZE / BASIC_TILE))
                        row.append(expanded_image)
                    map.append(tuple(row))
                map_draw[i] = tuple(map_draw[i])
            map_draw = tuple(map_draw)
            return map_draw

        # Function creates movement/collision map or water map #
        def movement_or_water_map(layer_num, level, type):
            map = []
            for y in range(0, MAP_SIZE):
                row = []
                for x in range(0, MAP_SIZE):
                    image = level.get_tile_image(x, y, layer_num)
                    if not image:
                        row.append(0)
                        continue
                    row.append(1)
                map.append(row if type == "movement" else tuple(row))
            return map if type == "movement" else tuple(map)

        # Loading and scaling water images to list #
        def load_water_images():
            def scale(image):
                original_rect = image.get_rect()
                image = pygame.transform.scale(image, (
                original_rect.width * TILE_SIZE / BASIC_TILE, original_rect.height * TILE_SIZE / BASIC_TILE))
                return image

            water_list = [main_level.get_tile_image(74 + x, 30, 5) for x in range(0, 12)]
            water_list = tuple(map(scale, water_list))
            return water_list

        # Creating attributes - scaled draw maps, movement/collision maps, water maps #
        self.main_map_draw = map_scaling(4, main_level)
        self.underground_map_draw = map_scaling(4, underground_level)
        self.main_map_jwrpg = movement_or_water_map(4, main_level, "movement")
        self.underground_map_jwrpg = movement_or_water_map(4, underground_level, "movement")
        self.main_map_water = movement_or_water_map(6, main_level, "water")
        self.underground_map_water = movement_or_water_map(5, underground_level, "water")
        self.water_images = load_water_images()
        self.water_parameter_1 = 0
        self.water_parameter_2 = 0

    ### Function calculates the center of map ###
    def get_center_coordinates(self):

        self.x = (DISPLAY_WIDTH - TILE_SIZE) // 2 - player.x * TILE_SIZE
        self.y = (DISPLAY_HEIGHT - TILE_SIZE) // 2 - player.y * TILE_SIZE

    ### Map drawing ###
    def draw_map(self, window):

        # Defining ranges #
        range_x1 = player.x2 - 7
        range_x2 = player.x2 + 8
        range_y1 = player.y2 - 6
        range_y2 = player.y2 + 7
        map = self.main_map_draw if self.level == "main" else self.underground_map_draw
        water = self.main_map_water if self.level == "main" else self.underground_map_water

        # Drawing #
        for z in range(len(map)):
            for y in range(range_y1, range_y2):
                for x in range(range_x1, range_x2):
                    if not map[z][y][x]:
                        continue
                    if z == 0:
                        if water[y][x] == 1:
                            window.blit(self.water_images[self.water_parameter_2],
                                      (x * TILE_SIZE + self.x, y * TILE_SIZE + self.y))
                            continue
                    window.blit(map[z][y][x], (x * TILE_SIZE + self.x, y * TILE_SIZE + self.y))

        # Changing water parameters #
        self.water_parameter_1 += 1
        if self.water_parameter_1 % 6 == 0:
            self.water_parameter_2 += 1
        if self.water_parameter_2 == 12:
            self.water_parameter_2 = 0
            self.water_parameter_1 = 0

    ### Change map level ###
    def change_map_level(self):

        if (player.y, player.x) in self.change_level_coordinates:
            if self.level == "main":
                self.main_map_jwrpg[player.y2][player.x2] = 0
                self.level = "underground"
            else:
                self.underground_map_jwrpg[player.y2][player.x2] = 0
                self.level = "main"
            player.y += 1
            player.y2 += 1
            player.m = 1
########################################################################################################################