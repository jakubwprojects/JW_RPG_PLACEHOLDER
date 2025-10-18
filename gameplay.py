import pygame
import jwrpg_Blackjack
from przeciwnik import Przeciwnik
import instances
from instances import gracz as player
from instances import window, fps_clock


### GAMEPLAY CLASS - REPRESENTS GAMEPLAY LOOP ##########################################################################
class Gameplay:

    @staticmethod
    def gameplay(enemy_list, npc_list, loot_list, loot_quest, map_jwrpg):

        # Player movement if no interaction #
        if not player.interakcja:
            player.ruch(map_jwrpg)
            # Attack functions - depends on equipped weapon #
            if player.bron == "miecz": # sword
                player.atak(enemy_list, map_jwrpg)
                player.atak_zaznaczenie(enemy_list, map_jwrpg)
            elif player.bron == "luk": # bow
                player.atak_dystansowy(enemy_list, map_jwrpg)
                player.atak_dystansowy_zaznaczenie(enemy_list, map_jwrpg)
                player.atak_dystansowy_celowanie(enemy_list, map_jwrpg)
        # Marking enemy with mouse #
        player.zaznaczenie_przeciwnika(enemy_list)
        # Marking enemy with space button #
        player.zaznacz_przeciwnika_spacja(enemy_list)
        # Using potions #
        if not player.interakcja:
            player.potion()
        # Interaction with NPCs #
        player.interakcja_npc_NEW(npc_list)
        # Changing weapon #
        player.zmiana_broni()
        # Picking up loot #
        player.zbierz_loot(loot_list, loot_quest)
        # Updating map center coordinates #
        instances.game_map.get_center_coordinates()
        # Drawing map #
        instances.game_map.draw_map(window)
        # Drawing NPCs #
        for npc in npc_list:
            npc.rysowanie_npc(instances.game_map.x, instances.game_map.y, window)
        # Drawing loot on map #
        Przeciwnik.rysowanie_loota(Przeciwnik, instances.game_map.x, instances.game_map.y, loot_list, window)
        # Drawing player graphic #
        player.rysowanie_grafiki_gracza(window, fps_clock)
        # Sorting enemy list to draw in order #
        enemy_list.sort(key = lambda przeciwnik: przeciwnik.y)
        # Movement, attack, spawn and drawing for enemies #
        for enemy in enemy_list:
            enemy.spawn()
            if enemy.imie == "Zając": # Non agressive enemies
                enemy.ruch_zwierzeta(map_jwrpg)
            else: # Agressive enemies
                enemy.atak()
                if enemy.imie in ("Biały Pająk", "Korsarz"): # Additional ranged attack
                    enemy.atak_dystansowy(map_jwrpg)
                enemy.ruch(map_jwrpg)
            enemy.rysowanie_przeciwnika(instances.game_map.x, instances.game_map.y, window)
        # Drawing player additional elements - name, attacks etc. #
        player.rysowanie_elementow_gracza(instances.game_map.x, instances.game_map.y, window)
        # Drawing dialogue windows / npcs gui #
        if player.interakcja:
            for npc in npc_list:
                npc.rysowanie_okna_dialogowego_sklepu_kowala_blackjacka_NEW(window)
                npc.wybor_opcji() # Choosing option
        # Quest story #
        instances.quest_manager.quest_flow()
        # Blackjack minigame #
        if instances.flint.f > 0:
            jwrpg_Blackjack.gra(instances.flint, player, window)

        ### DEV TOOL --> NEEDS IMPROVEMENT
        #player.dev_tool()

        # Drawing player UI #
        player.draw_ui(window)
        # Drawing slight #
        player.rysowanie_celownik(window)
        # Changing map level #
        instances.game_map.change_map_level()
        # Refreshing display #
        pygame.display.update()

########################################################################################################################

    @staticmethod
    def final_boss_gameplay(enemy_list, loot_list, loot_quest, map_jwrpg):

        # Player movement #
        if player.zycie and not player.interakcja:
            player.ruch(map_jwrpg)
            # Attack functions - depends on equipped weapon #
            if player.bron == "miecz": # sword
                player.atak(enemy_list, map_jwrpg)
                player.atak_zaznaczenie(enemy_list, map_jwrpg)
            elif player.bron == "luk": # bow
                player.atak_dystansowy(enemy_list, map_jwrpg)
                player.atak_dystansowy_zaznaczenie(enemy_list, map_jwrpg)
                player.atak_dystansowy_celowanie(enemy_list, map_jwrpg)
        # Marking enemy with mouse #
        player.zaznaczenie_przeciwnika(enemy_list)
        # Marking enemy with space button #
        player.zaznacz_przeciwnika_spacja(enemy_list)
        # Using potions #
        if player.zycie:
            player.potion()
        # Changing weapon #
        player.zmiana_broni()
        # Picking up loot #
        player.zbierz_loot(loot_list, loot_quest)
        # Updating map center coordinates #
        instances.game_map.get_center_coordinates()
        # Drawing map #
        instances.game_map.draw_map(window)
        # Drawing loot on map #
        Przeciwnik.rysowanie_loota(Przeciwnik, instances.game_map.x, instances.game_map.y, loot_list, window)
        # Drawing player graphic #
        player.rysowanie_grafiki_gracza(window, fps_clock)
        # Sorting enemy list to draw in order #
        enemy_list.sort(key = lambda przeciwnik: przeciwnik.y)

        # Movement, attack, spawn and drawing for enemies #
        for enemy in enemy_list:
            enemy.atak()
            if enemy.imie in ("Biały Pająk", "Korsarz", "Pradawny Smok"): # Additional ranged attack
                enemy.atak_dystansowy(map_jwrpg)
            enemy.ruch(map_jwrpg)
            enemy.rysowanie_przeciwnika(instances.game_map.x, instances.game_map.y, window)

        ##################################################
        instances.dragon.fire_circle_attack()
        instances.dragon.draw_large_hp_bar()
        instances.dragon.draw_casting_bar()
        instances.dragon.draw_fire_circle_animation()
        ##################################################

        # Drawing player additional elements - name, attacks etc. #
        player.rysowanie_elementow_gracza(instances.game_map.x, instances.game_map.y, window)
        # Quest story #
        instances.quest_manager.quest_flow()
        # Drawing player UI #
        player.draw_ui(window)
        # Drawing slight #
        player.rysowanie_celownik(window)
        # Refreshing display #
        pygame.display.update()

########################################################################################################################