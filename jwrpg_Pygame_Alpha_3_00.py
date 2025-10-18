### JW RPG Alpha 3.00 #################################################################
#######################################################################################
import pygame
#######################################################################################
from config.player_config import start_pos
from config.npc_config import npc_main_lvl, npc_underground_lvl
from config.enemies_config import enemy_pos, enemy_pos_underground, enemy_pos_boss
### Main settings #####################################################################
from config.MAIN_CONFIG import DISPLAY_WIDTH as szerokosc_okna, DISPLAY_HEIGHT as wysokosc_okna
#######################################################################################
import instances
### Initializing pygame ###############################################################
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sky_city.ogg")
glosnosc = 0.5
pygame.mixer.music.set_volume(glosnosc)
pygame.mixer.music.play(-1)
instances.window = pygame.display.set_mode((szerokosc_okna, wysokosc_okna), pygame.FULLSCREEN)
okno = instances.window
instances.fps_clock = pygame.time.Clock()
zegar_fps = instances.fps_clock
game_state = "menu"
#######################################################################################
### Creating instances of PLAYER, ENEMIES, NPCs, MENU, MAP ############################
#######################################################################################
from gracz import Gracz
instances.gracz = Gracz.load_player(Gracz, start_pos)
gracz = instances.gracz
#######################################################################################
from npc import NPC
(instances.thorne, instances.torin, instances.garrick, instances.miranda, instances.kowal, instances.vane,
 instances.flint) = NPC.load_npc(NPC, npc_main_lvl, npc_underground_lvl)
NPC.load_dialogue_lines(NPC)
#######################################################################################
from przeciwnik import Przeciwnik
Przeciwnik.load_enemies(Przeciwnik, enemy_pos, enemy_pos_underground)
from dragon import Dragon
Dragon.load_enemies(enemy_pos_boss)
#######################################################################################
from menu_class import Menu
menu = Menu()
#######################################################################################
from map_class import Map
instances.game_map = Map()
game_map = instances.game_map
#######################################################################################
from gameplay import Gameplay
#######################################################################################
from quest_manager import QuestManager
instances.quest_manager = QuestManager()
#######################################################################################
#######################################################################################


### GAME LOOP ##########################################################################################################
########################################################################################################################
while True:

    ### FPS ###
    zegar_fps.tick(60) # 60 FPS

    ### EVENTS ###
    for event in pygame.event.get():
        # Warunek wyjścia z pętli
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Zdarzenia naciśnięcia klawisza na klawiaturze
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if glosnosc < 1:
                    glosnosc = glosnosc + 0.1
                    pygame.mixer.music.set_volume(glosnosc)
            elif event.key == pygame.K_o:
                if glosnosc > 0:
                    glosnosc = glosnosc - 0.1
                    pygame.mixer.music.set_volume(glosnosc)
            elif event.key == pygame.K_l:
                pygame.quit()
                exit()

            ### DEV - zmiana poziomu mapy ###
            elif event.key == pygame.K_m:
                game_map.main_map_jwrpg[gracz.y2][gracz.x2] = 0
                game_map.level = "underground"
            elif event.key == pygame.K_b:
                game_map.underground_map_jwrpg[gracz.y2][gracz.x2] = 0
                game_map.level = "main"
            #############

            elif event.key == pygame.K_ESCAPE:
                pygame.time.delay(100)
                if game_state == "gameplay":
                    pygame.mouse.set_visible(True)
                    game_state = "menu"
                else:
                    if menu.type == "menu2":
                        game_state = "gameplay"
                    elif menu.type in ("load", "save"):
                        if menu.starting_type == "menu1":
                            menu.type = "menu1"
                        else:
                            menu.type = "menu2"

    ### GAMEPLAY ###
    if game_state == "gameplay":
        # Main level #
        if game_map.level == "main":
            Gameplay.gameplay(Przeciwnik.przeciwnicy_powierzchnia, NPC.npc_powierzchnia, Przeciwnik.loot_powierzchnia,
                              Przeciwnik.loot_przedmioty_fabula_powierzchnia, game_map.main_map_jwrpg)
        # Underground level #
        elif game_map.level == "underground":
            Gameplay.gameplay(Przeciwnik.przeciwnicy_podziemia, NPC.npc_podziemia, Przeciwnik.loot_podziemia,
                              Przeciwnik.loot_przedmioty_fabula_podziemia, game_map.underground_map_jwrpg)
        # Final boss fight #
        else:
            Gameplay.final_boss_gameplay(Dragon.enemies, Przeciwnik.loot_podziemia,
                                         Przeciwnik.loot_przedmioty_fabula_podziemia, game_map.underground_map_jwrpg)
    ### MENU ###
    elif game_state == "menu":
        menu.draw_menu(okno)
        game_state = menu.choose_action(game_state)
########################################################################################################################
########################################################################################################################