import pygame
from config.MAIN_CONFIG import (REFRESHING_1 as odswiezanie1, REFRESHING_2 as odswiezanie2,
                                DISPLAY_WIDTH as szerokosc_okna)
from instances import gracz
from assets import *
import instances


### Tworzenie klasy - NPC ###
class NPC:

    ### Atrybuty klasy - listy npc ###
    npc_powierzchnia = []
    npc_podziemia = []
    ##################################

    # Inicjalizator
    def __init__(self, x, y, imie, mozliwosc_interakcji, typ, map_lvl, imie_x):
        self.x = x
        self.y = y
        self.imie = imie
        self.kolor = "floral white"
        self.znak_aktywnosci = False
        self.interakcja = False
        self.f = 0 # Parametr do postępowania lini dialogowych, zależny od kliknięć LPM gracza w dialog
        self.mozliwosc_interakcji = mozliwosc_interakcji
        self.typ = typ
        self.map_level = map_lvl

        if self.imie == "Thorne": self.grafika = thorne_grafika_rozszerzona
        elif self.imie == "Torin": self.grafika = torin_grafika_rozszerzona
        elif self.imie == "Garrick": self.grafika = garrick_grafika_rozszerzona
        elif self.imie == "Miranda": self.grafika = miranda_grafika_rozszerzona
        elif self.imie == "Kowal": self.grafika = None
        elif self.imie == "Vane": self.grafika = lista_grafika_pirat_2[1]
        elif self.imie == "Flint": self.grafika = lista_grafika_pirat[1]

        self.imie_x_kalibracja = imie_x
        self.tekst_nazwa = pygame.font.Font(None, 38)
        self.tekst_sklep = pygame.font.Font(None, 55)
        self.tekst_sklep_2 = pygame.font.Font(None, 50)
        self.tekst_kowal = pygame.font.Font(None, 28)
        self.punkty = pygame.font.Font(None, 20)
        self.czas_ostatniej_interakcji = 0
        self.predkosc_interakcji = 2  # 2 razy na sekundę
        self.znak = 100
        self.znak_quest = 110
        self.znak_p = 0
        self.znak_dir = "up"

        ### Dodawanie przeciwników do list klasowych ########
        if self.map_level == "powierzchnia":
            NPC.npc_powierzchnia.append(self)
        else:
            NPC.npc_podziemia.append(self)
        #####################################################

    # Loading NPCs objects - CLASS METHOD #
    def load_npc(cls, npc_main, npc_underground):
        ### MAIN LEVEL - SURFACE ##
        for name, p in npc_main.items():
            NPC(p["x"], p["y"], name, p["mozliwosc_interakcji"], p["typ"], "powierzchnia", p["name_x"])
        ### UNDERGROUND LEVEL ###
        for name, p in npc_underground.items():
            NPC(p["x"], p["y"], name, p["mozliwosc_interakcji"], p["typ"], "podziemia", p["name_x"])
        ### Assign NPC to variables ###
        thorne = [npc for npc in NPC.npc_powierzchnia if npc.imie == "Thorne"][0]
        torin = [npc for npc in NPC.npc_powierzchnia if npc.imie == "Torin"][0]
        garrick = [npc for npc in NPC.npc_powierzchnia if npc.imie == "Garrick"][0]
        miranda = [npc for npc in NPC.npc_powierzchnia if npc.imie == "Miranda"][0]
        kowal = [npc for npc in NPC.npc_powierzchnia if npc.imie == "Kowal"][0]
        vane = [npc for npc in NPC.npc_podziemia if npc.imie == "Vane"][0]
        flint = [npc for npc in NPC.npc_podziemia if npc.imie == "Flint"][0]
        ### Returning variables ###
        return thorne, torin, garrick, miranda, kowal, vane, flint

    # Loading NPCs dialogue lines - CLASS METHOD #
    def load_dialogue_lines(cls):
        thorne, torin, garrick, miranda, kowal, vane, flint = (instances.thorne, instances.torin,
                                                               instances.garrick, instances.miranda,
                                                               instances.kowal, instances.vane, instances.flint)
        # Creating lists for dialogues
        garrick.dialog_lista = []
        garrick.dialog_lista_gracz = []
        torin.dialog_lista = []
        flint.dialog_lista = []
        torin.dialog_lista_gracz = []
        thorne.dialog_lista = []
        thorne.dialog_lista_gracz = []
        flint.dialog_lista_gracz = []
        miranda.dialog_lista = []
        miranda.dialog_lista_gracz = []
        vane.dialog_lista = []
        vane.dialog_lista_gracz = []

        ### PLAYER DIALOGUES ###

        # 1 ZADANIE #################################################
        garrick.dialog_lista_gracz.append("To znaczy?")
        garrick.dialog_lista_gracz.append("Dobra, zajmę się nimi.")
        garrick.dialog_lista_gracz.append("Dzięki.")
        garrick.dialog_lista_gracz.append("Jasne, zajrzę do niego.")
        #############################################################

        # 4 ZADANIE #################################################
        garrick.dialog_lista_gracz.append("Co z nimi?")
        garrick.dialog_lista_gracz.append("Gdzie je znajdę?")
        garrick.dialog_lista_gracz.append("Zajmę się nimi.")
        garrick.dialog_lista_gracz.append("Dzięki.")
        garrick.dialog_lista_gracz.append("Pójdę do niej.")
        #############################################################

        # SKLEP #####################################################
        torin.dialog_lista_gracz.append("Pokaż mi swoje towary.")
        #############################################################

        # 2 ZADANIE #################################################
        thorne.dialog_lista_gracz.append("O co chodzi?")
        thorne.dialog_lista_gracz.append("Gdzie jest ta jaskinia?")
        thorne.dialog_lista_gracz.append("Poszukam go.")

        thorne.dialog_lista_gracz.append("Finn nie żyje.")
        thorne.dialog_lista_gracz.append("Miał przy sobie dziennik.")
        thorne.dialog_lista_gracz.append("Musimy zbadać ten temat.")
        thorne.dialog_lista_gracz.append("I co wtedy?")
        thorne.dialog_lista_gracz.append("Dobrze, tak zrobię.")
        #############################################################

        # 3 ZADANIE #################################################
        miranda.dialog_lista_gracz.append("Skąd o tym wiesz?")
        miranda.dialog_lista_gracz.append("Niech będzie, poczekam.")
        miranda.dialog_lista_gracz.append("Jasne, idę do niego.")
        #############################################################

        # 5 ZADANIE #################################################
        miranda.dialog_lista_gracz.append("To znaczy?")
        miranda.dialog_lista_gracz.append("Niech Ci będzie.")
        miranda.dialog_lista_gracz.append("Co teraz?")
        miranda.dialog_lista_gracz.append("Co mam zrobić?")
        miranda.dialog_lista_gracz.append("Gdzie go szukać?")
        miranda.dialog_lista_gracz.append("Dobra, znajdę go.")
        #############################################################

        # 6 ZADANIE #################################################
        vane.dialog_lista_gracz.append("Pradawna siła?")
        vane.dialog_lista_gracz.append("Dobrze, tak zrobię.")
        vane.dialog_lista_gracz.append("Wróćmy do konkretów.")
        vane.dialog_lista_gracz.append("O kurwa...")
        vane.dialog_lista_gracz.append("Czuję, że jest mi to pisane.")
        vane.dialog_lista_gracz.append("Zrobię to.")

        # BLACKJACK #################################################
        flint.dialog_lista_gracz.append("Zagrajmy.")
        #############################################################

        ### NPC DIALOGUES ###

        # GARRICK

        # 1 ZADANIE ############################################################################
        garrick.dialog_lista.append("Witaj, łowco. Potrzebuję pomocy z polowaniem.")

        garrick.dialog_lista.append("Ostatnimi czasy wilki robią się coraz bardziej agresywne.")
        garrick.dialog_lista.append("Idź na południe do lasu i upoluj 10 z nich.")

        garrick.dialog_lista.append("Dzięki za pomoc, oby teraz było spokojniej.")
        garrick.dialog_lista.append("W nagrodę trzymaj 100 szt. złota.")

        garrick.dialog_lista.append("W wolnej chwili odwiedź Thorne'a. Pytał o Ciebie.")
        garrick.dialog_lista.append("Znajdziesz go na wzniesieniu na zachód od lasu.")
        ########################################################################################

        # 4 ZADANIE ############################################################################
        garrick.dialog_lista.append("Słyszałem co się stało z Finn'em, kiepska sprawa.")
        garrick.dialog_lista.append("Na wyspie zrobiło się niebezpiecznie, jeszcze te dziki...")

        garrick.dialog_lista.append("Ostatnio coraz śmielej podchodzą do wioski.")
        garrick.dialog_lista.append("Trzeba ukrócić to zachowanie. Zabij 15 z nich.")

        garrick.dialog_lista.append("Dziki znajdziesz na wziesieniu na zachód od wioski.")

        garrick.dialog_lista.append("Dobra robota, łowco. Może teraz dziki się uspokoją.")
        garrick.dialog_lista.append("W nagrodę trzymaj 200 szt. złota.")

        garrick.dialog_lista.append("Miranda pytała o Ciebie. Powinieneś ją odwiedzić.")
        ########################################################################################

        ### TORIN ###

        # SKLEP ################################################################################
        torin.dialog_lista.append("Prowadzę sklep, chcesz coś kupić?")
        ########################################################################################

        # THORNE

        # 2 ZADANIE ############################################################################
        thorne.dialog_lista.append("W końcu przyszedłeś. Mam dla Ciebie zadanie.")

        thorne.dialog_lista.append("Mój podwładny Finn udał się do jaskini zapolować na")
        thorne.dialog_lista.append("pająki, lecz długo nie wraca. Sprawdź co z nim.")

        thorne.dialog_lista.append("Wejście znajdziesz na wybrzeżu na południe stąd.")
        thorne.dialog_lista.append("Uważaj na te jebane pająki, pełno ich tam.")

        thorne.dialog_lista.append("I co, znalazłeś go?")

        thorne.dialog_lista.append("O kurwa, a zapowiadał się dobrze...")

        thorne.dialog_lista.append("Wspomina o szeptach... też je chyba kiedyś słyszałem.")
        thorne.dialog_lista.append("Ale myślałem, że po prostu za dużo wypiłem.")

        thorne.dialog_lista.append("Tak, masz rację, musimy się dowiedzieć o co chodzi.")
        thorne.dialog_lista.append("Potrzebujemy dowodów, idź zapolować na pająki i zbierz")
        thorne.dialog_lista.append("z nich 10 porcji pyłu.")

        thorne.dialog_lista.append("Gdy zbierzesz pył, zanieś go do zielarki Mirandy.")
        thorne.dialog_lista.append("Znajdziesz ją w wiosce.")
        ########################################################################################

        # MIRANDA

        # 3 ZADANIE ############################################################################
        miranda.dialog_lista.append("Dzień dobry, łowco. Udało Ci się zebrać pył?")

        miranda.dialog_lista.append("Ja wszystko wiem, zapomniałeś? Ten pył...")
        miranda.dialog_lista.append("Wyczuwam w nim coś dziwnego, lecz potrzebuję")
        miranda.dialog_lista.append("czasu by dokładnie go zbadać. Cierpliwości.")

        miranda.dialog_lista.append("W międzyczasie zajrzyj do Garricka, ma jakiś problem.")
        ########################################################################################

        # 5 ZADANIE ############################################################################
        miranda.dialog_lista.append("Łowco, już prawie... Lecz brakuje nam jednej rzeczy.")
        miranda.dialog_lista.append("Zdobądź 10 szt. pyłu z białych pająków.")
        miranda.dialog_lista.append("Znajdziesz je na wybrzeżu na zachód od wioski.")

        miranda.dialog_lista.append("Tak... mamy już wszystko...")

        miranda.dialog_lista.append("Ten pył... skrywa w sobie starożytną moc.")
        miranda.dialog_lista.append("Wydaje mi się, że piraci mogą coś wiedzieć. Ponoć ")
        miranda.dialog_lista.append("eksperymentują oni ostatnio z dziwnymi substancjami.")

        miranda.dialog_lista.append("Odnajdź ich przywódcę, Vane'a, i porozmawiaj z nim.")
        miranda.dialog_lista.append("Dotarcie do niego nie będzie jednak łatwe.")
        miranda.dialog_lista.append("Będziesz musiał się przebić przez jego załogę.")

        miranda.dialog_lista.append("Kryjówkę piratów znajdziesz w podziemiach, szukaj")
        miranda.dialog_lista.append("wejścia w północno-zachodniej części wyspy na plaży.")
        ########################################################################################

        # VANE

        # 6 ZADANIE ############################################################################
        vane.dialog_lista.append("Dłużej się nie dało? Słyszałem, że badasz sprawę pyłu.")
        vane.dialog_lista.append("Pył to tylko wierzchołek góry lodowej, na wyspie przebudziła")
        vane.dialog_lista.append("się pradawna siła, która kiedyś władała tą wyspą...")

        vane.dialog_lista.append("Jeśli chcesz poznać całą prawdę, będziesz musiał udowodnić")
        vane.dialog_lista.append("swoją wartość. Pokaż, że poradzisz sobie z moimi ludźmi.")

        vane.dialog_lista.append("Posłałeś kilku do piachu, imponujące. Najwidoczniej nie")
        vane.dialog_lista.append("nadawali się by walczyć u mego boku, więc jebać ich.")

        vane.dialog_lista.append("Ta pradawna siła... Udało nam się ustalić, że to istota")
        vane.dialog_lista.append("z innego wymiaru, a konkretniej jebany starożytny smok.")

        vane.dialog_lista.append("Dobrze powiedziane... Legenda głosi, że tylko wybraniec")
        vane.dialog_lista.append("jest w stanie go pokonać. Ja to pierdole, życie mi miłe,")
        vane.dialog_lista.append("ale Ty? Musisz spróbować, wyczuwam w Tobie potencjał.")

        vane.dialog_lista.append("To się okaże... Przygotuj się dobrze, bo nie będzie odwrotu.")
        vane.dialog_lista.append("Gdy będziesz gotowy, udaj się tunelem na południe. Na jego")
        vane.dialog_lista.append("końcu jest portal. Wejdź w niego i... zostań legendą.")
        ########################################################################################

        # FLINT

        # BLACKJACK ############################################################################
        flint.dialog_lista.append("Chcesz zagrać w Blackjacka? Jeśli nie, to wypad.")
        ########################################################################################

    # Funkcja rysowanie NPC
    def rysowanie_npc(self, mapa_x, mapa_y, okno):
        if abs(self.x - gracz.x) < 7 and abs(self.y - gracz.y) < 6:
            if self.imie == "Kowal":
                ...
            elif self.imie == "Flint" or self.imie == "Vane":
                okno.blit(self.grafika, (self.x * rozmiar_pola + mapa_x, self.y * rozmiar_pola + mapa_y - 10))
                okno.blit(self.tekst_nazwa.render(self.imie, True, (255, 255, 255)), (self.x * rozmiar_pola + self.imie_x_kalibracja + mapa_x, self.y * rozmiar_pola - 30 + mapa_y))
            else:
                okno.blit(self.grafika, (self.x * rozmiar_pola + mapa_x, self.y * rozmiar_pola + mapa_y))
                okno.blit(self.tekst_nazwa.render(self.imie, True, (255, 255, 255)), (self.x * rozmiar_pola +  self.imie_x_kalibracja + mapa_x, self.y * rozmiar_pola - 30 + mapa_y))
            if self.imie == "Torin" or self.imie == "Flint" or self.imie == "Kowal":
                self.znak_p += 1
                if self.znak_p % 3 == 0:
                    if self.znak_dir == "up":
                        self.znak += 1
                    else:
                        self.znak -= 1
                if self.znak_p == 30:
                    if self.znak_dir == "up":
                        self.znak_dir = "down"
                    else:
                        self.znak_dir = "up"
                    self.znak_p = 0
                if self.imie == "Kowal":
                    okno.blit(znak_ulepszenie, (self.x * rozmiar_pola + mapa_x + 25, self.y * rozmiar_pola + mapa_y - self.znak + 40))
                else:
                    okno.blit(znak_sklep, (self.x * rozmiar_pola + mapa_x + 10, self.y * rozmiar_pola + mapa_y - self.znak))

    # NEW - Funkcja rysowanie okna dialogowego, ui sklep, ui kowal
    def rysowanie_okna_dialogowego_sklepu_kowala_blackjacka_NEW(self, okno):
        if self.interakcja == True:

            ### BLACKJACK ###
            if self.typ == "BLACKJACK":

                if self.f == 0:
                    # Rysowanie okna dialogowego
                    pygame.draw.rect(okno, "grey13", (odswiezanie1, 885, odswiezanie2, 195))
                    # Rysowanie przycisków wyboru
                    pygame.draw.rect(okno, "grey81",
                                     (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885, odswiezanie2, 97))
                    pygame.draw.rect(okno, "grey28",
                                     (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885 + 97, odswiezanie2, 98))
                    okno.blit(self.tekst_nazwa.render("Nie", True, "grey13"),
                              (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 135))
                    # Dialog NPC
                    okno.blit(
                        pygame.font.Font(None, 38).render(f"{self.imie}: {self.dialog_lista[0]}", True, "floral white"),
                        (353, 972))
                    # Dialog gracza
                    okno.blit(pygame.font.Font(None, 38).render(f"{self.dialog_lista_gracz[0]}", True, "grey13"),
                              (1225, 920))
                elif self.f > 0:
                    ### RYSOWANIE TŁA ###
                    pygame.draw.rect(okno, "dimgrey", (odswiezanie1 + 150, 150, odswiezanie2 - 300, 1080 - 300))
                    pygame.draw.rect(okno, "grey13", (odswiezanie1 + 200, 200, odswiezanie2 - 400, 1080 - 400))


            ### SKLEP ###
            elif self.typ == "SKLEP":
                ### SKLEP OKNO DIALOGOWE WSTĘPNE ###
                if self.f == 0:
                    # Rysowanie okna dialogowego
                    pygame.draw.rect(okno, "grey13", (odswiezanie1, 885, odswiezanie2, 195))
                    # Rysowanie przycisków wyboru
                    pygame.draw.rect(okno, "grey81",
                                     (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885, odswiezanie2, 97))
                    pygame.draw.rect(okno, "grey28",
                                     (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885 + 97, odswiezanie2, 98))
                    okno.blit(self.tekst_nazwa.render("Nie", True, "grey13"),
                              (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 135))
                    # Dialog NPC
                    okno.blit(
                        pygame.font.Font(None, 38).render(f"{self.imie}: {self.dialog_lista[0]}", True, "floral white"),
                        (353, 972))
                    # Dialog gracza
                    okno.blit(pygame.font.Font(None, 38).render(f"{self.dialog_lista_gracz[0]}", True, "grey13"),
                              (1225, 920))
                ### RYSOWANIE SKLEPU ###
                elif self.f == 1:
                    pygame.draw.rect(okno, "dimgrey", (odswiezanie1 + 150, 150, odswiezanie2 - 300, 1080 - 300))
                    pygame.draw.rect(okno, "grey13", (odswiezanie1 + 200, 200, odswiezanie2 - 400, 1080 - 400))
                    okno.blit(self.tekst_sklep.render("SKLEP", True, "floral white"),
                              (810 + 85, 540 - 350 + 30))
                    okno.blit(hp_potion, (odswiezanie1 + 350, 325))
                    okno.blit(self.tekst_sklep_2.render("x5,  Cena: 25", True, "floral white"),
                              (odswiezanie1 + 470, 360))
                    okno.blit(mp_potion, (odswiezanie1 + 350, 450))
                    okno.blit(self.tekst_sklep_2.render("x5,  Cena: 25", True, "floral white"),
                              (odswiezanie1 + 470, 485))
                    okno.blit(strzala, (odswiezanie1 + 350, 575))
                    okno.blit(strzala, (odswiezanie1 + 330, 575))
                    okno.blit(strzala, (odswiezanie1 + 370, 575))
                    okno.blit(self.tekst_sklep_2.render("x50, Cena: 50", True, "floral white"),
                              (odswiezanie1 + 470, 610))
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 720, 335, 200, 80))
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 720, 460, 200, 80))
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 720, 585, 200, 80))
                    okno.blit(self.tekst_sklep_2.render("KUP", True, "floral white"),
                              (odswiezanie1 + 720 + 60, 360))
                    okno.blit(self.tekst_sklep_2.render("KUP", True, "floral white"),
                              (odswiezanie1 + 720 + 60, 485))
                    okno.blit(self.tekst_sklep_2.render("KUP", True, "floral white"),
                              (odswiezanie1 + 720 + 60, 610))

                    pygame.draw.rect(okno, "grey27", (760, 540 + 200, 400, 100))
                    okno.blit(self.tekst_sklep_2.render("ZAKOŃCZ", True, "floral white"),
                              (810 + 70, 540 + 200 + 30, 300, 100))

            ### KOWAL ###
            elif self.typ == "KOWAL":
                pygame.draw.rect(okno, "dimgrey", (odswiezanie1 + 150, 150, odswiezanie2 - 300, 1080 - 300))
                pygame.draw.rect(okno, "grey13", (odswiezanie1 + 200, 200, odswiezanie2 - 400, 1080 - 400))
                okno.blit(self.tekst_sklep.render("ULEPSZENIA", True, "floral white"),
                          (840 , 540 - 350 + 30))
                okno.blit(self.punkty.render(f"Punkty ulepszeń: {gracz.punkty_ulepszen}", True, "floral white"),
                          (900, 540 - 305 + 30))
                pygame.draw.rect(okno, "grey27", (760, 540 + 200, 400, 100))
                okno.blit(self.tekst_sklep_2.render("ZAKOŃCZ", True, "floral white"),
                          (810 + 70, 540 + 200 + 30, 300, 100))
                # Nazwy
                okno.blit(self.tekst_nazwa.render("Miecz", True, "floral white"),
                          (odswiezanie1 + 270, 310))
                okno.blit(self.tekst_nazwa.render("Łuk", True, "floral white"),
                          (odswiezanie1 + 270, 400))
                okno.blit(self.tekst_nazwa.render("Pancerz", True, "floral white"),
                            (odswiezanie1 + 270, 490))
                okno.blit(self.tekst_nazwa.render("Peleryna", True, "floral white"),
                          (odswiezanie1 + 270, 580))
                okno.blit(self.tekst_nazwa.render("Buty", True, "floral white"),
                          (odswiezanie1 + 270, 670))
                # Aktualny poziom
                okno.blit(self.tekst_kowal.render(f"Aktualny poziom: {gracz.miecz_poziom}, {gracz.miecz_staty[gracz.miecz_poziom]['dmg']} dmg, {gracz.miecz_staty[gracz.miecz_poziom]['crit']}% crit", True, "floral white"),
                          (odswiezanie1 + 410, 310))
                okno.blit(self.tekst_kowal.render(f"Aktualny poziom: {gracz.luk_poziom}, {gracz.luk_staty[gracz.luk_poziom]['dmg']} dmg, {gracz.luk_staty[gracz.luk_poziom]['crit']}% crit", True, "floral white"),
                          (odswiezanie1 + 410, 400))
                okno.blit(self.tekst_kowal.render(f"Aktualny poziom: {gracz.zbroja_poziom}, +{gracz.zbroja_staty[gracz.zbroja_poziom]['hp']} hp", True, "floral white"),
                      (odswiezanie1 + 410, 490))
                okno.blit(self.tekst_kowal.render(f"Aktualny poziom: {gracz.plaszcz_poziom}, +{gracz.plaszcz_staty[gracz.plaszcz_poziom]['mp']} mp", True, "floral white"),
                          (odswiezanie1 + 410, 580))
                okno.blit(self.tekst_kowal.render(f"Aktualny poziom: {gracz.buty_poziom}, +{gracz.buty_staty[gracz.buty_poziom]['info']} speed", True, "floral white"),
                          (odswiezanie1 + 410, 670))
                # Ulepszenie
                if gracz.miecz_staty.get(gracz.miecz_poziom + 1):
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 770, 280, 280, 80))
                    okno.blit(self.tekst_kowal.render(f"Poziom: {gracz.miecz_poziom + 1}, {gracz.miecz_staty[gracz.miecz_poziom + 1]['dmg']} dmg, {gracz.miecz_staty[gracz.miecz_poziom + 1]['crit']}% crit", True, "floral white"),
                              (odswiezanie1 + 790, 290))
                    okno.blit(self.tekst_kowal.render(f"ULEPSZ --> {gracz.miecz_staty[gracz.miecz_poziom + 1]['points']} punkty", True, "floral white"),
                              (odswiezanie1 + 820, 330))
                if gracz.luk_staty.get(gracz.luk_poziom + 1):
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 770, 370, 280, 80))
                    okno.blit(self.tekst_kowal.render(f"Poziom: {gracz.luk_poziom + 1}, {gracz.luk_staty[gracz.luk_poziom + 1]['dmg']} dmg, {gracz.luk_staty[gracz.luk_poziom + 1]['crit']}% crit", True, "floral white"),
                              (odswiezanie1 + 790, 380))
                    okno.blit(self.tekst_kowal.render(f"ULEPSZ --> {gracz.luk_staty[gracz.luk_poziom + 1]['points']} punkty", True, "floral white"),
                              (odswiezanie1 + 820, 420))
                if gracz.zbroja_staty.get(gracz.zbroja_poziom + 1):
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 770, 460, 280, 80))
                    okno.blit(self.tekst_kowal.render(f"Poziom: {gracz.zbroja_poziom + 1}, +{gracz.zbroja_staty[gracz.zbroja_poziom + 1]['hp']} hp", True, "floral white"),
                              (odswiezanie1 + 820, 470))
                    okno.blit(self.tekst_kowal.render(f"ULEPSZ --> {gracz.zbroja_staty[gracz.zbroja_poziom + 1]['points']} punkty", True, "floral white"),
                              (odswiezanie1 + 820, 510))
                if gracz.plaszcz_staty.get(gracz.plaszcz_poziom + 1):
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 770, 550, 280, 80))
                    okno.blit(self.tekst_kowal.render(f"Poziom: {gracz.plaszcz_poziom + 1}, +{gracz.plaszcz_staty[gracz.plaszcz_poziom + 1]['mp']} mp", True, "floral white"),
                              (odswiezanie1 + 820, 560))
                    okno.blit(self.tekst_kowal.render(f"ULEPSZ --> {gracz.plaszcz_staty[gracz.plaszcz_poziom + 1]['points']} punkty", True, "floral white"),
                              (odswiezanie1 + 820, 600))
                if gracz.buty_staty.get(gracz.buty_poziom + 1):
                    pygame.draw.rect(okno, "grey27", (odswiezanie1 + 770, 640, 280, 80))
                    okno.blit(self.tekst_kowal.render(f"Poziom: {gracz.buty_poziom + 1}, +{gracz.buty_staty[gracz.buty_poziom + 1]['info']} speed", True, "floral white"),
                              (odswiezanie1 + 820, 650))
                    okno.blit(self.tekst_kowal.render(f"ULEPSZ --> {gracz.buty_staty[gracz.buty_poziom + 1]['points']} punkty", True, "floral white"),
                              (odswiezanie1 + 820, 690))

            ### RESZTA NPC ###
            else:
                # Rysowanie okna dialogowego
                pygame.draw.rect(okno, "grey13", (odswiezanie1, 885, odswiezanie2, 885 + 97 + 98))
                # Rysowanie przycisków wyboru
                pygame.draw.rect(okno, "grey81",
                                 (szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885, odswiezanie2, 885 + 97))
                pygame.draw.rect(okno, "grey28", (
                szerokosc_okna / 2 + 2.5 * rozmiar_pola, 885 + 97, odswiezanie2, 885 + 97 + 98))
                okno.blit(self.tekst_nazwa.render("Zakończ", True, "grey13"),
                          (szerokosc_okna / 2 + 2.5 * rozmiar_pola + 20, 885 + 135))

    # NEW - wybór opcji dialogowych
    def wybor_opcji(self):
        if self.interakcja == True:
            nacisniecie = pygame.mouse.get_pressed()
            self.aktualny_czas_n = pygame.time.get_ticks()

            ### POSTĘPOWANIE DIALOGÓW FABULARNYCH
            if self.typ == "NPC":
                if nacisniecie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
                    if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                        self.czas_ostatniej_interakcji = self.aktualny_czas_n
                        mysz_x2, mysz_y2 = pygame.mouse.get_pos() # Wczytanie do zmiennych pozycji myszki
                        # Warunek górny przycisk
                        if mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 885 and mysz_y2 <= 982:
                            self.f += 1
                        # Warunek dolny przycisk - WYJŚCIE
                        elif mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 982 and mysz_y2 <= 1080:
                            self.interakcja = False
                            gracz.interakcja = False

            ### BLACKJACK ###
            elif self.typ == "BLACKJACK":
                ### Wstępny dialog ###
                if self.f == 0:
                    if nacisniecie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
                        if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                            self.czas_ostatniej_interakcji = self.aktualny_czas_n
                            mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                            # Warunek górny przycisk
                            if mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 885 and mysz_y2 <= 982:
                                self.f += 1
                            # Warunek dolny przycisk - WYJŚCIE
                            elif mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 982 and mysz_y2 <= 1080:
                                self.interakcja = False
                                gracz.interakcja = False

            ### SKLEP ###
            elif self.typ == "SKLEP":
                ### Wstępny dialog ###
                if self.f == 0:
                    if nacisniecie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
                        if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                            self.czas_ostatniej_interakcji = self.aktualny_czas_n
                            mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                            # Warunek górny przycisk
                            if mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 885 and mysz_y2 <= 982:
                                self.f += 1
                            # Warunek dolny przycisk - WYJŚCIE
                            elif mysz_x2 >= 1205 and mysz_x2 <= 1597 and mysz_y2 >= 982 and mysz_y2 <= 1080:
                                self.interakcja = False
                                gracz.interakcja = False
                ### Kupowanie ###
                elif self.f == 1:
                    if nacisniecie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
                        if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                            self.czas_ostatniej_interakcji = self.aktualny_czas_n
                            mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                            # Warunek 1 przycisk KUP - 5x hp potion
                            if mysz_x2 >= 1043 and mysz_x2 <= 1243 and mysz_y2 >= 335 and mysz_y2 <= 415:
                                if gracz.zloto >= 25:
                                    gracz.hp_potion += 5
                                    gracz.zloto -= 25
                            # Warunek 2 przycisk KUP - 5x mp potion
                            elif mysz_x2 >= 1043 and mysz_x2 <= 1243 and mysz_y2 >= 460 and mysz_y2 <= 540:
                                if gracz.zloto >= 25:
                                    gracz.mp_potion += 5
                                    gracz.zloto -= 25
                            # Warunek 3 przycisk KUP - 50x strzałą
                            elif mysz_x2 >= 1043 and mysz_x2 <= 1243 and mysz_y2 >= 585 and mysz_y2 <= 665:
                                if gracz.zloto >= 50:
                                    gracz.ilosc_strzal += 50
                                    gracz.zloto -= 50
                            # Warunek dolny przycisk - WYJŚCIE
                            elif mysz_x2 >= 760 and mysz_x2 <= 1160 and mysz_y2 >= 740 and mysz_y2 <= 840:
                                self.f = 0
                                self.interakcja = False
                                gracz.interakcja = False

            ### KOWAL - ULEPSZENIA ###
            elif self.typ == "KOWAL":
                if nacisniecie[0]:  # Sprawdzenie naciśnięcia lewego klawisza myszy
                    if self.aktualny_czas_n - self.czas_ostatniej_interakcji >= 1000 / self.predkosc_interakcji:
                        self.czas_ostatniej_interakcji = self.aktualny_czas_n
                        mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                        # SWORD
                        if mysz_x2 >= 1093 and mysz_x2 <= 1373 and mysz_y2 >= 280 and mysz_y2 <= 360:
                            gracz.upgrade_item("sword")
                        # BOW
                        elif mysz_x2 >= 1093 and mysz_x2 <= 1373 and mysz_y2 >= 370 and mysz_y2 <= 450:
                            gracz.upgrade_item("bow")
                        # ARMOR
                        elif mysz_x2 >= 1093 and mysz_x2 <= 1373 and mysz_y2 >= 460 and mysz_y2 <= 540:
                            gracz.upgrade_item("armor")
                        # CAPE
                        elif mysz_x2 >= 1093 and mysz_x2 <= 1373 and mysz_y2 >= 550 and mysz_y2 <= 630:
                            gracz.upgrade_item("cape")
                        # BOOTS
                        elif mysz_x2 >= 1093 and mysz_x2 <= 1373 and mysz_y2 >= 640 and mysz_y2 <= 720:
                            gracz.upgrade_item("boots")
                        # Warunek dolny przycisk - WYJŚCIE
                        elif mysz_x2 >= 760 and mysz_x2 <= 1160 and mysz_y2 >= 740 and mysz_y2 <= 840:
                            self.interakcja = False
                            gracz.interakcja = False

    # Funkcja zwracajaca slownik z parametrami fabuly NPC do zapisu - CLASS METHOD
    def slownik_parametry_npc_save(cls):
        npc_d = {"Thorne": instances.thorne.f,
                 "Garrick": instances.garrick.f,
                 "Miranda": instances.miranda.f,
                 "Vane": instances.vane.f}
        return npc_d

    # Funkcja ładująca parametry NPC z SAVE - CLASS METHOD
    def load_save(cls, save):
        for npc_name, f in save.items():
            for npc in NPC.npc_powierzchnia + NPC.npc_podziemia:
                if npc.imie == npc_name:
                    npc.f = f
                    break

    # New game - resets NPCs #
    @classmethod
    def new_game(cls):
        for npc in cls.npc_powierzchnia + cls.npc_podziemia:
            npc.f = 0
            npc.interakcja = False

    # Function draws sign above NPC #
    def draw_sign(self, window):
        if abs(self.x - gracz.x) <= 7 and abs(self.y - gracz.y) <= 6:
            if (instances.game_map.level == "main" and self.map_level == "powierzchnia" or
                instances.game_map.level == "underground" and self.map_level == "podziemia"):
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
                window.blit(znak, (self.x * rozmiar_pola + 42 + instances.game_map.x,
                                 self.y * rozmiar_pola + 15 - self.znak_quest + instances.game_map.y))