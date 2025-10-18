### PLAYER - Equipment upgrade parameters ###

### SWORD ###
sword_stats = {1: {"dmg": 10, "crit": 0},
               2: {"dmg": 20, "crit": 3, "points": 1},
               3: {"dmg": 30, "crit": 5, "points": 2},
               4: {"dmg": 40, "crit": 7, "points": 3},
               5: {"dmg": 50, "crit": 10, "points": 4}}
### BOW ###
bow_stats =   {1: {"dmg": 10, "crit": 0},
               2: {"dmg": 20, "crit": 3, "points": 1},
               3: {"dmg": 30, "crit": 5, "points": 2},
               4: {"dmg": 40, "crit": 7, "points": 3},
               5: {"dmg": 50, "crit": 10, "points": 4}}
### ARMOR ###
armor_stats = {1: {"hp": 0},
               2: {"hp": 50, "points": 1},
               3: {"hp": 100, "points": 2},
               4: {"hp": 150, "points": 3},
               5: {"hp": 200, "points": 4}}
### CAPE ###
cape_stats = {1: {"mp": 0},
              2: {"mp": 75, "points": 1},
              3: {"mp": 150, "points": 2},
              4: {"mp": 225, "points": 3},
              5: {"mp": 300, "points": 4}}
### BOOTS ###
boots_stats = {1: {"speed": 20, "info": 0},
               2: {"speed": 16, "info": 10, "points": 2},
               3: {"speed": 10, "info": 25, "points": 4},
               4: {"speed": 8, "info": 30, "points": 6}}

### PLAYER - Starting position (x, y) ###
start_pos = 89, 38

### LEVELING - LINEAR PROGRESSION 1-100 ###
progression_table = {1: (0, 300, 100, 100)} # min exp, max exp, hp, mp
increase = 100
base = 300
for lvl in range(2, 101):
    if lvl == 10: increase_hp, increase_mp = 20, 20
    else: increase_hp, increase_mp = 10, 10
    ### DICTIONARY WITH STATS FOR LEVELS 1-100
    progression_table[lvl] = (
    progression_table[lvl - 1][1], progression_table[lvl - 1][1] + base + increase * (lvl - 1),
    progression_table[lvl - 1][2] + increase_hp, progression_table[lvl - 1][3] + increase_mp)
############################################