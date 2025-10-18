import pygame
import os, json, datetime
from instances import gracz
from npc import NPC
from przeciwnik import Przeciwnik
from dragon import Dragon
from gracz import Gracz
import instances


### MENU CLASS - REPRESENTS MENU OBJECT ################################################################################
class Menu:

    ### Initializer of instance ###
    def __init__(self):

        self.type = "menu1" # "menu1" - after launch / "menu2" - during game / "load" / "save"
        self.starting_type = self.type
        self.load_save_info()
        self.load_images()
        self.load_fonts()

    ### Function loads save info from .json files ###
    def load_save_info(self):

        save_list = []
        for slot in range(1, 4):
            save_path = os.path.join("save", f"zapis_{slot}.json")
            if os.path.isfile(save_path):
                with open(save_path, "r") as f:
                    game_save = json.load(f)
                lvl = game_save["gracz"]["poziom"]
                data = game_save["data_zapisu"]
                save_list.append(f"LVL: {lvl}, Data: {data}")
            else:
                save_list.append("Pusty slot")
        self.save_info_1 = save_list[0]
        self.save_info_2 = save_list[1]
        self.save_info_3 = save_list[2]

    ### Function loads fonts ###
    def load_fonts(self):

        self.font_color = "floral white"
        self.font_50 = pygame.font.Font(None, 50)
        self.font_40 = pygame.font.Font(None, 40)
        self.font_30 = pygame.font.Font(None, 30)

    ### Function load images ###
    def load_images(self):

        self.image_logo = pygame.image.load("graphics/logo.png")
        self.image_background = pygame.image.load("graphics/background.jpg")

    ### Function drawing text with outline effect ###
    @staticmethod
    def render_text_with_outline(font, text, text_color, outline_color, outline_width=2):

        base = font.render(text, True, outline_color)
        size = base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width
        surface = pygame.Surface(size, pygame.SRCALPHA)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    surface.blit(font.render(text, True, outline_color), (dx + outline_width, dy + outline_width))
        surface.blit(font.render(text, True, text_color), (outline_width, outline_width))
        return surface

    ### Menu drawing ###
    def draw_menu(self, okno):

        # Background image
        okno.blit(self.image_background, (0, 0))
        # Buttons with text
        if self.type == "menu1":
            pygame.draw.rect(okno, "grey13", (760, 290, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 490, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 690, 400, 100))
            okno.blit(self.font_50.render("NOWA GRA", True, self.font_color), (860, 320, 300, 100))
            okno.blit(self.font_50.render("ZAŁADUJ GRĘ", True, self.font_color), (840, 520, 300, 100))
            okno.blit(self.font_50.render("WYJŚCIE", True, self.font_color), (880, 720, 300, 100))
            okno.blit(self.font_40.render("(Rozpocznij nową grę lub wczytaj zapis z końca gry)", True, self.font_color), (620, 990, 300, 100))

        elif self.type == "menu2":
            pygame.draw.rect(okno, "grey13", (760, 90, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 290, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 490, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 690, 400, 100))
            pygame.draw.rect(okno, "grey13", (760, 890, 400, 100))
            okno.blit(self.font_50.render("WZNÓW", True, self.font_color), (880, 120, 300, 100))
            okno.blit(self.font_50.render("NOWA GRA", True, self.font_color), (860, 320, 300, 100))
            okno.blit(self.font_50.render("ZAPISZ GRĘ", True, self.font_color), (850, 520, 300, 100))
            okno.blit(self.font_50.render("ZAŁADUJ GRĘ", True, self.font_color), (840, 720, 300, 100))
            okno.blit(self.font_50.render("WYJŚCIE", True, self.font_color), (880, 920, 300, 100))
        elif self.type in ("load", "save"):
            if self.type == "load":
                text_surf = Menu.render_text_with_outline(self.font_50, "ZAŁADUJ GRĘ", self.font_color,
                                                          (50, 50, 50), 2)
                okno.blit(text_surf, (830, 195))
            else:
                text_surf = Menu.render_text_with_outline(self.font_50, "ZAPISZ GRĘ", self.font_color,
                                                          (50, 50, 50), 2)
                okno.blit(text_surf, (845, 195))
            # Slots
            pygame.draw.rect(okno, "grey13", (660, 290, 400, 100))
            pygame.draw.rect(okno, "grey13", (660, 490, 400, 100))
            pygame.draw.rect(okno, "grey13", (660, 690, 400, 100))
            # Choose slots buttons
            pygame.draw.rect(okno, "grey27", (1060, 290, 200, 100))
            pygame.draw.rect(okno, "grey27", (1060, 490, 200, 100))
            pygame.draw.rect(okno, "grey27", (1060, 690, 200, 100))
            # Back button
            pygame.draw.rect(okno, "grey13", (760, 890, 400, 100))
            # Back text
            okno.blit(self.font_50.render("WRÓĆ", True, self.font_color), (900, 920, 300, 100))
            # Slots numeration
            okno.blit(self.font_50.render("1:", True, self.font_color), (690, 320, 300, 100))
            okno.blit(self.font_50.render("2:", True, self.font_color), (690, 520, 300, 100))
            okno.blit(self.font_50.render("3:", True, self.font_color), (690, 720, 300, 100))
            # Save info
            okno.blit(self.font_30.render(self.save_info_1, True, self.font_color), (730, 330, 300, 100))
            okno.blit(self.font_30.render(self.save_info_2, True, self.font_color), (730, 530, 300, 100))
            okno.blit(self.font_30.render(self.save_info_3, True, self.font_color), (730, 730, 300, 100))
            # Choose slots text
            okno.blit(self.font_40.render("WYBIERZ", True, self.font_color), (1096, 328, 200, 100))
            okno.blit(self.font_40.render("WYBIERZ", True, self.font_color), (1096, 528, 200, 100))
            okno.blit(self.font_40.render("WYBIERZ", True, self.font_color), (1096, 728, 200, 100))
        # Game logo
        okno.blit(self.image_logo, (1750, 1015))
        # Display update #
        pygame.display.update()

    ### Choosing action ###
    def choose_action(self, game_state):

        # Checking if left mouse button is pressed #
        option = pygame.mouse.get_pressed()
        if option[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Actions for menu1 #
            if self.type == "menu1":
                # New game #
                if mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 - 250 and mouse_y <= 540 - 250 + 100:
                    pygame.time.delay(100)
                    imie = self.input_name(instances.window)
                    instances.gracz.imie = imie
                    game_state = "gameplay"
                    self.type = "menu2"
                    self.starting_type = "menu2"
                # Load game #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 - 50 and mouse_y <= 540 - 50 + 100:
                    pygame.time.delay(100)
                    self.type = "load"
                # Quit #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 + 150 and mouse_y <= 540 + 150 + 100:
                    pygame.time.delay(100)
                    pygame.quit()
                    exit()

            # Actions for menu2 #
            elif self.type == "menu2":
                # Continue #
                if mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 - 450 and mouse_y <= 540 - 450 + 100:
                    pygame.time.delay(100)
                    game_state = "gameplay"
                # New game #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 - 250 and mouse_y <= 540 - 250 + 100:
                    pygame.time.delay(100)
                    self.new_game()
                    imie = self.input_name(instances.window)
                    instances.gracz.imie = imie
                    game_state = "gameplay"
                # Save game #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 - 50 and mouse_y <= 540 - 50 + 100:
                    pygame.time.delay(100)
                    self.type = "save"
                # Load game #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 + 150 and mouse_y <= 540 + 150 + 100:
                    pygame.time.delay(100)
                    self.type = "load"
                # Quit #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 + 350 and mouse_y <= 540 + 350 + 100:
                    pygame.time.delay(100)
                    pygame.quit()
                    exit()

            # Actions for load #
            elif self.type == "load":
                # 1 slot #
                if mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 - 250 and mouse_y <= 540 - 250 + 100:
                    pygame.time.delay(100)
                    if self.save_info_1 != "Pusty slot":
                        self.starting_type = "menu2"
                        self.load_game(1)
                        game_state = "gameplay"
                        self.type = "menu2"
                # 2 slot #
                elif mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 - 50 and mouse_y <= 540 - 50 + 100:
                    pygame.time.delay(100)
                    if self.save_info_2 != "Pusty slot":
                        self.starting_type = "menu2"
                        self.load_game(2)
                        game_state = "gameplay"
                        self.type = "menu2"
                # 3 slot #
                elif mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 + 150 and mouse_y <= 540 + 150 + 100:
                    pygame.time.delay(100)
                    if self.save_info_3 != "Pusty slot":
                        self.starting_type = "menu2"
                        self.load_game(3)
                        game_state = "gameplay"
                        self.type = "menu2"
                # Back #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 + 350 and mouse_y <= 540 + 350 + 100:
                    pygame.time.delay(100)
                    self.type = "menu1" if self.starting_type == "menu1" else "menu2"

            # Actions for save #
            elif self.type == "save":

                # 1 slot #
                if mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 - 250 and mouse_y <= 540 - 250 + 100:
                    if gracz.zycie and instances.game_map.level != "boss":
                        pygame.time.delay(100)
                        self.save_game(1)
                        self.type = "menu2"
                        game_state = "gameplay"
                # 2 slot #
                elif mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 - 50 and mouse_y <= 540 - 50 + 100:
                    if gracz.zycie and instances.game_map.level != "boss":
                        pygame.time.delay(100)
                        self.save_game(2)
                        self.type = "menu2"
                        game_state = "gameplay"
                # 3 slot #
                elif mouse_x >= 1060 and mouse_x <= 1060 + 200 and mouse_y >= 540 + 150 and mouse_y <= 540 + 150 + 100:
                    if gracz.zycie and instances.game_map.level != "boss":
                        pygame.time.delay(100)
                        self.save_game(3)
                        self.type = "menu2"
                        game_state = "gameplay"
                # Back #
                elif mouse_x >= 760 and mouse_x <= 760 + 400 and mouse_y >= 540 + 350 and mouse_y <= 540 + 350 + 100:
                    pygame.time.delay(100)
                    self.save_game(1)
                    self.type = "menu2"

        # Return game_state #
        return game_state

    ### SAVE GAME ###
    def save_game(self, slot):

        # Player parameters #
        player_save = gracz.slownik_parametry_gracza_save()
        # NPCs parameters #
        npc_save = NPC.slownik_parametry_npc_save(NPC)
        # Enemy parameters #
        enemy_save = Przeciwnik.slownik_przeciwnicy_save(Przeciwnik)
        # Data zapisu #
        data_save = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        # Whole structure #
        game_save = {"gracz": player_save,
                     "npc": npc_save,
                     "przeciwnicy": enemy_save,
                     "loot_powierzchnia": Przeciwnik.loot_powierzchnia,
                     "loot_podziemia": Przeciwnik.loot_podziemia,
                     "loot_fabula_powierzchnia": Przeciwnik.loot_przedmioty_fabula_powierzchnia,
                     "loot_fabula_podziemia": Przeciwnik.loot_przedmioty_fabula_podziemia,
                     "data_zapisu": data_save}
        # Saving to .json file #
        save_path = os.path.join("save", f"zapis_{slot}.json")
        with open(save_path, "w") as f:
            json.dump(game_save, f, indent=4)
        self.load_save_info()

    ### LOAD GAME ###
    def load_game(self, slot):

        # Ładowanie struktury z pliku .json #
        save_path = os.path.join("save", f"zapis_{slot}.json")
        if os.path.isfile(save_path):
            with open(save_path, "r") as f:
                game_save = json.load(f)
            # Ładowanie parametrów gracza #
            gracz.load_save(game_save["gracz"])
            # Ładowanie parametrów NPC #
            NPC.load_save(NPC, game_save["npc"])
            # Usuwanie przeciwnikow z movement map i zaznaczeń #
            for p in Przeciwnik.przeciwnicy_powierzchnia:
                instances.game_map.main_map_jwrpg[p.y][p.x] = 0
                p.zaznaczenie = False
            for p in Przeciwnik.przeciwnicy_podziemia:
                instances.game_map.underground_map_jwrpg[p.y][p.x] = 0
                p.zaznaczenie = False
            gracz.zaznaczenie = False
            # Ładowanie parametrów przeciwników i loota #
            loot_zloto = (game_save["loot_powierzchnia"], game_save["loot_podziemia"])
            loot_fabula = (game_save["loot_fabula_powierzchnia"], game_save["loot_fabula_podziemia"])
            Przeciwnik.load_save(Przeciwnik, game_save["przeciwnicy"], loot_zloto, loot_fabula)
            # Ładowanie poziomu mapy
            instances.game_map.level = game_save["gracz"]["map_lvl"]
            # Resetowanie boss mapy
            instances.quest_manager.dragon_progress = 1
            Dragon.new_game()
            # Ladowanie glownego soundtracku
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sky_city.ogg")
            pygame.mixer.music.play(-1)

    ### NEW GAME ###
    def new_game(self):

        if instances.game_map.level == "main":
            instances.game_map.main_map_jwrpg[gracz.y2][gracz.x2] = 0
        else:
            instances.game_map.underground_map_jwrpg[gracz.y2][gracz.x2] = 0
        instances.game_map.level = "main"
        gracz.new_game()
        NPC.new_game()
        Przeciwnik.new_game()
        Dragon.new_game()
        instances.quest_manager.progress = 0
        instances.quest_manager.story = 1
        instances.quest_manager.dragon_progress = 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sky_city.ogg")
        pygame.mixer.music.play(-1)

    ### GET PLAYER NAME ###
    def input_name(self, okno):

        font = pygame.font.Font(None, 48)
        input_text = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(input_text.strip()) > 0:
                            imie = input_text.strip()
                            text_surface = gracz.tekst_1.render(imie, True, "floral white")
                            szerokosc_tekstu = text_surface.get_width()
                            gracz.text_x = okno.get_width() // 2 - szerokosc_tekstu // 2 - 1
                            gracz.text_y = okno.get_height() // 2 - 89
                            return imie
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 20:
                            input_text += event.unicode

            okno.fill((0, 0, 0))
            prompt = font.render("Wpisz imię postaci:", True, (255, 255, 255))
            text_surface = font.render(input_text + "|", True, (255, 255, 0))

            center_x = okno.get_width() // 2
            prompt_pos = (center_x - prompt.get_width() // 2, okno.get_height() // 2 - 100)
            text_pos = (center_x - text_surface.get_width() // 2, okno.get_height() // 2)

            okno.blit(prompt, prompt_pos)
            okno.blit(text_surface, text_pos)
            pygame.display.flip()
########################################################################################################################