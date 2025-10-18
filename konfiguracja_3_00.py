import pygame
import json
import os
from pytmx import load_pygame

############################################################################
### Funkcja przypisująca zmiennym obrazy TMX - zwraca zmienne z obrazami ###
def ladowanie_obrazow(mapa_tmx, rozmiar_pola):

    try:

        ###############################################
        # Ładowanie grafiki z logo
        logo = pygame.image.load("logo.png")
        # Ładowanie grafiki znaku żółtego wykrzyknika
        znak = pygame.image.load("znak.png")
        # Ładowanie obrazu tła menu
        tlo_menu = pygame.image.load("background.jpg")
        # Ładowanie grafiki HP potion
        hp_potion = mapa_tmx.get_tile_image(19, 7, 5)
        original_rect = hp_potion.get_rect()
        hp_potion2 = pygame.transform.scale(hp_potion, (original_rect.width * rozmiar_pola / 62,
                                                        original_rect.height * rozmiar_pola / 62))
        hp_potion = pygame.transform.scale(hp_potion, (original_rect.width * rozmiar_pola / 32,
                                                       original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafiki MP potion
        mp_potion = mapa_tmx.get_tile_image(20, 7, 5)
        original_rect = mp_potion.get_rect()
        mp_potion2 = pygame.transform.scale(mp_potion, (original_rect.width * rozmiar_pola / 62,
                                                        original_rect.height * rozmiar_pola / 62))
        mp_potion = pygame.transform.scale(mp_potion, (original_rect.width * rozmiar_pola / 32,
                                                       original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafiki MIECZ
        miecz = mapa_tmx.get_tile_image(21, 2, 5)
        original_rect = miecz.get_rect()
        miecz = pygame.transform.scale(miecz, (original_rect.width * rozmiar_pola / 42,
                                               original_rect.height * rozmiar_pola / 42))
        # Ładowanie grafiki ŁUK
        luk = mapa_tmx.get_tile_image(20, 3, 5)
        original_rect = luk.get_rect()
        luk = pygame.transform.scale(luk, (original_rect.width * rozmiar_pola / 42,
                                           original_rect.height * rozmiar_pola / 42))
        # Ładowanie grafiki STRZAŁA
        strzala = mapa_tmx.get_tile_image(1, 1, 5)
        original_rect = strzala.get_rect()
        strzala2 = pygame.transform.scale(strzala, (original_rect.width * rozmiar_pola / 62,
                                                    original_rect.height * rozmiar_pola / 62))
        strzala = pygame.transform.scale(strzala, (original_rect.width * rozmiar_pola / 32,
                                                   original_rect.height * rozmiar_pola / 32))
        strzala_animacja = mapa_tmx.get_tile_image(1, 2, 5)
        original_rect = strzala_animacja.get_rect()
        strzala_animacja = pygame.transform.scale(strzala_animacja, (original_rect.width * rozmiar_pola / 32,
                                                                     original_rect.height * rozmiar_pola / 32))
        # Ładowanie znacznik sklepu
        znak_sklep = mapa_tmx.get_tile_image(5, 1, 5)
        original_rect = znak_sklep.get_rect()
        znak_sklep = pygame.transform.scale(znak_sklep, (original_rect.width * rozmiar_pola / 42,
                                                         original_rect.height * rozmiar_pola / 42))
        # Ładowanie grafiki OGNISTA STRZAŁA
        ognista_strzala = mapa_tmx.get_tile_image(2, 2, 5)
        original_rect = ognista_strzala.get_rect()
        ognista_strzala = pygame.transform.scale(ognista_strzala, (original_rect.width * rozmiar_pola / 32,
                                                                   original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafiki LOOT
        loot_grafika = mapa_tmx.get_tile_image(17, 5, 5)
        original_rect = loot_grafika.get_rect()
        loot_grafika = pygame.transform.scale(loot_grafika, (original_rect.width * rozmiar_pola / 32,
                                                             original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafiki KAMIEN
        kamien = mapa_tmx.get_tile_image(16, 5, 5)
        original_rect = kamien.get_rect()
        kamien = pygame.transform.scale(kamien, (original_rect.width * rozmiar_pola / 32,
                                                 original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafiki CIAŁO
        cialo = mapa_tmx.get_tile_image(5, 2, 5)
        original_rect = cialo.get_rect()
        cialo = pygame.transform.scale(cialo,(original_rect.width * rozmiar_pola / 37,
                                              original_rect.height * rozmiar_pola / 37))

    ########################################################################################################################

        # Ładowanie grafik wilka - lista przechowująca 4 grafiki wilka - idle + listy ruchu
        lista_grafika_wilk_w = [mapa_tmx.get_tile_image(1 + x, 95, 5) for x in range(6)]
        lista_grafika_wilk_s = [mapa_tmx.get_tile_image(1 + x, 96, 5) for x in range(6)]
        lista_grafika_wilk_a = [mapa_tmx.get_tile_image(1 + x, 97, 5) for x in range(6)]
        lista_grafika_wilk_d = [mapa_tmx.get_tile_image(1 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_wilk_w):
            original_rect = g.get_rect()
            lista_grafika_wilk_w[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_wilk_s):
            original_rect = g.get_rect()
            lista_grafika_wilk_s[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_wilk_a):
            original_rect = g.get_rect()
            lista_grafika_wilk_a[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_wilk_d):
            original_rect = g.get_rect()
            lista_grafika_wilk_d[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))

        lista_grafika_wilk = [mapa_tmx.get_tile_image(4, 92, 5), mapa_tmx.get_tile_image(4, 93, 5),
                              mapa_tmx.get_tile_image(3, 93, 5), mapa_tmx.get_tile_image(5, 93, 5)]
        for g in range(0, len(lista_grafika_wilk)):
            original_rect = lista_grafika_wilk[g].get_rect()
            lista_grafika_wilk[g] = pygame.transform.scale(lista_grafika_wilk[g],
                            (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik pająka - lista przechowująca 4 grafiki pająka - idle + listy ruchu
        lista_grafika_pajak_w = [mapa_tmx.get_tile_image(8 + x, 95, 5) for x in range(6)]
        lista_grafika_pajak_s = [mapa_tmx.get_tile_image(8 + x, 96, 5) for x in range(6)]
        lista_grafika_pajak_a = [mapa_tmx.get_tile_image(8 + x, 97, 5) for x in range(6)]
        lista_grafika_pajak_d = [mapa_tmx.get_tile_image(8 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_pajak_w):
            original_rect = g.get_rect()
            lista_grafika_pajak_w[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                  original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pajak_s):
            original_rect = g.get_rect()
            lista_grafika_pajak_s[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                  original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pajak_a):
            original_rect = g.get_rect()
            lista_grafika_pajak_a[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                  original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pajak_d):
            original_rect = g.get_rect()
            lista_grafika_pajak_d[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                  original_rect.height * rozmiar_pola / 32))

        lista_grafika_pajak = [mapa_tmx.get_tile_image(11, 92, 5), mapa_tmx.get_tile_image(11, 93, 5),
                               mapa_tmx.get_tile_image(10, 93, 5), mapa_tmx.get_tile_image(12, 93, 5)]
        for g in range(0, len(lista_grafika_pajak)):
            original_rect = lista_grafika_pajak[g].get_rect()
            lista_grafika_pajak[g] = pygame.transform.scale(lista_grafika_pajak[g],
                            (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik białego pająka - idle + listy ruchu
        lista_grafika_bialy_pajak_w = [mapa_tmx.get_tile_image(15 + x, 95, 5) for x in range(6)]
        lista_grafika_bialy_pajak_s = [mapa_tmx.get_tile_image(15 + x, 96, 5) for x in range(6)]
        lista_grafika_bialy_pajak_a = [mapa_tmx.get_tile_image(15 + x, 97, 5) for x in range(6)]
        lista_grafika_bialy_pajak_d = [mapa_tmx.get_tile_image(15 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_bialy_pajak_w):
            original_rect = g.get_rect()
            lista_grafika_bialy_pajak_w[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                        original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_bialy_pajak_s):
            original_rect = g.get_rect()
            lista_grafika_bialy_pajak_s[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                        original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_bialy_pajak_a):
            original_rect = g.get_rect()
            lista_grafika_bialy_pajak_a[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                        original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_bialy_pajak_d):
            original_rect = g.get_rect()
            lista_grafika_bialy_pajak_d[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                        original_rect.height * rozmiar_pola / 32))

        lista_grafika_bialy_pajak = [mapa_tmx.get_tile_image(18, 92, 5), mapa_tmx.get_tile_image(18, 93, 5),
                                     mapa_tmx.get_tile_image(17, 93, 5), mapa_tmx.get_tile_image(19, 93, 5)]
        for g in range(0, len(lista_grafika_bialy_pajak)):
            original_rect = lista_grafika_bialy_pajak[g].get_rect()
            lista_grafika_bialy_pajak[g] = pygame.transform.scale(lista_grafika_bialy_pajak[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik dzika - idle + listy ruchu
        lista_grafika_dzik_w = [mapa_tmx.get_tile_image(22 + x, 95, 5) for x in range(6)]
        lista_grafika_dzik_s = [mapa_tmx.get_tile_image(22 + x, 96, 5) for x in range(6)]
        lista_grafika_dzik_a = [mapa_tmx.get_tile_image(22 + x, 97, 5) for x in range(6)]
        lista_grafika_dzik_d = [mapa_tmx.get_tile_image(22 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_dzik_w):
            original_rect = g.get_rect()
            lista_grafika_dzik_w[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_dzik_s):
            original_rect = g.get_rect()
            lista_grafika_dzik_s[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_dzik_a):
            original_rect = g.get_rect()
            lista_grafika_dzik_a[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_dzik_d):
            original_rect = g.get_rect()
            lista_grafika_dzik_d[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                                 original_rect.height * rozmiar_pola / 32))

        lista_grafika_dzik = [mapa_tmx.get_tile_image(25, 92, 5), mapa_tmx.get_tile_image(25, 93, 5),
                              mapa_tmx.get_tile_image(24, 93, 5), mapa_tmx.get_tile_image(26, 93, 5)]
        for g in range(0, len(lista_grafika_dzik)):
            original_rect = lista_grafika_dzik[g].get_rect()
            lista_grafika_dzik[g] = pygame.transform.scale(lista_grafika_dzik[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik zająca - idle + listy ruchu
        lista_grafika_zajac_w = [mapa_tmx.get_tile_image(29 + x, 95, 5) for x in range(6)]
        lista_grafika_zajac_s = [mapa_tmx.get_tile_image(29 + x, 96, 5) for x in range(6)]
        lista_grafika_zajac_a = [mapa_tmx.get_tile_image(29 + x, 97, 5) for x in range(6)]
        lista_grafika_zajac_d = [mapa_tmx.get_tile_image(29 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_zajac_w):
            original_rect = g.get_rect()
            lista_grafika_zajac_w[i] = pygame.transform.scale(g, (
            original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_zajac_s):
            original_rect = g.get_rect()
            lista_grafika_zajac_s[i] = pygame.transform.scale(g, (
            original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_zajac_a):
            original_rect = g.get_rect()
            lista_grafika_zajac_a[i] = pygame.transform.scale(g, (
            original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_zajac_d):
            original_rect = g.get_rect()
            lista_grafika_zajac_d[i] = pygame.transform.scale(g, (
            original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

        lista_grafika_zajac = [mapa_tmx.get_tile_image(32, 92, 5), mapa_tmx.get_tile_image(32, 93, 5),
                              mapa_tmx.get_tile_image(31, 93, 5), mapa_tmx.get_tile_image(33, 93, 5)]
        for g in range(0, len(lista_grafika_zajac)):
            original_rect = lista_grafika_zajac[g].get_rect()
            lista_grafika_zajac[g] = pygame.transform.scale(lista_grafika_zajac[g], (
            original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik pirata - idle + listy ruchu
        lista_grafika_pirat_w = [mapa_tmx.get_tile_image(36 + x, 95, 5) for x in range(6)]
        lista_grafika_pirat_s = [mapa_tmx.get_tile_image(36 + x, 96, 5) for x in range(6)]
        lista_grafika_pirat_a = [mapa_tmx.get_tile_image(36 + x, 97, 5) for x in range(6)]
        lista_grafika_pirat_d = [mapa_tmx.get_tile_image(36 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_pirat_w):
            original_rect = g.get_rect()
            lista_grafika_pirat_w[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_s):
            original_rect = g.get_rect()
            lista_grafika_pirat_s[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_a):
            original_rect = g.get_rect()
            lista_grafika_pirat_a[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_d):
            original_rect = g.get_rect()
            lista_grafika_pirat_d[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

        lista_grafika_pirat = [mapa_tmx.get_tile_image(39, 92, 5), mapa_tmx.get_tile_image(39, 93, 5),
                               mapa_tmx.get_tile_image(38, 93, 5), mapa_tmx.get_tile_image(40, 93, 5)]
        for g in range(0, len(lista_grafika_pirat)):
            original_rect = lista_grafika_pirat[g].get_rect()
            lista_grafika_pirat[g] = pygame.transform.scale(lista_grafika_pirat[g], (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik pirata 2 - idle + listy ruchu
        lista_grafika_pirat_2_w = [mapa_tmx.get_tile_image(43 + x, 95, 5) for x in range(6)]
        lista_grafika_pirat_2_s = [mapa_tmx.get_tile_image(43 + x, 96, 5) for x in range(6)]
        lista_grafika_pirat_2_a = [mapa_tmx.get_tile_image(43 + x, 97, 5) for x in range(6)]
        lista_grafika_pirat_2_d = [mapa_tmx.get_tile_image(43 + x, 98, 5) for x in range(6)]

        for i, g in enumerate(lista_grafika_pirat_2_w):
            original_rect = g.get_rect()
            lista_grafika_pirat_2_w[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_2_s):
            original_rect = g.get_rect()
            lista_grafika_pirat_2_s[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_2_a):
            original_rect = g.get_rect()
            lista_grafika_pirat_2_a[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        for i, g in enumerate(lista_grafika_pirat_2_d):
            original_rect = g.get_rect()
            lista_grafika_pirat_2_d[i] = pygame.transform.scale(g, (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

        lista_grafika_pirat_2 = [mapa_tmx.get_tile_image(46, 92, 5), mapa_tmx.get_tile_image(46, 93, 5),
                               mapa_tmx.get_tile_image(45, 93, 5), mapa_tmx.get_tile_image(47, 93, 5)]
        for g in range(0, len(lista_grafika_pirat_2)):
            original_rect = lista_grafika_pirat_2[g].get_rect()
            lista_grafika_pirat_2[g] = pygame.transform.scale(lista_grafika_pirat_2[g], (
                original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie grafik gracza - lista przechowująca 4 grafiki gracza
        lista_grafika_gracz = [mapa_tmx.get_tile_image(37, 0, 5), mapa_tmx.get_tile_image(37, 1, 5),
                               mapa_tmx.get_tile_image(36, 1, 5), mapa_tmx.get_tile_image(38, 1, 5)]
        for g in range(0, len(lista_grafika_gracz)):
            original_rect = lista_grafika_gracz[g].get_rect()
            lista_grafika_gracz[g] = pygame.transform.scale(lista_grafika_gracz[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

        # Ładowanie grafik gracza - lista przechowująca grafiki chodzenia gracza
        # Ruch góra
        lista_grafika_gracz_ruch_gora = [mapa_tmx.get_tile_image(27, 3, 5), mapa_tmx.get_tile_image(29, 3, 5)]
        for g in range(0, len(lista_grafika_gracz_ruch_gora)):
            original_rect = lista_grafika_gracz_ruch_gora[g].get_rect()
            lista_grafika_gracz_ruch_gora[g] = pygame.transform.scale(lista_grafika_gracz_ruch_gora[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ruch dół
        lista_grafika_gracz_ruch_dol = [mapa_tmx.get_tile_image(27, 0, 5), mapa_tmx.get_tile_image(29, 0, 5)]
        for g in range(0, len(lista_grafika_gracz_ruch_dol)):
            original_rect = lista_grafika_gracz_ruch_dol[g].get_rect()
            lista_grafika_gracz_ruch_dol[g] = pygame.transform.scale(lista_grafika_gracz_ruch_dol[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ruch lewo
        lista_grafika_gracz_ruch_lewo = [mapa_tmx.get_tile_image(27, 1, 5), mapa_tmx.get_tile_image(29, 1, 5)]
        for g in range(0, len(lista_grafika_gracz_ruch_lewo)):
            original_rect = lista_grafika_gracz_ruch_lewo[g].get_rect()
            lista_grafika_gracz_ruch_lewo[g] = pygame.transform.scale(lista_grafika_gracz_ruch_lewo[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ruch prawo
        lista_grafika_gracz_ruch_prawo = [mapa_tmx.get_tile_image(27, 2, 5), mapa_tmx.get_tile_image(29, 2, 5)]
        for g in range(0, len(lista_grafika_gracz_ruch_prawo)):
            original_rect = lista_grafika_gracz_ruch_prawo[g].get_rect()
            lista_grafika_gracz_ruch_prawo[g] = pygame.transform.scale(lista_grafika_gracz_ruch_prawo[g],
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowaie grafik NPC - Thorne
        thorne_grafika = mapa_tmx.get_tile_image(32, 6, 5)
        original_rect = thorne_grafika.get_rect()
        thorne_grafika_rozszerzona = pygame.transform.scale(thorne_grafika,
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafik NPC - Torin
        torin_grafika = mapa_tmx.get_tile_image(31, 6, 5)
        original_rect = torin_grafika.get_rect()
        torin_grafika_rozszerzona = pygame.transform.scale(torin_grafika,
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafik NPC - Garrick
        garrick_grafika = mapa_tmx.get_tile_image(30, 6, 5)
        original_rect = garrick_grafika.get_rect()
        garrick_grafika_rozszerzona = pygame.transform.scale(garrick_grafika,
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafik NPC - Miranda
        miranda_grafika = mapa_tmx.get_tile_image(29, 6, 5)
        original_rect = miranda_grafika.get_rect()
        miranda_grafika_rozszerzona = pygame.transform.scale(miranda_grafika,
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))
        # Ładowanie grafki ataku gracza
        atak_gracza_grafika = mapa_tmx.get_tile_image(39, 0, 5)
        original_rect = atak_gracza_grafika.get_rect()
        atak_gracza_grafika_rozszerzona = pygame.transform.scale(atak_gracza_grafika,
                                (original_rect.width * rozmiar_pola / 32, original_rect.height * rozmiar_pola / 32))

    ########################################################################################################################

        # Ładowanie znaku ulepszenia
        znak_ulepszenie = mapa_tmx.get_tile_image(87, 37, 5)
        original_rect = znak_ulepszenie.get_rect()
        znak_ulepszenie = pygame.transform.scale(znak_ulepszenie,
                            (original_rect.width * rozmiar_pola / 46, original_rect.height * rozmiar_pola / 46))

        # Ładowanie grafik blood hit
        lista_blood_hit = [mapa_tmx.get_tile_image(1 + x, 90, 5) for x in range(8)]
        for i, g in enumerate(lista_blood_hit):
            original_rect = g.get_rect()
            lista_blood_hit[i] = pygame.transform.scale(g, (original_rect.width * rozmiar_pola / 32,
                                                            original_rect.height * rozmiar_pola / 32))

        return (lista_grafika_bialy_pajak_w, lista_grafika_bialy_pajak_s, lista_grafika_bialy_pajak_a,
                lista_grafika_bialy_pajak_d, znak_ulepszenie, lista_blood_hit, lista_grafika_pajak_w,
                lista_grafika_pajak_s, lista_grafika_pajak_a, lista_grafika_pajak_d, lista_grafika_wilk_w,
                lista_grafika_wilk_s, lista_grafika_wilk_a, lista_grafika_wilk_d, ognista_strzala, strzala_animacja,
                kamien, loot_grafika, znak_sklep, cialo, strzala, strzala2, miecz, luk, logo, znak, tlo_menu,
                hp_potion, hp_potion2, mp_potion, mp_potion2, lista_grafika_wilk, lista_grafika_pajak, lista_grafika_dzik,
                lista_grafika_bialy_pajak, lista_grafika_gracz, lista_grafika_gracz_ruch_gora, lista_grafika_gracz_ruch_dol,
                lista_grafika_gracz_ruch_lewo, lista_grafika_gracz_ruch_prawo, thorne_grafika_rozszerzona,
                torin_grafika_rozszerzona, garrick_grafika_rozszerzona, atak_gracza_grafika_rozszerzona,
                lista_grafika_zajac, lista_grafika_pirat, lista_grafika_pirat_2, miranda_grafika_rozszerzona,
                lista_grafika_dzik_w, lista_grafika_dzik_s, lista_grafika_dzik_a, lista_grafika_dzik_d,
                lista_grafika_zajac_w, lista_grafika_zajac_s, lista_grafika_zajac_a, lista_grafika_zajac_d,
                lista_grafika_pirat_w, lista_grafika_pirat_s, lista_grafika_pirat_a, lista_grafika_pirat_d,
                lista_grafika_pirat_2_w, lista_grafika_pirat_2_s, lista_grafika_pirat_2_a, lista_grafika_pirat_2_d)

    except Exception as e:
        print(e)

### Funkcja tworząca słownik z ilościami doświadczenia na każdy poziom, liniowo, lvl: 0 - 50 ###
def poziomy_ilosc_doswiadczenia_hp_mp():

    # Konfiguracja
    doswiadczenie = {1: (0, 300, 100, 100)}
    przyrost = 100 # Przyrost liniowy co poziom
    poziom_bazowy = 300
    hp_start = 100
    mp_start = 100

    # Tworzenie słownika
    for lvl in range(2, 101):

        if lvl == 10: przyrost_hp, przyrost_mp = 20, 20
        else: przyrost_hp, przyrost_mp = 10, 10

        doswiadczenie[lvl] = (
        doswiadczenie[lvl - 1][1], doswiadczenie[lvl - 1][1] + poziom_bazowy + przyrost * (lvl - 1),
        doswiadczenie[lvl - 1][2] + przyrost_hp, doswiadczenie[lvl - 1][3] + przyrost_mp)

    return doswiadczenie
############################################################################
############################################################################