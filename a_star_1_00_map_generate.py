### MAP GENERATOR FOR A-STAR PATH FINDER ##############################################################
#######################################################################################################
# generates map as list - player in the center, range of map equals to enemy movement activation ######
def generate_map_for_a_star(e_y, e_x, p_y, p_x, range_y, range_x, whole_map):

    # Calculating local map edges #
    min_y = p_y - range_y
    max_y = p_y + range_y + 1
    min_x = p_x - range_x
    max_x = p_x + range_x + 1
    # Slicing whole_map to get new local map #
    new_map = [row[min_x:max_x] for row in whole_map[min_y:max_y]]
    # Calculating player and enemy local coordinates - y, x #
    player_pos = (range_y, range_x) # <-- map center
    enemy_pos = (player_pos[0] + e_y - p_y, player_pos[1] + e_x - p_x)
    # Changing player field to 0 - allows pathfinder to find path #
    new_map[player_pos[0]][player_pos[1]] = 0
    # Returning new map, player_pos, enemy_pos
    return new_map, player_pos, enemy_pos
#######################################################################################################
#######################################################################################################