import sys
import pygame
import datetime
import os
import json
import shroom_raider
import time
import csv
import button

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (180, 30, 20)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Shroomraider")

menu_state = "main"

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

# Data
players = [player for player in os.listdir("data/players")]

# Images
menu_bg_img1 = pygame.image.load("assets/bg/1st Layer.png")
menu_bg_img2 = pygame.image.load("assets/bg/2nd Layer.png")
menu_bg_img3 = pygame.image.load("assets/bg/3rd Layer.png")
menu_bg_img4 = pygame.image.load("assets/bg/4th Layer.png")
menu_bg_img5 = pygame.image.load("assets/bg/5th Layer.png")


def reset_editor_data():
    # Reset editor world data to empty state
    global editor_world_data
    editor_world_data = []
    for row in range(EDITOR_ROWS):
        r = [-1] * EDITOR_MAX_COLS
        editor_world_data.append(r)


level_buttons = []
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

    save_editor_btn = button.Button(EDITOR_SCREEN_WIDTH + SIDE_MARGIN - 190, 768 // 2 + 220, save_surf, 1)
    exit_editor_btn = button.Button(EDITOR_SCREEN_WIDTH + SIDE_MARGIN - 190, 768 // 2 + 280, exit_surf, 1)

    # Create tile selection buttons
    editor_button_list = []
    button_col = 0
    button_row = 0

    for i in range(len(editor_img_list)):
        tile_button = button.Button(
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

    matrix = [[int(cell) for cell in row] for row in csv_data]
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
    return ''.join(convert_to_ascii.get(c, c) for c in map_str if c in convert_to_ascii)


# Main menu buttons
play_btn = menu_Button(128, 288, "Play", 60)
create_btn = menu_Button(128, 360, "Create Levels", 60)
lb_btn = menu_Button(128, 432, "Leaderboards", 60)
options_btn = menu_Button(128, 504, "Options", 60)
quit_btn = menu_Button(128, 576, "Quit", 60)

# Play menu buttons
create_plr_btn = text_Button_1(512, 640, "New Player", 48, white)
create_plr_done_btn = text_Button_1(512, 448, "Done", 48, white)
create_plr_back_btn = text_Button_1(256, 448, "Back", 48, white)
play_menu_back_btn = text_Button_1(128, 640, "Back", 48, white)
create_plr_btn_state = False
create_plr_done_btn_state = False
already_plr = False
inc_len = False
bonus_btn = text_Button_2(180, 550, "Bonus", 48)
story_btn = text_Button_2(375, 550, "Story", 48)
usermade_btn = text_Button_2(575, 550, "User-made", 48)
map_level_buttons()


# Map editor buttons
create_new_map_btn = text_Button_1(SCREEN_WIDTH - 500, 640, "Create New Map", 48, white)
edit_map_btn = text_Button_1(284, 400, "Edit", 48, white)
play_map_btn = text_Button_1(444, 400, "Play", 48, white)
close_popup_btn = text_Button_1(604, 400, "Cancel", 48, white)
create_map_confirm_btn = text_Button_1(580, 448, "Create", 48, white)
create_map_cancel_btn = text_Button_1(280, 448, "Cancel", 48, white)
max_levels_ok_btn = text_Button_1(470, 410, "OK", 48, white)


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

def map_level_menu():
    global menu_state, fade_count

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

    # Draw all level buttons
    for btn in level_buttons:
        if btn.draw():
            level = btn.level_num # This is the level number, should be same with the file name of the map in txt
            print(level)
            # TODO: play level

    # Back button
    if play_menu_back_btn.draw():
        menu_state = "main"
        fade_count = 0

    # Bonus levels button
    if bonus_btn.draw():
        print('bonus')
        # TODO: show bonus levels

    # Story levels button
    if story_btn.draw():
        print('story')
        # TODO: show story levels

    # User made levels button
    if usermade_btn.draw():
        print('usermade')
        # TODO: show usermade levels



players = [player for player in os.listdir("data/players")]

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
            already_plr = False
            inc_len = True
        create_plr_done_btn_state = False

    if already_plr:
        screen.blit(create_text("Already a player", 32, white)[0], (256, 384))
    if inc_len:
        screen.blit(create_text("Name must have a minimum of one character,", 24, white)[0], (256, 384))
        screen.blit(create_text("and a maximum of 15 character", 24, white)[0], (256, 408))


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

    pygame.draw.rect(screen, white, pygame.Rect(128, 128, 768, 768 - 256))

    text = create_text("Players", 60, white)[0]
    screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 60))

    if create_plr_btn.draw():
        create_plr_btn_state = True

    # Buttons
    if create_plr_btn_state:
        _create_player_menu()

    if play_menu_back_btn.draw():
        create_plr_btn_state = False
        menu_state = "main"
        fade_count = 0


def editor_laro_warning():
    overlay = pygame.Surface((768, 1024 - 200), pygame.SRCALPHA)
    box_rect = pygame.Rect(165, 350, 450, 100)
    gray_with_alpha = (128, 128, 128, 200)
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


def level_editor():
    global menu_state, editor_active, editor_current_tile, editor_world_data, fade_count
    global map_action_popup, selected_map, new_map_name_input, map_name_exists, map_name_invalid, create_new_map_state

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
        with open(f'data/custom_levels/{editor_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in editor_world_data:
                writer.writerow(row)

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
                    existing_maps = os.listdir('data/custom_levels') if os.path.exists('data/custom_levels') else []
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
            existing_maps = os.listdir('data/custom_levels') if os.path.exists('data/custom_levels') else []
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
    # TODO: delete button
    global menu_state, fade_count, selected_map, map_action_popup, map_buttons, create_new_map_state, editor_active, editor_world_data
    global editor_name, new_map_name_input, map_name_exists, map_name_invalid

    # Background
    screen.blit(menu_bg_img5, (0, 0))
    screen.blit(menu_bg_img4, (0, 0))
    screen.blit(menu_bg_img3, (0, 0))
    screen.blit(menu_bg_img2, (0, 0))
    screen.blit(menu_bg_img1, (0, 0))

    # Semi-background
    pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(96, 48, 1024 - 192, 768 - 96), border_radius=32)

    # Content area
    pygame.draw.rect(screen, white, pygame.Rect(128, 128, 768, 768 - 256))

    # Title
    text = create_text("Created Maps", 60, white)[0]
    screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 60))

    # Get custom maps
    custom_maps = []
    if os.path.exists('data/custom_levels'):
        for maps in os.listdir('data/custom_levels'):
            custom_maps.append(maps)

    # Create buttons for each map
    if not map_action_popup and not create_new_map_state:
        map_buttons = []
        y_pos = 135
        for i, map_name in enumerate(custom_maps):
            # Remove file extension for display
            display_name = map_name.replace('.csv', '')
            btn = text_Button_1(160, y_pos, display_name, 32, (75, 75, 75))
            map_buttons.append((btn, map_name))
            y_pos += 50

            # Check if map is clicked
            if btn.draw():
                selected_map = map_name
                map_action_popup = True

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
                with open(f'data/custom_levels/{selected_map}', newline='') as csvfile:
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
            # TODO: implement gameplay
            level_map = csv_to_map(f'data/custom_levels/{selected_map}') # This is the string format of the map
            map_action_popup = False
            selected_map = None

        if close_popup_btn.draw():
            map_action_popup = False
            selected_map = None

    # stay in create menu
    if not map_action_popup and editor_active:
        menu_state = "create"
        fade_count = 0

    # Show new map creation dialog
    if create_new_map_state:
        saved_dir_path = r'data/custom_levels'
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
    if play_menu_back_btn.draw() and not map_action_popup and not create_new_map_state:
        menu_state = "main"
        fade_count = 0


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


while __name__ == "__main__":

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
            fade_in(map_level_menu)
            fade_count += 1
        map_level_menu()

    pygame.display.flip()

