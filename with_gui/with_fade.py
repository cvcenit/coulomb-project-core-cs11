import sys, pygame, time, datetime, os
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

class text_Button_1():
    def __init__(self, x, y, text, s):
        text, capt = create_text(text, s, white)
        self.s = s
        self.capt = capt
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
            self.text, s = create_text(self.capt, self.s, white)
            self.hovered = False

        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action


class text_Button():
    def __init__(self, x, y, text, s):
        text, capt = create_text(text, s, main_color)
        self.s = s
        self.capt = capt
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
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if not self.rect.collidepoint(pos) and self.hovered == True:
            self.text, s = create_text(self.capt, self.s, main_color)
            self.hovered = False

        screen.blit(self.text, (self.rect.x, self.rect.y))

        return action


def create_text(text, s, color):
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=s)
    return font.render(text, True, color), text


def fade_black():
    alphaSurface = Surface((1024, 768), pygame.SRCALPHA) # The custom-surface of the size of the screen.
    alph = 0 # Set alpha to 0 before the main-loop.
    clock = pygame.time.Clock()

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
    clock = pygame.time.Clock()

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

# Data
players = [player for player in os.listdir("data/players")]


# Images
menu_bg_img1 = pygame.image.load("assets/bg/1st Layer.png")
menu_bg_img2 = pygame.image.load("assets/bg/2nd Layer.png")
menu_bg_img3 = pygame.image.load("assets/bg/3rd Layer.png")
menu_bg_img4 = pygame.image.load("assets/bg/4th Layer.png")
menu_bg_img5 = pygame.image.load("assets/bg/5th Layer.png")

# Main menu buttons
play_btn = text_Button(128, 288, "Play", 60)
create_btn = text_Button(128, 360, "Create Levels", 60)
lb_btn = text_Button(128, 432, "Leaderboards", 60)
options_btn = text_Button(128, 504, "Options", 60)
quit_btn = text_Button(128, 576, "Quit", 60)

# Play menu buttons
create_plr_btn = text_Button_1(512, 640, "New Player", 48)
create_plr_done_btn = text_Button_1(512, 448, "Done", 48)
create_plr_back_btn = text_Button_1(256, 448, "Back", 48)
play_menu_back_btn = text_Button_1(128, 640, "Back", 48)
create_plr_btn_state = False
create_plr_done_btn_state = False
already_plr = False
inc_len = False

def main_menu():
    global menu_state

    # Background
    screen.blit(menu_bg_img5, (0, 0))
    screen.blit(menu_bg_img4, (0, 0))
    screen.blit(menu_bg_img3, (0, 0))
    screen.blit(menu_bg_img2, (0, 0))
    screen.blit(menu_bg_img1, (0, 0))

    # Semi-background
    semibg = pygame.Surface((1024 - 256 - 128, 768 - 348), pygame.SRCALPHA)
    semibg.fill((0, 0, 0, 150))
    screen.blit(semibg, (92, 264))

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

def _create_player(name, date):
    """Creates a player file as .txt"""
    data = [name, date]
    with open(f"data/players/{name}.txt", "w", encoding="utf-8") as player_data:
        player_data.write("\n".join(data))

player_name_input = ""
def _create_player_menu():
    global player_name_input, create_plr_done_btn_state, players, create_plr_btn_state, already_plr, inc_len


    # Background
    pygame.draw.rect(screen, black, pygame.Rect(256, 256, 512, 256))

    # Text
    label = create_text("Name your player", 32, white)[0]
    screen.blit(label, (256, 256))
    text = create_text(player_name_input, 24, white)[0]
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                player_name_input = player_name_input[:-1]
            elif event.key != pygame.K_ESCAPE:
                player_name_input += event.unicode
    screen.blit(text, (256, 320))

    if create_plr_back_btn.draw():
        create_plr_btn_state = False

    if create_plr_done_btn.draw():
        create_plr_done_btn_state = True

    if create_plr_done_btn_state:
        current_time = datetime.datetime.now()
        if 0 < len(player_name_input) < 16:
            if player_name_input + ".txt" in players:
                already_plr = True
            else:
                _create_player(player_name_input, str(current_time)[:19])
                players.append(player_name_input + ".txt")
                create_plr_done_btn_state = False
                create_plr_btn_state = False
                already_plr = False
            inc_len = False
        else:
            inc_len = True
        create_plr_done_btn_state = False

    if already_plr:
        screen.blit(create_text("Already a player", 32, white)[0], (256, 384))
    if inc_len:
        screen.blit(create_text("Name must have a minimum of one character, and a maximum of 15 character", 32, white)[0], (256, 384))

def level_menu():
    global menu_state, fade_count, create_plr_btn_state
    # Background
    screen.blit(menu_bg_img5, (0, 0))
    screen.blit(menu_bg_img4, (0, 0))
    screen.blit(menu_bg_img3, (0, 0))
    screen.blit(menu_bg_img2, (0, 0))
    screen.blit(menu_bg_img1, (0, 0))

    # Semi-background
    pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(96, 48, 1024 - 192, 768 - 96), border_radius=32)
    
    pygame.draw.rect(screen, white, pygame.Rect(128, 128, 768, 768-256))

    text = create_text("Players", 60, white)[0]
    screen.blit(text, ((SCREEN_WIDTH - text.get_width())// 2, 60))

    if create_plr_btn.draw():
        create_plr_btn_state = True

    # Buttons
    if create_plr_btn_state:
        _create_player_menu()

    if play_menu_back_btn.draw():
        create_plr_btn_state = False
        menu_state = "main"
        fade_count = 0


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
            fade_black()
        fade_in()

    if menu_state == "options":
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_state = "main"
            fade_black()
        fade_in()

    pygame.display.flip()
