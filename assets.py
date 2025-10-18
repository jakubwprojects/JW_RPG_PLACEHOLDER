from pytmx import load_pygame
from MAIN_CONFIG import TILE_SIZE as rozmiar_pola
from konfiguracja_3_00 import ladowanie_obrazow

(
 lista_grafika_bialy_pajak_w, lista_grafika_bialy_pajak_s, lista_grafika_bialy_pajak_a, lista_grafika_bialy_pajak_d,
 znak_ulepszenie, lista_blood_hit, lista_grafika_pajak_w, lista_grafika_pajak_s, lista_grafika_pajak_a,
 lista_grafika_pajak_d, lista_grafika_wilk_w, lista_grafika_wilk_s, lista_grafika_wilk_a, lista_grafika_wilk_d,
 ognista_strzala, strzala_animacja, kamien, loot_grafika, znak_sklep, cialo, strzala, strzala2, miecz, luk, logo,
 znak, tlo_menu, hp_potion, hp_potion2, mp_potion, mp_potion2, lista_grafika_wilk, lista_grafika_pajak,
 lista_grafika_dzik, lista_grafika_bialy_pajak, lista_grafika_gracz, lista_grafika_gracz_ruch_gora,
 lista_grafika_gracz_ruch_dol, lista_grafika_gracz_ruch_lewo, lista_grafika_gracz_ruch_prawo,
 thorne_grafika_rozszerzona, torin_grafika_rozszerzona, garrick_grafika_rozszerzona,
 atak_gracza_grafika_rozszerzona, lista_grafika_zajac, lista_grafika_pirat, lista_grafika_pirat_2,
 miranda_grafika_rozszerzona, lista_grafika_dzik_w, lista_grafika_dzik_s, lista_grafika_dzik_a, lista_grafika_dzik_d,
 lista_grafika_zajac_w, lista_grafika_zajac_s, lista_grafika_zajac_a, lista_grafika_zajac_d,
 lista_grafika_pirat_w, lista_grafika_pirat_s, lista_grafika_pirat_a, lista_grafika_pirat_d,
 lista_grafika_pirat_2_w, lista_grafika_pirat_2_s, lista_grafika_pirat_2_a, lista_grafika_pirat_2_d
 ) = ladowanie_obrazow(load_pygame("mapa_2_00_placeholder.tmx"), rozmiar_pola)