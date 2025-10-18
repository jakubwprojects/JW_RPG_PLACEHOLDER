#######################################################################################################
### A-STAR PATH FINDING ALGORITHM #####################################################################
#######################################################################################################
# f = g + h <--- f - total cost, g - steps, h - manhatan distance -> return list of coordinates y, x ##
def a_star_path(map: list | tuple, start: tuple[int, int], end: tuple[int, int]) -> list:

    # Function calculates and returns manhatan distance #
    def manhatan_distance(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> int:
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

    # Checking fields - y, x #
    check_pos = ((-1, 0), (1, 0), (0, -1), (0, 1))
    # Find status #
    path_found = False
    # Calculating map edges #
    map_end_y = len(map)
    map_end_x = len(map[0])
    # Calculating starting h #
    h = manhatan_distance(start, end)
    # Starting g #
    g = 0
    # Starting f
    f = g + h
    # MAIN STRUCTURES #
    open = [[f, g, h, start, None]] # f, g, h, start_pos, parent
    closed = []
    # Analyzing path #
    while open:
        open.sort(key=lambda x: x[2]) # Sorting from min h
        open.sort(key=lambda x: x[0]) # Sorting from min f
        current_pos = open[0] # Assigning current analyzing position
        closed.append(open.pop(0)) # Moving current position to closed list
        # Checking if end - fields around player #
        if abs(current_pos[3][0] - end[0]) <= 1 and abs(current_pos[3][1] - end[1]) <= 1:
            end = current_pos[3]
            path_found = True
            break
        # Checking positions around current_pos #
        for y, x in check_pos:
            y_new = y + current_pos[3][0]
            x_new = x + current_pos[3][1]
            # Checking if not outside of map #
            if 0 <= y_new < map_end_y and 0 <= x_new < map_end_x:
                # Checking if field is empty #
                if map[y_new][x_new] != 1:
                    # Checking if field not in closed list #
                    if not any(e[3] == (y_new, x_new) for e in closed):
                        # Calculating g, h, f #
                        g = current_pos[1] + 1
                        h = manhatan_distance((y_new, x_new), end)
                        f = g + h
                        # Checking if field in open list #
                        open_check = [(i, e) for i, e in enumerate(open) if e[3] == (y_new, x_new)]
                        if open_check:
                            # Checking if new g is lower --> then replace element in open list #
                            if g < open_check[0][1][1]:
                                open[open_check[0][0]] = [f, g, h, (y_new, x_new), current_pos[3]]
                            continue
                        # Adding field to open list #
                        open.append([f, g, h, (y_new, x_new), current_pos[3]])
    # IF PATH FOUND --> Creating path coordinates list #
    if path_found:
        path_dict = {e[3]: e[4] for e in closed}
        path_list = [end]
        while start not in path_list:
            path_list.append(path_dict[path_list[-1]])
        path_list = path_list[::-1]
        # Return path coordinates from start to end #
        return path_list
    # IF PATH NOT FOUND --> return empty list #
    return []
#######################################################################################################
#######################################################################################################

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
