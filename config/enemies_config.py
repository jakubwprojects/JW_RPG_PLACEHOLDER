### ENEMIES - Statistics and parameters ###

enemies = {"Wilk":          {"hp": 100, "exp": 30, "attack": (5, 15), "dist_attack": None,
                             "speed": 25, "gold": (5, 10)},
           "Pająk":         {"hp": 150, "exp": 70, "attack": (10, 20), "dist_attack": None,
                             "speed": 25, "gold": (10, 15)},
           "Dzik":          {"hp": 100, "exp": 40, "attack": (7, 17), "dist_attack": None,
                             "speed": 25, "gold": (5, 15)},
           "Biały Pająk":   {"hp": 200, "exp": 100, "attack": (15, 25), "dist_attack": (5, 10),
                             "speed": 20, "gold": (15, 25)},
           "Zając":         {"hp": 10, "exp": 5, "attack": None, "dist_attack": None,
                             "speed": 25, "gold": (1, 10)},
           "Pirat":         {"hp": 250, "exp": 150, "attack": (30, 45), "dist_attack": None,
                             "speed": 20, "gold": (20, 30)},
           "Korsarz":       {"hp": 300, "exp": 250, "attack": (45, 60), "dist_attack": (20, 40),
                             "speed": 16, "gold": (30, 40)},
           "Pradawny Smok": {"hp": 5000, "exp": 1000, "attack": (5, 55), "dist_attack": (5, 55),
                             "speed": 20, "gold": (2000, 3000)}}

### BOSS SPECIAL ATTACK DMG ##########
dragon_fire_circle_attack = (300 * 2, 450 * 2)
######################################

### ENEMIES - Spawn positions (x, y) - 73 ###

### MAIN LVL - SURFACE - 41 ###

### Wolfes - 8 ###
wolf_pos = ((52, 61), (71, 54), (65, 66), (65, 78), (79, 68), (85, 77), (55, 72), (77, 81))
### Spiders - 6 ###
spider_pos = ((44, 85), (28, 83), (21, 78), (21, 70), (12, 72), (14, 64))
### Boars - 5 ###
boar_pos = ((38, 47), (29, 40), (31, 33), (23, 34), (39, 36))
### White Spiders - 8 ###
white_spider_pos = ((44, 32), (50, 28), (56, 25), (62, 27), (42, 53), (28, 47), (16, 42), (12, 57))
### Rabbits - 5 ###
rabbit_pos = ((31, 58), (30, 73), (40, 72), (25, 28), (34, 29))
### Pirates - 9 ###
pirate_pos = ((24, 18), (32, 12), (39, 26), (40, 10), (47, 18), (11, 19), (16, 11), (19, 26), (32, 19))

### UNDERGROUND LVL - 32 ###

### Spiders - 8 ###
spider_pos_underground = ((12, 74), (16, 78), (19, 85), (32, 83), (38, 78), (46, 77), (53, 83), (55, 75))
### Corsairs - 16 ###
corsair_pos_underground = ((11, 22), (21, 28), (28, 17), (40, 16), (40, 30), (32, 38), (32, 25), (23, 64),
                           (38, 61), (50, 54), (60, 60), (74, 54), (73, 68), (85, 63), (85, 74), (82, 86))
### Pirates - 8 ###
pirate_pos_underground = ((31, 66), (46, 61), (47, 48), (57, 54), (67, 66), (82, 57), (76, 77), (87, 83))

### BOSS LVL - 1 + 12 + 12###
pirate_pos_boss = ((71, 11), (65, 15), (78, 15), (58, 23), (70, 22), (81, 20), (77, 26), (61, 31), (71, 32),
                   (84, 30), (66, 35), (79, 36))
corsair_pos_boss = ((71, 11), (65, 15), (78, 15), (58, 23), (70, 22), (81, 20), (77, 26), (61, 31), (71, 32),
                   (84, 30), (66, 35), (79, 36))
dragon_pos_boss = ((70, 20),)

### ENEMY POSITIONS - dictionaries ###
enemy_pos = {"Wilk": wolf_pos, "Pająk": spider_pos, "Dzik": boar_pos, "Biały Pająk": white_spider_pos,
             "Zając": rabbit_pos, "Pirat": pirate_pos}
enemy_pos_underground = {"Pająk": spider_pos_underground, "Korsarz": corsair_pos_underground,
                         "Pirat": pirate_pos_underground}
enemy_pos_boss = {"Pirat": pirate_pos_boss, "Pradawny Smok": dragon_pos_boss, "Korsarz": corsair_pos_boss}
######################################