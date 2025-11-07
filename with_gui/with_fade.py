import sys, pygame, datetime, os, json
import time as pythontime
from pygame import *

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (180, 30, 20)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Shroomraider")

menu_state = "main"
clock = pygame.time.Clock()

class player_on_list():
    def __init__(self, name, count):
        self.name = name
        self.count = count
        width, height = 728, 80
        x, y = 148, 148 + (100 * count)
        self.width, self.height, self.x, self.y = width, height, x ,y
        self.clicked, self.hovered = False, False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        global delete_pop_up, create_plr_btn_state, inc_len, already_plr, player_name_input
        action = False
        delete = False
        pos = pygame.mouse.get_pos()

        # Hover effects
        if self.rect.collidepoint(pos):
            bg_outer = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
            bg_outer.fill((0, 0, 0, 0))
            pygame.draw.rect(bg_outer, (main_color), bg_outer.get_rect(), border_radius=16)
            screen.blit(bg_outer, (self.x - 4, self.y - 4))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.hovered = False


        # Background
        bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (255, 255, 255), bg.get_rect(), border_radius=16)
        screen.blit(bg, (self.x, self.y))

        # Player data
        with open(f"data/players/{self.name}.json", "r") as f:
            loaded_data = json.load(f)
        
        try:
            plr = loaded_data["name"]
            dt_created = loaded_data["time_created"]
            s = loaded_data["since_epoch"]
            maps = loaded_data["maps_finished"]
            ply_time = loaded_data["playing_time"]
            mush_tot = loaded_data["mush_collected"]
        except Exception as e:
            print(f"Invalid player file, error={e}")

        # Show data on screen
        plr_text_outer = create_text(plr, 32, black)[0]
        screen.blit(plr_text_outer, (self.x + 13, self.y + 4))
        plr_text = create_text(plr, 32, main_color)[0]
        screen.blit(plr_text, (self.x + 12, self.y + 4))
        dt_created_text = create_text(dt_created, 24, black)[0]
        screen.blit(dt_created_text, (self.x + 12, self.y + self.height//2))
        ply_time_text = create_text(f"| Play time: {ply_time}", 24, black)[0]
        screen.blit(ply_time_text, (self.x + 32 + dt_created_text.get_width(), self.y + self.height//2))
        mush_tot_text = create_text(f"| Mushrooms: {mush_tot}", 24, black)[0]
        screen.blit(mush_tot_text, (self.x + 48 + dt_created_text.get_width() + ply_time_text.get_width(), self.y + self.height//2))

        # Delete button
        plr_del_btn = text_Button_1(self.x + self.width - (32 * 6), self.y + 4, "Delete", 32, (255, 100, 100))
        if plr_del_btn.draw():
            delete_pop_up = True, self.name
            create_plr_btn_state = False
            inc_len = False
            already_plr = False
            player_name_input = ""
            # os.remove(f"data/players/{self.name}.json")

        return action, delete


class text_Button_1():
    def __init__(self, x, y, t, s, col):
        self.col = col
        text, capt = create_text(t, s, col)
        outer, capt = create_text(t, s, black)
        self.s = s
        self.capt = capt
        self.outer = outer
        self.width = text.get_width()
        self.height = text.get_height()
        self.text = text
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.text, s = create_text(self.capt, self.s, main_color)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.text, s = create_text(self.capt, self.s, self.col)
            self.outer, s = create_text(self.capt, self.s, black)
            self.hovered = False

        screen.blit(self.outer, (self.rect.x + 2, self.rect.y))
        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action


class text_Button():
    def __init__(self, x, y, t, s):
        text, capt = create_text(t, s, main_color)
        outer, capt = create_text(t, s, black)
        self.s = s
        self.capt = capt
        self.outer = outer
        self.width = text.get_width()
        self.height = text.get_height()
        self.text = text
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.text, s = create_text(self.capt, self.s + 12, white)
            self.outer, s = create_text(self.capt, self.s + 12, black)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.text, s = create_text(self.capt, self.s, main_color)
            self.outer, s = create_text(self.capt, self.s, black)
            self.hovered = False

        screen.blit(self.outer, (self.rect.x + 4, self.rect.y))
        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action


def create_text(text, s, color):
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=s)
    return font.render(text, True, color), text


def fade_black():
    alphaSurface = Surface((1024, 768), pygame.SRCALPHA) # The custom-surface of the size of the screen.
    alph = 0 # Set alpha to 0 before the main-loop.

    while alph < 245:
        alph += 10  # Increment alpha by a really small value

        alphaSurface.set_alpha(alph)
        alphaSurface.fill((0, 0, 0))  # Fill with black before blitting
        screen.blit(alphaSurface, (0, 0)) # Blit it to the screen-surface (Make them separate)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(480)  # Limit frame rate

def fade_in(surf):
    alphaSurface = Surface((1024, 768), pygame.SRCALPHA) # The custom-surface of the size of the screen.
    alph = 255 # Set alpha to 0 before the main-loop.

    while alph > 10:
        alph -= 10  # Increment alpha by a really small value

        surf()
        alphaSurface.fill((0, 0, 0, alph))  # Fill with black before blitting
        screen.blit(alphaSurface, (0, 0)) # Blit it to the screen-surface (Make them separate)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(480)  # Limit frame rate

fade_count = 0

# Images
menu_bg_img1 = pygame.image.load("assets/bg/1st Layer.png")
menu_bg_img2 = pygame.image.load("assets/bg/2nd Layer.png")
menu_bg_img3 = pygame.image.load("assets/bg/3rd Layer.png")
menu_bg_img4 = pygame.image.load("assets/bg/4th Layer.png")
menu_bg_img5 = pygame.image.load("assets/bg/5th Layer.png")

menu_bg_img1 = pygame.transform.scale(menu_bg_img1, (1024, 768))
menu_bg_img2 = pygame.transform.scale(menu_bg_img2, (1024, 768))
menu_bg_img3 = pygame.transform.scale(menu_bg_img3, (1024, 768))
menu_bg_img4 = pygame.transform.scale(menu_bg_img4, (1024, 768))
menu_bg_img5 = pygame.transform.scale(menu_bg_img5, (1024, 768))

# Main menu buttons
play_btn = text_Button(128, 288, "Play", 60)
create_btn = text_Button(128, 360, "Create Levels", 60)
lb_btn = text_Button(128, 432, "Leaderboards", 60)
options_btn = text_Button(128, 504, "Options", 60)
quit_btn = text_Button(128, 576, "Quit", 60)

# Play menu buttons
create_plr_btn = text_Button_1(512, 640, "New Player", 48, white)
create_plr_done_btn = text_Button_1(512, 448, "Done", 48, white)
create_plr_back_btn = text_Button_1((1000 - (24 * 16))//2, 448, "Back", 48, white)
play_menu_back_btn = text_Button_1(148, 640, "Back", 48, white)
delete_pop_up_back = text_Button_1((1000 - (24 * 16))//2, 448, "Back", 48, white)
delete_pop_up_confirm = text_Button_1(512, 448, "Confirm", 48, white)
page_back = text_Button_1(304, 640, "<", 48, white)
page_next = text_Button_1(352, 640, ">", 48, white)
create_plr_btn_state = False
create_plr_done_btn_state = False
already_plr = False
inc_len = False
delete_pop_up = False, ""
delete_pop_up_back_state = False
delete_pop_up_confirm_state = False

def menu_background():
    # Background
    screen.blit(menu_bg_img5, (0, 0))
    screen.blit(menu_bg_img4, (0, 0))
    screen.blit(menu_bg_img3, (0, 0))
    screen.blit(menu_bg_img2, (0, 0))
    screen.blit(menu_bg_img1, (0, 0))

    # 'Blur' background
    blur = pygame.Surface((1024, 768), pygame.SRCALPHA)
    blur.fill((0, 0, 0, 50))
    screen.blit(blur, (0, 0))

def main_menu():
    global menu_state

    # Background
    menu_background()

    # Semi-background
    semibg = pygame.Surface((1024 - 64 - 128, 768 - 348), pygame.SRCALPHA)
    semibg.fill((0, 0, 0, 0))
    pygame.draw.rect(semibg, (20, 50, 30, 150), semibg.get_rect(), border_radius=32)
    screen.blit(semibg, (92, 264))


    # Title
    title = create_text("SHROOM RAIDER", 112, main_color)[0]
    title_outer = create_text("SHROOM RAIDER", 112, black)[0]
    screen.blit(title_outer, ((1024 - title_outer.get_width()) // 2, 92))
    screen.blit(title, (((1024 - title.get_width()) // 2) - 4, 92))


    # Buttons
    if play_btn.draw():
        fade_black()
        menu_state = "play"
    elif create_btn.draw():
        fade_black()
        menu_state = "create"
    elif lb_btn.draw():
        fade_black()
        menu_state = "leaderboards"
    elif options_btn.draw():
        fade_black()
        menu_state = "options"
    elif quit_btn.draw():
        sys.exit()

players = [player for player in os.listdir("data/players")]

def _create_player(name, date, s):
    """Creates a player file as .txt"""
    data = {"name": name, "time_created": date, "since_epoch": s, "maps_finished": [], "playing_time": 0, "mush_collected": 0}
    with open(f"data/players/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

player_name_input = ""
def _create_player_menu():
    global player_name_input, create_plr_done_btn_state, players, create_plr_btn_state, already_plr, inc_len, delete_pop_up, delete_pop_up_back_state, delete_pop_up_confirm_state

    # Semi-background
    semibg = pygame.Surface((512, 256), pygame.SRCALPHA)
    semibg.fill((20, 100, 50, 0))

    pygame.draw.rect(semibg, (0, 0, 0, 225), semibg.get_rect(), border_radius=16)
    screen.blit(semibg, (256, 256))

    # Text
    label_outer = create_text("Name your player", 48, black)[0]
    screen.blit(label_outer, (((1012 - label_outer.get_width())//2) + 2, 268))
    label = create_text("Name your player", 48, white)[0]
    screen.blit(label, ((1012 - label.get_width())//2, 268))
    text = create_text(player_name_input, 32, main_color)[0]

    if max_plrs:
        screen.blit(create_text("Maximum of 10 players only", 22, white)[0], ((1000 - (24 * 16))//2, 408))
    else:
        if 0 <= len(player_name_input) < 16:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name_input = player_name_input[:-1]
                        inc_len = False
                    elif event.key != pygame.K_ESCAPE:
                        player_name_input += event.unicode
        else:
            player_name_input = player_name_input[:-1]
            inc_len = True

    screen.blit(text, ((1000 - (24 * 16))//2, 336))

    if create_plr_back_btn.draw():
        create_plr_btn_state = False
        inc_len = False
        already_plr = False
        player_name_input = ""

    if create_plr_done_btn.draw():
        create_plr_done_btn_state = True

    if create_plr_done_btn_state:
        current_time = datetime.datetime.now()
        if 0 < len(player_name_input) < 16:
            if player_name_input + ".json" in players:
                already_plr = True
            else:
                _create_player(player_name_input, str(current_time)[:19], pythontime.time()//1)
                players.append(player_name_input + ".json")
                create_plr_done_btn_state = False
                create_plr_btn_state = False
                already_plr = False
                player_name_input = ""
            inc_len = False
        else:
            already_plr = False
            inc_len = True
        create_plr_done_btn_state = False

    if already_plr:
        screen.blit(create_text("Already a player", 22, white)[0], ((1000 - (24 * 16))//2, 408))
    if inc_len:
        screen.blit(create_text("Name must have at least 1 character,", 22, white)[0], ((1000 - (24 * 16))//2, 384))
        screen.blit(create_text("and a maximum of 15 characters", 22, white)[0], ((1000 - (24 * 16))//2, 408))

player_page = 1
def players_list(page):
    # page is 0-indexed
    i = page * 5
    count = 0
    for player in players[i:i + 5]:
        p = player_on_list(str(player)[:-5], count)
        if p.draw()[0]:
            ...
        count += 1

def delete_player_confirmation(player):
    global delete_pop_up
    # Semi-background
    semibg = pygame.Surface((512, 256), pygame.SRCALPHA)
    semibg.fill((20, 100, 50, 0))

    pygame.draw.rect(semibg, (0, 0, 0, 225), semibg.get_rect(), border_radius=16)
    screen.blit(semibg, (256, 256))

    # Label
    title1 = create_text("Are you sure you", 48, white)[0]
    title2 = create_text(f"want to delete", 48, white)[0]
    title3 = create_text(f"'{player}'?", 48, main_color)[0]
    screen.blit(title1, ((1000 - (24 * 16))//2, 268))
    screen.blit(title2, ((1000 - (24 * 16))//2, 316))
    screen.blit(title3, ((1000 - (24 * 16))//2, 364))

    if delete_pop_up_back.draw():
        delete_pop_up = False, ""

    if delete_pop_up_confirm.draw():
        os.remove(f"data/players/{player}.json")
        delete_pop_up = False, ""

def level_menu():
    global menu_state, fade_count, create_plr_btn_state, delete_pop_up, player_page

    # Background
    menu_background()

    # Background surface
    bg_surf = pygame.Surface((1024 - 192, 768 - 96), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 0))

    # Semi-background
    pygame.draw.rect(bg_surf, (75, 75, 75, 100), bg_surf.get_rect(), border_radius=32)
    screen.blit(bg_surf, (96, 48))
    
    if player_page == 1:
        players_list(0)
    elif player_page == 2:
        players_list(1)

    if create_plr_btn.draw():
        create_plr_btn_state = True

    # Buttons
    if create_plr_btn_state:
        _create_player_menu()
        delete_pop_up = False, ""

    if play_menu_back_btn.draw():
        create_plr_btn_state = False
        delete_pop_up = False, ""
        menu_state = "main"
        fade_count = 0

    if delete_pop_up[0]:
        delete_player_confirmation(delete_pop_up[1])

    if page_back.draw():
        player_page = 1
    if page_next.draw():
        player_page = 2

    # Title
    text2 = create_text(f"PLAYERS      Page {player_page}/2", 60, black)[0]
    screen.blit(text2, ((148) + 4, 60))
    text1 = create_text(f"PLAYERS      Page {player_page}/2", 60, white)[0]
    screen.blit(text1, (148, 60))

def create_menu():
    text = create_text("Create", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))


def leaderboards_menu():
    text = create_text("Leaderboards", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))


def options_menu():
    text = create_text("Options", 60, main_color)[0]
    top_bar = pygame.Surface((768, 2))
    top_bar.fill(main_color)
    screen.blit(top_bar, (128, 128))
    screen.blit(text, (128, 48))

while True:

    players = [player for player in os.listdir("data/players")]
    if len(players) >= 10:
        max_plrs = True
    else:
        max_plrs = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if menu_state == "main":
        if fade_count == 0:
            fade_in(main_menu)
            fade_count += 1
        main_menu()

    if menu_state == "play":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            create_plr_btn_state = False
            menu_state = "main"
            fade_count = 0
        if fade_count == 1:
            fade_in(level_menu)
            fade_count += 1
        else:
            level_menu()

    if menu_state == "leaderboards":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
            fade_count = 0
        if fade_count == 1:
            fade_in(leaderboards_menu)
            fade_count += 1
        leaderboards_menu()

    if menu_state == "create":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
            fade_count = 0
        if fade_count == 1:
            fade_in(create_menu)
            fade_count += 1
        create_menu()

    if menu_state == "options":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
            fade_count = 0
        if fade_count == 1:
            fade_in(options_menu)
            fade_count += 1
        options_menu()

    pygame.display.flip()
