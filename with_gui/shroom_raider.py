import sys
import pygame
import datetime
import os
import json
import shroom_raider
import time
import csv
from argparse import ArgumentParser

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (180, 30, 20)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Shroomraider")

menu_state = "main"
default_map = '10 14\nTTTT~~~~~TTTTT\nT.L.~.xT~~~~~T\nT.R.~.~+~TTT~T\nT~.~~.~.~T~T~T\nT~~~~.~R~T~T~T\nT.~.Tx~~~T~T~T\nT...T.~T~T~T~T\nT~+...~..*~+~T\nT~~~~~~~~~~~~T\nTTTTTTTTTTTTTT'
gameplay_state = False, "Player", default_map, "MapName"
playing_from_play = True

# Custom map variables
selected_map = None
map_action_popup = False
create_new_map_btn = None
map_buttons = []
create_new_map_state = False
new_map_name_input = ""
map_name_exists = False
map_name_invalid = False

# Editor variables
editor_active = False
editor_name = ""
EDITOR_ROWS = 25
EDITOR_MAX_COLS = 25
EDITOR_TILE_SIZE = 29
EDITOR_BORDER = 20
EDITOR_GRID_SIZE = EDITOR_TILE_SIZE * EDITOR_ROWS
EDITOR_TILE_TYPES = 9
editor_current_tile = 0
editor_world_data = []
editor_img_list = []
editor_button_list = []

# Create menu bg
create_bg = pygame.image.load("assets/cave_bluelarge.png")
create_bg = pygame.transform.scale(create_bg, (1024, 1024))

clock = pygame.time.Clock()

class Button():
    def __init__(self,x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

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
        global delete_pop_up, create_plr_btn_state, inc_len, already_plr, player_name_input, plr_del_btn_state
        action = False
        pos = pygame.mouse.get_pos()

        if plr_del_btn_state:
            outer_color = (200, 50, 50)
            bg_color = (255, 150, 150)
        else:
            outer_color = (100, 200, 100)
            bg_color = (255, 255, 255)

        # Hover effects
        if not create_plr_btn_state and not delete_pop_up:
            if self.rect.collidepoint(pos):
                bg_outer = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
                bg_outer.fill((0, 0, 0, 0))
                pygame.draw.rect(bg_outer, outer_color, bg_outer.get_rect(), border_radius=16)
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
        pygame.draw.rect(bg, (bg_color), bg.get_rect(), border_radius=16)
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

        return action


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


class text_Button_2():
    # Used for buttons in the map level menu
    def __init__(self, x, y, text, s):
        self.capt = text
        self.s = s

        temp_text = create_text(text, s, (150, 150, 150))[0]
        self.width = temp_text.get_width() + 40
        self.height = 70

        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Hover effect
        if self.rect.collidepoint(pos):
            # Outer glow when hovered
            outer_rect = pygame.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
            pygame.draw.rect(screen, main_color, outer_rect, border_radius=16)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Button background
        if self.hovered:
            pygame.draw.rect(screen, (120, 120, 120), self.rect, border_radius=16)
        else:
            pygame.draw.rect(screen, (150, 150, 150), self.rect, border_radius=16)

        # Border
        pygame.draw.rect(screen, (75, 75, 75), self.rect, width=3, border_radius=16)

        # Text
        text_outer = create_text(self.capt, self.s, black)[0]
        text_main = create_text(self.capt, self.s, main_color)[0]

        text_x = self.x + (self.width - text_main.get_width()) // 2
        text_y = self.y + (self.height - text_main.get_height()) // 2

        screen.blit(text_outer, (text_x + 2, text_y + 2))
        screen.blit(text_main, (text_x, text_y))

        return action


class menu_Button():
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


class level_Button():
    # Used for the level buttons in the map menu
    def __init__(self, x, y, level_num):
        self.level_num = level_num
        self.width = 120
        self.height = 120
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.clicked = False
        self.hovered = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Hover effect
        if self.rect.collidepoint(pos):
            # Outer glow when hovered
            outer_rect = pygame.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
            pygame.draw.rect(screen, main_color, outer_rect, border_radius=16)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            self.hovered = True
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Button background
        if self.hovered:
            pygame.draw.rect(screen, (220, 220, 220), self.rect, border_radius=16)
        else:
            pygame.draw.rect(screen, white, self.rect, border_radius=16)

        # Border
        pygame.draw.rect(screen, (75, 75, 75), self.rect, width=3, border_radius=16)

        # Level number text
        level_text_outer = create_text(str(self.level_num), 64, black)[0]
        level_text = create_text(str(self.level_num), 64, main_color)[0]

        text_x = self.x + (self.width - level_text.get_width()) // 2
        text_y = self.y + (self.height - level_text.get_height()) // 2

        screen.blit(level_text_outer, (text_x + 2, text_y + 2))
        screen.blit(level_text, (text_x, text_y))

        return action


def create_text(text, s, color):
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=s)
    return font.render(text, True, color), text


def fade_black():
    alphaSurface = pygame.Surface((1024, 768), pygame.SRCALPHA)
    alph = 0
    clock = pygame.time.Clock()

    while alph < 245:
        alph += 10

        alphaSurface.set_alpha(alph)
        alphaSurface.fill((0, 0, 0))
        screen.blit(alphaSurface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(480)


def fade_in(surf):
    alphaSurface = pygame.Surface((1024, 768), pygame.SRCALPHA)
    alph = 255
    clock = pygame.time.Clock()

    while alph > 10:
        alph -= 10

        surf()
        alphaSurface.fill((0, 0, 0, alph))
        screen.blit(alphaSurface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(480)


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
play_btn = menu_Button(128, 288, "Play", 60)
create_btn = menu_Button(128, 360, "Create Levels", 60)
lb_btn = menu_Button(128, 432, "Leaderboards", 60)
options_btn = menu_Button(128, 504, "Options", 60)
quit_btn = menu_Button(128, 576, "Quit", 60)

# Play menu buttons
play_menu_back_btn = text_Button_1(148, 640, "Back", 48, white)
page_back = text_Button_1(278, 640, "<", 48, white)
page_next = text_Button_1(304, 640, ">", 48, white)
# Create player button
create_plr_btn = text_Button_1(584, 640, "New Player", 48, white)
create_plr_done_btn = text_Button_1(512, 448, "Done", 48, white)
create_plr_back_btn = text_Button_1((1000 - (24 * 16))//2, 448, "Back", 48, white)
# Delete button
plr_del_btn = text_Button_1(352, 640, "Delete", 48, white)
delete_pop_up_back = text_Button_1((1000 - (24 * 16))//2, 448, "Back", 48, white)
delete_pop_up_confirm = text_Button_1(512, 448, "Confirm", 48, white)
cancel_del_plr_btn = text_Button_1(352, 640, "Cancel", 48, white)
# map buttons
bonus_btn = text_Button_2(180, 550, "Bonus", 48)
story_btn = text_Button_2(375, 550, "Story", 48)
usermade_btn = text_Button_2(575, 550, "User-made", 48)

# States
create_plr_btn_state = False
create_plr_done_btn_state = False
already_plr = False
inc_len = False
plr_del_btn_state = False
delete_pop_up = False
map_level_menu_state = False, 'playername'

who_to_del = ""

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
    global players
    data = {"name": name, "time_created": date, "since_epoch": s, "maps_finished": [], "playing_time": 0, "mush_collected": 0}
    with open(f"data/players/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

player_name_input = ""
def _create_player_menu():
    global player_name_input, create_plr_done_btn_state, players, create_plr_btn_state, already_plr, inc_len, delete_pop_up

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
                    elif event.key != pygame.K_ESCAPE and event.key != pygame.K_MINUS:
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
                _create_player(player_name_input, str(current_time)[:19], time.time()//1)
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
    global delete_pop_up, plr_del_btn_state, who_to_del, map_level_menu_state, players
    # page is 0-indexed
    i = page * 5
    count = 0

    if plr_del_btn_state:
        for player in players[i:i + 5]:
            p = player_on_list(str(player)[:-5], count)
            if p.draw():
                delete_pop_up = True
                who_to_del = player[:-5]
            count += 1
        if delete_pop_up:
            delete_player_confirmation(who_to_del)
    else:
        for player in players[i:i + 5]:
            p = player_on_list(str(player)[:-5], count)
            if p.draw():
                map_level_menu_state = True, player[:-5]
            count += 1

def delete_player_confirmation(player):
    global delete_pop_up, plr_del_btn_state
    # Semi-background
    semibg = pygame.Surface((512, 256), pygame.SRCALPHA)
    semibg.fill((20, 100, 50, 0))

    pygame.draw.rect(semibg, (0, 0, 0, 225), semibg.get_rect(), border_radius=16)
    screen.blit(semibg, (256, 256))

    # Label
    title1 = create_text("Are you sure you", 40, white)[0]
    title2 = create_text(f"want to delete", 40, white)[0]
    title3 = create_text(f"'{player}'?", 40, main_color)[0]
    screen.blit(title1, ((1000 - (24 * 16))//2, 268))
    screen.blit(title2, ((1000 - (24 * 16))//2, 316))
    screen.blit(title3, ((1000 - (24 * 16))//2, 364))

    if delete_pop_up_back.draw():
        delete_pop_up = False

    if delete_pop_up_confirm.draw():
        os.remove(f"data/players/{player}.json")
        delete_pop_up = False
        plr_del_btn_state = False

story_btn_state = False
bonus_btn_state = False
usermade_btn_state = False
level_buttons = []
def map_level_menu(player):
    global menu_state, fade_count, map_level_menu_state, gameplay_state, story_btn_state
    global bonus_btn_state, usermade_btn_state, bonus_levels_buttons, usermade_levels_buttons

    # Background
    screen.blit(menu_bg_img5, (0, 0))
    screen.blit(menu_bg_img4, (0, 0))
    screen.blit(menu_bg_img3, (0, 0))
    screen.blit(menu_bg_img2, (0, 0))
    screen.blit(menu_bg_img1, (0, 0))

    # Blur background
    blur = pygame.Surface((1024, 768), pygame.SRCALPHA)
    blur.fill((0, 0, 0, 50))
    screen.blit(blur, (0, 0))

    # Semi-background panel
    panel_bg = pygame.Surface((824, 640), pygame.SRCALPHA)
    panel_bg.fill((0, 0, 0, 0))
    pygame.draw.rect(panel_bg, (0, 0, 0, 150), panel_bg.get_rect(), border_radius=32)
    pygame.draw.rect(panel_bg, (*white, 255), panel_bg.get_rect(), width=1, border_radius=32)
    screen.blit(panel_bg, (100, 74))

    # Title
    title_outer = create_text("LEVELS", 80, black)[0]
    title = create_text("LEVELS", 80, white)[0]
    screen.blit(title_outer, ((1024 - title.get_width()) // 2 + 3, 103))
    screen.blit(title, ((1024 - title.get_width()) // 2, 100))

    # Back button
    if play_menu_back_btn.draw():
        map_level_menu_state = False, ''

    # Bonus levels button
    if bonus_btn.draw():
        story_btn_state = False
        bonus_btn_state = True
        usermade_btn_state = False

    # Story levels button
    if story_btn.draw():
        story_btn_state = True
        bonus_btn_state = False
        usermade_btn_state = False

    # User made levels button
    if usermade_btn.draw():
        story_btn_state = False
        bonus_btn_state = False
        usermade_btn_state = True

    if story_btn_state:
        map_level_buttons()
        # Draw all level buttons
        for btn in level_buttons:
            if btn.draw():
                level = btn.level_num # This is the level number, should be same with the file name of the map in txt
                with open(f'data/maps/story/{level}.txt') as mapfile:
                    to_text = mapfile.read()
                gameplay_state = True, map_level_menu_state[1], to_text, str(level)

    if bonus_btn_state:
        bonus_level_buttons()
        for btn in bonus_levels_buttons:
            if btn.draw():
                level = btn.level_num # This is the level number, should be same with the file name of the map in txt
                with open(f'data/maps/bonus/{level}.txt') as mapfile:
                    to_text = mapfile.read()
                gameplay_state = True, map_level_menu_state[1], to_text, str(level)

    if usermade_btn_state:
        usermade_level_buttons()
        for btn in usermade_levels_buttons:
            if btn.draw():
                level = btn.level_num # This is the level number, should be same with the file name of the map in txt
                with open(f'data/maps/user_made/{level}.txt') as mapfile:
                    to_text = mapfile.read()
                gameplay_state = True, map_level_menu_state[1], to_text, str(level)


def level_menu():
    global menu_state, fade_count, create_plr_btn_state, delete_pop_up, player_page, plr_del_btn_state, inc_len, already_plr, player_name_input

    # Background
    menu_background()

    if map_level_menu_state[0]:
        map_level_menu(map_level_menu_state[1])
    else:
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
            delete_pop_up = False

        if play_menu_back_btn.draw():
            create_plr_btn_state = False
            delete_pop_up = False
            menu_state = "main"
            fade_count = 0

        if plr_del_btn_state:
            if cancel_del_plr_btn.draw():
                plr_del_btn_state = False
                delete_pop_up = False
                create_plr_btn_state = False
                inc_len = False
                already_plr = False
                player_name_input = ""
        else:
            if plr_del_btn.draw():
                plr_del_btn_state = True
                create_plr_btn_state = False
                inc_len = False
                already_plr = False
                player_name_input = ""

        if page_back.draw():
            player_page = 1
        if page_next.draw():
            player_page = 2

        # Title
        text2 = create_text(f"PLAYERS      Page {player_page}/2", 60, black)[0]
        screen.blit(text2, ((148) + 4, 60))
        text1 = create_text(f"PLAYERS      Page {player_page}/2", 60, white)[0]
        screen.blit(text1, (148, 60))

# Map editor buttons
create_new_map_btn = text_Button_1(SCREEN_WIDTH - 500, 640, "Create New Map", 48, white)
edit_map_btn = text_Button_1(284, 400, "Edit", 48, white)
play_map_btn = text_Button_1(444, 400, "Play", 48, white)
close_popup_btn = text_Button_1(604, 400, "Cancel", 48, white)
create_map_confirm_btn = text_Button_1(580, 448, "Create", 48, white)
create_map_cancel_btn = text_Button_1(280, 448, "Cancel", 48, white)
max_levels_ok_btn = text_Button_1(470, 410, "OK", 48, white)

map_delete_btn = text_Button_1(316, 640, "Delete", 48, white)
map_delete_popup_back = text_Button_1((1000 - (24 * 16))//2, 448, "Back", 48, white)
map_delete_popup_confirm = text_Button_1(512, 448, "Confirm", 48, white)
map_delete_cancel_button = text_Button_1(316, 640, "Cancel", 48, white)
map_delete_btn_state = False
map_delete_popup = False


def reset_editor_data():
    # Reset editor world data to empty state
    global editor_world_data
    editor_world_data = []
    for row in range(EDITOR_ROWS):
        r = [-1] * EDITOR_MAX_COLS
        editor_world_data.append(r)

bonus_levels = [level for level in os.listdir("data/maps/bonus")]
bonus_levels_buttons = []
def bonus_level_buttons():
    global bonus_levels, bonus_levels_buttons
    bonus_levels_buttons = []

    # Displays 10 level buttons in a 2 rows of 5
    start_x = 150
    start_y = 220
    spacing_x = 150
    spacing_y = 180

    for i, level in enumerate(bonus_levels):
        row = i // 5
        col = i % 5
        x = start_x + (col * spacing_x)
        y = start_y + (row * spacing_y)
        bonus_levels_buttons.append(level_Button(x, y, level[:-4]))

usermade_levels = [level for level in os.listdir("data/maps/user_made")]
usermade_levels_buttons = []
def usermade_level_buttons():
    global usermade_levels, usermade_levels_buttons
    usermade_levels_buttons = []

    # Displays 10 level buttons in a 2 rows of 5
    start_x = 150
    start_y = 220
    spacing_x = 150
    spacing_y = 180

    for i, level in enumerate(usermade_levels):
        row = i // 5
        col = i % 5
        x = start_x + (col * spacing_x)
        y = start_y + (row * spacing_y)
        usermade_levels_buttons.append(level_Button(x, y, level[:-4]))

def map_level_buttons():
    global level_buttons
    level_buttons = []

    # Displays 10 level buttons in a 2 rows of 5
    start_x = 150
    start_y = 220
    spacing_x = 150
    spacing_y = 180

    for i in range(10):
        row = i // 5
        col = i % 5
        x = start_x + (col * spacing_x)
        y = start_y + (row * spacing_y)
        level_buttons.append(level_Button(x, y, i + 1))


def load_editor_assets():
    global editor_img_list, editor_world_data, editor_button_list, save_editor_btn, exit_editor_btn
    global editor_active, create_new_map_state, map_action_popup, selected_map, new_map_name_input, map_name_exists, map_name_invalid, menu_state, fade_count

    # Load tile images
    editor_img_list = []
    for x in range(EDITOR_TILE_TYPES):
        img = pygame.image.load(f'img/{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (EDITOR_TILE_SIZE, EDITOR_TILE_SIZE))
        editor_img_list.append(img)

    # Create empty tile list (if not already loaded from file)
    if not editor_world_data:
        reset_editor_data()

    # Create save and exit buttons for editor
    save_surf = pygame.Surface((100, 40))
    save_surf.fill((200, 25, 25))
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=24)
    text = font.render("SAVE", True, white)
    text_rect = text.get_rect(center=(50, 20))
    save_surf.blit(text, text_rect)

    exit_surf = pygame.Surface((100, 40))
    exit_surf.fill((200, 25, 25))
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=24)
    text = font.render("EXIT", True, white)
    text_rect = text.get_rect(center=(50, 20))
    exit_surf.blit(text, text_rect)

    EDITOR_SCREEN_WIDTH = 1024 - 200
    SIDE_MARGIN = 200

    save_editor_btn = Button(EDITOR_SCREEN_WIDTH + SIDE_MARGIN - 190, 768 // 2 + 220, save_surf, 1)
    exit_editor_btn = Button(EDITOR_SCREEN_WIDTH + SIDE_MARGIN - 190, 768 // 2 + 280, exit_surf, 1)

    # Create tile selection buttons
    editor_button_list = []
    button_col = 0
    button_row = 0

    for i in range(len(editor_img_list)):
        tile_button = Button(
            EDITOR_SCREEN_WIDTH + (60 * button_row) + 35,  # Adjust tile buttons horizontally
            (60 * button_col) + 55,  # Adjust tile buttons vertically
            editor_img_list[i],
            1.5
        )
        editor_button_list.append(tile_button)
        button_col += 1

    # Exit button - return to create menu
    if exit_editor_btn.draw(screen):
        print('exit')
        editor_active = False
        create_new_map_state = False
        map_action_popup = False
        selected_map = None
        new_map_name_input = ""
        map_name_exists = False
        map_name_invalid = False
        menu_state = "create"
        fade_count = 1
        # Reset editor data
        reset_editor_data()
        return


def csv_to_map(file_path):
    # Turns csv content into playable map in string form
    csv_data = []
    final_map = []
    first_row, last_row, first_col, last_col = 0, 0, 0, 0

    # Read CSV data into a 2D list
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csv_data.append(row)

    matrix = [[-1 if int(cell) == 8 else int(cell) for cell in row] for row in csv_data]
    # Transpose to check columns
    transposed = list(zip(*matrix))

    # Find first row with non -1 values
    for i in range(len(matrix)):
        if any(char != -1 for char in matrix[i]):
            first_row = i
            break

    # Find last row with non -1 values
    for i in range(len(matrix) - 1, -1, -1):
        if any(char != -1 for char in matrix[i]):
            last_row = i
            break

    # Find first column with non -1 values
    for i in range(len(transposed)):
        if any(char != -1 for char in transposed[i]):
            first_col = i
            break

    # Find last column with non -1 values
    for i in range(len(transposed) - 1, -1, -1):
        if any(char != -1 for char in transposed[i]):
            last_col = i
            break

    # Extract valid area and convert to strings
    for i in range(first_row, last_row + 1):
        row_data = []
        for j in range(first_col, last_col + 1):
            row_data.append(str(matrix[i][j]))
        final_map.append(', '.join(row_data))

    map_str = '\n'.join(row for row in final_map)

    convert_to_ascii = {
        '-1': '.',
        '0': 'L',
        '1': '.',
        '2': '~',
        '3': 'T',
        '4': '+',
        '5': 'R',
        '6': 'x',
        '7': '*',
        '\n': '\n'
    }

    converted = ''.join(convert_to_ascii.get(c, c) for c in map_str if c in convert_to_ascii)

    map_rows = str(converted.count('\n') + 1)
    if '\n' in converted:
        map_cols = str(len(converted[:converted.index('\n')]))
    else:
        map_cols = str(len(converted))

    return map_rows + ' ' + map_cols + '\n' + converted + '\n'


def editor_laro_warning():
    # Error pop up box showing "laro can only be placed once" and exits once mouse clicks outside grid
    overlay = pygame.Surface((768, 1024 - 200), pygame.SRCALPHA)
    box_rect = pygame.Rect(165, 350, 450, 100)
    gray_with_alpha = (128, 128, 128, 120)
    pygame.draw.rect(overlay, gray_with_alpha, box_rect, border_radius=10)

    text1 = create_text("Laro can only be placed once!", 26, black)[0]
    text2 = create_text("Click outside the grid to continue.", 14, black)[0]
    text_rect1 = text1.get_rect(center=box_rect.center)
    text_rect2 = text1.get_rect(center=box_rect.center)
    text_rect2.y += 40

    overlay.blit(text1, text_rect1)
    screen.blit(overlay, (0, 0))
    overlay.blit(text2, text_rect2)
    screen.blit(overlay, (0, 0))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def laro_save_warning():
    # Error pop up box showing "you can't play without laro craft" and exits once mouse clicks anywhere
    overlay = pygame.Surface((768, 1024 - 200), pygame.SRCALPHA)
    box_rect = pygame.Rect(165, 350, 500, 90)
    gray_with_alpha = (128, 128, 128, 120)
    pygame.draw.rect(overlay, gray_with_alpha, box_rect, border_radius=10)

    text1 = create_text("You can't play without Laro Craft!", 26, black)[0]
    text2 = create_text("Click anywhere to continue.", 14, black)[0]
    text_rect1 = text1.get_rect(center=box_rect.center)
    text_rect2 = text1.get_rect(center=box_rect.center)
    text_rect2.y += 40

    overlay.blit(text1, text_rect1)
    screen.blit(overlay, (0, 0))
    overlay.blit(text2, text_rect2)
    screen.blit(overlay, (0, 0))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def mush_save_warning():
    # Error pop up box showing "you can't play without mushrooms" and exits once mouse clicks anywhere
    overlay = pygame.Surface((768, 1024 - 200), pygame.SRCALPHA)
    box_rect = pygame.Rect(165, 350, 500, 90)
    gray_with_alpha = (128, 128, 128, 120)
    pygame.draw.rect(overlay, gray_with_alpha, box_rect, border_radius=10)

    text1 = create_text("You can't play without mushrooms!", 26, black)[0]
    text2 = create_text("Click anywhere to continue.", 14, black)[0]
    text_rect1 = text1.get_rect(center=box_rect.center)
    text_rect2 = text1.get_rect(center=box_rect.center)
    text_rect2.y += 40

    overlay.blit(text1, text_rect1)
    screen.blit(overlay, (0, 0))
    overlay.blit(text2, text_rect2)
    screen.blit(overlay, (0, 0))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def level_editor():
    global menu_state, editor_active, editor_current_tile, editor_world_data, fade_count
    global map_action_popup, selected_map, new_map_name_input, map_name_exists, map_name_invalid, create_new_map_state, usermade_levels

    screen.blit(create_bg, (0, 0))
    gray_bg = pygame.Surface((1024, 1024), pygame.SRCALPHA)
    gray_bg.fill((0, 0, 0, 50))
    screen.blit(gray_bg, (0, 0))

    map_bg = pygame.Surface((EDITOR_GRID_SIZE, EDITOR_GRID_SIZE), pygame.SRCALPHA)
    map_bg.fill((0, 0, 0, 0))
    pygame.draw.rect(map_bg, (0, 0, 0, 150), map_bg.get_rect())
    pygame.draw.rect(map_bg, (*white, 255), map_bg.get_rect(), width=1)
    screen.blit(map_bg, (EDITOR_BORDER, EDITOR_BORDER))

    # draw grid
    for c in range(1, EDITOR_MAX_COLS + 1):  # vertical lines
        pygame.draw.line(screen, (169, 169, 169), (c * EDITOR_TILE_SIZE + 20, 20), (c * EDITOR_TILE_SIZE + 20, EDITOR_GRID_SIZE + EDITOR_BORDER))
    for c in range(1, EDITOR_ROWS + 1):  # horizontal lines
        pygame.draw.line(screen, (169, 169, 169), (20, c * EDITOR_TILE_SIZE + 20), (EDITOR_GRID_SIZE + EDITOR_BORDER, c * EDITOR_TILE_SIZE + 20))

    # draw world map
    for y, row in enumerate(editor_world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < 8:
                screen.blit(editor_img_list[tile], (x * EDITOR_TILE_SIZE + EDITOR_BORDER, y * EDITOR_TILE_SIZE + EDITOR_BORDER))

    # draw tile panel
    side_bg = pygame.Surface((160, 700), pygame.SRCALPHA)
    side_bg.fill((0, 0, 0, 0))
    pygame.draw.rect(side_bg, (0, 0, 0, 150), side_bg.get_rect())
    pygame.draw.rect(side_bg, (*white, 255), side_bg.get_rect(), width=1, border_radius=24)
    screen.blit(side_bg, (800, 30))

    # Save button
    if save_editor_btn.draw(screen):
        check_laro = any(0 in data for data in editor_world_data) # Checks if a laro craft is in the created level
        check_mush = any(4 in data for data in editor_world_data) # Checks if a mushroom is in the created level
        if not check_laro:
            laro_save_warning()
        elif not check_mush:
            mush_save_warning()
        else:
            # Saves first in csv file then turns it to txt file
            with open(f'data/maps/csv_user_made/{editor_name}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in editor_world_data:
                    writer.writerow(row)
            with open(f'data/maps/user_made/{editor_name}.txt', 'w') as txtfile:
                txtfile.write(csv_to_map(f'data/maps/csv_user_made/{editor_name}.csv'))
            usermade_levels.append(f"{editor_name}.txt")

    # Exit button - return to create menu
    if exit_editor_btn.draw(screen):
        editor_active = False
        create_new_map_state = False
        map_action_popup = False
        selected_map = None
        new_map_name_input = ""
        map_name_exists = False
        map_name_invalid = False
        menu_state = "create"
        fade_count = 0
        # Reset editor data
        reset_editor_data()
        return

    # Choose a tile
    button_count = 0
    for button_count, i in enumerate(editor_button_list):
        if i.draw(screen):
            editor_current_tile = button_count

    # Highlight the selected tile
    pygame.draw.rect(screen, main_color, editor_button_list[editor_current_tile].rect, 2)

    # Add new tiles to the screen
    pos = pygame.mouse.get_pos()
    x = (pos[0] - EDITOR_BORDER) // EDITOR_TILE_SIZE
    y = (pos[1] - EDITOR_BORDER) // EDITOR_TILE_SIZE

    # Check that the coordinates are within the tile area
    if EDITOR_BORDER < pos[0] < EDITOR_GRID_SIZE + EDITOR_BORDER and EDITOR_BORDER < pos[1] < EDITOR_GRID_SIZE + EDITOR_BORDER:
        if pygame.mouse.get_pressed()[0] == 1:
            if editor_world_data[y][x] != editor_current_tile:
                if editor_current_tile == 0:
                    check_laro = any(0 in data for data in editor_world_data)
                    if check_laro:
                        editor_laro_warning()
                    else:
                        editor_world_data[y][x] = editor_current_tile
                else:
                    editor_world_data[y][x] = editor_current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            editor_world_data[y][x] = -1


def _create_new_map_dialog():
    global new_map_name_input, create_new_map_state, map_name_exists, map_name_invalid, editor_active, editor_name
    global editor_world_data

    # Background overlay
    overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Dialog box
    pygame.draw.rect(screen, black, pygame.Rect(256, 256, 512, 256))
    pygame.draw.rect(screen, main_color, pygame.Rect(256, 256, 512, 256), width=4)

    # Text
    label = create_text("Enter Level Name", 32, white)[0]
    screen.blit(label, (512 - label.get_width() // 2, 280))

    # Input field background
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(280, 340, 464, 40))
    pygame.draw.rect(screen, white, pygame.Rect(280, 340, 464, 40), width=2)

    # Display input text
    text = create_text(new_map_name_input, 24, white)[0]
    screen.blit(text, (290, 348))

    # Handle text input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                new_map_name_input = new_map_name_input[:-1]
                map_name_exists = False
                map_name_invalid = False
            elif event.key == pygame.K_RETURN:
                if 0 < len(new_map_name_input) < 30:
                    existing_maps = os.listdir('data/maps/csv_user_made') if os.path.exists('data/maps/csv_user_made') else []
                    if new_map_name_input + '.csv' not in existing_maps:
                        # Launch editor internally
                        editor_name = new_map_name_input
                        reset_editor_data()  # Start with empty map
                        editor_active = True
                        create_new_map_state = False
                        new_map_name_input = ""
                        load_editor_assets()
                    else:
                        map_name_exists = True
                else:
                    map_name_invalid = True
            elif event.key != pygame.K_ESCAPE and len(new_map_name_input) < 29:
                if event.unicode.isalnum() or event.unicode in ' -_':
                    new_map_name_input += event.unicode
                    map_name_exists = False
                    map_name_invalid = False

    # Cancel button
    if create_map_cancel_btn.draw():
        create_new_map_state = False
        new_map_name_input = ""
        map_name_exists = False
        map_name_invalid = False

    # Create button
    if create_map_confirm_btn.draw():
        if 0 < len(new_map_name_input) < 30:
            existing_maps = os.listdir('data/maps/csv_user_made') if os.path.exists('data/maps/csv_user_made') else []
            if new_map_name_input + '.csv' not in existing_maps:
                # Launch editor internally
                editor_name = new_map_name_input
                reset_editor_data()  # Start with empty map
                editor_active = True
                create_new_map_state = False
                new_map_name_input = ""
                load_editor_assets()
            else:
                map_name_exists = True
        else:
            map_name_invalid = True

    # Error messages
    if map_name_exists:
        error_text = create_text("A map with this name already exists!", 20, (255, 100, 100))[0]
        screen.blit(error_text, (512 - error_text.get_width() // 2, 400))

    if map_name_invalid:
        error_text = create_text("Name must be 1-29 characters long", 20, (255, 100, 100))[0]
        screen.blit(error_text, (512 - error_text.get_width() // 2, 400))


def create_menu():
    global menu_state, fade_count, selected_map, map_action_popup, map_buttons, create_new_map_state, editor_active, editor_world_data
    global editor_name, new_map_name_input, map_name_exists, map_name_invalid, gameplay_state, playing_from_play
    global map_delete_popup_back, map_delete_popup_confirm, map_delete_btn, map_delete_cancel, map_delete_btn_state, map_delete_popup, usermade_levels


    # Background
    menu_background()

    # Background surface
    bg_surf = pygame.Surface((1024 - 192, 768 - 96), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 0))

    # Semi-background
    pygame.draw.rect(bg_surf, (75, 75, 75, 100), bg_surf.get_rect(), border_radius=32)
    screen.blit(bg_surf, (96, 48))

    # Title
    text = create_text("Created Maps", 60, white)[0]
    screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 60))

    # Get custom maps
    custom_maps = []
    if os.path.exists('data/maps/csv_user_made'):
        for maps in os.listdir('data/maps/csv_user_made'):
            custom_maps.append(maps)

    # Create buttons for each map
    if not map_action_popup and not create_new_map_state:
        map_buttons = []
        y_pos = 135
        for i, map_name in enumerate(custom_maps):
            # Remove file extension for display
            display_name = map_name.replace('.csv', '')
            btn = text_Button_1(160, y_pos, display_name, 32, white)
            map_buttons.append((btn, map_name))
            y_pos += 50

            # Check if map is clicked
            if btn.draw():
                # Checks first if delete button is clicked
                if map_delete_btn_state:
                    map_delete_popup = True
                else:
                    map_action_popup = True
                selected_map = map_name

    # Show popup if a map is selected
    if map_action_popup and selected_map and not create_new_map_state:
        # Darken background
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Popup box
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(256, 256, 512, 256), border_radius=16)
        pygame.draw.rect(screen, main_color, pygame.Rect(256, 256, 512, 256), width=4, border_radius=16)

        # Selected map name
        map_text = create_text(f"Map: {selected_map.replace('.csv', '')}", 36, white)[0]
        screen.blit(map_text, (512 - map_text.get_width() // 2, 300))

        # Action buttons
        if edit_map_btn.draw():
            # Load existing map and launch editor
            editor_name = selected_map.replace('.csv', '')

            # Load the map data
            try:
                with open(f'data/maps/csv_user_made/{selected_map}', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    editor_world_data = []
                    for row in reader:
                        # Handle empty values and convert to int
                        processed_row = []
                        for tile in row:
                            if tile.strip() == '' or tile.strip() == '-1':
                                processed_row.append(-1)
                            else:
                                try:
                                    processed_row.append(int(tile))
                                except ValueError:
                                    processed_row.append(-1)
                        editor_world_data.append(processed_row)

                    # Ensure we have exactly EDITOR_ROWS rows
                    while len(editor_world_data) < EDITOR_ROWS:
                        editor_world_data.append([-1] * EDITOR_MAX_COLS)

                    # Ensure each row has exactly EDITOR_MAX_COLS columns
                    for i in range(len(editor_world_data)):
                        while len(editor_world_data[i]) < EDITOR_MAX_COLS:
                            editor_world_data[i].append(-1)
                        # Trim if too long
                        editor_world_data[i] = editor_world_data[i][:EDITOR_MAX_COLS]

                    # Trim to exact row count
                    editor_world_data = editor_world_data[:EDITOR_ROWS]

            except Exception as e:
                print(f"Error loading map: {e}")
                reset_editor_data()

            # Reset all states before entering editor
            editor_active = True
            map_action_popup = False
            create_new_map_state = False
            selected_map = None
            new_map_name_input = ""
            map_name_exists = False
            map_name_invalid = False

            load_editor_assets()

        if play_map_btn.draw():
            level_map = csv_to_map(f'data/maps/csv_user_made/{selected_map}') # This is the string format of the map
            gameplay_state = True, 'testingfrommap', level_map, f'{selected_map}'
            playing_from_play = False
            map_action_popup = False
            selected_map = None

        if close_popup_btn.draw():
            map_action_popup = False
            selected_map = None

    # Show delete popup if a map is selected
    if not map_action_popup and not create_new_map_state:
        if map_delete_popup:
            # Semi-background
            semibg = pygame.Surface((512, 256), pygame.SRCALPHA)
            semibg.fill((20, 100, 50, 0))

            pygame.draw.rect(semibg, (0, 0, 0, 225), semibg.get_rect(), border_radius=16)
            screen.blit(semibg, (256, 256))

            # Label
            title1 = create_text("Are you sure you", 40, white)[0]
            title2 = create_text(f"want to delete", 40, white)[0]
            title3 = create_text(f"'{selected_map[:-4]}'?", 40, main_color)[0]
            screen.blit(title1, ((1000 - (24 * 16))//2, 268))
            screen.blit(title2, ((1000 - (24 * 16))//2, 316))
            screen.blit(title3, ((1000 - (24 * 16))//2, 364))

            if map_delete_popup_back.draw():
                map_delete_popup = False

            if map_delete_popup_confirm.draw():
                os.remove(f"data/maps/csv_user_made/{selected_map}")
                os.remove(f"data/maps/user_made/{selected_map[:-4]}.txt")
                usermade_levels.remove(f'{selected_map[:-4]}.txt')
                map_delete_popup = False
                map_delete_btn_state = False


    # stay in create menu
    if not map_action_popup and editor_active:
        menu_state = "create"
        fade_count = 0

    # Show new map creation dialog
    if create_new_map_state:
        saved_dir_path = r'data/maps/csv_user_made'
        saved_count = len([entry for entry in os.listdir(saved_dir_path) if os.path.isfile(os.path.join(saved_dir_path, entry))])
        if saved_count < 10:
            _create_new_map_dialog()
        else:
            # Show max levels error popup
            overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            # Error dialog box
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(256, 256, 500, 230), border_radius=16)
            pygame.draw.rect(screen, main_color, pygame.Rect(256, 256, 500, 230), width=4, border_radius=16)

            error_msg1 = create_text("You have reached the maximum", 24, (200, 200, 200))[0]
            error_msg2 = create_text("of 10 created levels.", 24, (200, 200, 200))[0]
            error_msg3 = create_text("Delete a level to create a new one.", 20, (150, 150, 150))[0]

            screen.blit(error_msg1, (512 - error_msg1.get_width() // 2, 300))
            screen.blit(error_msg2, (512 - error_msg2.get_width() // 2, 330))
            screen.blit(error_msg3, (512 - error_msg3.get_width() // 2, 380))

            # OK button to close
            if max_levels_ok_btn.draw():
                create_new_map_state = False

    # Create new map button (only show if not in popup)
    if not map_action_popup and not create_new_map_state:
        if create_new_map_btn.draw():
            create_new_map_state = True
            new_map_name_input = ""

    # Back button
    if not map_action_popup and not create_new_map_state:
        if play_menu_back_btn.draw() and not map_action_popup and not create_new_map_state:
            menu_state = "main"
            fade_count = 0

        if map_delete_btn_state:
            if map_delete_cancel_button.draw():
                map_delete_btn_state = False
        else:
            if map_delete_btn.draw():
                map_delete_btn_state = True


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


# GAME LOGIC STARTS HERE
def add_args():
    ''' Adds arguments, will only be called if __name__ == "__main__" below '''
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-f', '--stage_file')
    parser.add_argument('-m', '--movement')
    parser.add_argument('-o', '--output_file')
    return parser.parse_args()

def pick_map(stage_file=None):
    ''' Returns default map if there's no stage_file, else returns the stage file '''
    global default_map
    if stage_file == None:
        return default_map
    else:
        with open(stage_file, "r", encoding="utf-8") as lvl:
          return lvl.read()

def choose_mode(output_file=None):
    ''' Checks if -o has an argument, returns either "play" or an empty string to determine the mode'''
    return 'play' if output_file is None else ''

if __name__ == "__main__":
    args = add_args()
    mode = choose_mode(args.output_file) # Mode if to play or to output
    lvlmap = pick_map(args.stage_file) # Map as string/raw
else:
    mode = choose_mode() # Mode if to play or to output
    lvlmap = pick_map() # Map as string/raw

def game_function(player="default-Player", level_map=None, level_map_name="default-Map"):
    global menu_state, gameplay_state, mode, lvlmap, playing_from_play, args, lvlmap

    class gameplay_Text_Button():
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
            nonlocal menu_btn_state, controls_popup_state
            action = False
            pos = pygame.mouse.get_pos()

            if self.capt == "MENU" or self.capt == "RESTART":
                if not menu_btn_state and not controls_popup_state and not lose_state and not LVL_MUSHROOMS == player_mushroom_count:
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
            else:
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

    # Assets: Tiles
    tree_img = pygame.image.load("assets/tiles/tree.png")
    plr_img = pygame.image.load("assets/tiles/plr.png")
    empty_img = pygame.image.load("assets/tiles/empty.png")
    pavement_img = pygame.image.load("assets/tiles/pavement.png")
    water_img = pygame.image.load("assets/tiles/water.png")
    rock_img = pygame.image.load("assets/tiles/rock.gif")
    axe_img = pygame.image.load("assets/tiles/axe.png")
    flamethrower_img = pygame.image.load("assets/tiles/flamethrower.png")
    mush_img = pygame.image.load("assets/tiles/mush.png")

    # Pause menu buttons
    menu_resume_btn = gameplay_Text_Button((6 * 48)//4 + (SCREEN_WIDTH - (6 * 48))//2, 192, "Resume", 48, white)
    menu_controls_btn = gameplay_Text_Button((8 * 48)//4 + (SCREEN_WIDTH - (8 * 48))//2, 252, "Controls", 48, white)
    menu_return_btn = gameplay_Text_Button((13 * 48)//4 + (SCREEN_WIDTH - (13 * 48))//2, 310, "Back to Maps", 48, white)
    controls_back_btn = gameplay_Text_Button((4 * 48)//4 + (SCREEN_WIDTH - (4 * 48))//2, 368, "Back", 48, white)
    menu_btn_state = False
    menu_controls_btn_state = False
    controls_popup_state = False

    # Lose popup
    lose_state = False

    # level bg
    level_bg = pygame.image.load("assets/cave_bluelarge.png")
    level_bg = pygame.transform.scale(level_bg, (1024, 768))

    if level_map:
        lvlmap = level_map

    # Main loop 'count'
    main = 0

    # Makes a list with the tiles as its elements from "lvlmap" excluding the values for the height and width
    lvlmapcontent = list(lvlmap[lvlmap.index('\n')+1:])

    # Takes the integer strings at their respective indices (height before ' '; width after ' ' and before the first \n) and converts into integers
    try:
        GRID_HEIGHT = int(lvlmap[:lvlmap.index(' ')])
        GRID_WIDTH = int(lvlmap[lvlmap.index(' ')+1: lvlmap.index('\n')])
    except (TypeError, IndexError):
        print("INVALID MAP")
        raise TypeError

    # Serves as the base grid for the level (will not be mutated)
    MOTHERGRID = list(''.join(lvlmapcontent))

    # Serves as the working grid for the level (will be mutated)
    grid = list(''.join(lvlmapcontent))

    # Counts the amount of mushrooms needed to win the level
    LVL_MUSHROOMS = 0
    for x in lvlmap:
        if x == "+":
            LVL_MUSHROOMS += 1

    # Lists the indices of '\n' characters
    _n_indices = range(lvlmapcontent.index('\n'), len(lvlmapcontent), GRID_WIDTH + 1)

    # Default player attributes
    item = []
    history = {'player': ['.']}
    found_item = None
    drowned = False
    player_mushroom_count = 0
    player_index = grid.index('L')

    # Library of inputs with their corresponding change in index (+1 in width to accommodate for the '\n' characters)
    moves = {
        'W': -(GRID_WIDTH + 1),
        'S': GRID_WIDTH + 1,
        'A': -1,
        'D': 1,
        'P': 0
    }

    def pickup(tile):
        # Adds current tile to the list of items held by the player
        item.append(tile)

    def flame_spread(start_row, start_col):
        # Returns the new map when flamethrower is used, or when player approaches tree while holding flamethrower
        nonlocal grid

        grid_string = ''.join(grid)
        grid_2d_list = [list(row) for row in grid_string.strip().split('\n')]
        row, col = len(grid_2d_list), len(grid_2d_list[0])

        def in_bounds(r, c):
            # Returns True if 2d index is within the range of row and column
            return 0 <= r < row and 0 <= c < col

        def flamethrowed(r, c):
            # Replaces 'T' to '.' if another 'T' shares the same side with the initial approached 'T' and is within the bounds else the recursion stops
            if not in_bounds(r, c) or grid_2d_list[r][c] != 'T':
                return
            grid_2d_list[r][c] = '.'

            # Continously calls itself for every direction 
            for change_row, change_col in [(-1,0), (1,0), (0,-1), (0,1)]:
                flamethrowed(r + change_row, c + change_col)

        # Will only call flamethrowed if the player is approaching 'T'
        if grid_2d_list[start_row][start_col] == 'T':
            flamethrowed(start_row, start_col)

        new_grid_string = '\n'.join(''.join(row) for row in grid_2d_list)

        return list(new_grid_string)

    def describe_tile(tile):
        # Returns a tile converted from ASCII character to its tile name
        return {
            '.': 'empty',
            'T': 'tree',
            '+': 'mushroom',
            'R': 'rock',
            'L': 'player',
            '`': 'water',
            '_': 'paved',
            'x': 'axe',
            '*': 'flamethrower',
            None: 'Nothing',
        }.get(tile, 'unknown')

    def _move_player(direction):

        # Takes the directional input of the player and moves the player accordingly

        nonlocal player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item, drowned
        global mode

        def moveto(under_tile):

            # Mutates the grid; Doesn't return anything
            nonlocal player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history

            # Sets the tile left behind by the player as the tile it previously was based on the history list
            grid[player_index] = f"{history['player'][0]}" 
            history['player'].pop()

            # Sets the tile at new_index as the player tile
            grid[new_index] = 'L'

            # Updates the current player_index
            player_index = new_index

            # Appends the under_tile(the tile the player moved to) into the history list
            history['player'].append(under_tile)

        # The targeted index of the player based on the move
        new_index = player_index + moves[direction]

        # Checks if either the targeted index is out of bounds
        if not (0 <= new_index < len(grid)) or new_index in _n_indices: # Avoids the mutation of \n indices: 
            if mode == "play":
                print("You can't move outside the grid!")
            return

        else:
            # Gets the tile of the targeted index
            target_tile = grid[new_index]

            # Checks the nature of the targeted tile
            if target_tile == 'T':
                if not item: # Player will not move anywhere if not holding an axe
                    if mode == "play":
                        print("You bumped into a tree!")
                elif item[0] == 'x': # Tree will turn into empty space if player is holding an axe
                    moveto('.')
                    item.clear() # Item is cleared every time after used
                    found_item = None
                elif item[0] == '*': # flame_spread function is called when player is holding flamethrower
                    col = (new_index % (GRID_WIDTH+1))
                    row = (new_index - col) // GRID_WIDTH
                    grid = flame_spread(row, col)
                    moveto('.')
                    item.clear() # Item is cleared every time after used
                    found_item = None
                return

            elif target_tile == 'R':

                # New position of the rock as it moves along with the player
                new_rock_index = new_index + moves[direction]

                if mode == "play":

                    # Checks if it is possible to move the rock to the new index
                    rock_under_tile = '.'

                    if f"Rock {new_index}" in history:  # Sets the tile under the rock based on history, so that the 'moveto' function appends the correct under_tile when the player moves
                        rock_under_tile = history[f"Rock {new_index}"]

                    if new_rock_index >= len(grid) or new_rock_index in _n_indices: # Checks if it will go out of bounds or in a '\n' index
                        print("You can't move the rock there")
                        return

                    elif grid[new_rock_index] == "~":   # Converts a water tile into a paved tile
                        grid[new_rock_index] = "_"
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == ".":    # Moves the rock along an empty tile
                        grid[new_rock_index] = "R"
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == "_":   # Moves the rock along a paved tile
                        grid[new_rock_index] = "R"
                        history[f"Rock {new_rock_index}"] = "_" # Takes note of the tile under the rock
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == "R" or 'x' or '*':   # Checks if the player is trying to move two rocks at the same time or into a non-empty tile
                        print("You can't push the rock there!")
                        return

                    if f"Rock {new_index}" in history:    # Removes the Rock at index new_index from history after it gets moved
                        del history[f"Rock {new_index}"]

                    return

                else:
                    if new_rock_index >= len(grid) or new_rock_index in _n_indices: # Checks if it will go out of bounds or in a '\n' index
                        print("You can't move the rock there")
                        return
                    elif grid[new_rock_index] == "~":   # Converts a water tile into a paved tile
                        grid[new_rock_index] = "_"
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == ".":    # Moves the rock along an empty tile
                        grid[new_rock_index] = "R"
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == "_":   # Moves the rock along a paved tile
                        grid[new_rock_index] = "R"
                        history[f"Rock {new_rock_index}"] = "_" # Takes note of the tile under the rock
                        moveto(rock_under_tile)

                    elif grid[new_rock_index] == "R" or 'x' or '*':   # Checks if the player is trying to move two rocks at the same time or into a non-empty tile
                        print("You can't push the rock there!")
                        return

                if f"Rock {new_index}" in history:  # Removes the Rock at index new_index from history after it gets moved
                        del history[f"Rock {new_index}"]

                return

            elif target_tile == '~':

                # Moves the player into the water
                moveto('~')

                # Changes the following player attributes
                drowned = True

                return

            elif target_tile == "+":

                # Increases the collected mushroom count of the player
                player_mushroom_count += 1

                # Checks if the player has reached the required amount of mushrooms
                if player_mushroom_count == LVL_MUSHROOMS:
                    moveto('+')

                # Moves the player and leaves an empty tile
                moveto('.')
                return

            elif target_tile == "x":

                # Updates the found item as an axe
                found_item = 'x'
                moveto('x')

                return

            elif target_tile == "*":

                # Updates the found item as a flamethrower
                found_item = '*'
                moveto('*')

                return

            elif target_tile == "_":

                # No items in a paved tile
                found_item = None
                moveto('_')

                return

            else:

                # No items in an empty tile
                found_item = None
                moveto('.')

                return

    def move_player(direction):

        # Takes the user input and proceeds accordingly
        nonlocal player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item

        # Processes each input in a string of inputs
        for inp in direction:
            inp = inp.upper()
            if main == 0:
                if inp == 'Q':
                    main += 1

                elif inp == 'P':
                    # Picks up the found item
                    if mode == "play":
                        if not found_item:
                            print("Invalid move. Use W, A, S, D.")
                        elif len(item) == 1:
                            print('You already have an item, you can\'t pickup another')
                        else:
                            pickup(found_item)
                            found_item = None
                            history['player'][-1] = '.' # Sets the previous tile as an empty tile after picking up the item
                    else:
                        if not found_item:
                            pass
                        elif len(item) == 1:
                            pass
                        else:
                            pickup(found_item)
                            found_item = None
                            history['player'][-1] = '.' # Sets the previous tile as an empty tile after picking up the item

                elif inp == "!":
                    # Restarts the game

                    # Restores the player attributes back to default
                    player_index = MOTHERGRID.index('L')
                    grid = list(MOTHERGRID)
                    found_item = None
                    item = []
                    history = {'player': ['.']}
                    player_mushroom_count = 0

                elif inp in moves:
                    _move_player(inp)

                # Breaks the loop when an invalid input is detected
                else:
                    break
            else:
                break

    time_when_called = time.time()
    disposable = True
    lost_at_time = time.time()
    won_at_time = time.time()

    if GRID_WIDTH >= GRID_HEIGHT:
        scale1 = 704 // (GRID_WIDTH)
        y_offset = (768 - (GRID_HEIGHT * scale1)) // 2
        x_offset = (768 - 704) // 2
    else:
        scale1 = 704 // (GRID_HEIGHT)
        y_offset = (768 - (GRID_HEIGHT * scale1)) // 2
        x_offset = (768 - 704) // 2

    scale = (scale1, scale1)

    tile_assets = {
    '.': empty_img,
    'L': plr_img,
    'T': tree_img,
    '+': mush_img,
    'R': rock_img,
    '~': water_img,
    '_': pavement_img,
    'x': axe_img,
    '*': flamethrower_img,
    '\n': '\n'
    }

    tile_assets_scaled = {
    '.': pygame.transform.scale(empty_img, scale),
    'L': pygame.transform.scale(plr_img, scale),
    'T': pygame.transform.scale(tree_img, scale),
    '+': pygame.transform.scale(mush_img, (scale1//2, scale1//2)),
    'R': pygame.transform.scale(rock_img, scale),
    '~': pygame.transform.scale(water_img, scale),
    '_': pygame.transform.scale(pavement_img, scale),
    'x': pygame.transform.scale(axe_img, scale),
    '*': pygame.transform.scale(flamethrower_img, scale),
    '\n': '\n'
    }

    def load_map(level):
        nonlocal drowned
        map_surface = pygame.Surface((704, (GRID_HEIGHT * scale1)), pygame.SRCALPHA)
        map_surface.fill((0, 0, 0, 0))
        current_row = 0
        current_col = 0
        for tile in level:
            if tile != '\n':
                if tile == '+':
                    map_surface.blit(tile_assets_scaled.get('.'), ((scale1 * current_col), (scale1 * current_row)))
                    map_surface.blit(tile_assets_scaled.get(tile, tile), ((scale1 * current_col) + (scale1 // 4), (scale1 * current_row ) + (scale1 // 4)))
                    current_col += 1
                else:
                    if tile == 'L' and drowned:
                        map_surface.blit(tile_assets_scaled.get('~'), ((scale1 * current_col), (scale1 * current_row)))
                    else:
                        map_surface.blit(tile_assets_scaled.get('.'), ((scale1 * current_col), (scale1 * current_row)))
                    map_surface.blit(tile_assets_scaled.get(tile, tile), ((scale1 * current_col), (scale1 * current_row)))
                    current_col += 1
            else:
                current_row += 1
                current_col = 0
        return map_surface

    def controls_popup():
        nonlocal controls_back_btn, controls_popup_state, menu_btn_state
        global SCREEN_WIDTH
        
        # Cover
        cover = pygame.Surface((1024, 768), pygame.SRCALPHA)
        cover.fill((0, 0, 0, 100))
        screen.blit(cover, (0, 0))

        # Background
        bg = pygame.Surface((464, 368), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0), bg.get_rect(), border_radius=24)
        pygame.draw.rect(bg, (255, 255, 255), bg.get_rect(), width=1, border_radius=24)
        screen.blit(bg, (((SCREEN_WIDTH - 464)//2), 96))

        # Texts
        w = create_text("W: Move upward", 32, white)[0]
        a = create_text("A: Move leftward", 32, white)[0]
        s = create_text("S: Move southward", 32, white)[0]
        d = create_text("D: Move rightward", 32, white)[0]
        p = create_text("P: Pickup item", 32, white)[0]

        screen.blit(w, ((SCREEN_WIDTH - w.get_width())//2, 120))
        screen.blit(a, ((SCREEN_WIDTH - a.get_width())//2, 164))
        screen.blit(s, ((SCREEN_WIDTH - s.get_width())//2, 208))
        screen.blit(d, ((SCREEN_WIDTH - d.get_width())//2, 252))
        screen.blit(p, ((SCREEN_WIDTH - p.get_width())//2, 296))

        if controls_back_btn.draw():
            controls_popup_state = False
            menu_btn_state = True

    def pause_menu():
        nonlocal menu_resume_btn, menu_return_btn, menu_controls_btn, controls_back_btn, menu_btn_state, controls_popup_state, menu_controls_btn_state
        nonlocal player_mushroom_count, LVL_MUSHROOMS, found_item
        global SCREEN_WIDTH, gameplay_state
        # Cover
        cover = pygame.Surface((1024, 768), pygame.SRCALPHA)
        cover.fill((0, 0, 0, 100))
        screen.blit(cover, (0, 0))

        # Background
        bg = pygame.Surface((464, 232), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0), bg.get_rect(), border_radius=24)
        pygame.draw.rect(bg, (255, 255, 255), bg.get_rect(), width=1, border_radius=24)
        screen.blit(bg, (((SCREEN_WIDTH - 464)//2), 168))

        if menu_resume_btn.draw():
            menu_btn_state = False
            controls_popup_state = False

        if menu_return_btn.draw():
            menu_btn_state = False
            menu_controls_btn_state = False
            gameplay_state = False, gameplay_state[1:]

        if menu_controls_btn.draw():
            menu_btn_state = False
            controls_popup_state = True

    def side_bar():
        nonlocal menu_btn_state, controls_popup_state, mush_img, item, player_index, grid, MOTHERGRID, found_item, history, player_mushroom_count, LVL_MUSHROOMS, drowned
        nonlocal time_when_called, lost_at_time, disposable, won_at_time
        # Main bg
        bg = pygame.Surface((224, 720), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0, 150), bg.get_rect())
        pygame.draw.rect(bg, (*white, 200), bg.get_rect(), width=1)
        screen.blit(bg, (768, (768 - 744)))

        # Menu button
        menu_btn = gameplay_Text_Button(768 + (212 - (2 * 64))//2, 768 - 744, "MENU", 64, white)

        # Mushroom count
        text_lvlmush = create_text(f": {player_mushroom_count}/{LVL_MUSHROOMS}", 48, white)[0]
        screen.blit(pygame.transform.scale(mush_img, (50, 50)), (768 - 40 + (212 - (2 * 48))//2, 768 - 744 + (96 * 1)))
        screen.blit(text_lvlmush, (768 + (212 - (2 * 40))//2, 768 - 744 + (96 * 1 - 3)))

        # On ground
        text_item_ground = create_text("On ground:", 28, white)[0]
        text_found_on_ground = create_text(describe_tile(found_item).title(), 28, white)[0]
        screen.blit(text_item_ground, (768 + (212 - (5 * 28))//2, 768 - 744 + (96 * 2)))
        screen.blit(text_found_on_ground, (768 + (212 - (5 * 28))//2, 768 - 744 + (96 * 2 + 28)))

        # Holding
        text_holding = create_text("Holding:", 28, white)[0]
        if not item:
            text_item_held = create_text("Nothing", 28, white)[0]
        else:
            text_item_held = create_text(f"{describe_tile(*item)}".title(), 28, white)[0]
        screen.blit(text_holding, (768 + (212 - (5 * 28))//2, 768 - 744 + (96 * 3)))
        screen.blit(text_item_held, (768 + (212 - (5 * 28))//2, 768 - 744 + (96 * 3 + 28)))

        # Restart button
        restart_btn = gameplay_Text_Button(768 + (212 - (4 * 40))//2, 768 - 744 + (96 * 4), "RESTART", 40, white)

        if restart_btn.draw():
            # Restores the player attributes back to default
            player_index = MOTHERGRID.index('L')
            grid = list(MOTHERGRID)
            found_item = None
            drowned = False
            item = []
            history = {'player': ['.']}
            player_mushroom_count = 0
            lose_state = False
            disposable = True
            time_when_called = time.time()
            lost_at_time = time.time()
            won_at_time = time.time()

        # Time
        if not drowned and not (menu_btn_state or controls_popup_state):
            time_elapsed = time.time()
        else:
            time_elapsed = lost_at_time

        if LVL_MUSHROOMS == player_mushroom_count:
            time_elapsed = won_at_time

        current_time = int(time_elapsed - time_when_called)
        seconds = str(current_time % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        minutes = current_time // 60

        text_time = create_text(f"{minutes}: {seconds}", 28, white)[0]
        screen.blit(text_time, (768 + (212 - (text_time.get_width()))//2, 768 - 744 + (96 * 4 + 40)))
        
        if menu_btn.draw():
            menu_btn_state = True
            controls_popup_state = False

        if menu_btn_state:
            pause_menu()

        if controls_popup_state:
            controls_popup()

    def win():
        nonlocal lose_state, found_item, player_mushroom_count, LVL_MUSHROOMS, player_index, grid, drowned, item, history, MOTHERGRID
        nonlocal time_when_called, disposable, won_at_time
        global SCREEN_WIDTH, gameplay_state, playing_from_play
        found_item = None

        # Cover
        cover = pygame.Surface((1024, 768), pygame.SRCALPHA)
        cover.fill((0, 0, 0, 100))
        screen.blit(cover, (0, 0))

        # Background
        bg = pygame.Surface((768, 640), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0, 215), bg.get_rect(), border_radius=24)
        pygame.draw.rect(bg, (255, 255, 255), bg.get_rect(), width=1, border_radius=24)
        screen.blit(bg, (((SCREEN_WIDTH - 768)//2), 64))

        # Text
        text_you_won = create_text("You Won!", 128, main_color)[0]
        screen.blit(text_you_won, (((SCREEN_WIDTH - text_you_won.get_width())//2), 96))
        text_poetic_win = create_text(f"Commendable... Worthy of praise...", 34, main_color)[0]
        x_align_on = ((SCREEN_WIDTH - text_poetic_win.get_width())//2)
        screen.blit(text_poetic_win, (x_align_on, 224))

        # Player name, current map
        text_plr_name = create_text(f'Won as "{player}"', 28, white)[0]
        screen.blit(text_plr_name, (x_align_on, 288))
        text_map_name = create_text(f'Deployed on "{level_map_name}"', 28, white)[0]
        screen.blit(text_map_name, (x_align_on, 320))

        # Mushroom collected
        text_mush_collected = create_text(f'Collected {player_mushroom_count} out of {LVL_MUSHROOMS} mushrooms', 28, white)[0]
        screen.blit(text_mush_collected, (x_align_on, 364))

        # Time
        current_time = int(won_at_time - time_when_called)
        seconds = current_time % 60
        minutes = current_time // 60
        text_time_lost = create_text(f"Won after {minutes} minutes and {seconds} seconds", 28, white)[0]
        screen.blit(text_time_lost, (x_align_on, 396))

        # Retry, Back to map menu button
        back_to_lvl_btn = gameplay_Text_Button(x_align_on, 484, "Back to map menu", 48, white)
        replay_btn = gameplay_Text_Button(x_align_on, 538, "Replay", 48, white)
        next_lvl_btn = gameplay_Text_Button(x_align_on, 595, "Next level", 48, white)
        
        if back_to_lvl_btn.draw():
            gameplay_state = False, gameplay_state[1:]

        if replay_btn.draw():
            # Restores the player attributes back to default
            player_index = MOTHERGRID.index('L')
            grid = list(MOTHERGRID)
            found_item = None
            drowned = False
            item = []
            history = {'player': ['.']}
            player_mushroom_count = 0
            lose_state = False
            disposable = True
            time_when_called = time.time()
            lost_at_time = time.time()
            won_at_time = time.time()

        if playing_from_play:
            if next_lvl_btn.draw():
                # next level
                pass


    def lose():
        nonlocal lose_state, found_item, player_mushroom_count, LVL_MUSHROOMS, player_index, grid, drowned, item, history, MOTHERGRID
        nonlocal time_when_called, lost_at_time, disposable
        global SCREEN_WIDTH, gameplay_state
        found_item = None

        # Cover
        cover = pygame.Surface((1024, 768), pygame.SRCALPHA)
        cover.fill((0, 0, 0, 100))
        screen.blit(cover, (0, 0))

        # Background
        bg = pygame.Surface((768, 640), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0, 215), bg.get_rect(), border_radius=24)
        pygame.draw.rect(bg, (255, 255, 255), bg.get_rect(), width=1, border_radius=24)
        screen.blit(bg, (((SCREEN_WIDTH - 768)//2), 64))

        # Text
        text_you_lost = create_text("You Lost", 128, main_color)[0]
        screen.blit(text_you_lost, (((SCREEN_WIDTH - text_you_lost.get_width())//2), 96))
        text_poetic_death = create_text("One is unable to flow with the sea", 34, main_color)[0]
        x_align_on = ((SCREEN_WIDTH - text_poetic_death.get_width())//2)
        screen.blit(text_poetic_death, (x_align_on, 224))

        # Player name, current map
        text_plr_name = create_text(f'Lost as "{player}"', 28, white)[0]
        screen.blit(text_plr_name, (x_align_on, 288))
        text_map_name = create_text(f'Deployed on "{level_map_name}"', 28, white)[0]
        screen.blit(text_map_name, (x_align_on, 320))

        # Mushroom collected
        text_mush_collected = create_text(f'Collected {player_mushroom_count} out of {LVL_MUSHROOMS} mushrooms', 28, white)[0]
        screen.blit(text_mush_collected, (x_align_on, 364))

        # Time
        lost_at_time_lost = lost_at_time

        current_time = int(lost_at_time_lost - time_when_called)
        seconds = current_time % 60
        minutes = current_time // 60
        text_time_lost = create_text(f"Lost after {minutes} minutes and {seconds} seconds", 28, white)[0]
        screen.blit(text_time_lost, (x_align_on, 396))

        # Retry, Back to map menu button
        back_to_lvl_btn = gameplay_Text_Button(x_align_on, 484, "Back to map menu", 48, white)
        retry_btn = gameplay_Text_Button(x_align_on, 538, "Retry", 48, white)
        
        if back_to_lvl_btn.draw():
            gameplay_state = False, gameplay_state[1:]

        if retry_btn.draw():
            # Restores the player attributes back to default
            player_index = MOTHERGRID.index('L')
            grid = list(MOTHERGRID)
            found_item = None
            drowned = False
            item = []
            history = {'player': ['.']}
            player_mushroom_count = 0
            lose_state = False
            disposable = True
            time_when_called = time.time()
            lost_at_time = time.time()
            won_at_time = time.time()

    def save_player_data(playername, mapfile):
        plr = loaded_data["name"]
        dt_created = loaded_data["time_created"]
        s = loaded_data["since_epoch"]
        maps = loaded_data["maps_finished"]
        ply_time = loaded_data["playing_time"]
        mush_tot = loaded_data["mush_collected"]
        with open(f"data/players/{playername}.json") as player_data:
            data = json.load(player_data)
            #json.dump()

    current_map = load_map(grid)
    def game_screen():
        nonlocal lose_state

        screen.blit(level_bg, (0, 0))
        gray_bg = pygame.Surface((1024, 1024), pygame.SRCALPHA)
        gray_bg.fill((0, 0, 0, 50))
        screen.blit(gray_bg, (0, 0))

        map_bg = pygame.Surface(((GRID_WIDTH * scale1) + 2, (GRID_HEIGHT * scale1) + 2), pygame.SRCALPHA)
        map_bg.fill((0, 0, 0, 0))
        pygame.draw.rect(map_bg, (0, 0, 0, 150), map_bg.get_rect())
        pygame.draw.rect(map_bg, (*white, 200), map_bg.get_rect(), width=1)
        screen.blit(map_bg, (x_offset - 1, y_offset - 1))

        screen.blit(current_map, (x_offset, y_offset))
        side_bar()

        if LVL_MUSHROOMS == player_mushroom_count:
            win()

        if drowned:
            lose_state = True

        if lose_state:
            lose()
    if __name__ == "__main__":
        # Outputs args.output_file if -o was called, else run the game.
        if mode == "":
            with open(args.output_file, "w", encoding="utf-8") as output:
                move_player(args.movement)

                # Contents of the output file: no/clear and grid
                if player_mushroom_count == LVL_MUSHROOMS:
                    output.write(f"CLEAR\n{"".join(grid)}")
                else:
                    output.write((f"NO CLEAR\n{"".join(grid)}"))
        else:
            while True:


                if disposable and lose_state:
                    lost_at_time = time.time()
                    disposable = False

                if disposable and LVL_MUSHROOMS == player_mushroom_count:
                    won_at_time = time.time()
                    disposable = False

                if pygame.KEYDOWN and not menu_btn_state and not controls_popup_state:
                    current_map = load_map(grid)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if not lose_state and not (LVL_MUSHROOMS == player_mushroom_count):
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                if menu_btn_state == True:
                                    menu_btn_state = False
                                else:
                                    menu_btn_state = True
                                controls_popup_state = False
                    if not menu_btn_state and not controls_popup_state:
                        if not (LVL_MUSHROOMS == player_mushroom_count or drowned or lose_state):
                            if event.type == pygame.KEYDOWN:
                                if event.unicode.upper() in moves:
                                    print(event.unicode.upper())
                                    move_player(event.unicode.upper())
                
                game_screen()
                
                pygame.display.flip()

                if not gameplay_state[0]:
                    break


if __name__ == "__main__":
    # Outputs args.output_file if -o was called, else run the game.
    if mode == "":
        game_function()
    else:
        if not args.stage_file:
            while True:
                if gameplay_state[0]:
                    not_needed, PLAYER_NAME, MAP_FILE, MAP_NAME = gameplay_state
                    game_function(player=PLAYER_NAME, level_map=MAP_FILE, level_map_name=MAP_NAME)
                else:
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

                        # Check if editor is active
                        if editor_active:
                            level_editor()
                        elif menu_state == "main":
                            if fade_count == 0:
                                fade_in(main_menu)
                                fade_count += 1
                            main_menu()

                        elif menu_state == "play":
                            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                create_plr_btn_state = False
                                menu_state = "main"
                                fade_count = 0
                            if fade_count == 1:
                                fade_in(level_menu)
                                fade_count += 1
                            else:
                                level_menu()

                        elif menu_state == "leaderboards":
                            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                menu_state = "main"
                                fade_count = 0
                            if fade_count == 1:
                                fade_in(leaderboards_menu)
                                fade_count += 1
                            leaderboards_menu()

                        elif menu_state == "create":
                            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                menu_state = "main"
                                fade_count = 0
                            if fade_count == 1:
                                fade_in(create_menu)
                                fade_count += 1
                            else:
                                create_menu()

                        elif menu_state == "options":
                            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                menu_state = "main"
                                fade_count = 0
                            if fade_count == 1:
                                fade_in(options_menu)
                                fade_count += 1
                            options_menu()

                        pygame.display.flip()

                        if gameplay_state[0]:
                            break
        else:
            gameplay_state = True, "", lvlmap, ""
            game_function(level_map=lvlmap, level_map_name=args.stage_file)