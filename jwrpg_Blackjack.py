### GRA - BLACKJACK ###
import random
import os
import pygame

### ŁADOWANIE WSZYSTKICH OBIEKTÓW I ZMIENNYCH ###
def ladowanie():
    ### Tworzenie słownika przechowującego karty - 0 zostaną zastąpione przez grafiki ###
    cards = {"A_karo": 0, "2_karo": 0, "3_karo": 0, "4_karo": 0, "5_karo": 0, "6_karo": 0, "7_karo": 0, "8_karo": 0,
             "9_karo": 0, "10_karo": 0, "J_karo": 0, "Q_karo": 0, "K_karo": 0,

             "A_kier": 0, "2_kier": 0, "3_kier": 0, "4_kier": 0, "5_kier": 0, "6_kier": 0, "7_kier": 0, "8_kier": 0,
             "9_kier": 0, "10_kier": 0, "J_kier": 0, "Q_kier": 0, "K_kier": 0,

             "A_trefl": 0, "2_trefl": 0, "3_trefl": 0, "4_trefl": 0, "5_trefl": 0, "6_trefl": 0, "7_trefl": 0,
             "8_trefl": 0, "9_trefl": 0, "10_trefl": 0, "J_trefl": 0, "Q_trefl": 0, "K_trefl": 0,

             "A_pik": 0, "2_pik": 0, "3_pik": 0, "4_pik": 0, "5_pik": 0, "6_pik": 0, "7_pik": 0, "8_pik": 0,
             "9_pik": 0, "10_pik": 0, "J_pik": 0, "Q_pik": 0, "K_pik": 0}

    ### Podfunkcja - PRZYPISYWANIE GRAFIK DO WARTOŚCI KLUCZY ###
    def przypisanie_grafik(karty):
        sciezka = os.path.join("tilesets", "karty")
        lista_nazwy_kart = os.listdir(sciezka)
        for nazwa in lista_nazwy_kart:
            karty[nazwa[:-4]] = pygame.image.load(os.path.join(sciezka, nazwa))
        return karty

    ### Wczytywanie obrazów ###
    cards = przypisanie_grafik(cards)

    ### Zmienna początkowa kasa gracza do obstawienia ###
    obstawienie_gracza = None

    ### CZYSZCZENIE/TWORZENIE RĘKI GRACZA I KRUPIERA ###
    gracz_reka = []
    krupier_reka = []

    ### CZYSZCZENIE/TWORZENIE ZMIENNYCH PRZECHOWUJĄCYCH WYNIKI ###
    gracz_wynik = 0
    krupier_wynik = 0

    return cards, obstawienie_gracza, gracz_reka, krupier_reka, gracz_wynik, krupier_wynik

### FUNKCJA LICZĄCA WYNIK KART ###
def liczenie_wyniku(reka: list) -> int:
    wynik = 0
    asy = 0
    for karta in reka:
        if karta[0].isdigit():
            wynik += int(karta[0]) if not karta[1].isdigit() else 10
        elif karta[0] in ["J", "Q", "K"]:
            wynik += 10
        elif karta[0] == "A":
            wynik += 11
            asy += 1
    for _ in range(asy):
        if wynik > 21:
            wynik -= 10
    return wynik

#################################################################################
#### GŁÓWNY PRZEPŁYW GRY ########################################################
def gra(flint, gracz, okno):

    # ŁADOWANIE OBIEKTÓW I ZMIENNYCH
    if flint.f == 1:
        gracz.cards_2 = gracz.cards.copy()
        flint.f = 2

    # OBSTAWIANIE GRY
    elif flint.f == 2:
        okno.blit(flint.tekst_sklep_2.render("Flint: Za jaką kwotę chcesz zagrać?", True, "mint cream"), (670, 285))
        pygame.draw.rect(okno, "grey27", (700, 430, 200, 100))
        okno.blit(flint.tekst_nazwa.render("5 szt. złota", True, "mint cream"), (730, 467))
        pygame.draw.rect(okno, "grey27", (1023, 430, 200, 100))
        okno.blit(flint.tekst_nazwa.render("10 szt. złota", True, "mint cream"), (1046, 467))
        pygame.draw.rect(okno, "grey27", (700, 600, 200, 100))
        okno.blit(flint.tekst_nazwa.render("25 szt. złota", True, "mint cream"), (723, 637))
        pygame.draw.rect(okno, "grey27", (1023, 600, 200, 100))
        okno.blit(flint.tekst_nazwa.render("50 szt. złota", True, "mint cream"), (1046, 637))

        wybor = pygame.mouse.get_pressed()
        gracz.aktualny_czas_n = pygame.time.get_ticks()

        if wybor[0]:
            if gracz.aktualny_czas_n - gracz.czas_ostatniej_interakcji >= 1000 / gracz.predkosc_interakcji:
                gracz.czas_ostatniej_interakcji = gracz.aktualny_czas_n
                mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                # OBSTAWIENIE 5 szt. ZŁOTA
                if mysz_x2 >= 700 and mysz_x2 <= 900 and mysz_y2 >= 430 and mysz_y2 <= 530:
                    gracz.obstawienie_gracza = 5
                    gracz.zloto -= 5
                    flint.f = 3
                # OBSTAWIENIE 10 szt. ZŁOTA
                elif mysz_x2 >= 1023 and mysz_x2 <= 1223 and mysz_y2 >= 430 and mysz_y2 <= 530:
                    gracz.obstawienie_gracza = 10
                    gracz.zloto -= 10
                    flint.f = 3
                # OBSTAWIENIE 25 szt. ZŁOTA
                elif mysz_x2 >= 700 and mysz_x2 <= 900 and mysz_y2 >= 600 and mysz_y2 <= 700:
                    gracz.obstawienie_gracza = 25
                    gracz.zloto -= 25
                    flint.f = 3
                # OBSTAWIENIE 50 szt. ZŁOTA
                elif mysz_x2 >= 1023 and mysz_x2 <= 1223 and mysz_y2 >= 600 and mysz_y2 <= 700:
                    gracz.obstawienie_gracza = 50
                    gracz.zloto -= 50
                    flint.f = 3

    # LOSOWANIE POCZĄTKOWYCH KART #
    elif flint.f == 3:
        ### LOSOWANIE RĘKI GRACZA I LICZENIE WYNIKU ###
        for _ in range(2):
            losowy_index = random.choice(list(gracz.cards_2.keys()))
            gracz.gracz_reka.append(losowy_index)
            gracz.cards_2.pop(losowy_index)
        gracz.gracz_wynik = liczenie_wyniku(gracz.gracz_reka)
        ### LOSOWANIE RĘKI KRUPIERA I LICZENIE WYNIKU ###
        losowy_index = random.choice(list(gracz.cards_2.keys()))
        gracz.krupier_reka.append(losowy_index)
        gracz.cards_2.pop(losowy_index)
        gracz.krupier_wynik = liczenie_wyniku(gracz.krupier_reka)
        flint.f = 4

    # DOBIERANIE KART - ANIMACJA #
    elif flint.f == 4:
        # RYSOWANIE STARTOWEJ RĘKI GRACZA I KRUPIERA #
        gracz.czas_karty += 1
        if gracz.czas_karty > 50:
            okno.blit(gracz.cards[gracz.gracz_reka[0]], (870 + 50 * 0, 680))
        if gracz.czas_karty > 100:
            okno.blit(gracz.cards[gracz.gracz_reka[0]], (870 + 50 * 0, 680))
            okno.blit(gracz.cards[gracz.gracz_reka[1]], (870 + 50 * 1, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
        if gracz.czas_karty > 150:
            okno.blit(gracz.cards[gracz.gracz_reka[0]], (870 + 50 * 0, 680))
            okno.blit(gracz.cards[gracz.gracz_reka[1]], (870 + 50 * 1, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
            okno.blit(gracz.cards_tyl, (870 + 50 * 0, 257))
        if gracz.czas_karty > 200:
            okno.blit(gracz.cards[gracz.gracz_reka[0]], (870 + 50 * 0, 680))
            okno.blit(gracz.cards[gracz.gracz_reka[1]], (870 + 50 * 1, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
            okno.blit(gracz.cards_tyl, (870 + 50 * 0, 257))
            okno.blit(gracz.cards[gracz.krupier_reka[0]], (870 + 50 * 1, 257))
            okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))
            flint.f = 5
            gracz.czas_karty = 0

    # RUCH GRACZA #
    elif flint.f == 5:
        for x, karta in enumerate(gracz.gracz_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
        okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
        okno.blit(gracz.cards_tyl, (870 + 50 * 0, 257))
        okno.blit(gracz.cards[gracz.krupier_reka[0]], (870 + 50 * 1, 257))
        okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))

        if gracz.gracz_wynik < 21:
            pygame.draw.rect(okno, "grey27", (1218, 700, 150, 80))
            okno.blit(flint.tekst_nazwa.render("Karta", True, "mint cream"), (1258, 725))
            pygame.draw.rect(okno, "grey27", (550, 700, 150, 80))
            okno.blit(flint.tekst_nazwa.render("Pas", True, "mint cream"), (600, 725))

        ### Warunek Blackjacka w 2 ruchach ###
        if gracz.gracz_wynik >= 21:
            flint.f = 6

        ### Wybór opcji ###
        wybor = pygame.mouse.get_pressed()
        gracz.aktualny_czas_n = pygame.time.get_ticks()

        if wybor[0]:
            if gracz.aktualny_czas_n - gracz.czas_ostatniej_interakcji >= 1000 / gracz.predkosc_interakcji:
                gracz.czas_ostatniej_interakcji = gracz.aktualny_czas_n
                mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki
                # KARTA
                if mysz_x2 >= 1218 and mysz_x2 <= 1368 and mysz_y2 >= 700 and mysz_y2 <= 780:
                    losowy_index = random.choice(list(gracz.cards_2.keys()))
                    gracz.gracz_reka.append(losowy_index)
                    gracz.cards_2.pop(losowy_index)
                    gracz.gracz_wynik = liczenie_wyniku(gracz.gracz_reka)

                # PAS
                elif mysz_x2 >= 550 and mysz_x2 <= 700 and mysz_y2 >= 700 and mysz_y2 <= 780:
                    flint.f = 6

    # ODSŁONIĘCIE DRUGIEJ KARTY PRZEZ KRUPIERA #
    elif flint.f == 6:
        for x, karta in enumerate(gracz.gracz_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
        okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
        okno.blit(gracz.cards_tyl, (870 + 50 * 0, 257))
        okno.blit(gracz.cards[gracz.krupier_reka[0]], (870 + 50 * 1, 257))
        okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))

        gracz.czas_karty += 1

        if gracz.czas_karty > 50:
            losowy_index = random.choice(list(gracz.cards_2.keys()))
            gracz.krupier_reka.insert(0, losowy_index)
            gracz.cards_2.pop(losowy_index)
            gracz.krupier_wynik = liczenie_wyniku(gracz.krupier_reka)
            gracz.czas_karty = 0
            flint.f = 7
            ### Warunek zakończenia, gdy gracz przekroczył 21 ###
            if gracz.gracz_wynik > 21 or gracz.krupier_wynik > 16:
                flint.f = 10

    # DOBIERANIE KART PRZEZ KRUPIERA cz. 1 - stopuje na >= 17 #
    elif flint.f == 7:
        if gracz.krupier_wynik < 17:
            for x, karta in enumerate(gracz.gracz_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
            for x, karta in enumerate(gracz.krupier_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 257))
            okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))
            gracz.czas_karty += 1
            if gracz.czas_karty > 50:
                losowy_index = random.choice(list(gracz.cards_2.keys()))
                gracz.krupier_reka.append(losowy_index)
                gracz.cards_2.pop(losowy_index)
                gracz.krupier_wynik = liczenie_wyniku(gracz.krupier_reka)
                gracz.czas_karty = 0
                flint.f = 8
                if gracz.krupier_wynik > 16:
                    flint.f = 10
        else:
            flint.f = 10

    # DOBIERANIE KART PRZEZ KRUPIERA cz. 2 - stopuje na >= 17 #
    elif flint.f == 8:
        if gracz.krupier_wynik < 17:
            for x, karta in enumerate(gracz.gracz_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
            for x, karta in enumerate(gracz.krupier_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 257))
            okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))
            gracz.czas_karty += 1
            if gracz.czas_karty > 50:
                losowy_index = random.choice(list(gracz.cards_2.keys()))
                gracz.krupier_reka.append(losowy_index)
                gracz.cards_2.pop(losowy_index)
                gracz.krupier_wynik = liczenie_wyniku(gracz.krupier_reka)
                gracz.czas_karty = 0
                flint.f = 9
                if gracz.krupier_wynik > 16:
                    flint.f = 10
        else:
            flint.f = 10

    # DOBIERANIE KART PRZEZ KRUPIERA cz. 3 - stopuje na >= 17 #
    elif flint.f == 9:
        if gracz.krupier_wynik < 17:
            for x, karta in enumerate(gracz.gracz_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
            okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
            for x, karta in enumerate(gracz.krupier_reka):
                okno.blit(gracz.cards[karta], (870 + 50 * x, 257))
            okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))
            gracz.czas_karty += 1
            if gracz.czas_karty > 50:
                losowy_index = random.choice(list(gracz.cards_2.keys()))
                gracz.krupier_reka.append(losowy_index)
                gracz.cards_2.pop(losowy_index)
                gracz.krupier_wynik = liczenie_wyniku(gracz.krupier_reka)
                gracz.czas_karty = 0
                flint.f = 10
        else:
            flint.f = 10

    ### PODLICZANIE WYNIKU I DODAWANIE KASY W PRZYPADKU WYGRANEJ ###
    elif flint.f == 10:
        for x, karta in enumerate(gracz.gracz_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
        okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
        for x, karta in enumerate(gracz.krupier_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 257))
        okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))

        pygame.draw.rect(okno, "grey27", (1218, 700, 150, 80))
        okno.blit(flint.tekst_nazwa.render("Graj dalej", True, "mint cream"), (1231, 725))
        pygame.draw.rect(okno, "grey27", (550, 700, 150, 80))
        okno.blit(flint.tekst_nazwa.render("Koniec", True, "mint cream"), (580, 725))

        if gracz.gracz_wynik > 21 or (gracz.gracz_wynik < 21 and gracz.gracz_wynik < gracz.krupier_wynik and gracz.krupier_wynik <= 21):
            pass
        elif gracz.gracz_wynik == gracz.krupier_wynik:
            gracz.zloto += gracz.obstawienie_gracza
        else:
            gracz.zloto += 2 * gracz.obstawienie_gracza

        flint.f = 11

    ### WYBÓR CZY KONIEC, CZY GRAĆ DALEJ ###
    elif flint.f == 11:
        for x, karta in enumerate(gracz.gracz_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 680))
        okno.blit(flint.tekst_sklep_2.render(f"{gracz.imie}: {gracz.gracz_wynik}", True, "mint cream"), (856, 620))
        for x, karta in enumerate(gracz.krupier_reka):
            okno.blit(gracz.cards[karta], (870 + 50 * x, 257))
        okno.blit(flint.tekst_sklep_2.render(f"Flint: {gracz.krupier_wynik}", True, "mint cream"), (892, 424))

        pygame.draw.rect(okno, "grey27", (1218, 700, 150, 80))
        okno.blit(flint.tekst_nazwa.render("Graj dalej", True, "mint cream"), (1231, 725))
        pygame.draw.rect(okno, "grey27", (550, 700, 150, 80))
        okno.blit(flint.tekst_nazwa.render("Koniec", True, "mint cream"), (580, 725))

        if gracz.gracz_wynik > 21 or (gracz.gracz_wynik < 21 and gracz.gracz_wynik < gracz.krupier_wynik and gracz.krupier_wynik <= 21):
            okno.blit(flint.tekst_sklep_2.render("Przegrałeś...", True, "orange red"), (865, 524))
        elif gracz.gracz_wynik == gracz.krupier_wynik:
            okno.blit(flint.tekst_sklep_2.render("Remis", True, "orange red"), (895, 524))
        else:
            okno.blit(flint.tekst_sklep_2.render(f"Wygrałeś {gracz.obstawienie_gracza * 2} szt. złota!", True, "green3"), (780, 524))

        ### Wybór opcji ###
        wybor = pygame.mouse.get_pressed()
        gracz.aktualny_czas_n = pygame.time.get_ticks()

        if wybor[0]:
            if gracz.aktualny_czas_n - gracz.czas_ostatniej_interakcji >= 1000 / gracz.predkosc_interakcji:
                gracz.czas_ostatniej_interakcji = gracz.aktualny_czas_n
                mysz_x2, mysz_y2 = pygame.mouse.get_pos()  # Wczytanie do zmiennych pozycji myszki

                # GRAJ DALEJ
                if mysz_x2 >= 1218 and mysz_x2 <= 1368 and mysz_y2 >= 700 and mysz_y2 <= 780:
                    flint.f = 1
                    gracz.cards_2 = gracz.cards.copy()
                    gracz.obstawienie_gracza = 0
                    gracz.gracz_reka.clear()
                    gracz.krupier_reka.clear()
                    gracz.gracz_wynik = 0
                    gracz.krupier_wynik = 0
                    gracz.czas_karty = 0

                # KONIEC
                elif mysz_x2 >= 550 and mysz_x2 <= 700 and mysz_y2 >= 700 and mysz_y2 <= 780:
                    flint.f = 0
                    gracz.interakcja = False
                    flint.interakcja = False
                    gracz.cards_2 = gracz.cards.copy()
                    gracz.obstawienie_gracza = 0
                    gracz.gracz_reka.clear()
                    gracz.krupier_reka.clear()
                    gracz.gracz_wynik = 0
                    gracz.krupier_wynik = 0
                    gracz.czas_karty = 0
#####################################################################################
#####################################################################################