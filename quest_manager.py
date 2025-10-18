import pygame
from MAIN_CONFIG import TILE_SIZE as rozmiar_pola, REFRESHING_1 as odswiezanie1, DISPLAY_WIDTH as szerokosc_okna
from MAIN_CONFIG import REFRESHING_2 as odswiezanie2
from instances import gracz, game_map, window as okno, thorne, torin, garrick, miranda, kowal, vane, flint
from przeciwnik import Przeciwnik
from dragon import Dragon
from assets import znak, cialo
import instances


### QUEST MAIN CONFIG - DEV #######
WOLFES_TO_BE_KILLED = 3 ######## 10
DUST_TO_BE_COLLECTED = 3 ####### 10
BOARS_TO_BE_KILLED = 3 ######### 15
WHITE_DUST_TO_BE_COLLECTED = 3 # 10
PIRATES_TO_BE_KILLED = 3 ####### 15
###################################


### QUEST MANAGER CLASS - represents story of the game #################################################################
class QuestManager:

    ### Initializer ###
    def __init__(self):

        self.progress = 0 # Overall progress - f
        self.story = 1 # Quest number - fabula
        self.dragon_progress = 1 # Final boss parameter
        self.font = pygame.font.Font(None, 38)
        self.quests = [self.quest_1, self.quest_2, self.quest_3, self.quest_4,
                       self.quest_5, self.quest_6, self.quest_7]

    #########################################
    ### 1 QUEST - Hunt wolves for Garrick ###
    def quest_1(self):

        # Talking with Garrick #
        if self.progress == 0:

            # Enabling talking with Garrick
            if not garrick.mozliwosc_interakcji:
                garrick.mozliwosc_interakcji = True

            # Drawing sign above Garrick
            garrick.draw_sign(okno)

            # Dialogue lines
            if garrick.interakcja:
                if garrick.f == 0:
                    # Garrick
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista[garrick.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif garrick.f == 1:
                    # Garrick
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista[garrick.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 1]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                # After talking with Garrick
                elif garrick.f == 2:
                    self.progress = 1  # Changing progress
                    garrick.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    garrick.interakcja = False

        # Killing wolves #
        elif self.progress == 1:

            # Checking if 10 wolves killed
            if gracz.licznik >= WOLFES_TO_BE_KILLED:
                self.progress = 2 # Changing progress

        # Returning to Garrick #
        elif self.progress == 2:

            # Enabling talking with Garrick
            if not garrick.mozliwosc_interakcji:
                garrick.mozliwosc_interakcji = True

            # Drawing sign above Garrick
            garrick.draw_sign(okno)

            # Dialogue lines
            if garrick.interakcja:
                if garrick.f == 2:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 1]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 2]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif garrick.f == 3:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 2]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 3]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                # After talking with Garrick
                elif garrick.f == 4:
                    self.story = 2 # Changing story parameter
                    self.progress = 3 # Changing progress
                    gracz.gold = True
                    gracz.gold_ile = 100
                    garrick.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    garrick.interakcja = False
                    gracz.zloto += 100

    ### 2 QUEST - Thorne cave adventure #####
    def quest_2(self):

        # Talking with Thorne #
        if self.progress == 3:

            # Enabling talking with Garrick
            if not thorne.mozliwosc_interakcji:
                thorne.mozliwosc_interakcji = True

            # Drawing sign above Thorne
            thorne.draw_sign(okno)

            # Dialogue lines
            if thorne.interakcja:
                if thorne.f == 0:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 1:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 1]}", True,
                                         "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 2:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 1]}", True,
                                         "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 2]}", True,
                                         "floral white"),
                        (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                # After talking with Thorne
                elif thorne.f == 3:
                    self.progress = 4  # Changing progress
                    thorne.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    thorne.interakcja = False
                    gracz.licznik = 0

        # Finding body in cave #
        elif self.progress == 4:

            # Dead body drawing with sign
            if game_map.level == "underground":
                if abs(61 - gracz.x) < 7 and abs(79 - gracz.y) < 6:
                    okno.blit(cialo, ((61 * rozmiar_pola + game_map.x,
                                       79 * rozmiar_pola + game_map.y + 10)))
                    thorne.znak_p += 1
                    if thorne.znak_p % 3 == 0:
                        if thorne.znak_dir == "up":
                            thorne.znak_quest += 1
                        else:
                            thorne.znak_quest -= 1
                    if thorne.znak_p == 30:
                        if thorne.znak_dir == "up":
                            thorne.znak_dir = "down"
                        else:
                            thorne.znak_dir = "up"
                        thorne.znak_p = 0
                    okno.blit(znak, (61 * rozmiar_pola + 42 + game_map.x,
                                     79 * rozmiar_pola + 35 - thorne.znak_quest + game_map.y))

                    # Dead body action - finding Finn diary
                    przycisk = pygame.key.get_pressed()
                    if przycisk[pygame.K_e] and abs(gracz.x - 61) <= 1 and abs(gracz.y - 79) <= 1:
                        gracz.interakcja = True

                    # Drawing diary
                    if gracz.interakcja == True:
                        pygame.draw.rect(okno, "dimgrey", (odswiezanie1 + 150, 150,
                                                           odswiezanie2 - 300, 1080 - 300))
                        pygame.draw.rect(okno, "grey13", (odswiezanie1 + 200, 200,
                                                          odswiezanie2 - 400, 1080 - 400))
                        okno.blit(thorne.tekst_sklep_2.render("Dziennik Finn'a", True, "floral white"),
                                  (810 + 20, 540 - 350 + 60 + 50))
                        okno.blit(
                            thorne.tekst_nazwa.render("Jestem ranny... Trucizna pająków działa szybciej niż myślałem. ",
                                                      True, "floral white"), (540, 400 + 40))
                        okno.blit(thorne.tekst_nazwa.render(
                            "Są silniejsze niż kiedykolwiek. Mam wrażenie, że coś je kontroluje.", True,
                            "floral white"), (540, 400 + 60 + 40))
                        okno.blit(
                            thorne.tekst_nazwa.render("Słyszę dziwne szepty w nieznanym mi języku... chyba umieram.",
                                                      True, "floral white"), (540, 400 + 120 + 40))

                        pygame.draw.rect(okno, "grey27", (810, 540 + 200, 300, 100))
                        okno.blit(thorne.tekst_sklep_2.render("ZABIERZ", True, "floral white"),
                                  (810 + 70, 540 + 200 + 30, 300, 100))

                        # Taking diary
                        zabierz = pygame.mouse.get_pressed()
                        if zabierz[0]:
                            x, y = pygame.mouse.get_pos()
                            if x >= 810 and x <= 1110 and y >= 740 and y <= 840:
                                self.progress = 5 # Changing progress
                                gracz.interakcja = False

        # Returning to Thorne #
        elif self.progress == 5:

            # Dead body drawing
            if game_map.level == "underground":
                if abs(61 - gracz.x) < 7 and abs(79 - gracz.y) < 6:
                    okno.blit(cialo, ((61 * rozmiar_pola + game_map.x, 79 * rozmiar_pola + game_map.y + 10)))

            # Enabling talking with Thorne
            if not thorne.mozliwosc_interakcji:
                thorne.mozliwosc_interakcji = True

            # Drawing sign above Thorne
            thorne.draw_sign(okno)

            # Dialogue lines
            if thorne.interakcja:
                if thorne.f == 3:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 2]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 4:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 2]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 5:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 2]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 3]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 6:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 3]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 4]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 5]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif thorne.f == 7:
                    # NPC
                    okno.blit(self.font.render(f"{thorne.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 5]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista[thorne.f + 6]}", True,
                                         "floral white"), (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{thorne.dialog_lista_gracz[thorne.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                # After talking with Thorne
                elif thorne.f == 8:
                    self.progress = 6 # Changing progress
                    self.story = 3 # Changing story parameter
                    thorne.mozliwosc_interakcji = False
                    gracz.new_exp = True
                    gracz.exp = 500
                    gracz.interakcja = False
                    thorne.interakcja = False
                    gracz.doswiadczenie += 500
                    gracz.nowy_poziom()
                    gracz.procent_nastepny_poziom = round(
                        (gracz.doswiadczenie - gracz.doswiadczenie_slownik[gracz.poziom][0]) * 100 / (
                                gracz.doswiadczenie_slownik[gracz.poziom][1] -
                                gracz.doswiadczenie_slownik[gracz.poziom][0]), 1)
                    gracz.licznik = 0

    ### 3 QUEST - Spider dust ###############
    def quest_3(self):

        # Obtaining spider dust #
        if self.progress == 6:

            # Sign drawing above looted items
            if game_map.level == "main":
                for pyl in Przeciwnik.loot_przedmioty_fabula_powierzchnia:
                    if abs(pyl[0] - gracz.x) <= 7 and abs(pyl[1] - gracz.y) <= 6:
                        thorne.znak_p += 1
                        if thorne.znak_p % 3 == 0:
                            if thorne.znak_dir == "up":
                                thorne.znak_quest += 1
                            else:
                                thorne.znak_quest -= 1
                        if thorne.znak_p == 30:
                            if thorne.znak_dir == "up":
                                thorne.znak_dir = "down"
                            else:
                                thorne.znak_dir = "up"
                            thorne.znak_p = 0
                        okno.blit(znak, (pyl[0] * rozmiar_pola + 42 + game_map.x,
                                         pyl[1] * rozmiar_pola + 35 - thorne.znak_quest + game_map.y))
            else:
                for pyl in Przeciwnik.loot_przedmioty_fabula_podziemia:
                    if abs(pyl[0] - gracz.x) <= 7 and abs(pyl[1] - gracz.y) <= 6:
                        thorne.znak_p += 1
                        if thorne.znak_p % 3 == 0:
                            if thorne.znak_dir == "up":
                                thorne.znak_quest += 1
                            else:
                                thorne.znak_quest -= 1
                        if thorne.znak_p == 30:
                            if thorne.znak_dir == "up":
                                thorne.znak_dir = "down"
                            else:
                                thorne.znak_dir = "up"
                            thorne.znak_p = 0
                        okno.blit(znak, (pyl[0] * rozmiar_pola + 42 + game_map.x,
                                         pyl[1] * rozmiar_pola + 35 - thorne.znak_quest + game_map.y))

            # After collecting the dust
            if gracz.licznik >= DUST_TO_BE_COLLECTED:
                self.progress = 7 # Changing progress
                gracz.licznik = 0
                Przeciwnik.loot_przedmioty_fabula_powierzchnia.clear()
                Przeciwnik.loot_przedmioty_fabula_podziemia.clear()

        # Taking dust to Miranda #
        elif self.progress == 7:

            # Allowing interaction with Miranda
            if not miranda.mozliwosc_interakcji:
                miranda.mozliwosc_interakcji = True

            # Drawing sign above Miranda
            miranda.draw_sign(okno)

            # Dialogue lines
            if miranda.interakcja:
                if miranda.f == 0:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 1:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f]}", True, "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 1]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 2]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 2:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{miranda.dialog_lista[miranda.f + 2]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                # After talking to Miranda
                elif miranda.f == 3:
                    self.progress = 8 # Changing progress
                    self.story = 4 # Changing story parameter
                    miranda.f = 4
                    miranda.mozliwosc_interakcji = False
                    gracz.new_exp = True
                    gracz.exp = 750
                    gracz.interakcja = False
                    miranda.interakcja = False
                    gracz.doswiadczenie += 750
                    gracz.nowy_poziom()
                    gracz.procent_nastepny_poziom = round(
                        (gracz.doswiadczenie - gracz.doswiadczenie_slownik[gracz.poziom][0]) * 100 / (
                                gracz.doswiadczenie_slownik[gracz.poziom][1] -
                                gracz.doswiadczenie_slownik[gracz.poziom][0]), 1)
                    gracz.licznik = 0

    ### 4 QUEST - Hunt boars for Garrick ####
    def quest_4(self):

        # Talking with Garrick #
        if self.progress == 8:

            # Enabling talking with Garrick
            if not garrick.mozliwosc_interakcji:
                garrick.mozliwosc_interakcji = True

            # Drawing sign above Garrick
            garrick.draw_sign(okno)

            # Dialogue lines
            if garrick.interakcja:
                if garrick.f == 4:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 3]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 4]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif garrick.f == 5:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 4]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 5]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif garrick.f == 6:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 5]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking to Garrick
                elif garrick.f == 7:
                    self.progress = 9 # Changing progress
                    garrick.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    garrick.interakcja = False

        # Killing boars #
        elif self.progress == 9:

            # Checking if 15 boars killed
            if gracz.licznik >= BOARS_TO_BE_KILLED:
                self.progress = 10 # Changing progress
                gracz.licznik = 0

        # Coming back to Garrick #
        elif self.progress == 10:

            # Enabling talking with Garrick
            if not garrick.mozliwosc_interakcji:
                garrick.mozliwosc_interakcji = True

            # Drawing sign above Garrick
            garrick.draw_sign(okno)

            # Dialogue lines
            if garrick.interakcja:
                if garrick.f == 7:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 5]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 - 15))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 6]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif garrick.f == 8:
                    # NPC
                    okno.blit(self.font.render(f"{garrick.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{garrick.dialog_lista[garrick.f + 6]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 120, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{garrick.dialog_lista_gracz[garrick.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking to Garrick
                elif garrick.f == 9:
                    self.progress = 11 # Changing progress
                    self.story = 5 # Changing story parameter
                    garrick.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    garrick.interakcja = False
                    gracz.gold = True
                    gracz.gold_ile = 250
                    gracz.zloto += 250

    ### 5 QUEST - White Spider dust #########
    def quest_5(self):

        # Talking with Miranda #
        if self.progress == 11:

            # Enabling talking with Miranda
            if not miranda.mozliwosc_interakcji:
                miranda.mozliwosc_interakcji = True

            # Drawing sign above Miranda
            miranda.draw_sign(okno)

            # Dialogue lines
            if miranda.interakcja:
                if miranda.f == 4:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(self.font.render(f"{miranda.dialog_lista[miranda.f + 1]}", True,
                                                                "floral white"),
                              (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    # Player
                    okno.blit(self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                                "grey13"),
                              (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 5:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 1]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 2]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                                "grey13"),
                              (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking to Miranda
                elif miranda.f == 6:
                    self.progress = 12  # Changing progress
                    miranda.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    miranda.interakcja = False
                    gracz.licznik = 0

        # Collecting White Spider dust #
        elif self.progress == 12:

            # Sign drawing above looted items
            if game_map.level == "main":
                for pyl in Przeciwnik.loot_przedmioty_fabula_powierzchnia:
                    if abs(pyl[0] - gracz.x) <= 7 and abs(pyl[1] - gracz.y) <= 6:
                        miranda.znak_p += 1
                        if miranda.znak_p % 3 == 0:
                            if miranda.znak_dir == "up":
                                miranda.znak_quest += 1
                            else:
                                miranda.znak_quest -= 1
                        if miranda.znak_p == 30:
                            if miranda.znak_dir == "up":
                                miranda.znak_dir = "down"
                            else:
                                miranda.znak_dir = "up"
                            miranda.znak_p = 0
                        okno.blit(znak, (pyl[0] * rozmiar_pola + 42 + game_map.x,
                                         pyl[1] * rozmiar_pola + 35 - miranda.znak_quest + game_map.y))

            # Collecting dust
            if gracz.licznik >= WHITE_DUST_TO_BE_COLLECTED:
                self.progress = 13 # Changing progress
                gracz.licznik = 0
                Przeciwnik.loot_przedmioty_fabula_powierzchnia.clear()
                Przeciwnik.loot_przedmioty_fabula_podziemia.clear()

        # Coming back to Miranda #
        elif self.progress == 13:

            # Enabling talking with Miranda
            if not miranda.mozliwosc_interakcji:
                miranda.mozliwosc_interakcji = True

            # Drawing sign above Miranda
            miranda.draw_sign(okno)

            # Dialogue lines
            if miranda.interakcja:
                if miranda.f == 6:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 2]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                          "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 7:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 2]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 3]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 4]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                          "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 8:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 4]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 5]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 6]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                          "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif miranda.f == 9:
                    # NPC
                    okno.blit(self.font.render(f"{miranda.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 6]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista[miranda.f + 7]}", True,
                                                          "floral white"),
                        (odswiezanie1 + 30 + 130, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{miranda.dialog_lista_gracz[miranda.f - 1]}", True,
                                                          "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking with Miranda
                elif miranda.f == 10:
                    self.story = 6 # Changing story parameter
                    self.progress = 14 # Changing progress
                    miranda.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    miranda.interakcja = False
                    gracz.licznik = 0

    ### 6 QUEST - Pirate's hideout ##########
    def quest_6(self):

        # Talking to Vane #
        if self.progress == 14:

            # Enabling talking with Vane
            if not vane.mozliwosc_interakcji:
                vane.mozliwosc_interakcji = True

            # Drawing sign above Miranda
            vane.draw_sign(okno)

            # Dialogue lines
            if vane.interakcja:
                if vane.f == 0:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 1]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 2]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif vane.f == 1:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 2]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 3]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking to Vane
                elif vane.f == 2:
                    self.progress = 15 # Changing progress
                    gracz.licznik = [0, 0]
                    vane.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    vane.interakcja = False

        # Killing pirates and corsairs #
        elif self.progress == 15:

            # After hunt
            if gracz.licznik[0] >= PIRATES_TO_BE_KILLED and gracz.licznik[1] >= PIRATES_TO_BE_KILLED:
                self.progress = 16 # Changing progress
                vane.mozliwosc_interakcji = True
                gracz.licznik = 0

        # Returning to Vane #
        elif self.progress == 16:

            # Enabling talking with Vane
            if not vane.mozliwosc_interakcji:
                vane.mozliwosc_interakcji = True

            # Drawing sign above Miranda
            vane.draw_sign(okno)

            # Dialogue lines
            if vane.interakcja:
                if vane.f == 2:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 3]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 4]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif vane.f == 3:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 4]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 5]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif vane.f == 4:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 5]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 6]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 7]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                elif vane.f == 5:
                    # NPC
                    okno.blit(self.font.render(f"{vane.imie}:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 7]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 - 40))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 8]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista[vane.f + 9]}", True, "floral white"),
                        (odswiezanie1 + 110, 885 + 97 - 10 + 40))
                    # Player
                    okno.blit(
                        self.font.render(f"{vane.dialog_lista_gracz[vane.f]}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))
                # After talking to Vane
                elif vane.f == 6:
                    self.progress = 17 # Changing progress
                    self.story = 7 # Changing story parameter
                    vane.mozliwosc_interakcji = False
                    gracz.interakcja = False
                    vane.interakcja = False

    ### 7 QUEST - Dragon battle #############
    def quest_7(self):

        # Entering a portal #
        if self.progress == 17:

            # Teleport to dragon boss area
            if game_map.level == "underground":
                if gracz.x == 87 and gracz.y == 86:
                    game_map.underground_map_jwrpg[gracz.y2][gracz.x2] = 0
                    game_map.level = "boss" # Changing map level
                    self.progress = 18 # Changing progress
                    gracz.licznik = 0
                    gracz.x = 77
                    gracz.x2 = 77
                    gracz.y = 37
                    gracz.y2 = 37
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("dragon_fight.ogg")
                    pygame.mixer.music.play(-1)

        # Killing the dragon #
        elif self.progress == 18:

            # Spawning mobs if 3/4 or less hp and making dragon immune to attacks until all mobs are killed
            if self.dragon_progress == 1:
                if instances.dragon.hp <= 0.75 * instances.dragon.max_hp:
                    Dragon.spawn_enemies(1)
                    instances.dragon.immune = True  # Making dragon immune to attacks
                    self.dragon_progress = 2 # Changing parameter

            # Killing all mobs to cancel dragon's being immune
            elif self.dragon_progress == 2:
                if all(e.status == False for e in Dragon.enemies if type(e) == Przeciwnik):
                    instances.dragon.immune = False # Cancelling being immune
                    self.dragon_progress = 3 # Changing parameter

            # Spawning mobs if 1/2 or less hp and making dragon immune to attacks until all mobs are killed
            elif self.dragon_progress == 3:
                if instances.dragon.hp <= 0.5 * instances.dragon.max_hp:
                    Dragon.spawn_enemies(2)
                    instances.dragon.immune = True  # Making dragon immune to attacks
                    self.dragon_progress = 4 # Changing parameter

            # Killing all mobs to cancel dragon's being immune
            elif self.dragon_progress == 4:
                if all(e.status == False for e in Dragon.enemies if type(e) == Przeciwnik):
                    instances.dragon.immune = False  # Cancelling being immune
                    self.dragon_progress = 5  # Changing parameter

            # Spawning mobs if 1/4 or less hp and making dragon immune to attacks until all mobs are killed
            elif self.dragon_progress == 5:
                if instances.dragon.hp <= 0.25 * instances.dragon.max_hp:
                    Dragon.spawn_enemies(3)
                    instances.dragon.immune = True  # Making dragon immune to attacks
                    self.dragon_progress = 6 # Changing parameter

            # Killing all mobs to cancel dragon's being immune
            elif self.dragon_progress == 6:
                if all(e.status == False for e in Dragon.enemies if type(e) == Przeciwnik):
                    instances.dragon.immune = False  # Cancelling being immune
                    self.dragon_progress = 7  # Changing parameter

            # Killing the dragon
            elif self.dragon_progress == 7:
                if instances.dragon.hp <= 0:
                    self.progress = 19 # Changing progress parameter
                    game_map.underground_map_jwrpg[instances.dragon.dead_y][instances.dragon.dead_x] = 1
                    self.znak_p = 0
                    self.znak_quest = 0
                    self.znak_dir = "up"
                    self.final_line = 0
                    self.czas_ostatniej_interakcji = 0
                    self.predkosc_interakcji = 2

        # When dragon is killed #
        elif self.progress == 19:

            if abs(instances.dragon.dead_x - gracz.x) < 7 and abs(instances.dragon.dead_y - gracz.y) < 6:

                if self.final_line < 2:
                    pygame.draw.rect(okno, "orange", (
                        instances.dragon.dead_x * rozmiar_pola + game_map.x,
                        instances.dragon.dead_y * rozmiar_pola + game_map.y,
                        rozmiar_pola,
                        rozmiar_pola))
                    okno.blit(instances.dragon.tekst_nazwa.render("Pradawny Smok", True, "floral white"),
                              (instances.dragon.dead_x * rozmiar_pola - 39 + game_map.x,
                               instances.dragon.dead_y * rozmiar_pola - 37 + game_map.y))
                    self.znak_p += 1
                    if self.znak_p % 3 == 0:
                        if self.znak_dir == "up":
                            self.znak_quest += 1
                        else:
                            self.znak_quest -= 1
                    if self.znak_p == 30:
                        if self.znak_dir == "up":
                            self.znak_dir = "down"
                        else:
                            self.znak_dir = "up"
                        self.znak_p = 0
                    okno.blit(znak, (instances.dragon.dead_x * rozmiar_pola + 42 + game_map.x,
                                     (instances.dragon.dead_y - 1) * rozmiar_pola + 1 - self.znak_quest + game_map.y))

                przycisk = pygame.key.get_pressed()
                if (przycisk[pygame.K_e] and abs(instances.dragon.dead_x - gracz.x) <= 1 and
                        abs(instances.dragon.dead_y - gracz.y) <= 1):
                    gracz.interakcja = True

            if gracz.interakcja:

                nacisniecie = pygame.mouse.get_pressed()
                self.aktualny_czas_n = pygame.time.get_ticks()
                if nacisniecie[0]:
                    if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                        self.czas_ostatniej_interakcji = self.aktualny_czas_n
                        mysz_x2, mysz_y2 = pygame.mouse.get_pos()
                        if self.final_line < 2:
                            if mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 885 and mysz_y2 <= 982:
                                self.final_line += 1
                            elif mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 982 and mysz_y2 <= 1080:
                                gracz.interakcja = False

                if self.final_line < 2:
                    pygame.draw.rect(okno, "grey13", (odswiezanie1, 885, odswiezanie2, 885 + 97 + 98))
                    pygame.draw.rect(okno, "grey81",
                                     (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885, odswiezanie2, 885 + 97))
                    pygame.draw.rect(okno, "grey28", (
                        szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885 + 97, odswiezanie2, 885 + 97 + 98))
                    okno.blit(instances.vane.tekst_nazwa.render("Zakończ", True, "grey13"),
                              (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 135))

                if self.final_line == 0:
                    # Dragon
                    okno.blit(self.font.render("Pradawny Smok:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{instances.dragon.line_1}", True,
                                         "floral white"), (odswiezanie1 + 30 + 230, 885 + 97 - 10 - 15))
                    okno.blit(
                        self.font.render(f"{instances.dragon.line_2}", True,
                                     "floral white"), (odswiezanie1 + 30 + 230, 885 + 97 - 10 + 25))
                    # Player
                    okno.blit(
                        self.font.render(f"{instances.dragon.player_line_1}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 35))

                elif self.final_line == 1:
                    # Dragon
                    okno.blit(self.font.render("Pradawny Smok:", True, "floral white"),
                              (odswiezanie1 + 30, 885 + 97 - 10))
                    okno.blit(
                        self.font.render(f"{instances.dragon.line_3}", True,
                                         "floral white"), (odswiezanie1 + 30 + 230, 885 + 97 - 10))
                    # Player
                    okno.blit(
                        self.font.render(f"{instances.dragon.player_line_2}", True, "grey13"),
                        (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 30, 885 + 35))

                elif self.final_line == 2:
                    game_map.underground_map_jwrpg[instances.dragon.dead_y][instances.dragon.dead_x] = 0
                    pygame.draw.rect(okno, "black", (323, 450, 1920 - 2 * 323, 140))
                    tekst = gracz.tekst_nie_zyjesz.render("GRATULACJE, UKOŃCZYŁEŚ GRĘ", True, "green")
                    tekst_rect = tekst.get_rect(center=(1920 // 2, 520))
                    okno.blit(tekst, tekst_rect)

    #########################################
    #########################################

    ### Quest flow ###
    def quest_flow(self):

        self.quests[self.story - 1]()
########################################################################################################################