import pygame
import random
from enemies_config import dragon_fire_circle_attack, enemy_pos_boss
from MAIN_CONFIG import TILE_SIZE as rozmiar_pola
from assets import atak_gracza_grafika_rozszerzona
from przeciwnik import Przeciwnik
import instances
from instances import gracz


### DRAGON CLASS - REPRESENTS FINAL BOSS ###############################################################################
class Dragon(Przeciwnik):

    # Class enemy list #
    enemies = []

    ### Initializer ###
    def __init__(self, x, y, imie, map_lvl):
        super().__init__(x, y, imie, map_lvl)
        # Fire circle attack parameters #
        self.fire_circle_dmg = dragon_fire_circle_attack
        self.current_time_fire_circle = 0
        self.last_time_fire_circle = 0
        self.speed_fire_circle = 15 * 1000 # 15 seconds cooldown
        self.loading_fire_circle = False # Casting fire circle
        self.speed_loading_fire_circle = 2 * 1000 # 2 seconds casting time
        self.current_time_loading_fire_circle = 0
        self.fire_circle_animation = False
        self.fire_circle_area = ((-3, 0), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, -1), (-1, 0),
                                 (-1, 1), (-1, 2), (0, -3), (0, -2), (0, -1), (0, 1), (0,2), (0,3), (1, -2), (1, -1),
                                 (1, 0), (1, 1), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (3, 0))
        self.a = 1 # Drawing fire circle animation parameter
        self.immune = False
        self.final_line = 0
        self.dead_x = 0
        self.dead_y = 0
        self.dialogue_lines()

    ### Enemies loading ###
    @classmethod
    def load_enemies(cls, enemy_pos_boss):
        for enemy_name, positions in enemy_pos_boss.items():
            for x, y in positions:
                if enemy_name != "Pradawny Smok":
                    enemy = Przeciwnik(x, y, enemy_name, "boss")
                    enemy.x, enemy.y, enemy.x3, enemy.y3, enemy.status = 0, 0, 0, 0, False
                    Dragon.enemies.append(enemy)
                else:
                    instances.dragon = Dragon(x, y, enemy_name, "boss")
                    Dragon.enemies.append(instances.dragon)

    ### Movement - no move when casting spells ###
    def ruch(self, mapa_jwrpg):
        if not self.loading_fire_circle:
            super().ruch(mapa_jwrpg)

    ### Drawing large hp bar ###
    def draw_large_hp_bar(self):
        if self.hp > 0:
            color = "green2" if self.hp > 0.5 * self.max_hp else "yellow2" if self.hp > 0.2 * self.max_hp else "firebrick1"
            pygame.draw.rect(instances.window, "black", (353, 1000, 1214, 20))
            pygame.draw.rect(instances.window, color, (353, 1000, (self.hp * (1214)) / self.max_hp, 20))
            instances.window.blit(self.tekst_nazwa.render("Pradawny Smok", True, "mint cream"), (875, 970))

    ### Drawing casting bar ###
    def draw_casting_bar(self):
        if self.loading_fire_circle:
            bar_x = self.x3 * rozmiar_pola + instances.game_map.x
            bar_y = self.y3 * rozmiar_pola + instances.game_map.y - 10 - 15
            bar_width = rozmiar_pola
            bar_height = 10
            pygame.draw.rect(instances.window, "black", (bar_x, bar_y, bar_width, bar_height))
            elapsed_time = pygame.time.get_ticks() - self.current_time_loading_fire_circle
            percent_loaded = min(elapsed_time / self.speed_loading_fire_circle, 1.0)
            orange_width = int(bar_width * percent_loaded)
            pygame.draw.rect(instances.window, "orange", (bar_x, bar_y, orange_width, bar_height))

    ### Drawing fire circle attack animation ###
    def draw_fire_circle_animation(self):
        if self.fire_circle_animation:
            if self.a < 15:
                for y, x in self.fire_circle_area:
                    instances.window.blit(atak_gracza_grafika_rozszerzona,
                              ((self.x3 + x) * rozmiar_pola + instances.game_map.x,
                               (self.y3 + y) * rozmiar_pola + instances.game_map.y))
                self.a += 1
            elif self.a == 15:
                self.fire_circle_animation = False
                self.a = 1

    ### Spawning mobs ###
    @classmethod
    def spawn_enemies(cls, wave):
        waves = {1: ["Pirat"], 2: ["Korsarz"], 3: ["Pirat", "Korsarz"]}
        for enemy in cls.enemies:
            if type(enemy) == Przeciwnik and enemy.imie in waves[wave]:
                enemy.hp = enemy.max_hp
                enemy.status = True
                enemy.x = enemy.spawn_x
                enemy.y = enemy.spawn_y
                enemy.x3 = enemy.spawn_x
                enemy.y3 = enemy.spawn_y

    ### Large aoe attack around dragon ###
    def fire_circle_attack(self):
        # No attack
        if not self.loading_fire_circle:
            self.current_time_fire_circle = pygame.time.get_ticks() # Counting time only when not loading attack
            if self.current_time_fire_circle - self.last_time_fire_circle >= self.speed_fire_circle:
                if abs(self.x - gracz.x) <= 2 and abs(self.y - gracz.y) <= 2 and self.ilosc_ruchow == 0:
                    self.last_time_fire_circle = self.current_time_fire_circle
                    self.loading_fire_circle = True # Changing loading attack parameter
                    self.current_time_loading_fire_circle = pygame.time.get_ticks() # Starting casting point
        # Casting
        elif self.loading_fire_circle:
            now = pygame.time.get_ticks() # Counting time to cast
            if now - self.current_time_loading_fire_circle >= self.speed_loading_fire_circle:
                self.loading_fire_circle = False
                # Attack
                self.fire_circle_animation = True # Animation parameter
                for y, x in self.fire_circle_area:
                    if (self.y + y, self.x + x) == (gracz.y2, gracz.x2):
                        gracz.taken_dmg = random.randint(self.fire_circle_dmg[0], self.fire_circle_dmg[1])
                        gracz.hp -= gracz.taken_dmg
                        gracz.animacja_otrzymane_obrazenia = True
                        gracz.g = 42
                        if gracz.hp <= 0:
                            gracz.zycie = False
                            gracz.interakcja = True
                        break

    ### Dialogue lines after defeat ###
    def dialogue_lines(self):
        self.line_1 = "Myślisz, że wygrałeś śmiertelniku?"
        self.line_2 = "Najgorsze wkrótce nadejdzie..."
        self.line_3 = "Niech triumf stanie się twoim ciężarem."
        self.player_line_1 = "To twój koniec."
        self.player_line_2 = "<DOBIJ>"

    ### New game ###
    @classmethod
    def new_game(cls):
        for p in cls.enemies:
            instances.game_map.underground_map_jwrpg[p.y][p.x] = 0
        instances.game_map.underground_map_jwrpg[instances.dragon.dead_y][instances.dragon.dead_x] = 0
        cls.enemies.clear()
        cls.load_enemies(enemy_pos_boss)
########################################################################################################################