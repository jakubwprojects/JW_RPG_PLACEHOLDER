import os.path
import pygame
import math
import random
import jwrpg_Blackjack
from config.MAIN_CONFIG import (DISPLAY_HEIGHT as wysokosc_okna, REFRESHING_1 as odswiezanie1,
                                REFRESHING_3 as odswiezanie3)
from config.player_config import sword_stats, bow_stats, armor_stats, cape_stats, boots_stats, progression_table, start_pos
from assets import *
import instances


### Tworzenie klasy - Gracz ###
class Gracz:

    # Inicjalizator
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imie = "Rinngen"
        self.doswiadczenie = 0
        self.poziom = 1
        self.hp = 100
        self.mp = 100
        self.max_hp = self.hp
        self.max_mp = self.mp
        self.predkosc_ataku = 1  # 1 uderzenie na sekundę

        self.zadane_obrazenia = None  # Obrażenia zadawane obszarowym atakiem
        self.zadane_obrazenia_2 = None  # Obrażenia zadawane zaznaczonym atakiem

        self.czas_ostatniego_ruchu = 0  # zmienna do warunku if kontrolującego prędkość gracza
        self.czas_ostatniego_ataku = 0  # zmienna do warunku if - cooldown ataku
        self.animacja_atak_q = False
        self.animacja_atak_x = False
        self.animacja_pola = ()
        self.animacja_pola_strzal = ()
        self.celownik = False
        self.celownik_prev = False
        self.a = 1  # Parametr do określenia czasu wyświetlania ataku
        self.m = 1  # Parametr określający kierunek w który skierowany jest gracz, zależy od ruchu
        # 0 - Góra, 1 - Dół, 2 - Lewo, 3 - Prawo
        self.ilosc_ruchow = 0  # Parametr do płynnego przechodzenia gracza do innego pola
        self.kierunek_ruchu = "w"  # Kierunki ruchu w/s/a/d
        self.cooldown_potion = 0.5  # 1 potion na 2 sekundy
        self.hp_potion = 100  # Leczenie
        self.mp_potion = 100  # Mana
        self.zloto = 0  # Złoto - waluta
        self.x2 = self.x
        self.y2 = self.y
        self.g = 42.0  # Wartość do animacji otrzymwania obrażeń przez przeciwników
        self.animacja_otrzymane_obrazenia = False
        self.czas_ostatniego_leczenia = 0
        self.fabula = 1

        # Parametry czasowe do zbierania lootu
        self.aktualny_czas_loot = 0
        self.czas_ostatniego_loota = 0

        # Parametry do funkcji zaznaczanie przeciwników przez gracza
        self.zaznaczenie = False  # PARAMETR DO ZAZNACZANIA PRZECIWNIKÓW - True/False
        self.czas_ostatniego_zaznaczenia = 0
        self.predkosc_zaznaczenia = 3  # 3 razy na sekundę
        self.czas_ostatniego_ataku_zaznaczenie = 0
        self.poprzedni_ruch = "0"

        self.otrzymane_obrazenia = 5
        self.czas_ostatniej_interakcji = 0  # Zmienna do funkcji interakcji z NPC
        self.predkosc_interakcji = 2  # 2 razy na sekundę
        self.interakcja = False

        # Parametr do napisu ile podniesiono złota
        self.gold = False
        self.gold_g = 42.0
        self.gold_ile = 0

        # Parametr do napisu nowy poziom
        self.lvl_up = False
        self.lvl_up_g = 42.0

        # Parametry do napisu + ile expa po pokonaniu przeciwnika
        self.new_exp = False
        self.new_exp_g = 42.0
        self.exp = 0

        # Parametr do postępu w fabule grze
        self.f = 0
        self.licznik = 0

        # Parametry animacji wody - roboczo w tym miejscu
        self.parametr_woda = 0
        self.parametr_woda2 = 0

        # Parametry do napisow hp/mp
        self.potion_use = False
        self.potion_type = None
        self.potion_value = None
        self.potion_g = 42.0

        # NOWY PARAMETR - Wybrana broń
        self.bron = "miecz"
        self.czysty_strzal = False  # Parametr do strzelania z łuku
        self.sposob_strzalu = ""  # Informuje o sposobie użytego strzału
        self.ilosc_strzal = 100  # Ilość strzał
        self.animacja_strzal = False  # Parametr do animacji strzału
        self.kat_obrotu_strzaly = 0  # Parametr do obrotu animacji strzali
        self.ss = 0
        self.sss = 0
        self.ssss = 0
        self.funkcja_y = []
        self.funkcja_x = []
        self.funkcja_lambda = None
        self.czysty_strzal_specjalny = False
        self.czysty_strzal_aoe = False
        self.animacja_strzal_specjalny = False
        self.animacja_strzal_aoe = False
        self.animacja_strzal_aoe_2 = False
        self.kat_obrotu_strzaly_specjalny = 0
        self.kat_obrotu_strzaly_aoe = 0
        self.funkcja_y2 = []
        self.funkcja_x2 = []
        self.funkcja_lambda2 = None
        self.funkcja_y3 = []
        self.funkcja_x3 = []
        self.funkcja_lambda3 = None

        # PAREMETRY DO SPAWNU PRZECIWNIKÓW
        self.aktualny_czas_spawn = 0
        self.czas_ostatniego_spawnu = 0
        self.predkosc_spawnu = 0.1

        self.zycie = True  # Parametr do napisu nie żyjesz - śmierć gracza

        self.tekst_wspolrzedne = pygame.font.Font(None, 45)
        self.tekst_fps = pygame.font.Font(None, 50)
        self.tekst_1 = pygame.font.Font(None, 38)
        self.tekst_2 = pygame.font.Font(None, 32)
        self.tekst_3 = pygame.font.Font(None, 36)
        self.tekst_nie_zyjesz = pygame.font.Font(None, 60)
        self.ui_1 = pygame.font.Font(None, 30)
        self.ui_2 = pygame.font.Font(None, 26)
        self.ui_3 = pygame.font.Font(None, 34)
        self.ui_4 = pygame.font.Font(None, 18)

        ###
        self.zaladowano_gre = False
        self.level_mapy = "powierzchnia"
        ###
        self.procent_nastepny_poziom = 0.0
        ### Ładowanie słownika z doświadczeniem, hp, mp na każdy lvl 1-50 ################
        self.doswiadczenie_slownik = progression_table
        ##################################################################################

        ### Ładowanie zmiennych do gry Blackjack ###
        (self.cards, self.obstawienie_gracza, self.gracz_reka, self.krupier_reka,
         self.gracz_wynik, self.krupier_wynik) = jwrpg_Blackjack.ladowanie()
        self.cards_tyl = pygame.image.load(os.path.join("tilesets", "karta_tyl", "card_back.png"))
        self.czas_karty = 0
        ############################################

        ### statystyki ekwipunek
        self.miecz_poziom = 1
        self.luk_poziom = 1
        self.zbroja_poziom = 1
        self.plaszcz_poziom = 1
        self.buty_poziom = 1

        ### punkty ulepszeń, 1/lvl
        self.punkty_ulepszen = 0

        ### statystyki ekwipunku
        self.miecz_staty = sword_stats
        self.luk_staty = bow_stats
        self.zbroja_staty = armor_stats
        self.plaszcz_staty = cape_stats
        self.buty_staty = boots_stats
        ########################

        ### speed - based on fps ###
        self.predkosc_chodzenia = self.buty_staty[self.buty_poziom]["speed"]  # 1 pole / x klatek
        self.predkosc_chodzenia = 4  # DEV

        self.dev = False
        self.map_lvl = "powierzchnia"

        self.attack_sword = self.miecz_staty[self.miecz_poziom]["dmg"]
        self.crit_sword = self.miecz_staty[self.miecz_poziom]["crit"]
        self.attack_bow = self.luk_staty[self.luk_poziom]["dmg"]
        self.crit_bow = self.luk_staty[self.luk_poziom]["crit"]
        self.max_hp += self.zbroja_staty[self.zbroja_poziom]["hp"]
        self.max_mp += self.plaszcz_staty[self.plaszcz_poziom]["mp"]
        self.predkosc_chodzenia = self.buty_staty[self.buty_poziom]["speed"]

        # Wczytywanie opisów zadań
        self.load_quest_descriptions()
        ############################

    # Load player - CLASS METHOD #
    def load_player(cls, start_pos):
        gracz = Gracz(start_pos[0], start_pos[1])
        return gracz

    # NEW - DEV TOOL #
    def dev_tool(self):
        dev = pygame.key.get_pressed()
        self.aktualny_czas_n = pygame.time.get_ticks()
        if dev[pygame.K_t]:
            if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                self.czas_ostatniej_interakcji = self.aktualny_czas_n
                if not self.dev:
                    self.dev = True
                else:
                    self.dev = False

        if self.dev:
            pygame.draw.rect(okno, "dimgrey", (odswiezanie1 + 150, 150, odswiezanie2 - 300, 1080 - 300))
            pygame.draw.rect(okno, "grey13", (odswiezanie1 + 200, 200, odswiezanie2 - 400, 1080 - 400))
            okno.blit(kowal.tekst_sklep.render("DEV TOOL", True, "floral white"),
                      (850, 540 - 350 + 30))

    # Funkcja ruch gracza - zmienia pola self.x, self.y
    def ruch(self, mapa_jwrpg):

        kierunek = pygame.key.get_pressed()

        if self.ilosc_ruchow == 0:

            if not kierunek[pygame.K_LSHIFT]:

                if kierunek[pygame.K_w]:
                    self.m = 0
                    if mapa_jwrpg[self.y2 - 1][self.x2] == 0:
                        self.ilosc_ruchow = self.predkosc_chodzenia
                        mapa_jwrpg[self.y2][self.x2] = 0
                        mapa_jwrpg[self.y2 - 1][self.x2] = 1
                        self.kierunek_ruchu = "w"

                elif kierunek[pygame.K_s]:
                    self.m = 1
                    if mapa_jwrpg[self.y2 + 1][self.x2] == 0:
                        self.ilosc_ruchow = self.predkosc_chodzenia
                        mapa_jwrpg[self.y2][self.x2] = 0
                        mapa_jwrpg[self.y2 + 1][self.x2] = 1
                        self.kierunek_ruchu = "s"

                elif kierunek[pygame.K_a]:
                    self.m = 2
                    if mapa_jwrpg[self.y2][self.x2 - 1] == 0:
                        self.ilosc_ruchow = self.predkosc_chodzenia
                        mapa_jwrpg[self.y2][self.x2] = 0
                        mapa_jwrpg[self.y2][self.x2 - 1] = 1
                        self.kierunek_ruchu = "a"

                elif kierunek[pygame.K_d]:
                    self.m = 3
                    if mapa_jwrpg[self.y2][self.x2 + 1] == 0:
                        self.ilosc_ruchow = self.predkosc_chodzenia
                        mapa_jwrpg[self.y2][self.x2] = 0
                        mapa_jwrpg[self.y2][self.x2 + 1] = 1
                        self.kierunek_ruchu = "d"

            # Obrót w miejscu - SHIFT + W/S/A/D
            elif kierunek[pygame.K_LSHIFT]:
                if kierunek[pygame.K_w]:
                    self.m = 0
                elif kierunek[pygame.K_s]:
                    self.m = 1
                elif kierunek[pygame.K_a]:
                    self.m = 2
                elif kierunek[pygame.K_d]:
                    self.m = 3

        # Zmiana pozycji gracza
        if self.ilosc_ruchow > 0:

            self.ilosc_ruchow -= 1

            if self.kierunek_ruchu == "w":
                self.y -= 1 / self.predkosc_chodzenia
                self.y = round(self.y, 5)
                self.y2 = math.floor(self.y)
            elif self.kierunek_ruchu == "s":
                self.y += 1 / self.predkosc_chodzenia
                self.y = round(self.y, 5)
                self.y2 = math.ceil(self.y)
            elif self.kierunek_ruchu == "a":
                self.x -= 1 / self.predkosc_chodzenia
                self.x = round(self.x, 5)
                self.x2 = math.floor(self.x)
            elif self.kierunek_ruchu == "d":
                self.x += 1 / self.predkosc_chodzenia
                self.x = round(self.x, 5)
                self.x2 = math.ceil(self.x)

    # Funkcja rysująca grafikę gracza
    def rysowanie_grafiki_gracza(self, okno, zegar_fps):

        # Grafika gracza
        z = 0  # Parametr do określania poprzedniego ruchu gracza i zmiane animacji gdy ten sam kierunek
        if self.poprzedni_ruch == self.kierunek_ruchu:
            z = 1

        ruch_r = [x for x in range(self.predkosc_chodzenia, int((self.predkosc_chodzenia / 2)) - 1, -1)]
        ruch_s = [x for x in range(int((self.predkosc_chodzenia / 2)) - 1, -1, -1)]

        if self.ilosc_ruchow in ruch_r:
            if self.kierunek_ruchu == "w":
                lolo = lista_grafika_gracz_ruch_gora[1 - z]
            elif self.kierunek_ruchu == "s":
                lolo = lista_grafika_gracz_ruch_dol[1 - z]
            elif self.kierunek_ruchu == "a":
                lolo = lista_grafika_gracz_ruch_lewo[1 - z]
            elif self.kierunek_ruchu == "d":
                lolo = lista_grafika_gracz_ruch_prawo[1 - z]

        elif self.ilosc_ruchow in ruch_s:
            lolo = lista_grafika_gracz[self.m]

            if self.ilosc_ruchow == 0 and self.poprzedni_ruch == self.kierunek_ruchu:
                self.poprzedni_ruch = "0"

            elif self.ilosc_ruchow == 0:
                self.poprzedni_ruch = self.kierunek_ruchu

        okno.blit(lolo, (911, 491))

        # Rysowanie współrzędnych gracza
        wspolrzedne_gracza = self.tekst_wspolrzedne.render((f"x, y = {self.x}, {self.y}"), True, "floral white")
        okno.blit(wspolrzedne_gracza, (870, 1038))

        # Rysowanie wskaźnika fps
        okno.blit(self.tekst_fps.render(f"FPS: {round(zegar_fps.get_fps(), 0)}", True, "floral white"),
                  (332, 1038))

    # Funkcja rysująca imie, hp i ataki gracza
    def rysowanie_elementow_gracza(self, mapa_x, mapa_y, okno):

        # Nazwa gracza
        okno.blit(self.tekst_1.render(self.imie, True, "floral white"), (self.text_x, self.text_y))

        # Pasek HP
        pygame.draw.rect(okno, "black", (911, 481, 98, 10))
        pygame.draw.rect(okno, "green2", (911, 481, (self.hp * rozmiar_pola) / self.max_hp, 10))

        # Otrzymane obrażenia
        if self.animacja_otrzymane_obrazenia == True:
            if self.g < 106.0:
                okno.blit(self.tekst_2.render(f"{self.otrzymane_obrazenia}", True, "red"),
                          (self.x * rozmiar_pola + 43 + mapa_x, self.y * rozmiar_pola - self.g + mapa_y))
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
                okno.blit(lista_blood_hit[hit_index], (self.x * rozmiar_pola + mapa_x - 16 * rozmiar_pola / 32,
                                                       self.y * rozmiar_pola + mapa_y - 16 * rozmiar_pola / 32))
                self.g += 2.0
            elif self.g == 106.0:
                self.animacja_otrzymane_obrazenia = False
                self.g = 42.0

        # Atak obszarowy gracza - Q
        if self.animacja_atak_q == True:
            if self.a < 15:
                # Rysowanie ataku na polach dookoła gracza
                for x, y in self.animacja_pola:
                    okno.blit(atak_gracza_grafika_rozszerzona,
                              (x * rozmiar_pola + mapa_x, y * rozmiar_pola + mapa_y))
                self.a += 1
            elif self.a == 15:
                self.animacja_atak_q = False
                self.a = 1

        # Atak obszarowy gracza - X
        if self.animacja_atak_x == True:
            if self.a < 15:
                # Rysowanie ataku na polach przed graczem
                for x, y in self.animacja_pola:
                    okno.blit(atak_gracza_grafika_rozszerzona,
                              (x * rozmiar_pola + mapa_x, y * rozmiar_pola + mapa_y))
                self.a += 1
            elif self.a == 15:
                self.animacja_atak_x = False
                self.a = 1

        # Rysowanie ile podniesiono złota
        if self.gold == True:
            if self.gold_g < 100.0:
                okno.blit(self.tekst_3.render(f"+{self.gold_ile} złoto", True, "gold"),
                          (self.x * rozmiar_pola - 4 + mapa_x, self.y * rozmiar_pola - self.gold_g + mapa_y))
                self.gold_g += 2.0
            elif self.gold_g == 100.0:
                self.gold = False
                self.gold_g = 42.0
                self.gold_ile = 0

        # Rysowanie informacji o uzyciu potiona
        if self.potion_use == True:
            if self.potion_g < 100.0:
                if self.potion_type == "hp":
                    okno.blit(self.tekst_3.render(f"+{self.potion_value} hp", True, "lawngreen"),
                              (self.x * rozmiar_pola + 2 + mapa_x, self.y * rozmiar_pola - self.potion_g + mapa_y))
                else:
                    okno.blit(self.tekst_3.render(f"+{self.potion_value} mp", True, "deepskyblue"),
                              (self.x * rozmiar_pola + 2 + mapa_x, self.y * rozmiar_pola - self.potion_g + mapa_y))
                self.potion_g += 2.0
            elif self.potion_g == 100.0:
                self.potion_use = False
                self.potion_g = 42.0

        # Rysowanie napisu "NOWY POZIOM", po awansowaniu na kolejny lvl
        if self.lvl_up == True:
            if self.lvl_up_g < 100.0:
                okno.blit(self.tekst_3.render("NOWY POZIOM", True, "indigo"),
                          (self.x * rozmiar_pola - 42 + mapa_x, self.y * rozmiar_pola - self.lvl_up_g + mapa_y))
                self.lvl_up_g += 2.0
            elif self.lvl_up_g == 100.0:
                self.lvl_up = False
                self.lvl_up_g = 42.0

        # Rysowanie ilości zdobytego expa, po zabiciu przeciwnika
        elif self.new_exp == True:
            if self.new_exp_g < 100.0:
                okno.blit(self.tekst_3.render(f"+{self.exp} exp", True, "floral white"),
                          (self.x * rozmiar_pola - 3 + mapa_x, self.y * rozmiar_pola - self.new_exp_g + mapa_y))
                self.new_exp_g += 2.0
            elif self.new_exp_g == 100.0:
                self.new_exp = False
                self.new_exp_g = 42.0
                self.exp = 0

        # Rysowanie animacji lecenia strzały w przeciwnika
        if self.animacja_strzal == True:

            strzala_obrocona = pygame.transform.rotate(strzala_animacja, self.kat_obrotu_strzaly)
            # Uzyskanie prostokąta granicznego dla obróconego obrazka
            rotated_rect = strzala_obrocona.get_rect()
            # Ustawienie pozycji prostokąta granicznego na podstawie oryginalnej pozycji gracza i mapy
            rotated_rect.center = self.funkcja_lambda(self.ss, mapa_x, mapa_y)
            # Rysowanie obróconego obrazka z dostosowanym prostokątem granicznym
            okno.blit(strzala_obrocona, rotated_rect)
            self.ss += 1
            try:
                if self.ss == len(self.funkcja_x):
                    self.ss = 0
                    self.animacja_strzal = False
            except:
                if self.ss == len(self.funkcja_y):
                    self.ss = 0
                    self.animacja_strzal = False

        if self.animacja_strzal_specjalny == True:

            ognista_strzala_obrocona = pygame.transform.rotate(ognista_strzala, self.kat_obrotu_strzaly_specjalny)
            # Uzyskanie prostokąta granicznego dla obróconego obrazka
            rotated_rect2 = ognista_strzala_obrocona.get_rect()
            # Ustawienie pozycji prostokąta granicznego na podstawie oryginalnej pozycji gracza i mapy
            rotated_rect2.center = self.funkcja_lambda2(self.sss, mapa_x, mapa_y)
            # Rysowanie obróconego obrazka z dostosowanym prostokątem granicznym
            okno.blit(ognista_strzala_obrocona, rotated_rect2)
            self.sss += 1
            try:
                if self.sss == len(self.funkcja_x2):
                    self.sss = 0
                    self.animacja_strzal_specjalny = False
            except:
                if self.sss == len(self.funkcja_y2):
                    self.sss = 0
                    self.animacja_strzal_specjalny = False

        if self.animacja_strzal_aoe:

            strzala_obrocona_aoe = pygame.transform.rotate(strzala_animacja, self.kat_obrotu_strzaly_aoe)
            # Uzyskanie prostokąta granicznego dla obróconego obrazka
            rotated_rect_aoe = strzala_obrocona_aoe.get_rect()
            # Ustawienie pozycji prostokąta granicznego na podstawie oryginalnej pozycji gracza i mapy
            try:
                rotated_rect_aoe.center = self.funkcja_lambda3(self.ssss, mapa_x, mapa_y)
            except:
                with open("debugger.txt", "a") as f:
                    f.write(f"funkcja x3: {self.funkcja_x3}, funkcja y3: {self.funkcja_y3}, ssss: {self.ssss}\n")
                    exit()
            # Rysowanie obróconego obrazka z dostosowanym prostokątem granicznym
            okno.blit(strzala_obrocona_aoe, rotated_rect_aoe)
            self.ssss += 1
            try:
                if self.ssss == len(self.funkcja_x3):
                    self.ssss = 0
                    self.animacja_strzal_aoe = False
            except:
                if self.ssss == len(self.funkcja_y3):
                    self.ssss = 0
                    self.animacja_strzal_aoe = False

        if self.animacja_strzal_aoe_2:

            if self.a < 15:
                # Rysowanie ataku na polach dookoła gracza
                for x, y in self.animacja_pola_strzal:
                    okno.blit(atak_gracza_grafika_rozszerzona,
                              (x * rozmiar_pola + mapa_x, y * rozmiar_pola + mapa_y))
                self.a += 1
            elif self.a == 15:
                self.animacja_strzal_aoe_2 = False
                self.a = 1

        # Rysowanie napisu NIE ZYJESZ w przypadku śmierci gracza
        if self.zycie == False:
            pygame.draw.rect(okno, "black", (323, 450, 1920 - 2 * 323, 140))
            okno.blit(self.tekst_nie_zyjesz.render("NIE ŻYJESZ", True, "red"), (860, 495))

    # Function draws player UI #
    def draw_ui(self, okno):

        ui_1 = self.ui_1
        ui_2 = self.ui_2
        ui_3 = self.ui_3
        ui_4 = self.ui_4
        # Rysowanie UI - text bar #
        pygame.draw.rect(okno, "dimgrey", (0, 0, odswiezanie1, wysokosc_okna))
        pygame.draw.rect(okno, "dimgrey", (odswiezanie3, 0, odswiezanie1, wysokosc_okna))
        # Rysowanie logo gry
        okno.blit(logo, (1750, 1015))
        # Rysowanie instrukcji sterowania
        instrukcja_1 = ui_1.render((f"STEROWANIE: "), True, "floral white")
        okno.blit(instrukcja_1, (10, 630))
        instrukcja_1 = ui_2.render((f"ESC - Menu"), True, "grey7")
        okno.blit(instrukcja_1, (10, 660))
        instrukcja_1 = ui_2.render((f"W/S/A/D - chodzenie"), True, "grey7")
        okno.blit(instrukcja_1, (10, 690))
        instrukcja_1 = ui_2.render((f"SHIFT + W/S/A/D - obrót"), True, "grey7")
        okno.blit(instrukcja_1, (10, 720))
        instrukcja_1 = ui_2.render((f"E - interakcja"), True, "grey7")
        okno.blit(instrukcja_1, (10, 750))
        instrukcja_1 = ui_2.render((f"PPM - zaznaczenie"), True, "grey7")
        okno.blit(instrukcja_1, (10, 780))
        instrukcja_1 = ui_2.render((f"SPACJA - auto zaznaczenie "), True, "grey7")
        okno.blit(instrukcja_1, (10, 810))
        instrukcja_1 = ui_2.render((f"Q - atak specjalny 1"), True, "grey7")
        okno.blit(instrukcja_1, (10, 840))
        instrukcja_1 = ui_2.render((f"X - atak specjalny 2"), True, "grey7")
        okno.blit(instrukcja_1, (10, 870))

        instrukcja_1 = ui_2.render((f"1/2 - użycie HP/MP"), True, "grey7")
        okno.blit(instrukcja_1, (10, 900))
        instrukcja_1 = ui_2.render((f"P - muzyka głośniej"), True, "grey7")
        okno.blit(instrukcja_1, (10, 930))
        instrukcja_1 = ui_2.render((f"O - muzyka ciszej"), True, "grey7")
        okno.blit(instrukcja_1, (10, 960))
        instrukcja_1 = ui_1.render((f"DEV: "), True, "floral white")
        okno.blit(instrukcja_1, (10, 990))
        instrukcja_1 = ui_2.render((f"B/M - Zmiana poziomów mapy"), True, "grey7")
        okno.blit(instrukcja_1, (10, 1020))
        instrukcja_1 = ui_2.render((f"L - wyjście z gry"), True, "grey7")
        okno.blit(instrukcja_1, (10, 1050))


        # RYSOWANIE TRACKERA ZADAŃ
        # Rysowanie prostokąta
        pygame.draw.rect(okno, "grey23", (10, 10, 303, 30))
        # Rysowanie napisów
        okno.blit(ui_1.render(f"Zadanie {instances.quest_manager.story}:", True, "floral white"), (15, 15))
        okno.blit(ui_1.render(self.opis_zadan[instances.quest_manager.progress], True, "grey7"), (15, 55))
        # Rysowanie licznika
        if instances.quest_manager.progress == 1:
            okno.blit(ui_1.render(f"Wilki: {self.licznik} / 10 (DEV 3)", True, "floral white"), (15, 95))
        elif instances.quest_manager.progress == 6:
            okno.blit(ui_1.render(f"Pył: {self.licznik} / 10 (DEV 3)", True, "floral white"), (15, 95))
        elif instances.quest_manager.progress == 9:
            okno.blit(ui_1.render(f"Dziki: {self.licznik} / 15 (DEV 3)", True, "floral white"), (15, 95))
        elif instances.quest_manager.progress == 12:
            okno.blit(ui_1.render(f"Pył: {self.licznik} / 10 (DEV 3)", True, "floral white"), (15, 95))
        elif instances.quest_manager.progress == 15:
            okno.blit(ui_1.render(f"Piraci: {self.licznik[0]} / 15 (DEV 3)", True, "floral white"), (15, 95))
            okno.blit(ui_1.render(f"Korsarze: {self.licznik[1]} / 15 (DEV 3)", True, "floral white"), (15, 135))

        # Rysowanie pasków HP i MP w UI
        # Pasek HP
        pygame.draw.rect(okno, "black", (1607, 10, 303, 40))
        pygame.draw.rect(okno, "green3", (1607, 10, (self.hp * (323 - 20)) / self.max_hp, 40))
        okno.blit(ui_3.render(f"HP: {self.hp} / {self.max_hp}", True, "mint cream"), (1692, 20))
        # Pasek MP
        pygame.draw.rect(okno, "black", (1607, 60, 303, 40))
        pygame.draw.rect(okno, "dodgerblue2", (1607, 60, (self.mp * (323 - 20)) / self.max_mp, 40))
        okno.blit(ui_3.render(f"MP: {self.mp} / {self.max_mp}", True, "mint cream"), (1692, 70))

        # Rysowanie grafik i liczby HP Potion i MP Potion i Strzał
        # HP Potion
        okno.blit(hp_potion2, (1607, 110))
        okno.blit(ui_1.render(f": {self.hp_potion}", True, "floral white"), (1655, 127))
        # MP Potion
        okno.blit(mp_potion2, (1707, 110))
        okno.blit(ui_1.render(f": {self.mp_potion}", True, "floral white"), (1756, 127))
        # Strzały
        okno.blit(strzala2, (1817, 115))
        okno.blit(strzala2, (1807, 115))
        okno.blit(strzala2, (1797, 115))
        okno.blit(ui_1.render(f": {self.ilosc_strzal}", True, "floral white"), (1860, 127))

        # Rysowanie stopki STATYSTYKI POSTACI
        pygame.draw.rect(okno, "grey23", (1607, 180, 303, 30))
        okno.blit(ui_1.render("Statystyki postaci", True, "floral white"), (1672, 185))

        # Rysowanie statystyk postaci - + PROGRESS DO NASTĘPNEGO POZIMU
        okno.blit(ui_1.render(f"Poziom: {self.poziom}", True, "floral white"), (1632, 220))
        okno.blit(ui_1.render(f"Doświadczenie: {self.doswiadczenie}", True, "floral white"), (1632, 250))
        okno.blit(ui_1.render(f"Złoto: {self.zloto}", True, "floral white"), (1632, 280))

        pygame.draw.rect(okno, "black", (1770, 218, 139, 21))
        pygame.draw.rect(okno, "dark slate blue", (1770, 218, self.procent_nastepny_poziom * 139 / 100, 21))
        okno.blit(ui_2.render(f"{self.procent_nastepny_poziom} %", True, "floral white"), (1819, 221))

        # Rysowanie stopki BROŃ
        pygame.draw.rect(okno, "grey23", (1607, 310, 303, 30))
        okno.blit(ui_1.render("Broń", True, "floral white"), (1732, 316))

        # Rysowanie ikonki miecza
        okno.blit(miecz, (1657, 355))
        # Rysowanie ikonki łuku
        okno.blit(luk, (1782, 355))
        # Rysowanie przycisków WYBIERZ
        pygame.draw.rect(okno, "grey23", (1657, 439, 74, 20))
        pygame.draw.rect(okno, "grey23", (1782, 439, 74, 20))

        # Rysowanie napisów na przyciskach WYBIERZ
        okno.blit(ui_4.render("Wybierz", True, "floral white"), (1670, 443))
        okno.blit(ui_4.render("Wybierz", True, "floral white"), (1795, 443))

        # Rysowanie poziomów broni
        okno.blit(ui_4.render(f"Poziom: {self.miecz_poziom}", True, "floral white"), (1668, 468))
        okno.blit(ui_4.render(f"Poziom: {self.luk_poziom}", True, "floral white"), (1793, 468))

        # Statystyki broni
        okno.blit(ui_4.render(
            f"Atak: {self.miecz_staty[self.miecz_poziom]["dmg"]} |  Crit: {self.miecz_staty[self.miecz_poziom]["crit"]}%",
            True, "floral white"), (1640, 483))
        okno.blit(ui_4.render(
            f"Atak: {self.luk_staty[self.luk_poziom]["dmg"]} |  Crit: {self.luk_staty[self.luk_poziom]["crit"]}%",
            True, "floral white"), (1770, 483))

        # Rysowanie zaznaczenia broni
        # MIECZ
        if self.bron == "miecz":
            pygame.draw.rect(okno, "grey28", (1657, 354, 74, 3))
            pygame.draw.rect(okno, "grey28", (1657, 354, 3, 74))
            pygame.draw.rect(okno, "grey28", (1656, 426, 76, 3))
            pygame.draw.rect(okno, "grey28", (1729, 354, 3, 74))
        # ŁUK
        elif self.bron == "luk":
            pygame.draw.rect(okno, "grey28", (1782, 354, 74, 3))
            pygame.draw.rect(okno, "grey28", (1781, 354, 3, 74))
            pygame.draw.rect(okno, "grey28", (1781, 426, 76, 3))
            pygame.draw.rect(okno, "grey28", (1854, 354, 3, 74))

        # Rysowanie stopki PANCERZ
        pygame.draw.rect(okno, "grey23", (1607, 510, 303, 30))
        okno.blit(ui_1.render("Pancerz", True, "floral white"), (1722, 516))

        # Statystyki pancerza
        okno.blit(ui_2.render(
            f"Zbroja   - Poziom: {self.zbroja_poziom} | +{self.zbroja_staty[self.zbroja_poziom]["hp"]} HP", True,
            "floral white"), (1635, 555))
        okno.blit(ui_2.render(
            f"Płaszcz - Poziom: {self.plaszcz_poziom} | +{self.plaszcz_staty[self.plaszcz_poziom]["mp"]} MP", True,
            "floral white"), (1635, 580))
        okno.blit(ui_2.render(
            f"Buty      - Poziom: {self.buty_poziom} | +{self.buty_staty[self.buty_poziom]["info"]} Speed", True,
            "floral white"), (1635, 605))

        # Rysowanie stopki Rozwój
        pygame.draw.rect(okno, "grey23", (1607, 640, 303, 30))
        okno.blit(ui_1.render("Rozwój", True, "floral white"), (1727, 646))

        # Punkty rozwoju
        okno.blit(ui_2.render(f"Punkty ulepszeń: {self.punkty_ulepszen}", True, "floral white"), (1635, 685))

        ################################################################################################################

    # Funkcja zaznaczanie przeciwnika przez gracza
    def zaznaczenie_przeciwnika(self, zbior_przeciwnik):
        zaznaczenie = pygame.mouse.get_pressed()
        self.aktualny_czas_z = pygame.time.get_ticks()
        if zaznaczenie[2]:  # Sprawdzenie naciśnięcia prawego klawisza myszy
            mysz_x, mysz_y = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
            if mysz_x >= 323 and mysz_x <= 1597:
                # Zamiana pozycji myszki na pole do warunku sprawdzania
                mysz_x = ((mysz_x - 323) / rozmiar_pola)
                mysz_y = (mysz_y / rozmiar_pola)
                mysz_x -= 6
                mysz_x = int(mysz_x + self.x)
                mysz_y -= 5
                mysz_y = int(mysz_y + self.y)
                for przeciwnik in zbior_przeciwnik:
                    if przeciwnik.x == mysz_x and przeciwnik.y == mysz_y:
                        if self.aktualny_czas_z - self.czas_ostatniego_zaznaczenia >= 1000 / self.predkosc_zaznaczenia:
                            self.czas_ostatniego_zaznaczenia = self.aktualny_czas_z
                            for potwor in zbior_przeciwnik:
                                if potwor.x != mysz_x or potwor.y != mysz_y:
                                    potwor.zaznaczenie = False
                            if przeciwnik.zaznaczenie == False:
                                przeciwnik.zaznaczenie = True
                                self.zaznaczenie = True
                                break
                            elif przeciwnik.zaznaczenie == True:
                                przeciwnik.zaznaczenie = False
                                self.zaznaczenie = False
                                break

    # Funkcja przeliczająca obrażenia zadane przez gracza
    def calculate_dmg(self, attack_type):
        crit = random.randint(1, 100)
        if attack_type == "sword_attack":
            m = 2 if crit <= self.crit_sword else 1
            dmg = random.randint(self.attack_sword - 5, self.attack_sword + 5)
        elif attack_type == "bow_attack":
            m = 2 if crit <= self.crit_bow else 1
            dmg = random.randint(self.attack_bow - 5, self.attack_bow + 5)
        elif attack_type == "sword_special_attack":
            m = 2 if crit <= self.crit_sword else 1
            dmg = random.randint(self.attack_sword, self.attack_sword + 10)
        elif attack_type == "bow_special_attack":
            m = 2 if crit <= self.crit_bow else 1
            dmg = random.randint(self.attack_bow, self.attack_bow + 10)
        return m * dmg, True if m == 2 else False

    # Funkcja ulepszenia danej czesci ekwipunku
    def upgrade_item(self, item):
        if item == "sword":
            if self.miecz_staty.get(self.miecz_poziom + 1):
                if self.punkty_ulepszen >= self.miecz_staty[self.miecz_poziom + 1]["points"]:
                    self.punkty_ulepszen -= self.miecz_staty[self.miecz_poziom + 1]["points"]
                    self.miecz_poziom += 1
                    self.attack_sword = self.miecz_staty[self.miecz_poziom]["dmg"]
                    self.crit_sword = self.miecz_staty[self.miecz_poziom]["crit"]
        elif item == "bow":
            if self.luk_staty.get(self.luk_poziom + 1):
                if self.punkty_ulepszen >= self.luk_staty[self.luk_poziom + 1]["points"]:
                    self.punkty_ulepszen -= self.luk_staty[self.luk_poziom + 1]["points"]
                    self.luk_poziom += 1
                    self.attack_bow = self.luk_staty[self.luk_poziom]["dmg"]
                    self.crit_bow = self.luk_staty[self.luk_poziom]["crit"]
        elif item == "armor":
            if self.zbroja_staty.get(self.zbroja_poziom + 1):
                if self.punkty_ulepszen >= self.zbroja_staty[self.zbroja_poziom + 1]["points"]:
                    self.punkty_ulepszen -= self.zbroja_staty[self.zbroja_poziom + 1]["points"]
                    self.zbroja_poziom += 1
                    self.max_hp = progression_table[self.poziom][2] + self.zbroja_staty[self.zbroja_poziom]["hp"]
        elif item == "cape":
            if self.plaszcz_staty.get(self.plaszcz_poziom + 1):
                if self.punkty_ulepszen >= self.plaszcz_staty[self.plaszcz_poziom + 1]["points"]:
                    self.punkty_ulepszen -= self.plaszcz_staty[self.plaszcz_poziom + 1]["points"]
                    self.plaszcz_poziom += 1
                    self.max_mp = progression_table[self.poziom][3] + self.plaszcz_staty[self.plaszcz_poziom]["mp"]
        elif item == "boots":
            if self.buty_staty.get(self.buty_poziom + 1):
                if self.punkty_ulepszen >= self.buty_staty[self.buty_poziom + 1]["points"]:
                    self.punkty_ulepszen -= self.buty_staty[self.buty_poziom + 1]["points"]
                    self.buty_poziom += 1
                    self.predkosc_chodzenia = self.buty_staty[self.buty_poziom]["speed"]

    # Funkcja atak zaznaczonego przeciwnika przez gracza
    def atak_zaznaczenie(self, zbior_przeciwnik, mapa_jwrpg):
        self.aktualny_czas_az = pygame.time.get_ticks()
        if self.zaznaczenie == True:
            if self.aktualny_czas_az - self.czas_ostatniego_ataku_zaznaczenie >= 1000 / self.predkosc_ataku:
                for przeciwnik in zbior_przeciwnik:
                    if abs(self.x - przeciwnik.x) <= 1 and abs(
                            self.y - przeciwnik.y) <= 1 and przeciwnik.zaznaczenie == True:
                        self.czas_ostatniego_ataku_zaznaczenie = self.aktualny_czas_az
                        przeciwnik.animacja_otrzymane_obrazenia_2 = True
                        przeciwnik.x2 = przeciwnik.x
                        przeciwnik.y2 = przeciwnik.y
                        self.zadane_obrazenia_2, crit = self.calculate_dmg("sword_attack")
                        if przeciwnik.imie == "Pradawny Smok" and instances.dragon.immune:
                            self.zadane_obrazenia_2, crit = 0, False
                        if crit:
                            przeciwnik.critical_hit_2 = True
                        przeciwnik.hp -= self.zadane_obrazenia_2
                        if przeciwnik.hp <= 0:
                            przeciwnik.losowanie_i_dodawanie_loota()
                            self.new_exp = True
                            self.exp = przeciwnik.doswiadczenie
                            self.new_exp_g = 42
                            przeciwnik.status = False
                            przeciwnik.zaznaczenie = False
                            mapa_jwrpg[przeciwnik.y][przeciwnik.x] = 0
                            przeciwnik.x = 0
                            przeciwnik.y = 0
                            przeciwnik.x3 = 0
                            przeciwnik.y3 = 0
                            self.doswiadczenie += przeciwnik.doswiadczenie
                            self.nowy_poziom()
                            self.procent_nastepny_poziom = round(
                                (self.doswiadczenie - self.doswiadczenie_slownik[self.poziom][0]) * 100 / (
                                        self.doswiadczenie_slownik[self.poziom][1] -
                                        self.doswiadczenie_slownik[self.poziom][0]), 1)
                            ### Fabuła wskaźniki
                            if instances.quest_manager.progress == 1 and przeciwnik.imie == "Wilk":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 9 and przeciwnik.imie == "Dzik":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 15:
                                if przeciwnik.imie == "Pirat" and self.licznik[0] < 15:
                                    self.licznik[0] += 1
                                elif przeciwnik.imie == "Korsarz" and self.licznik[1] < 15:
                                    self.licznik[1] += 1
                        break

    # Funkcja atak gracza - zasięg obszarowy na 1 pole dookoła gracza i pole gracza
    def atak(self, zbior_przeciwnik, mapa_jwrpg):
        atak = pygame.key.get_pressed()
        self.aktualny_czas2 = pygame.time.get_ticks()
        if atak[pygame.K_q] or atak[pygame.K_x]:
            mana = 20 if atak[pygame.K_x] else 40
            if self.aktualny_czas2 - self.czas_ostatniego_ataku >= 1000 / self.predkosc_ataku and self.mp >= mana:
                self.czas_ostatniego_ataku = self.aktualny_czas2

                if atak[pygame.K_q]:
                    self.animacja_pola = ((-1 + self.x2, -1 + self.y2), (-1 + self.x2, 0 + self.y2),
                                          (-1 + self.x2, 1 + self.y2), (0 + self.x2, -1 + self.y2),
                                          (0 + self.x2, 1 + self.y2), (1 + self.x2, -1 + self.y2),
                                          (1 + self.x2, 0 + self.y2), (1 + self.x2, 1 + self.y2))
                    przeciwnicy = [p for p in zbior_przeciwnik if
                                   abs(self.x - p.x) <= 1 and abs(self.y - p.y) <= 1 and p.status == True]
                    self.mp = self.mp - 40
                    self.animacja_atak_q = True

                elif atak[pygame.K_x]:
                    if self.m == 0:
                        f = ((-1 + self.x2, -1 + self.y2), (0 + self.x2, -1 + self.y2), (1 + self.x2, -1 + self.y2))
                    elif self.m == 1:
                        f = ((-1 + self.x2, 1 + self.y2), (0 + self.x2, 1 + self.y2), (1 + self.x2, 1 + self.y2))
                    elif self.m == 2:
                        f = ((-1 + self.x2, -1 + self.y2), (-1 + self.x2, 0 + self.y2), (-1 + self.x2, 1 + self.y2))
                    else:
                        f = ((1 + self.x2, -1 + self.y2), (1 + self.x2, 0 + self.y2), (1 + self.x2, 1 + self.y2))
                    self.animacja_pola = f
                    przeciwnicy = [p for p in zbior_przeciwnik if (p.x, p.y) in f and p.status == True]
                    self.mp = self.mp - 20
                    self.animacja_atak_x = True

                self.zadane_obrazenia, crit = self.calculate_dmg("sword_special_attack")
                # Pętla po wszystkich obiektach z utworzonej listy przeciwnicy
                for przeciwnik in przeciwnicy:
                    if not (przeciwnik.imie == "Pradawny Smok" and instances.dragon.immune):
                        # Logika ataku
                        if crit:
                            przeciwnik.critical_hit = True
                        przeciwnik.animacja_otrzymane_obrazenia = True
                        przeciwnik.x2 = przeciwnik.x
                        przeciwnik.y2 = przeciwnik.y
                        przeciwnik.hp -= self.zadane_obrazenia
                    if przeciwnik.hp <= 0:
                        przeciwnik.losowanie_i_dodawanie_loota()
                        ### DO PRZEROBIENIA BY NALICZALO DOBRZE EXPA JAK JESZCZE JEST WYSWIETLANY STARY
                        if self.new_exp_g > 42:
                            self.exp = 0
                        self.new_exp = True
                        self.exp += przeciwnik.doswiadczenie
                        self.new_exp_g = 42
                        przeciwnik.status = False
                        przeciwnik.zaznaczenie = False
                        mapa_jwrpg[przeciwnik.y][przeciwnik.x] = 0
                        przeciwnik.x = 0
                        przeciwnik.y = 0
                        przeciwnik.x3 = 0
                        przeciwnik.y3 = 0
                        self.doswiadczenie += przeciwnik.doswiadczenie
                        self.nowy_poziom()
                        self.procent_nastepny_poziom = round(
                            (self.doswiadczenie - self.doswiadczenie_slownik[self.poziom][0]) * 100 / (
                                    self.doswiadczenie_slownik[self.poziom][1] -
                                    self.doswiadczenie_slownik[self.poziom][0]), 1)
                        ### Fabuła wskaźniki
                        if instances.quest_manager.progress == 1 and przeciwnik.imie == "Wilk":
                            self.licznik += 1
                        elif instances.quest_manager.progress == 9 and przeciwnik.imie == "Dzik":
                            self.licznik += 1
                        elif instances.quest_manager.progress == 15:
                            if przeciwnik.imie == "Pirat" and self.licznik[0] < 15:
                                self.licznik[0] += 1
                            elif przeciwnik.imie == "Korsarz" and self.licznik[1] < 15:
                                self.licznik[1] += 1

    # Funkcja poziom gracza - zmienia self.poziom
    def nowy_poziom(self):
        if self.doswiadczenie >= self.doswiadczenie_slownik[self.poziom][1]:
            self.poziom += 1
            self.punkty_ulepszen += 1
            self.max_hp = self.doswiadczenie_slownik[self.poziom][2]
            self.max_hp += self.zbroja_staty[self.zbroja_poziom]["hp"]
            self.max_mp = self.doswiadczenie_slownik[self.poziom][3]
            self.max_mp += self.plaszcz_staty[self.plaszcz_poziom]["mp"]
            self.hp = self.max_hp
            self.mp = self.max_mp
            self.lvl_up = True

    # Funkcja leczenie gracza - zmienia self.hp/self.mp
    def potion(self):
        przycisk_leczenie = pygame.key.get_pressed()
        self.aktualny_czas4 = pygame.time.get_ticks()
        if przycisk_leczenie[pygame.K_1]:
            if self.hp_potion > 0:
                if self.aktualny_czas4 - self.czas_ostatniego_leczenia >= 1000 / self.predkosc_ataku:
                    self.czas_ostatniego_leczenia = self.aktualny_czas4
                    hp = random.randint(int(self.max_hp * 0.3), int(self.max_hp * 0.5))
                    if self.hp + hp <= self.max_hp:
                        self.potion_value = hp
                        self.hp += hp
                    else:
                        self.potion_value = self.max_hp - self.hp
                        self.hp = self.max_hp
                    self.hp_potion -= 1
                    self.potion_use = True
                    self.potion_type = "hp"
        elif przycisk_leczenie[pygame.K_2]:
            if self.mp_potion > 0:
                if self.aktualny_czas4 - self.czas_ostatniego_leczenia >= 1000 / self.predkosc_ataku:
                    self.czas_ostatniego_leczenia = self.aktualny_czas4
                    mp = random.randint(int(self.max_mp * 0.3), int(self.max_mp * 0.5))
                    if self.mp + mp <= self.max_mp:
                        self.potion_value = mp
                        self.mp += mp
                    else:
                        self.potion_value = self.max_mp - self.mp
                        self.mp = self.max_mp
                    self.mp_potion -= 1
                    self.potion_use = True
                    self.potion_type = "mp"

    # NEW - funkcja rozpoczęcie interakcji z NPC
    def interakcja_npc_NEW(self, zbior_npc):
        interakcja = pygame.key.get_pressed()
        self.aktualny_czas_i = pygame.time.get_ticks()
        if interakcja[pygame.K_e]:
            if self.aktualny_czas_i - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                self.czas_ostatniej_interakcji = self.aktualny_czas_i
                for npc in zbior_npc:
                    # Sprawdzenie pola gracza z pozycja npc na polu mapy
                    if abs(self.x - npc.x) <= 1 and abs(self.y - npc.y) <= 1 and npc.mozliwosc_interakcji == True:
                        # Zmiana parametrów interakcji
                        self.interakcja = True
                        npc.interakcja = True
                        break

    # Funkcja zmiana rodzaju broni
    def zmiana_broni(self):
        zmiana = pygame.mouse.get_pressed()
        if zmiana[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
            mysz_x, mysz_y = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
            if mysz_x >= 1657 and mysz_x <= 1731 and mysz_y >= 439 and mysz_y <= 459:
                self.bron = "miecz"
                self.celownik = False
                pygame.mouse.set_visible(True)
            elif mysz_x >= 1782 and mysz_x <= 1856 and mysz_y >= 439 and mysz_y <= 459:
                self.bron = "luk"

    # Funkcja ataku dystansowego zaznaczonego przeciwnika
    def atak_dystansowy_zaznaczenie(self, zbior_przeciwnik, mapa_jwrpg):
        self.aktualny_czas_az = pygame.time.get_ticks()
        if self.zaznaczenie == True and self.ilosc_strzal > 0:
            if self.aktualny_czas_az - self.czas_ostatniego_ataku_zaznaczenie >= 1000 / self.predkosc_ataku:
                for przeciwnik in zbior_przeciwnik:
                    if przeciwnik.zaznaczenie == True and abs(self.x - przeciwnik.x) <= 6 and abs(
                            self.y - przeciwnik.y) <= 5:
                        self.obliczenia_atak_dystansowy(przeciwnik.x, przeciwnik.y, przeciwnik.x2, przeciwnik.y2,
                                                        przeciwnik.x3, przeciwnik.y3, "normal",
                                                        mapa_jwrpg)

                    if self.czysty_strzal == True:

                        ########## PO UDANYM ATAKU #############
                        self.czas_ostatniego_ataku_zaznaczenie = self.aktualny_czas_az
                        przeciwnik.animacja_otrzymane_obrazenia_2 = True
                        przeciwnik.x2 = przeciwnik.x
                        przeciwnik.y2 = przeciwnik.y
                        self.zadane_obrazenia_2, crit = self.calculate_dmg("bow_attack")
                        if przeciwnik.imie == "Pradawny Smok" and instances.dragon.immune:
                            self.zadane_obrazenia_2, crit = 0, False
                        if crit:
                            przeciwnik.critical_hit_2 = True
                        przeciwnik.hp -= self.zadane_obrazenia_2
                        self.ilosc_strzal -= 1
                        self.czysty_strzal = False
                        self.sposob_strzalu = ""
                        if przeciwnik.hp <= 0:
                            przeciwnik.losowanie_i_dodawanie_loota()
                            self.new_exp = True
                            self.exp = przeciwnik.doswiadczenie
                            self.new_exp_g = 42
                            przeciwnik.status = False
                            przeciwnik.zaznaczenie = False
                            mapa_jwrpg[przeciwnik.y][przeciwnik.x] = 0
                            przeciwnik.x2 = przeciwnik.x
                            przeciwnik.y2 = przeciwnik.y
                            przeciwnik.x = 0
                            przeciwnik.y = 0
                            przeciwnik.x3 = 0
                            przeciwnik.y3 = 0
                            self.doswiadczenie += przeciwnik.doswiadczenie
                            self.nowy_poziom()
                            self.procent_nastepny_poziom = round(
                                (self.doswiadczenie - self.doswiadczenie_slownik[self.poziom][0]) * 100 / (
                                        self.doswiadczenie_slownik[self.poziom][1] -
                                        self.doswiadczenie_slownik[self.poziom][0]), 1)
                            if instances.quest_manager.progress == 1 and przeciwnik.imie == "Wilk":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 9 and przeciwnik.imie == "Dzik":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 15:
                                if przeciwnik.imie == "Pirat" and self.licznik[0] < 15:
                                    self.licznik[0] += 1
                                elif przeciwnik.imie == "Korsarz" and self.licznik[1] < 15:
                                    self.licznik[1] += 1
                        break

    # Funkcja specjalnego ataku dystansowego
    def atak_dystansowy(self, zbior_przeciwnik, mapa_jwrpg):

        atak = pygame.key.get_pressed()
        self.aktualny_czas2 = pygame.time.get_ticks()
        if atak[pygame.K_q] and self.zaznaczenie == True:
            if self.aktualny_czas2 - self.czas_ostatniego_ataku >= 1000 / self.predkosc_ataku and self.mp >= 20:
                for przeciwnik in zbior_przeciwnik:
                    if przeciwnik.zaznaczenie == True and abs(self.x - przeciwnik.x) <= 6 and abs(
                            self.y - przeciwnik.y) <= 5:
                        self.obliczenia_atak_dystansowy(przeciwnik.x, przeciwnik.y, przeciwnik.x2, przeciwnik.y2,
                                                        przeciwnik.x3, przeciwnik.y3, "special_hit",
                                                        mapa_jwrpg)

                    if self.czysty_strzal_specjalny == True:

                        ########## PO UDANYM ATAKU #############
                        self.czas_ostatniego_ataku = self.aktualny_czas2
                        przeciwnik.animacja_otrzymane_obrazenia = True
                        przeciwnik.x2 = przeciwnik.x
                        przeciwnik.y2 = przeciwnik.y
                        self.zadane_obrazenia, crit = self.calculate_dmg("bow_special_attack")
                        if przeciwnik.imie == "Pradawny Smok" and instances.dragon.immune:
                            self.zadane_obrazenia, crit = 0, False
                        if crit:
                            przeciwnik.critical_hit = True
                        przeciwnik.hp -= self.zadane_obrazenia
                        self.mp = self.mp - 20
                        self.czysty_strzal_specjalny = False
                        self.sposob_strzalu_special = ""
                        if przeciwnik.hp <= 0:
                            przeciwnik.losowanie_i_dodawanie_loota()
                            self.new_exp = True
                            self.exp = przeciwnik.doswiadczenie
                            self.new_exp_g = 42
                            przeciwnik.status = False
                            przeciwnik.zaznaczenie = False
                            mapa_jwrpg[przeciwnik.y][przeciwnik.x] = 0
                            przeciwnik.x2 = przeciwnik.x
                            przeciwnik.y2 = przeciwnik.y
                            przeciwnik.x = 0
                            przeciwnik.y = 0
                            przeciwnik.x3 = 0
                            przeciwnik.y3 = 0
                            self.doswiadczenie += przeciwnik.doswiadczenie
                            self.nowy_poziom()
                            self.procent_nastepny_poziom = round(
                                (self.doswiadczenie - self.doswiadczenie_slownik[self.poziom][0]) * 100 / (
                                        self.doswiadczenie_slownik[self.poziom][1] -
                                        self.doswiadczenie_slownik[self.poziom][0]), 1)
                            if instances.quest_manager.progress == 1 and przeciwnik.imie == "Wilk":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 9 and przeciwnik.imie == "Dzik":
                                self.licznik += 1
                            elif instances.quest_manager.progress == 15:
                                if przeciwnik.imie == "Pirat" and self.licznik[0] < 15:
                                    self.licznik[0] += 1
                                elif przeciwnik.imie == "Korsarz" and self.licznik[1] < 15:
                                    self.licznik[1] += 1
                        break

    # Funkcja atak dystansowy specjalny - celowanie
    def atak_dystansowy_celowanie(self, zbior_przeciwnik, mapa_jwrpg):

        celownik = pygame.key.get_pressed()
        if celownik[pygame.K_x]:
            if self.celownik == False and self.celownik_prev:
                self.celownik = True
                pygame.mouse.set_visible(False)
                self.celownik_prev = False
            elif self.celownik == True and self.celownik_prev:
                self.celownik = False
                pygame.mouse.set_visible(True)
                self.celownik_prev = False
        elif not self.celownik_prev:
            self.celownik_prev = True

        if self.celownik:
            strzal = pygame.mouse.get_pressed()
            if strzal[
                0] and self.aktualny_czas2 - self.czas_ostatniego_ataku >= 1000 / self.predkosc_ataku and self.mp >= 40:
                mysz_x, mysz_y = pygame.mouse.get_pos()
                if mysz_x >= 323 and mysz_x <= 1597:
                    mysz_x = ((mysz_x - 323) / rozmiar_pola)
                    mysz_y = (mysz_y / rozmiar_pola)
                    mysz_x -= 6
                    mysz_x = int(mysz_x + self.x)
                    mysz_y -= 5
                    mysz_y = int(mysz_y + self.y)

                    # Sprawdzenie strzału
                    self.obliczenia_atak_dystansowy(mysz_x, mysz_y, mysz_x, mysz_y, mysz_x, mysz_y, "aoe",
                                                    mapa_jwrpg)

                    if self.czysty_strzal_aoe:
                        self.czas_ostatniego_ataku = self.aktualny_czas2
                        self.animacja_pola_strzal = ((-1 + mysz_x, -1 + mysz_y), (-1 + mysz_x, 0 + mysz_y),
                                                     (-1 + mysz_x, 1 + mysz_y), (0 + mysz_x, -1 + mysz_y),
                                                     (0 + mysz_x, 1 + mysz_y), (1 + mysz_x, -1 + mysz_y),
                                                     (1 + mysz_x, 0 + mysz_y), (1 + mysz_x, 1 + mysz_y),
                                                     (mysz_x, mysz_y))
                        przeciwnicy = [p for p in zbior_przeciwnik if
                                       (p.x, p.y) in self.animacja_pola_strzal and p.status]
                        self.zadane_obrazenia, crit = self.calculate_dmg("bow_special_attack")
                        self.mp = self.mp - 40
                        for przeciwnik in przeciwnicy:
                            if not (przeciwnik.imie == "Pradawny Smok" and instances.dragon.immune):
                                przeciwnik.animacja_otrzymane_obrazenia = True
                                przeciwnik.x2 = przeciwnik.x
                                przeciwnik.y2 = przeciwnik.y
                                if crit:
                                    przeciwnik.critical_hit = True
                                przeciwnik.hp -= self.zadane_obrazenia
                            if przeciwnik.hp <= 0:
                                przeciwnik.losowanie_i_dodawanie_loota()
                                self.new_exp = True
                                self.exp = przeciwnik.doswiadczenie
                                self.new_exp_g = 42
                                przeciwnik.status = False
                                przeciwnik.zaznaczenie = False
                                mapa_jwrpg[przeciwnik.y][przeciwnik.x] = 0
                                przeciwnik.x2 = przeciwnik.x
                                przeciwnik.y2 = przeciwnik.y
                                przeciwnik.x = 0
                                przeciwnik.y = 0
                                przeciwnik.x3 = 0
                                przeciwnik.y3 = 0
                                self.doswiadczenie += przeciwnik.doswiadczenie
                                self.nowy_poziom()
                                self.procent_nastepny_poziom = round(
                                    (self.doswiadczenie - self.doswiadczenie_slownik[self.poziom][0]) * 100 / (
                                            self.doswiadczenie_slownik[self.poziom][1] -
                                            self.doswiadczenie_slownik[self.poziom][0]), 1)
                                if instances.quest_manager.progress == 1 and przeciwnik.imie == "Wilk":
                                    self.licznik += 1
                                elif instances.quest_manager.progress == 9 and przeciwnik.imie == "Dzik":
                                    self.licznik += 1
                                elif instances.quest_manager.progress == 15:
                                    if przeciwnik.imie == "Pirat" and self.licznik[0] < 15:
                                        self.licznik[0] += 1
                                    elif przeciwnik.imie == "Korsarz" and self.licznik[1] < 15:
                                        self.licznik[1] += 1
                        self.sposob_strzalu_aoe = ""
                        self.czysty_strzal_aoe = False
                        self.celownik = False
                        pygame.mouse.set_visible(True)

    # Funkcja rysowanie celownika
    def rysowanie_celownik(self, okno):
        if self.celownik:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            line_length = 15
            pygame.draw.line(okno, "grey", (mouse_x - line_length, mouse_y - line_length),
                             (mouse_x + line_length, mouse_y + line_length), 3)
            pygame.draw.line(okno, "grey", (mouse_x - line_length, mouse_y + line_length),
                             (mouse_x + line_length, mouse_y - line_length), 3)

    # Funkcja sprawdzajaca kolizję na trasie strzały --> tworząca trasę strzały
    def obliczenia_atak_dystansowy(self, target_x, target_y, target_x2, target_y2, target_x3, target_y3, attack_type,
                                   mapa_jwrpg):

        atak = False

        # I. Gracz stoi w linii prostej do przeciwnika, poziomo lub pionowo
        if self.x2 == target_x or self.y2 == target_y:

            # SPRAWDZENIE TRASY POZIOMEJ
            if self.y2 == target_y:

                # Gdy przeciwnik jest na Prawo od gracza - warunek odstęp conajmniej 1 pole
                if self.x2 < target_x - 1:
                    # Ilość pól do sprawdzenia
                    droga: int = int(target_x - self.x2)
                    # Sprawdzanie kolizji na trasie
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y2][self.x2 + x + 1] == 0:
                            atak = True
                            sposob_strzalu = "1 sposób poziomo P - STRZAŁ"
                            kat_obrotu = 225
                        elif mapa_jwrpg[self.y2][self.x2 + x + 1] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break

                # Gdy przeciwnik jest na Lewo od gracza - warunek odstęp conajmniej 1 pole
                elif self.x2 > target_x + 1:
                    # Ilość pól do sprawdzenia
                    droga: int = int(self.x2 - target_x)
                    # Sprawdzanie kolizji na trasie
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y2][self.x2 - x - 1] == 0:
                            atak = True
                            sposob_strzalu = "1 sposób poziomo L - STRZAŁ"
                            kat_obrotu = 45
                        elif mapa_jwrpg[self.y2][self.x2 - x - 1] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break

            # SPRAWDZENIE TRASY PIONOWEJ
            elif self.x2 == target_x:

                # Gdy przeciwnik jest na Dół od gracza - warunek odstęp conajmniej 1 pole
                if self.y2 < target_y - 1:
                    # Ilość pól do sprawdzenia
                    droga: int = int(target_y - self.y2)
                    # Sprawdzanie kolizji na trasie
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y2 + x + 1][self.x2] == 0:
                            atak = True
                            sposob_strzalu = "1 sposób pionowo D - STRZAŁ"
                            kat_obrotu = 135
                        elif mapa_jwrpg[self.y2 + x + 1][self.x2] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break

                # Gdy przeciwnik jest na Góra od gracza - warunek odstęp conajmniej 1 pole
                elif self.y2 > target_y + 1:
                    # Ilość pól do sprawdzenia
                    droga: int = int(self.y2 - target_y)
                    # Sprawdzanie kolizji na trasie
                    for x in range(0, droga - 1):
                        if mapa_jwrpg[self.y2 - x - 1][self.x2] == 0:
                            atak = True
                            sposob_strzalu = "1 sposób pionowo G - STRZAŁ"
                            kat_obrotu = 315
                        elif mapa_jwrpg[self.y2 - x - 1][self.x2] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break

        # II. Gracz stoi równo na ukos od przeciwnika, abs_x == abs_y
        elif abs(self.x2 - target_x) == abs(self.y2 - target_y):

            # DÓŁ-PRAWO
            if self.x2 < target_x - 1 and self.y2 < target_y - 1:
                droga: int = int(target_x - self.x2)
                for x in range(0, droga - 1):
                    if mapa_jwrpg[self.y2 + x + 1][self.x2 + x + 1] == 0:
                        atak = True
                        sposob_strzalu = "2 sposób DÓŁ-PRAWO - STRZAŁ"
                        kat_obrotu = 180
                    elif mapa_jwrpg[self.y2 + x + 1][self.x2 + x + 1] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break

            # DÓŁ-LEWO
            elif self.x2 > target_x + 1 and self.y2 < target_y - 1:
                droga: int = int(self.x2 - target_x)
                for x in range(0, droga - 1):
                    if mapa_jwrpg[self.y2 + x + 1][self.x2 - x - 1] == 0:
                        atak = True
                        sposob_strzalu = "2 sposób DÓŁ-LEWO - STRZAŁ"
                        kat_obrotu = 90
                    elif mapa_jwrpg[self.y2 + x + 1][self.x2 - x - 1] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break

            # GÓRA-PRAWO
            elif self.x2 < target_x - 1 and self.y2 > target_y + 1:
                droga: int = int(target_x - self.x2)
                for x in range(0, droga - 1):
                    if mapa_jwrpg[self.y2 - x - 1][self.x2 + x + 1] == 0:
                        atak = True
                        sposob_strzalu = "2 sposób GÓRA-PRAWO - STRZAŁ"
                        kat_obrotu = 270
                    elif mapa_jwrpg[self.y2 - x - 1][self.x2 + x + 1] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break

            # GÓRA-LEWO
            elif self.x2 > target_x + 1 and self.y2 > target_y + 1:
                droga: int = int(self.x2 - target_x)
                for x in range(0, droga - 1):
                    if mapa_jwrpg[self.y2 - x - 1][self.x2 - x - 1] == 0:
                        atak = True
                        sposob_strzalu = "2 sposób GÓRA-LEWO - STRZAŁ"
                        kat_obrotu = 0
                    elif mapa_jwrpg[self.y2 - x - 1][self.x2 - x - 1] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break

        # III. Gracz stoki nierówno na ukos od przeciwnika (tworzenie funkcji liniowej trasy)
        elif abs(self.x2 - target_x) != abs(self.y2 - target_y):

            # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
            m = (target_y - self.y2) / (target_x - self.x2)
            b = self.y2 - m * self.x2

            # Sprawdzenie kolizji na trasie przebiegu funkcji liniowej

            # Gdy abs x = 1 a abs y > 1
            if abs(self.x2 - target_x) == 1 and abs(self.y2 - target_y) > 1:

                # DÓŁ
                if self.y2 < target_y:
                    y = self.y2 + 1
                    while y <= target_y - 1:
                        x = (y - b) / m
                        if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break
                        y += 0.1
                    else:
                        atak = True
                        if self.x2 > target_x:
                            sposob_strzalu = "3 sposób 1 DÓŁ-LEWO - STRZAŁ"
                            kat_obrotu = 90
                        elif self.x2 < target_x:
                            sposob_strzalu = "3 sposób 1 DÓŁ-PRAWO - STRZAŁ"
                            kat_obrotu = 180

                # GÓRA
                elif self.y2 > target_y:
                    y = self.y2 - 1
                    while y >= target_y + 1:
                        x = (y - b) / m
                        if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                                mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                            atak = False
                            sposob_strzalu = "Nie można oddać strzału"
                            break
                        y -= 0.1
                    else:
                        atak = True
                        if self.x2 > target_x:
                            sposob_strzalu = "3 sposób 1 GÓRA-LEWO - STRZAŁ"
                            kat_obrotu = 0
                        elif self.x2 < target_x:
                            sposob_strzalu = "3 sposób 1 GÓRA-PRAWO - STRZAŁ"
                            kat_obrotu = 270

            # PRAWO
            elif self.x2 <= target_x - 1:
                x = self.x2 + 1
                while x <= target_x - 1:
                    y = m * x + b
                    if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                            mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break
                    x += 0.1
                else:
                    atak = True
                    if self.y2 > target_y:
                        sposob_strzalu = "3 sposób 2 GÓRA-PRAWO - STRZAŁ"
                        kat_obrotu = 270
                    elif self.y2 < target_y:
                        sposob_strzalu = "3 sposób 2 DÓŁ-PRAWO - STRZAŁ"
                        kat_obrotu = 180

            # LEWO
            elif self.x2 >= target_x + 1:
                x = self.x2 - 1
                while x >= target_x + 1:
                    y = m * x + b
                    if mapa_jwrpg[int(math.floor(y))][int(math.ceil(x))] == 1 or \
                            mapa_jwrpg[int(math.ceil(y))][int(math.ceil(x))] == 1:
                        atak = False
                        sposob_strzalu = "Nie można oddać strzału"
                        break
                    x = x - 0.1
                else:
                    atak = True
                    if self.y2 > target_y:
                        sposob_strzalu = "3 sposób 2 GÓRA-LEWO - STRZAŁ"
                        kat_obrotu = 0
                    elif self.y2 < target_y:
                        sposob_strzalu = "3 sposób 2 DÓŁ-LEWO - STRZAŁ"
                        kat_obrotu = 90

        # Czysty strzał
        if atak:

            # Obliczenie kąta obrotu dla 3 sposobu
            if sposob_strzalu[0] == "3":
                delta_x = target_x - self.x
                delta_y = target_y - self.y
                # Obliczenie kąta w radianach od osi poziomej
                kat_rad = math.atan2(delta_x, delta_y)
                # Konwersja na stopnie
                kat_obrotu = 135 + math.degrees(kat_rad)

            # Tworzenie list ze współrzędnymi do iteracji dla strzału oraz funkcji lambda
            target_x2 = target_x3  # zamiennie przeciwnik.x
            target_y2 = target_y3  # zamiennie przeciwnik.y

            # 1 SPOSÓB - POZIOMO - PRAWO
            if sposob_strzalu == "1 sposób poziomo P - STRZAŁ":
                odleglosc = abs(self.x - target_x2)
                funkcja_x = [self.x + 0.5 * x for x in range(1, round(odleglosc / 0.5))]
                funkcja_y = self.y
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    self.y * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 1 SPOSÓB - POZIOMO - LEWO
            elif sposob_strzalu == "1 sposób poziomo L - STRZAŁ":
                odleglosc = abs(self.x - target_x2)
                funkcja_x = [self.x - 0.5 * x for x in range(1, round(odleglosc / 0.5))]
                funkcja_y = self.y
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    self.y * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 1 SPOSÓB - PIONOWO - DÓŁ
            elif sposob_strzalu == "1 sposób pionowo D - STRZAŁ":
                odleglosc = abs(self.y - target_y2)
                funkcja_y = [self.y + 0.5 * y for y in range(1, round(odleglosc / 0.5))]
                funkcja_x = self.x
                funkcja_lambda = lambda y_lambda, mapa_x, mapa_y: (
                    self.x * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[y_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 1 SPOSÓB - PIONOWO - GÓRA
            elif sposob_strzalu == "1 sposób pionowo G - STRZAŁ":
                odleglosc = abs(self.y - target_y2)
                funkcja_y = [self.y - 0.5 * y for y in range(1, round(odleglosc / 0.5))]
                funkcja_x = self.x
                funkcja_lambda = lambda y_lambda, mapa_x, mapa_y: (
                    self.x * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[y_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)

            # 2 SPOSÓB - DÓŁ PRAWO
            elif sposob_strzalu == "2 sposób DÓŁ-PRAWO - STRZAŁ":
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                funkcja_x = [self.x + 0.354 * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y + 0.354 * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 2 SPOSÓB - DÓŁ LEWO
            elif sposob_strzalu == "2 sposób DÓŁ-LEWO - STRZAŁ":
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                funkcja_x = [self.x - 0.354 * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y + 0.354 * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 2 SPOSÓB - GÓRA PRAWO
            elif sposob_strzalu == "2 sposób GÓRA-PRAWO - STRZAŁ":
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                funkcja_x = [self.x + 0.354 * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y - 0.354 * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 2 SPOSÓB - GÓRA LEWO
            elif sposob_strzalu == "2 sposób GÓRA-LEWO - STRZAŁ":
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                funkcja_x = [self.x - 0.354 * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y - 0.354 * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)

            # 3 SPOSÓB 1 DÓŁ LEWO
            elif sposob_strzalu == "3 sposób 1 DÓŁ-LEWO - STRZAŁ" or sposob_strzalu == "3 sposób 2 DÓŁ-LEWO - STRZAŁ":
                # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                m = (target_y2 - self.y) / (target_x2 - self.x)
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                # Wyznaczenie kroku po x
                x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                # Wyznaczenie kroku po y
                y_przemieszczenie = abs(m * x_przemieszczenie)
                funkcja_x = [self.x - x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y + y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 3 SPOSÓB 1 DÓŁ PRAWO
            elif sposob_strzalu == "3 sposób 1 DÓŁ-PRAWO - STRZAŁ" or sposob_strzalu == "3 sposób 2 DÓŁ-PRAWO - STRZAŁ":
                # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                m = (target_y2 - self.y) / (target_x2 - self.x)
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                # Wyznaczenie kroku po x
                x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                # Wyznaczenie kroku po y
                y_przemieszczenie = abs(m * x_przemieszczenie)
                funkcja_x = [self.x + x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y + y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 3 SPOSÓB 1 GÓRA-LEWO
            elif sposob_strzalu == "3 sposób 1 GÓRA-LEWO - STRZAŁ" or sposob_strzalu == "3 sposób 2 GÓRA-LEWO - STRZAŁ":
                # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                m = (target_y2 - self.y) / (target_x2 - self.x)
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                # Wyznaczenie kroku po x
                x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                # Wyznaczenie kroku po y
                y_przemieszczenie = abs(m * x_przemieszczenie)
                funkcja_x = [self.x - x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y - y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)
            # 3 SPOSÓB 1 GÓRA-PRAWO
            elif sposob_strzalu == "3 sposób 1 GÓRA-PRAWO - STRZAŁ" or sposob_strzalu == "3 sposób 2 GÓRA-PRAWO - STRZAŁ":
                # TWORZENIE FUNKCJI LINIOWEJ NA PODSTAWIE POŁOŻENIA GRACZA I PRZECIWNIKA (y = m * x + b)
                m = (target_y2 - self.y) / (target_x2 - self.x)
                przekatna = ((abs(self.x - target_x2)) ** 2 + (abs(self.y - target_y2)) ** 2) ** 0.5
                # Wyznaczenie kroku po x
                x_przemieszczenie = abs(0.5 / (1 + m ** 2) ** 0.5)
                # Wyznaczenie kroku po y
                y_przemieszczenie = abs(m * x_przemieszczenie)
                funkcja_x = [self.x + x_przemieszczenie * x for x in range(1, round(przekatna / 0.5))]
                funkcja_y = [self.y - y_przemieszczenie * y for y in range(1, round(przekatna / 0.5))]
                funkcja_lambda = lambda x_lambda, mapa_x, mapa_y: (
                    funkcja_x[x_lambda] * rozmiar_pola + mapa_x + rozmiar_pola / 2,
                    funkcja_y[x_lambda] * rozmiar_pola + mapa_y + rozmiar_pola / 2)

            if not funkcja_x or not funkcja_y:
                with open("debugger.txt", "a") as f:
                    f.write("+1\n")

            ### Ładowanie parametrów klasowych ###
            if attack_type == "normal":
                self.czysty_strzal = True
                self.kat_obrotu_strzaly = kat_obrotu
                self.sposob_strzalu = sposob_strzalu
                self.animacja_strzal = True
                self.funkcja_x = funkcja_x
                self.funkcja_y = funkcja_y
                self.funkcja_lambda = funkcja_lambda
            elif attack_type == "special_hit":
                self.czysty_strzal_specjalny = True
                self.kat_obrotu_strzaly_specjalny = kat_obrotu
                self.sposob_strzalu_special = sposob_strzalu
                self.animacja_strzal_specjalny = True
                self.funkcja_x2 = funkcja_x
                self.funkcja_y2 = funkcja_y
                self.funkcja_lambda2 = funkcja_lambda
            elif attack_type == "aoe":
                self.czysty_strzal_aoe = True
                self.kat_obrotu_strzaly_aoe = kat_obrotu
                self.sposob_strzalu_aoe = sposob_strzalu
                self.animacja_strzal_aoe = True
                self.animacja_strzal_aoe_2 = True
                self.funkcja_x3 = funkcja_x
                self.funkcja_y3 = funkcja_y
                self.funkcja_lambda3 = funkcja_lambda

    ### Funkcja - zbieranie loota ###
    def zbierz_loot(self, loot, loot_quest):
        zbieranie = pygame.mouse.get_pressed()
        self.aktualny_czas_loot = pygame.time.get_ticks()
        if zbieranie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
            mysz_x, mysz_y = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
            if mysz_x >= 323 and mysz_x <= 1597:
                # Zamiana pozycji myszki na pole do warunku sprawdzania
                mysz_x = ((mysz_x - 323) / rozmiar_pola)
                mysz_y = (mysz_y / rozmiar_pola)
                mysz_x -= 6
                mysz_x = int(mysz_x + self.x)
                mysz_y -= 5
                mysz_y = int(mysz_y + self.y)
                for index, loots in enumerate(loot):
                    if loots[0] == mysz_x and loots[1] == mysz_y and abs(self.x - loots[0]) <= 1 and abs(
                            self.y - loots[1]) <= 1:
                        if self.aktualny_czas_loot - self.czas_ostatniego_loota >= 1000 / self.predkosc_zaznaczenia:
                            self.czas_ostatniego_loota = self.aktualny_czas_loot
                            self.zloto += loots[2]["zloto"]
                            self.gold_ile = loots[2]["zloto"]
                            loot.pop(index)  ### USUWANIE LOOTA Z LISTY PO ZEBRANIU PRZEZ GRACZA
                            if self.gold == False:
                                self.gold = True
                            else:
                                self.gold_g = 42

                ### ZBIERANIE PRZEDMIOTÓW FABUŁA - NEW ###
                if instances.quest_manager.progress in [6, 12]:
                    for index, pyl in enumerate(loot_quest):
                        if pyl[0] == mysz_x and pyl[1] == mysz_y and abs(self.x - pyl[0]) <= 1 and abs(
                                self.y - pyl[1]) <= 1:
                            self.licznik += 1
                            loot_quest.pop(index)
                            break

    ### Funkcja zaznaczenie spacja przeciwnika najblizszego/przelaczenie na kolejnego ###
    def zaznacz_przeciwnika_spacja(self, zbior_przeciwnik):
        przycisk_spacja_przeciwnik = pygame.key.get_pressed()
        self.aktualny_czas99 = pygame.time.get_ticks()
        if przycisk_spacja_przeciwnik[pygame.K_SPACE]:
            if self.aktualny_czas4 - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                self.czas_ostatniej_interakcji = self.aktualny_czas99

                zaznaczenie = [p for p in zbior_przeciwnik if p.zaznaczenie == True]

                if not zaznaczenie:
                    lista_przeciwnik = [(p, (abs(p.x - self.x) ** 2 + abs(p.y - self.y) ** 2) ** 0.5) for p in
                                        zbior_przeciwnik if (abs(p.x - self.x) < 7 and abs(p.y - self.y) < 6)]
                    lista_przeciwnik.sort(key=lambda x: x[1])
                    if lista_przeciwnik:
                        lista_przeciwnik[0][0].zaznaczenie = True
                        self.zaznaczenie = True

                elif zaznaczenie:
                    lista_przeciwnik = [(p, (abs(p.x - self.x) ** 2 + abs(p.y - self.y) ** 2) ** 0.5) for p in
                                        zbior_przeciwnik if
                                        (abs(p.x - self.x) < 7 and abs(p.y - self.y) < 6) and p not in zaznaczenie]
                    lista_przeciwnik.sort(key=lambda x: x[1])
                    if lista_przeciwnik:
                        lista_przeciwnik[0][0].zaznaczenie = True
                        zaznaczenie[0].zaznaczenie = False
                        self.zaznaczenie = True

    # Funkcja wczytująca opisy zadań
    def load_quest_descriptions(self):
        self.opis_zadan = []
        zadanie0 = "Porozmawiaj z Garrickiem."
        zadanie1 = "Zabij 10 wilków."
        zadanie2 = "Wróć do Garricka."
        zadanie3 = "Udaj się do Thorne'a."
        zadanie4 = "Odnajdź Finn'a w jaskini."
        zadanie5 = "Wróć do Thorne'a."
        zadanie6 = "Zbierz 10 szt. pyłu z pająków."
        zadanie7 = "Dostarcz pył Mirandzie."
        zadanie8 = "Idź do Garricka."
        zadanie9 = "Zabij 15 dzików."
        zadanie10 = "Wróć do Garricka."
        zadanie11 = "Odwiedź Mirandę."
        zadanie12 = "Zdobądź pył z białych pająków."
        zadanie13 = "Zanieś pył Mirandzie."
        zadanie14 = "Znajdź kryjówkę piratów."
        zadanie15 = "Zabij piratów i korsarzy."
        zadanie16 = "Porozmawiaj z Vane'em."
        zadanie17 = "Wejdź do portalu."
        zadanie18 = "Zabij pradawnego smoka."
        zadanie19 = "Porozmawiaj ze smokiem."
        self.opis_zadan.append(zadanie0)
        self.opis_zadan.append(zadanie1)
        self.opis_zadan.append(zadanie2)
        self.opis_zadan.append(zadanie3)
        self.opis_zadan.append(zadanie4)
        self.opis_zadan.append(zadanie5)
        self.opis_zadan.append(zadanie6)
        self.opis_zadan.append(zadanie7)
        self.opis_zadan.append(zadanie8)
        self.opis_zadan.append(zadanie9)
        self.opis_zadan.append(zadanie10)
        self.opis_zadan.append(zadanie11)
        self.opis_zadan.append(zadanie12)
        self.opis_zadan.append(zadanie13)
        self.opis_zadan.append(zadanie14)
        self.opis_zadan.append(zadanie15)
        self.opis_zadan.append(zadanie16)
        self.opis_zadan.append(zadanie17)
        self.opis_zadan.append(zadanie18)
        self.opis_zadan.append(zadanie19)

    # Funkcja zwracajaca slownik z parametrami gracza do zapisu
    def slownik_parametry_gracza_save(self):
        gracz_d = {"x": self.x,
                   "y": self.y,
                   "x2": self.x2,
                   "y2": self.y2,
                   "m": self.m,
                   "ilosc_ruchow": self.ilosc_ruchow,
                   "imie": self.imie,
                   "doswiadczenie": self.doswiadczenie,
                   "poziom": self.poziom,
                   "hp": self.hp,
                   "mp": self.mp,
                   "max_hp": self.max_hp,
                   "max_mp": self.max_mp,
                   "zloto": self.zloto,
                   "hp_potion": self.hp_potion,
                   "mp_potion": self.mp_potion,
                   "strzaly": self.ilosc_strzal,
                   "bron": self.bron,
                   "zycie": self.zycie,
                   "map_lvl": instances.game_map.level,
                   "predkosc": self.predkosc_chodzenia,
                   "f": instances.quest_manager.progress,
                   "fabula": instances.quest_manager.story,
                   "licznik": self.licznik,
                   "procent_poziom": self.procent_nastepny_poziom,
                   "text_x": self.text_x,
                   "text_y": self.text_y,

                   "punkty_ulepszen": self.punkty_ulepszen,
                   "attack_sword": self.attack_sword,
                   "attack_bow": self.attack_bow,
                   "crit_sword": self.crit_sword,
                   "crit_bow": self.crit_bow,
                   "miecz_poziom": self.miecz_poziom,
                   "luk_poziom": self.luk_poziom,
                   "zbroja_poziom": self.zbroja_poziom,
                   "plaszcz_poziom": self.plaszcz_poziom,
                   "buty_poziom": self.buty_poziom}
        return gracz_d

    # Funkcja ładująca parametry gracza z SAVE
    def load_save(self, save):
        if instances.game_map.level == "main":
            instances.game_map.main_map_jwrpg[self.y2][self.x2] = 0
        else:
            instances.game_map.underground_map_jwrpg[self.y2][self.x2] = 0
        instances.game_map.level = save["map_lvl"]
        instances.quest_manager.progress = save["f"]
        instances.quest_manager.story = save["fabula"]
        self.x = save["x"]
        self.y = save["y"]
        self.x2 = save["x2"]
        self.y2 = save["y2"]
        self.m = save["m"]
        self.kierunek_ruchu = "w" if self.m == 0 else "s" if self.m == 1 else "a" if self.m == 2 else "d"
        self.ilosc_ruchow = save["ilosc_ruchow"]
        self.imie = save["imie"]
        self.doswiadczenie = save["doswiadczenie"]
        self.poziom = save["poziom"]
        self.hp = save["hp"]
        self.mp = save["mp"]
        self.max_hp = save["max_hp"]
        self.max_mp = save["max_mp"]
        self.zloto = save["zloto"]
        self.hp_potion = save["hp_potion"]
        self.mp_potion = save["mp_potion"]
        self.ilosc_strzal = save["strzaly"]
        self.bron = save["bron"]
        self.zycie = save["zycie"]
        self.predkosc_chodzenia = save["predkosc"]
        self.licznik = save["licznik"]
        self.procent_nastepny_poziom = save["procent_poziom"]
        self.text_x = save["text_x"]
        self.text_y = save["text_y"]
        self.punkty_ulepszen = save["punkty_ulepszen"]
        self.attack_sword = save["attack_sword"]
        self.attack_bow = save["attack_bow"]
        self.crit_sword = save["crit_sword"]
        self.crit_bow = save["crit_bow"]
        self.miecz_poziom = save["miecz_poziom"]
        self.luk_poziom = save["luk_poziom"]
        self.zbroja_poziom = save["zbroja_poziom"]
        self.plaszcz_poziom = save["plaszcz_poziom"]
        self.buty_poziom = save["buty_poziom"]
        self.zaznaczenie = False
        self.interakcja = False

    # New game - resets player
    def new_game(self):
        self.__init__(start_pos[0], start_pos[1])