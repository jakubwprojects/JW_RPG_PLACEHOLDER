import pygame
from pytmx import load_pygame
import random
import math
from enemies_config import enemies, enemy_pos, enemy_pos_underground
from MAIN_CONFIG import TILE_SIZE as rozmiar_pola
### A-star pathfinder 1_00 ############################################################
from a_star_1_00 import a_star_pathfinder
from a_star_1_00_map_generate import generate_map_for_a_star
#######################################################################################
import instances
from instances import gracz
from assets import *


### Tworzenie klasy - Przeciwnik ###
class Przeciwnik:

    ### LISTA PRZECIWNIKÓW - powierzchnia i podziemia ###
    przeciwnicy_powierzchnia = []
    przeciwnicy_podziemia = []
    #####################################################
    ### LISTA LOOT - atrybut klasy ######################
    loot_powierzchnia = []
    loot_podziemia = []
    loot_przedmioty_fabula_powierzchnia = []
    loot_przedmioty_fabula_podziemia = []
    #####################################################
    ### GRAFIKI PRZECIWNIKÓW ############################
    grafika_idle = {"Wilk": lista_grafika_wilk,
                    "Pająk": lista_grafika_pajak,
                    "Biały Pająk": lista_grafika_bialy_pajak,
                    "Dzik": lista_grafika_dzik,
                    "Zając": lista_grafika_zajac,
                    "Pirat": lista_grafika_pirat,
                    "Korsarz": lista_grafika_pirat_2}
    #####################################################
    grafika_move = {"Wilk": [lista_grafika_wilk_w, lista_grafika_wilk_s,
                             lista_grafika_wilk_a, lista_grafika_wilk_d],
                    "Pająk": [lista_grafika_pajak_w, lista_grafika_pajak_s,
                              lista_grafika_pajak_a, lista_grafika_pajak_d],
                    "Biały Pająk": [lista_grafika_bialy_pajak_w, lista_grafika_bialy_pajak_s,
                                    lista_grafika_bialy_pajak_a, lista_grafika_bialy_pajak_d],
                    "Dzik": [lista_grafika_dzik_w, lista_grafika_dzik_s,
                             lista_grafika_dzik_a, lista_grafika_dzik_d],
                    "Zając": [lista_grafika_zajac_w, lista_grafika_zajac_s,
                              lista_grafika_zajac_a, lista_grafika_zajac_d],
                    "Pirat": [lista_grafika_pirat_w, lista_grafika_pirat_s,
                              lista_grafika_pirat_a, lista_grafika_pirat_d],
                    "Korsarz": [lista_grafika_pirat_2_w, lista_grafika_pirat_2_s,
                                lista_grafika_pirat_2_a, lista_grafika_pirat_2_d]}
    #####################################################
    grafika_name = {"Wilk": (23, -37),
                    "Pająk": (23, -37),
                    "Biały Pająk": (-12, - 37),
                    "Dzik": (23, -37),
                    "Zając": (23, -37),
                    "Pirat": (23, -52),
                    "Korsarz": (5, -52),
                    "Pradawny Smok": (-35, -37)}
    ######################################################
    grafika_shift = {"Wilk": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Pająk": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Biały Pająk": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Dzik": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Zając": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Pirat": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
                     "Korsarz": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}}
    ######################################################

    # Inicjalizator
    def __init__(self, x, y, imie, map_lvl):
        ### Podstawowe parametry ############################
        self.x = x
        self.y = y
        self.imie = imie
        self.hp = enemies[imie]["hp"]
        self.max_hp = self.hp
        self.doswiadczenie = enemies[imie]["exp"]
        self.status = True
        self.predkosc_chodzenia = enemies[imie]["speed"]
        self.dmg = enemies[imie]["attack"]
        self.dist_dmg = enemies[imie]["dist_attack"]
        self.gold = enemies[imie]["gold"]
        ### Parametry do animacji, chodzenia, ataku i spawnu ###
        self.predkosc_ataku = 0.5  # 1 atak na 2 sekundy
        self.animacja_otrzymane_obrazenia = False
        self.animacja_otrzymane_obrazenia_2 = False
        self.g = 42.0  # Wartość do animacji otrzymwania obrażeń przez przeciwników
        self.g_2 = 42.0
        self.x2 = x  # Wartości do animacji dostawanego dmg przez przeciwnika
        self.y2 = y  # Wartości do animacji dostawanego dmg przez przeciwnika
        self.m = 1  # Wskaźnik mówiący o kierunku przeciwnika, zależny od jego ruchu
        self.x_tracker = self.x  # Parametry do funkcji ruchu
        self.y_tracker = self.y  # Parametry do funkcji ruchu
        self.kolizja = False  # Parametr do sprawdzania kolizji na trackerze
        self.ruch_tracker = 0  # Parametr do zwracania rodzaju ruchu z trackera
        self.ilosc_ruchow = 0
        self.x3 = self.x
        self.y3 = self.y
        self.czas_ostatniego_ataku = 0
        self.czas_ostatniego_ataku2 = 0
        self.spawn_x = self.x  # Współrzędna x do spawnu
        self.spawn_y = self.y  # Współrzęda y do spawnu
        self.tekst_nazwa = pygame.font.Font(None, 34)
        self.tekst_nazwa2 = pygame.font.Font(None, 32)
        self.zaznaczenie = False  # PARAMETR DO ZAZNACZANIA PRZECIWNIKÓW - True/False
        self.ss = 0  # Parametry do ataków dystansowych
        self.animacja_strzal = False
        self.funkcja_y2 = []
        self.funkcja_x2 = []
        self.funkcja_lambda2 = None
        self.critical_hit = False
        self.critical_hit_2 = False

        ### Spawn parameters ###
        self.aktualny_czas_spawn = 0
        self.czas_ostatniego_spawnu = 0
        self.predkosc_spawnu = 10 * 1000 # 10 sec
        self.dead_start_counting_time = True
        ########################

        ### Dodawanie przeciwników do list klasowych ########
        if map_lvl == "powierzchnia":
            Przeciwnik.przeciwnicy_powierzchnia.append(self)
        elif map_lvl == "podziemia":
            Przeciwnik.przeciwnicy_podziemia.append(self)
        #####################################################

    # Loading enemy objects - CLASS METHOD #
    def load_enemies(cls, enemy_pos_main, enemy_pos_underground):
        ### MAIN LEVEL - SURFACE ###
        for enemy_name, positions in enemy_pos_main.items():
            for x, y in positions:
                Przeciwnik(x, y, enemy_name, "powierzchnia")
        ### UNDERGROUND LEVEL ###
        for enemy_name, positions in enemy_pos_underground.items():
            for x, y in positions:
                Przeciwnik(x, y, enemy_name, "podziemia")

    # Rysowanie przeciwników
    def rysowanie_przeciwnika(self, mapa_x, mapa_y, okno):

        if self.status == True and abs(self.x - gracz.x) <= 7 and abs(self.y - gracz.y) <= 6:

            if self.imie != "Pradawny Smok":

                # SELECTING IMAGE #

                # IDLE #
                if self.ilosc_ruchow == 0:
                    image = Przeciwnik.grafika_idle[self.imie][self.m]

                # MOVEMENT #
                else:
                    image = Przeciwnik.grafika_move[self.imie][self.m]
                    if self.predkosc_chodzenia == 25:
                        if self.ilosc_ruchow in (25, 24, 23, 22, 21): image = image[0]
                        elif self.ilosc_ruchow in (20, 19, 18, 17): image = image[1]
                        elif self.ilosc_ruchow in (16, 15, 14, 13): image = image[2]
                        elif self.ilosc_ruchow in (12, 11, 10, 9): image = image[3]
                        elif self.ilosc_ruchow in (8, 7, 6, 5): image = image[4]
                        elif self.ilosc_ruchow in (4, 3, 2, 1): image = image[5]
                    elif self.predkosc_chodzenia == 20:
                        if self.ilosc_ruchow in (20, 19, 18, 17): image = image[0]
                        elif self.ilosc_ruchow in (16, 15, 14): image = image[1]
                        elif self.ilosc_ruchow in (13, 12, 11): image = image[2]
                        elif self.ilosc_ruchow in (10, 9, 8): image = image[3]
                        elif self.ilosc_ruchow in (7, 6, 5): image = image[4]
                        elif self.ilosc_ruchow in (4, 3, 2, 1): image = image[5]
                    elif self.predkosc_chodzenia == 16:
                        if self.ilosc_ruchow in (16, 15): image = image[0]
                        elif self.ilosc_ruchow in (14, 13, 12): image = image[1]
                        elif self.ilosc_ruchow in (11, 10, 9): image = image[2]
                        elif self.ilosc_ruchow in (8, 7, 6): image = image[3]
                        elif self.ilosc_ruchow in (5, 4, 3): image = image[4]
                        elif self.ilosc_ruchow in (2, 1): image = image[5]

                # DRAWING IMAGE #
                okno.blit(image,
                (self.x3 * rozmiar_pola + mapa_x + Przeciwnik.grafika_shift[self.imie][self.m][0] * rozmiar_pola / 32,
                 self.y3 * rozmiar_pola + mapa_y + Przeciwnik.grafika_shift[self.imie][self.m][1] * rozmiar_pola / 32))

                # DRAWING NAME #
                okno.blit(self.tekst_nazwa.render(self.imie, True, "floral white"),
                              (self.x3 * rozmiar_pola + Przeciwnik.grafika_name[self.imie][0] + mapa_x,
                               self.y3 * rozmiar_pola + Przeciwnik.grafika_name[self.imie][1] + mapa_y))


            elif self.imie == "Pradawny Smok":

                # Graphic
                pygame.draw.rect(okno, "orange", (
                    self.x3 * rozmiar_pola + mapa_x,
                    self.y3 * rozmiar_pola + mapa_y,
                    rozmiar_pola,
                    rozmiar_pola))
                # Name
                okno.blit(self.tekst_nazwa.render(self.imie, True, "floral white"),
                          (self.x3 * rozmiar_pola - 39 + mapa_x, self.y3 * rozmiar_pola - 37 + mapa_y))



            # Paski HP
            if self.imie == "Pirat" or self.imie == "Korsarz":
                pygame.draw.rect(okno, "black", (
                    self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10 - 15,
                    rozmiar_pola, 10))
                if self.hp > 0.5 * self.max_hp:
                    pygame.draw.rect(okno, "green2", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10 - 15,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))
                elif self.hp > 0.2 * self.max_hp:
                    pygame.draw.rect(okno, "yellow2", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10 - 15,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))
                elif self.hp >= 0:
                    pygame.draw.rect(okno, "firebrick1", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10 - 15,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))

            else:
                pygame.draw.rect(okno, "black", (
                    self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10, rozmiar_pola,
                    10))
                if self.hp > 0.5 * self.max_hp:
                    pygame.draw.rect(okno, "green2", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))
                elif self.hp > 0.2 * self.max_hp:
                    pygame.draw.rect(okno, "yellow2", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))
                elif self.hp >= 0:
                    pygame.draw.rect(okno, "firebrick1", (
                        self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y - 10,
                        (self.hp * rozmiar_pola) / self.max_hp, 10))

        # Otrzymywane obrażenia - atak obszarowy
        if self.animacja_otrzymane_obrazenia == True:
            if self.g < 106.0:
                if self.critical_hit:
                    okno.blit(self.tekst_nazwa2.render("CRITICAL HIT", True, "red"), (
                        self.x2 * rozmiar_pola - 25 + mapa_x, self.y2 * rozmiar_pola - self.g - 30 + mapa_y))
                okno.blit(self.tekst_nazwa2.render(f"{gracz.zadane_obrazenia}", True, "red"), (
                    self.x2 * rozmiar_pola + 35 + mapa_x, self.y2 * rozmiar_pola - self.g + mapa_y))
                if self.g < 50:
                    hit_index = 0
                elif self.g < 58:
                    hit_index = 1
                elif self.g < 66:
                    hit_index = 2
                elif self.g < 74:
                    hit_index = 3
                elif self.g < 82:
                    hit_index = 4
                elif self.g < 90:
                    hit_index = 5
                elif self.g < 98:
                    hit_index = 6
                elif self.g < 106:
                    hit_index = 7
                okno.blit(lista_blood_hit[hit_index], (self.x2 * rozmiar_pola + mapa_x - 16 * rozmiar_pola / 32,
                                                       self.y2 * rozmiar_pola + mapa_y - 16 * rozmiar_pola / 32))
                self.g += 2.0

            elif self.g == 106.0:
                self.animacja_otrzymane_obrazenia = False
                self.critical_hit = False
                self.g = 42.0

        # Otrzymywane obrażenia - atak zaznaczenie
        if self.animacja_otrzymane_obrazenia_2 == True:
            if self.g_2 < 106.0:
                if self.critical_hit_2:
                    okno.blit(self.tekst_nazwa2.render("CRITICAL HIT", True, "red"), (
                        self.x2 * rozmiar_pola - 25 + mapa_x, self.y2 * rozmiar_pola - self.g_2 - 30 + mapa_y))
                okno.blit(self.tekst_nazwa2.render(f"{gracz.zadane_obrazenia_2}", True, "red"), (
                    self.x2 * rozmiar_pola + 35 + mapa_x, self.y2 * rozmiar_pola - self.g_2 + mapa_y))
                if self.g_2 < 50:
                    hit_index = 0
                elif self.g_2 < 58:
                    hit_index = 1
                elif self.g_2 < 66:
                    hit_index = 2
                elif self.g_2 < 74:
                    hit_index = 3
                elif self.g_2 < 82:
                    hit_index = 4
                elif self.g_2 < 90:
                    hit_index = 5
                elif self.g_2 < 98:
                    hit_index = 6
                elif self.g_2 < 106:
                    hit_index = 7
                okno.blit(lista_blood_hit[hit_index], (self.x2 * rozmiar_pola + mapa_x - 16 * rozmiar_pola / 32,
                                                       self.y2 * rozmiar_pola + mapa_y - 16 * rozmiar_pola / 32))
                self.g_2 += 2.0

            elif self.g_2 == 106.0:
                self.animacja_otrzymane_obrazenia_2 = False
                self.critical_hit_2 = False
                self.g_2 = 42.0

        # Zaznaczenie przeciwnika przez gracza
        if self.zaznaczenie == True:
            pygame.draw.rect(okno, "brown2", (
                self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y, rozmiar_pola, 4))
            pygame.draw.rect(okno, "brown2", (
                self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y + rozmiar_pola - 4,
                rozmiar_pola, 4))
            pygame.draw.rect(okno, "brown2", (
                self.x3 * rozmiar_pola + mapa_x, self.y3 * rozmiar_pola + mapa_y, 4, rozmiar_pola))
            pygame.draw.rect(okno, "brown2", (
                self.x3 * rozmiar_pola + mapa_x + rozmiar_pola - 4, self.y3 * rozmiar_pola + mapa_y, 4,
                rozmiar_pola))

        # Rysowanie animacji lecenia pocisku w gracza
        if self.animacja_strzal == True:

            rotated_rect2 = kamien.get_rect()
            try:
                rotated_rect2.center = self.funkcja_lambda2(self.ss, mapa_x, mapa_y)
            except:
                self.ss = 0
                self.animacja_strzal = False
            # Rysowanie obróconego obrazka z dostosowanym prostokątem granicznym
            okno.blit(kamien, rotated_rect2)
            self.ss += 1
            try:
                if self.ss == len(self.funkcja_x2):
                    self.ss = 0
                    self.animacja_strzal = False
            except:
                if self.ss == len(self.funkcja_y2):
                    self.ss = 0
                    self.animacja_strzal = False

    # Przemieszczanie się przeciwnika do gracza
    def ruch(self, mapa_jwrpg):

        if self.status == True and abs(self.x - gracz.x) <= 8 and abs(self.y - gracz.y) <= 7:

            if self.ilosc_ruchow == 0:

                ### Funkcja wyliczająca ruch przeciwnika
                self.tracker(mapa_jwrpg)

                if self.ruch_tracker == "w":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.y -= 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 0
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.y += 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 0
                elif self.ruch_tracker == "s":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.y += 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 1
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.y -= 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 1
                elif self.ruch_tracker == "a":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.x -= 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 2
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.x += 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 2
                elif self.ruch_tracker == "d":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.x += 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 3
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.x -= 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 3
                elif self.ruch_tracker == 0:
                    pass

                self.x3 = self.x
                self.y3 = self.y

        if self.ilosc_ruchow > 0:
            self.ilosc_ruchow -= 1

            if self.ruch_tracker == "w":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.y3 += 1
                self.y3 -= 1 / self.predkosc_chodzenia
                self.y3 = round(self.y3, 5)
            elif self.ruch_tracker == "s":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.y3 -= 1
                self.y3 += 1 / self.predkosc_chodzenia
                self.y3 = round(self.y3, 5)
            elif self.ruch_tracker == "a":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.x3 += 1
                self.x3 -= 1 / self.predkosc_chodzenia
                self.x3 = round(self.x3, 5)
            elif self.ruch_tracker == "d":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.x3 -= 1
                self.x3 += 1 / self.predkosc_chodzenia
                self.x3 = round(self.x3, 5)

    # Przemieszczanie się zwierząt
    def ruch_zwierzeta(self, mapa_jwrpg):

        if self.status == True and abs(self.x - gracz.x) < 8 and abs(self.y - gracz.y) < 7:

            if self.ilosc_ruchow == 0:
                # Funkcja wyliczająca ruch zwierząt
                self.tracker_zwierzeta(mapa_jwrpg)

                if self.ruch_tracker == "w":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.y -= 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 0
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.y += 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 0
                elif self.ruch_tracker == "s":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.y += 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 1
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.y -= 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 1
                elif self.ruch_tracker == "a":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.x -= 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 2
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.x += 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 2
                elif self.ruch_tracker == "d":
                    mapa_jwrpg[self.y][self.x] = 0
                    self.x += 1
                    if mapa_jwrpg[self.y][self.x] == 0:
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 3
                        self.ilosc_ruchow = self.predkosc_chodzenia
                    elif mapa_jwrpg[self.y][self.x] == 1:
                        self.x -= 1
                        mapa_jwrpg[self.y][self.x] = 1
                        self.m = 3
                elif self.ruch_tracker == 0:
                    pass

                self.x3 = self.x
                self.y3 = self.y

        if self.ilosc_ruchow > 0:
            self.ilosc_ruchow -= 1

            if self.ruch_tracker == "w":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.y3 += 1
                self.y3 -= 1 / self.predkosc_chodzenia
                self.y3 = round(self.y3, 5)
            elif self.ruch_tracker == "s":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.y3 -= 1
                self.y3 += 1 / self.predkosc_chodzenia
                self.y3 = round(self.y3, 5)
            elif self.ruch_tracker == "a":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.x3 += 1
                self.x3 -= 1 / self.predkosc_chodzenia
                self.x3 = round(self.x3, 5)
            elif self.ruch_tracker == "d":
                if self.ilosc_ruchow == self.predkosc_chodzenia - 1:
                    self.x3 -= 1
                self.x3 += 1 / self.predkosc_chodzenia
                self.x3 = round(self.x3, 5)

    # Losowanie ruchu dla zwierzat
    def tracker_zwierzeta(self, mapa_jwrpg):

        if self.status == True:
            # Random choice #
            moves = []
            check_pos = ((-1, 0, "w"), (1, 0, "s"), (0, -1, "a"), (0, 1, "d"))
            for y, x, move in check_pos:
                if mapa_jwrpg[self.y + y][self.x + x] == 0:
                    moves.append(move)
            self.ruch_tracker = random.choice(moves) if moves else 0

    # Funkcja Tracker  $$$ Beta 1.00 - A* pathfinder $$$
    def tracker(self, mapa_jwrpg):

        if abs(self.x - gracz.x) <= 1 and abs(self.y - gracz.y) <= 1:
            self.ruch_tracker = 0

        else:
            ### Generating local map for a-star ###
            local_map, player_pos, enemy_pos = generate_map_for_a_star(self.y, self.x, gracz.y2, gracz.x2,
                                                                       7, 8, mapa_jwrpg)
            ### Running A-STAR PATHFINDER ###
            path = a_star_pathfinder(local_map, enemy_pos, player_pos)

            ### If path found ###
            if path:
                if len(path) > 1:
                    ### Checking first move and calculating direction ###
                    moves_d = {(-1, 0): "w", (1, 0): "s", (0, -1): "a", (0, 1): "d"}
                    difference_y = path[1][0] - path[0][0]
                    difference_x = path[1][1] - path[0][1]
                    self.ruch_tracker = moves_d[(difference_y), difference_x]
                else:
                    self.ruch_tracker = 0

            ### If no path found - random choice ###
            else:
                moves = []
                check_pos = ((-1, 0, "w"), (1, 0, "s"), (0, -1, "a"), (0, 1, "d"))
                for y, x, move in check_pos:
                    if mapa_jwrpg[self.y + y][self.x + x] == 0:
                        moves.append(move)
                self.ruch_tracker = random.choice(moves) if moves else 0

    # Funcka atak przeciwnika - atakuje gdy wykryje dookoła siebie gracza
    def atak(self):
        self.aktualny_czas5 = pygame.time.get_ticks()
        if self.aktualny_czas5 - self.czas_ostatniego_ataku >= 1000 / self.predkosc_ataku and abs(
                self.x - gracz.x) <= 1 and abs(self.y - gracz.y) <= 1:
            self.czas_ostatniego_ataku = self.aktualny_czas5
            if gracz.hp > 0:
                ### Losowanie i odejmowanie dmg ###
                gracz.otrzymane_obrazenia = random.randint(self.dmg[0], self.dmg[1])
                gracz.hp -= gracz.otrzymane_obrazenia
                #####################
                gracz.animacja_otrzymane_obrazenia = True
                gracz.g = 42
                if gracz.hp <= 0:
                    gracz.zycie = False
                    gracz.interakcja = True

    # Funkcja atak dystansowy przeciwnika
    def atak_dystansowy(self, mapa_jwrpg):

        self.aktualny_czas6 = pygame.time.get_ticks()
        if self.aktualny_czas6 - self.czas_ostatniego_ataku2 >= 1000 / self.predkosc_ataku and (
                (7 > abs(self.x - gracz.x) > 1 and abs(self.y - gracz.y) < 6) or (
                6 > abs(self.y - gracz.y) > 1 and abs(self.x - gracz.x) < 7)):
            self.czas_ostatniego_ataku2 = self.aktualny_czas6

            ######### III możliwości ustawienia - atak dystansowy łuk #######

            # I. Przeciwnik stoi w linii prostej do gracza, poziomo lub pionowo
            if self.x == gracz.x2 or self.y == gracz.y2:

                # SPRAWDZENIE TRASY POZIOMEJ
                if self.y == gracz.y2:

                    # Gdy przeciwnik jest na Prawo od gracza - warunek odstęp conajmniej 1 pole
                    if self.x < gracz.x2 - 1:
                        # Ilość pól do sprawdzenia
                        droga: int = int(gracz.x2 - self.x)
                        # Sprawdzanie kolizji na trasie
                        for x in range(0, droga - 1):
                            if mapa_jwrpg[self.y][self.x + x + 1] == 0:
                                self.czysty_strzal = True
                                self.sposob_strzalu = "1 sposób poziomo P - STRZAŁ"
                            elif mapa_jwrpg[self.y][self.x + x + 1] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break

                    # Gdy przeciwnik jest na Lewo od gracza - warunek odstęp conajmniej 1 pole
                    elif self.x > gracz.x2 + 1:
                        # Ilość pól do sprawdzenia
                        droga: int = int(self.x - gracz.x2)
                        # Sprawdzanie kolizji na trasie
                        for x in range(0, droga - 1):
                            if mapa_jwrpg[self.y][self.x - x - 1] == 0:
                                self.czysty_strzal = True
                                self.sposob_strzalu = "1 sposób poziomo L - STRZAŁ"
                            elif mapa_jwrpg[self.y][self.x - x - 1] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break

                # SPRAWDZENIE TRASY PIONOWEJ
                elif self.x == gracz.x2:

                    # Gdy przeciwnik jest na Dół od gracza - warunek odstęp conajmniej 1 pole
                    if self.y < gracz.y2 - 1:
                        # Ilość pól do sprawdzenia
                        droga: int = int(gracz.y2 - self.y)
                        # Sprawdzanie kolizji na trasie
                        for x in range(0, droga - 1):
                            if mapa_jwrpg[self.y + x + 1][self.x] == 0:
                                self.czysty_strzal = True
                                self.sposob_strzalu = "1 sposób pionowo D - STRZAŁ"
                            elif mapa_jwrpg[self.y + x + 1][self.x] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break

                    # Gdy przeciwnik jest na Góra od gracza - warunek odstęp conajmniej 1 pole
                    elif self.y > gracz.y2 + 1:
                        # Ilość pól do sprawdzenia
                        droga: int = int(self.y - gracz.y2)
                        # Sprawdzanie kolizji na trasie
                        for x in range(0, droga - 1):
                            if mapa_jwrpg[self.y - x - 1][self.x] == 0:
                                self.czysty_strzal = True
                                self.sposob_strzalu = "1 sposób pionowo G - STRZAŁ"
                            elif mapa_jwrpg[self.y - x - 1][self.x] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break

            # II. Gracz stoi równo na ukos od przeciwnika, abs_x == abs_y
            elif abs(self.x - gracz.x2) == abs(self.y - gracz.y2):

                # DÓŁ-PRAWO
                if self.x < gracz.x2 - 1 and self.y < gracz.y2 - 1:
                    droga: int = int(gracz.x2 - self.x)
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y + x + 1][self.x + x + 1] == 0:
                            self.czysty_strzal = True
                            self.sposob_strzalu = "2 sposób DÓŁ-PRAWO - STRZAŁ"
                        elif mapa_jwrpg[self.y + x + 1][self.x + x + 1] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break

                # DÓŁ-LEWO
                elif self.x > gracz.x2 + 1 and self.y < gracz.y2 - 1:
                    droga: int = int(self.x - gracz.x2)
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y + x + 1][self.x - x - 1] == 0:
                            self.czysty_strzal = True
                            self.sposob_strzalu = "2 sposób DÓŁ-LEWO - STRZAŁ"
                        elif mapa_jwrpg[self.y + x + 1][self.x - x - 1] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break

                # GÓRA-PRAWO
                elif self.x < gracz.x2 - 1 and self.y > gracz.y2 + 1:
                    droga: int = int(gracz.x2 - self.x)
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y - x - 1][self.x + x + 1] == 0:
                            self.czysty_strzal = True
                            self.sposob_strzalu = "2 sposób GÓRA-PRAWO - STRZAŁ"
                        elif mapa_jwrpg[self.y - x - 1][self.x + x + 1] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break

                # GÓRA-LEWO
                elif self.x > gracz.x2 + 1 and self.y > gracz.y2 + 1:
                    droga: int = int(self.x - gracz.x2)
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y - x - 1][self.x - x - 1] == 0:
                            self.czysty_strzal = True
                            self.sposob_strzalu = "2 sposób GÓRA-LEWO - STRZAŁ"
                        elif mapa_jwrpg[self.y - x - 1][self.x - x - 1] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break

            # III. Gracz stoki nierówno na ukos od przeciwnika (tworzenie funkcji liniowej trasy)
            elif abs(self.x - gracz.x2) != abs(self.y - gracz.y2):

                # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                m = (gracz.y2 - self.y) / (gracz.x2 - self.x)
                b = self.y - m * self.x

                # Sprawdzenie kolizji na trasie przebiegu funkcji liniowej

                # Gdy abs x = 1 a abs y > 1
                if abs(self.x - gracz.x2) == 1 and abs(self.y - gracz.y2) > 1:

                    # DÓŁ
                    if self.y < gracz.y2:
                        y = self.y + 1
                        while y <= gracz.y2 - 1:
                            x = (y - b) / m
                            if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                    mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break
                            y += 0.1
                        else:
                            self.czysty_strzal = True
                            if self.x > gracz.x2:
                                self.sposob_strzalu = "3 sposób 1 DÓŁ-LEWO - STRZAŁ"
                            elif self.x < gracz.x2:
                                self.sposob_strzalu = "3 sposób 1 DÓŁ-PRAWO - STRZAŁ"

                    # GÓRA
                    elif self.y > gracz.y2:
                        y = self.y - 1
                        while y >= gracz.y2 + 1:
                            x = (y - b) / m
                            if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                    mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                                self.czysty_strzal = False
                                self.sposob_strzalu = "Nie można oddać strzału"
                                break
                            y -= 0.1
                        else:
                            self.czysty_strzal = True
                            if self.x > gracz.x2:
                                self.sposob_strzalu = "3 sposób 1 GÓRA-LEWO - STRZAŁ"
                            elif self.x < gracz.x2:
                                self.sposob_strzalu = "3 sposób 1 GÓRA-PRAWO - STRZAŁ"

                # PRAWO
                elif self.x <= gracz.x2 - 1:
                    x = self.x + 1
                    while x <= gracz.x2 - 1:
                        y = m * x + b
                        if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break
                        x = x + 0.1
                    else:
                        self.czysty_strzal = True
                        if self.y > gracz.y2:
                            self.sposob_strzalu = "3 sposób 2 GÓRA-PRAWO - STRZAŁ"
                        elif self.y < gracz.y2:
                            self.sposob_strzalu = "3 sposób 2 DÓŁ-PRAWO - STRZAŁ"

                # LEWO
                elif self.x >= gracz.x2 + 1:
                    x = self.x - 1
                    while x >= gracz.x2 + 1:
                        y = m * x + b
                        if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                            self.czysty_strzal = False
                            self.sposob_strzalu = "Nie można oddać strzału"
                            break
                        x = x - 0.1
                    else:
                        self.czysty_strzal = True
                        if self.y > gracz.y2:
                            self.sposob_strzalu = "3 sposób 2 GÓRA-LEWO - STRZAŁ"
                        elif self.y < gracz.y2:
                            self.sposob_strzalu = "3 sposób 2 DÓŁ-LEWO - STRZAŁ"

            if self.czysty_strzal == True:

                # Włączenie parametru odpowiedzialnego za rysowanie strzału
                self.animacja_strzal = True
                #################################################################################

                # 1 SPOSÓB - POZIOMO - PRAWO
                if self.sposob_strzalu == "1 sposób poziomo P - STRZAŁ":
                    odleglosc = abs(self.x3 - gracz.x2)
                    self.funkcja_x2 = [self.x3 + 0.5 * x for x in range(1, round(odleglosc / 0.5))]
                    self.funkcja_y2 = self.y3
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.y3 * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 1 SPOSÓB - POZIOMO - LEWO
                elif self.sposob_strzalu == "1 sposób poziomo L - STRZAŁ":
                    odleglosc = abs(self.x3 - gracz.x2)
                    self.funkcja_x2 = [self.x3 - 0.5 * x for x in range(1, round(odleglosc / 0.5))]
                    self.funkcja_y2 = self.y3
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.y3 * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 1 SPOSÓB - PIONOWO - DÓŁ
                elif self.sposob_strzalu == "1 sposób pionowo D - STRZAŁ":
                    odleglosc = abs(self.y3 - gracz.y2)
                    self.funkcja_y2 = [self.y3 + 0.5 * y for y in range(1, round(odleglosc / 0.5))]
                    self.funkcja_x2 = self.x3
                    self.funkcja_lambda2 = lambda y_lambda, mapa_x, mapa_y: (
                        self.x3 * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[y_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 1 SPOSÓB - PIONOWO - GÓRA
                elif self.sposob_strzalu == "1 sposób pionowo G - STRZAŁ":
                    odleglosc = abs(self.y3 - gracz.y2)
                    self.funkcja_y2 = [self.y3 - 0.5 * y for y in range(1, round(odleglosc / 0.5))]
                    self.funkcja_x2 = self.x3
                    self.funkcja_lambda2 = lambda y_lambda, mapa_x, mapa_y: (
                        self.x3 * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[y_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)

                # 2 SPOSÓB - DÓŁ PRAWO
                elif self.sposob_strzalu == "2 sposób DÓŁ-PRAWO - STRZAŁ":
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    self.funkcja_x2 = [self.x3 + 0.354 * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 + 0.354 * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 2 SPOSÓB - DÓŁ LEWO
                elif self.sposob_strzalu == "2 sposób DÓŁ-LEWO - STRZAŁ":
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    self.funkcja_x2 = [self.x3 - 0.354 * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 + 0.354 * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 2 SPOSÓB - GÓRA PRAWO
                elif self.sposob_strzalu == "2 sposób GÓRA-PRAWO - STRZAŁ":
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    self.funkcja_x2 = [self.x3 + 0.354 * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 - 0.354 * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 2 SPOSÓB - GÓRA LEWO
                elif self.sposob_strzalu == "2 sposób GÓRA-LEWO - STRZAŁ":
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    self.funkcja_x2 = [self.x3 - 0.354 * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 - 0.354 * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)

                ############################################################################################
                # 3 SPOSÓB 1 DÓŁ LEWO
                elif self.sposob_strzalu == "3 sposób 1 DÓŁ-LEWO - STRZAŁ" or self.sposob_strzalu == "3 sposób 2 DÓŁ-LEWO - STRZAŁ":
                    # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                    m = (gracz.y2 - self.y3) / (gracz.x2 - self.x3)
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    # Wyznaczenie kroku po x
                    x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                    # Wyznaczenie kroku po y
                    y_przemieszczenie = abs(m * x_przemieszczenie)
                    self.funkcja_x2 = [self.x3 - x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 + y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 3 SPOSÓB 1 DÓŁ PRAWO
                elif self.sposob_strzalu == "3 sposób 1 DÓŁ-PRAWO - STRZAŁ" or self.sposob_strzalu == "3 sposób 2 DÓŁ-PRAWO - STRZAŁ":
                    # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                    m = (gracz.y2 - self.y3) / (gracz.x2 - self.x3)
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    # Wyznaczenie kroku po x
                    x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                    # Wyznaczenie kroku po y
                    y_przemieszczenie = abs(m * x_przemieszczenie)
                    self.funkcja_x2 = [self.x3 + x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 + y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 3 SPOSÓB 1 GÓRA-LEWO
                elif self.sposob_strzalu == "3 sposób 1 GÓRA-LEWO - STRZAŁ" or self.sposob_strzalu == "3 sposób 2 GÓRA-LEWO - STRZAŁ":
                    # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                    m = (gracz.y2 - self.y3) / (gracz.x2 - self.x3)
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    # Wyznaczenie kroku po x
                    x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                    # Wyznaczenie kroku po y
                    y_przemieszczenie = abs(m * x_przemieszczenie)
                    self.funkcja_x2 = [self.x3 - x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 - y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                # 3 SPOSÓB 1 GÓRA-PRAWO
                elif self.sposob_strzalu == "3 sposób 1 GÓRA-PRAWO - STRZAŁ" or self.sposob_strzalu == "3 sposób 2 GÓRA-PRAWO - STRZAŁ":
                    # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                    m = (gracz.y2 - self.y3) / (gracz.x2 - self.x3)
                    przekatna = ((abs(self.x3 - gracz.x2)) ** 2 + (abs(self.y3 - gracz.y2)) ** 2) ** 0.5
                    # Wyznaczenie kroku po x
                    x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                    # Wyznaczenie kroku po y
                    y_przemieszczenie = abs(m * x_przemieszczenie)
                    self.funkcja_x2 = [self.x3 + x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                    self.funkcja_y2 = [self.y3 - y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                    self.funkcja_lambda2 = lambda x_lambda, mapa_x, mapa_y: (
                        self.funkcja_x2[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                        self.funkcja_y2[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
                ############################################################################################

                if gracz.hp > 0:
                    if (self.x == 0 and self.y == 0) or (self.y2 == 0 and self.x2 == 0) or (
                            self.y3 == 0 and self.x3 == 0):
                        with open("arrow_error_log.txt", "a") as plik:
                            plik.write(
                                f"X = {self.x}, Y: {self.y}, X3: {self.x3}, Y3: {self.y3}, GRACZ X: {gracz.x}, GRACZ Y: {gracz.y}, GRACZ X2: {gracz.x2}, GRACZ Y2: {gracz.y2}, SPOSÓB STRZAŁU: {self.sposob_strzalu}")
                    ### Losowanie i odejmowanie dmg ###
                    gracz.otrzymane_obrazenia = random.randint(self.dist_dmg[0], self.dist_dmg[1])
                    gracz.hp -= gracz.otrzymane_obrazenia
                    #####################
                    gracz.animacja_otrzymane_obrazenia = True
                    self.czysty_strzal = False
                    self.sposob_strzalu = ""
                    gracz.g = 42
                    if gracz.hp <= 0:
                        gracz.zycie = False
                        gracz.interakcja = True

    ### FUNKCJA LOOT ######################################
    def losowanie_i_dodawanie_loota(self):
        game_map = instances.game_map

        loot_table = [["zloto", self.gold[0], self.gold[1]]]
        loot_dict = {}
        for index, item in enumerate(loot_table):
            if index == 0:
                loot_dict[item[0]] = random.randint(item[1], item[2])
            else:
                losowanie = random.randint(1, item[1])
                if losowanie == item[1]:
                    loot_dict[item[0]] = 1
        x = self.x
        y = self.y
        if game_map.level == "main":
            Przeciwnik.loot_powierzchnia.append([x, y, loot_dict])
        else:
            Przeciwnik.loot_podziemia.append([x, y, loot_dict])

        ### Losowanie przedmiotów do fabuły NEW ####################
        if instances.quest_manager.progress in [6, 12, 18]:
            if ((self.imie == "Pająk" and instances.quest_manager.progress == 6) or
                (self.imie == "Biały Pająk" and instances.quest_manager.progress == 12)):
                losowanie = random.randint(1, 3)
                if losowanie == 3:
                    if game_map.level == "main":
                        Przeciwnik.loot_przedmioty_fabula_powierzchnia.append([x, y])
                    else:
                        Przeciwnik.loot_przedmioty_fabula_podziemia.append([x, y])
            ### Pradawny smok pokonany - przypisanie współrzędnych ###
            if self.imie == "Pradawny Smok":
                self.dead_x = self.x
                self.dead_y = self.y
        ############################################################

    ### FUNKCJA KLASY - RYSOWANIE LOOTA NA MAPIE ##########
    def rysowanie_loota(cls, mapa_x, mapa_y, loot, okno):
        for loots in loot:
            if abs(loots[0] - gracz.x) <= 7 and abs(loots[1] - gracz.y) <= 6:
                okno.blit(loot_grafika, (loots[0] * rozmiar_pola + mapa_x, loots[1] * rozmiar_pola + mapa_y))

    # Funkcja zwracajaca slownik z parametrami przeciwnikow do zapisu - CLASS METHOD
    def slownik_przeciwnicy_save(cls):
        # Przeciwnicy powierzchnia #
        przeciwnicy_m = [(p.x, p.y, p.hp, p.status, p.spawn_x, p.spawn_y) for p in Przeciwnik.przeciwnicy_powierzchnia]
        # Przeciwnicy podziemia #
        przeciwnicy_p = [(p.x, p.y, p.hp, p.status, p.spawn_x, p.spawn_y) for p in Przeciwnik.przeciwnicy_podziemia]
        # Zwrócenie slownika
        przeciwnicy_save = {"powierzchnia": przeciwnicy_m, "podziemia": przeciwnicy_p}
        return przeciwnicy_save

    # Funkcja ładująca parametry przeciwnikow z SAVE - CLASS METHOD
    def load_save(cls, enemies_save, loot_save, loot_quest_save):
        # Powierzchnia #
        for p in Przeciwnik.przeciwnicy_powierzchnia:
            for x, y, hp, status, spawn_x, spawn_y in enemies_save["powierzchnia"]:
                if p.spawn_x == spawn_x and p.spawn_y == spawn_y:
                    instances.game_map.main_map_jwrpg[p.y][p.x] = 0
                    p.x = x
                    p.y = y
                    p.x3 = x
                    p.y3 = y
                    p.ilosc_ruchow = 0
                    p.hp = hp
                    p.status = status
                    p.zaznaczenie = False
                    break
        # Podziemia #
        for p in Przeciwnik.przeciwnicy_podziemia:
            for x, y, hp, status, spawn_x, spawn_y in enemies_save["podziemia"]:
                if p.spawn_x == spawn_x and p.spawn_y == spawn_y:
                    instances.game_map.underground_map_jwrpg[p.y][p.x] = 0
                    p.x = x
                    p.y = y
                    p.x3 = x
                    p.y3 = y
                    p.ilosc_ruchow = 0
                    p.hp = hp
                    p.status = status
                    p.zaznaczenie = False
                    break
        # Loot #
        Przeciwnik.loot_powierzchnia = [l for l in loot_save[0]]
        Przeciwnik.loot_podziemia = [l for l in loot_save[1]]
        Przeciwnik.loot_przedmioty_fabula_powierzchnia = [l for l in loot_quest_save[0]]
        Przeciwnik.loot_przedmioty_fabula_podziemia = [l for l in loot_quest_save[1]]

    # New game - resets enemies #
    @classmethod
    def new_game(cls):
        cls.loot_powierzchnia.clear()
        cls.loot_podziemia.clear()
        for p in cls.przeciwnicy_powierzchnia:
            instances.game_map.main_map_jwrpg[p.y][p.x] = 0
            p.x = p.spawn_x
            p.y = p.spawn_y
            p.x3 = p.spawn_x
            p.y3 = p.spawn_y
            p.status = True
            p.m = 0
            p.hp = p.max_hp
            p.x_tracker = p.spawn_x
            p.y_tracker = p.spawn_y
            p.kolizja = False
            p.ilosc_ruchow = 0
            p.ruch_tracker = 0
            p.zaznaczenie = False
        for p in cls.przeciwnicy_podziemia:
            instances.game_map.underground_map_jwrpg[p.y][p.x] = 0
            p.x = p.spawn_x
            p.y = p.spawn_y
            p.x3 = p.spawn_x
            p.y3 = p.spawn_y
            p.status = True
            p.m = 0
            p.hp = p.max_hp
            p.x_tracker = p.spawn_x
            p.y_tracker = p.spawn_y
            p.kolizja = False
            p.ilosc_ruchow = 0
            p.ruch_tracker = 0
            p.zaznaczenie = False

    # Enemy spawn #
    def spawn(self):
        # Checking if dead
        if not self.status:
            if self.dead_start_counting_time:
                self.dead_time_counter = pygame.time.get_ticks()
                self.dead_start_counting_time = False
            # Calculating time
            self.aktualny_czas_spawn = pygame.time.get_ticks()
            if self.aktualny_czas_spawn - self.dead_time_counter >= self.predkosc_spawnu:
                # Checking if enemy outside of player draw range
                if (abs(self.spawn_x - gracz.x) > 8 or abs(self.spawn_y - gracz.y) > 7):
                    self.dead_start_counting_time = True
                    # Spawning
                    self.hp = self.max_hp
                    self.status = True
                    self.x = self.spawn_x
                    self.y = self.spawn_y
                    self.x3 = self.spawn_x
                    self.y3 = self.spawn_y