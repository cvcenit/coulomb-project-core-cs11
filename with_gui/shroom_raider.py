import os
import sys
import pygame
from argparse import ArgumentParser

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
black = (0, 0, 0)
white = (255, 255, 255)
main_color = (180, 30, 20)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Shroomraider")

class gameplay_text_button():
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
        global menu_btn_state, controls_popup_state
        action = False
        pos = pygame.mouse.get_pos()

        if self.capt == "MENU" or self.capt == "RESTART":
            if not menu_btn_state and not controls_popup_state:
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

def create_text(text, s, color):
    font = pygame.font.Font("Syne_Mono/SyneMono-Regular.ttf", size=s)
    return font.render(text, True, color), text


def add_args():
    ''' Adds arguments, will only be called if __name__ == "__main__" below '''
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-f', '--stage_file')
    parser.add_argument('-m', '--movement')
    parser.add_argument('-o', '--output_file')
    return parser.parse_args()

def pick_map(stage_file=None):
    ''' Returns default map if there's no stage_file, else returns the stage file '''
    if stage_file == None:
        return '10 14\nTTTT~~~~~TTTTT\nT.L.~.xT~~~~~T\nT.R.~.~+~TTT~T\nT~.~~.~.~T~T~T\nT~~~~.~R~T~T~T\nT.~.Tx~~~T~T~T\nT...T.~T~T~T~T\nT~+...~..*~+~T\nT~~~~~~~~~~~~T\nTTTTTTTTTTTTTT'
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

# Main loop 'count'
main = 0

# Default player attributes
item = []
history = ['.']
found_item = None
drowned = False
player_mushroom_count = 0

# Makes a list with the tiles as its elements from "lvlmap" excluding the values for the height and width
lvlmapcontent = list(lvlmap[lvlmap.index('\n')+1:])

# Takes the integer strings at their respective indices (height before ' '; width after ' ' and before the first \n) and converts into integers
try:
    GRID_HEIGHT = int(lvlmap[:lvlmap.index(' ')])
    GRID_WIDTH = int(lvlmap[lvlmap.index(' ')+1: lvlmap.index('\n')])
except TypeError:
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

player_index = grid.index('L')

# Library of inputs with their corresponding change in index (+1 in width to accommodate for the '\n' characters)
moves = {
    'W': -(GRID_WIDTH + 1),
    'S': GRID_WIDTH + 1,
    'A': -1,
    'D': 1,
    'P': 0
}

def char_to_emoji(level):
    # Returns the level converted from text characters to emoji
    emoji = {
        '.': '　',
        'L': '🧑',
        'T': '🌲',
        '+': '🍄',
        'R': '🪨',
        '~': '🟦',
        '_': '⬜',
        'x': '🪓',
        '*': '🔥',
        '\n': '\n'
        }
    return ''.join(emoji.get(c, c) for c in level if c in emoji)

def pickup(tile):
    # Adds current tile to the list of items held by the player
    item.append(tile)
    # Returns the current tile in emoji form
    return char_to_emoji(tile)

def flame_spread(start_row, start_col):
    # Returns the new map when flamethrower is used, or when player approaches tree while holding flamethrower
    global grid

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

    global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item, drowned, mode

    def moveto(under_tile):

        # Mutates the grid; Doesn't return anything
        global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history

        # Sets the tile left behind by the player as the tile it previously was based on the history list
        grid[player_index] = f"{history[0]}" 
        history.pop()

        # Sets the tile at new_index as the player tile
        grid[new_index] = 'L'

        # Updates the current player_index
        player_index = new_index

        # Appends the under_tile(the tile the player moved to) into the history list
        history.append(under_tile)

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

                if new_rock_index > len(grid) or new_rock_index in _n_indices: # Checks if it will go out of bounds or in a '\n' index
                    print("You can't move the rock there")
                    return

                elif grid[new_rock_index] == "~":   # Converts a water tile into a paved tile
                    grid[new_rock_index] = "_"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "." or grid[new_rock_index] == "_":    # Moves the rock along
                    grid[new_rock_index] = "R"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "R":   # Checks if the player is trying to move two rocks at the same time
                    print("You don't have the strength to push more than one rocks!")
                    return
            else:
                if grid[new_rock_index] == "~":    # Converts a water tile into a paved tile
                    grid[new_rock_index] = "_"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "." or grid[new_rock_index] == "_":    # Moves the rock along
                    grid[new_rock_index] = "R"
                    moveto('.')
                    return

            return

        elif target_tile == '~':

            # Moves the player into the water
            moveto('~')

            # Changes the following player attributes
            drowned = True
            main += 1

            return

        elif target_tile == "+":

            # Increases the collected mushroom count of the player
            player_mushroom_count += 1

            # Checks if the player has reached the required amount of mushrooms
            if player_mushroom_count == LVL_MUSHROOMS:
                moveto('+')
                main += 1

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
    global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item

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
                        history[-1] = '.' # Sets the previous tile as an empty tile after picking up the item
                else:
                    if not found_item:
                        pass
                    elif len(item) == 1:
                        pass
                    else:
                        pickup(found_item)
                        found_item = None
                        history[-1] = '.' # Sets the previous tile as an empty tile after picking up the item

            elif inp == "!":
                # Restarts the game

                # Restores the player attributes back to default
                player_index = MOTHERGRID.index('L')
                grid = list(MOTHERGRID)
                found_item = None
                item = []
                history = ['.']
                player_mushroom_count = 0

            elif inp in moves:
                _move_player(inp)

            # Breaks the loop when an invalid input is detected
            else:
                break
        else:
            break


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
menu_resume_btn = gameplay_text_button((6 * 48)//4 + (SCREEN_WIDTH - (6 * 48))//2, 192, "Resume", 48, white)
menu_controls_btn = gameplay_text_button((8 * 48)//4 + (SCREEN_WIDTH - (8 * 48))//2, 252, "Controls", 48, white)
menu_return_btn = gameplay_text_button((15 * 48)//4 + (SCREEN_WIDTH - (15 * 48))//2, 310, "Back to Levels", 48, white)
controls_back_btn = gameplay_text_button((4 * 48)//4 + (SCREEN_WIDTH - (4 * 48))//2, 368, "Back", 48, white)
menu_btn_state = False
menu_controls_btn_state = False
controls_popup_state = False

# Lose popup

lose_state = False

# level bg
level_bg = pygame.image.load("assets/cave_bluelarge.png")
level_bg = pygame.transform.scale(level_bg, (1024, 1024))

def main_loop():
    global main, grid, drowned, LVL_MUSHROOMS, player_mushroom_count, GRID_WIDTH, GRID_HEIGHT, menu_state
    global mush_img, flamethrower_img, axe_img, rock_img, water_img, pavement_img, empty_img, plr_img, tree_img
    global menu_resume_btn, menu_return_btn, menu_controls_btn, controls_back_btn, menu_btn_state, controls_popup_state, menu_controls_btn_state
    global level_bg, item, player_index, grid, MOTHERGRID, found_item, history

    scale1 = 704 // (GRID_WIDTH)
    y_offset = (768 - (GRID_HEIGHT * scale1)) // 2
    x_offset = (768 - 704) // 2

    # 320 px left for width

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
        global drowned
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
        global controls_back_btn, controls_popup_state, menu_btn_state, SCREEN_WIDTH
        
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
        global menu_resume_btn, menu_return_btn, menu_controls_btn, controls_back_btn, menu_btn_state, controls_popup_state, menu_controls_btn_state
        global player_mushroom_count, LVL_MUSHROOMS, found_item
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
            menu_state = "play"

        if menu_controls_btn.draw():
            menu_btn_state = False
            controls_popup_state = True

    def side_bar():
        global menu_btn_state, controls_popup_state, mush_img, item, player_index, grid, MOTHERGRID, found_item, history, player_mushroom_count, LVL_MUSHROOMS, drowned
        # Main bg
        bg = pygame.Surface((224, (GRID_HEIGHT * scale1) + 2), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 0))
        pygame.draw.rect(bg, (0, 0, 0, 150), bg.get_rect())
        pygame.draw.rect(bg, (*white, 200), bg.get_rect(), width=1)
        screen.blit(bg, (768, (y_offset - 1)))

        # Menu button
        menu_btn = gameplay_text_button(768 + (212 - (2 * 64))//2, y_offset, "MENU", 64, white)

        # Mushroom count
        text_lvlmush = create_text(f": {player_mushroom_count}/{LVL_MUSHROOMS}", 48, white)[0]
        screen.blit(pygame.transform.scale(mush_img, (50, 50)), (768 - 40 + (212 - (2 * 48))//2, y_offset + (96 * 1)))
        screen.blit(text_lvlmush, (768 + (212 - (2 * 40))//2, y_offset + (96 * 1 - 3)))

        # On ground
        text_item_ground = create_text("On ground:", 28, white)[0]
        text_found_on_ground = create_text(describe_tile(found_item).title(), 28, white)[0]
        screen.blit(text_item_ground, (768 + (212 - (5 * 28))//2, y_offset + (96 * 2)))
        screen.blit(text_found_on_ground, (768 + (212 - (5 * 28))//2, y_offset + (96 * 2 + 28)))

        # Holding
        text_holding = create_text("Holding:", 28, white)[0]
        if not item:
            text_item_held = create_text("Nothing", 28, white)[0]
        else:
            text_item_held = create_text(f"{describe_tile(*item)}".title(), 28, white)[0]
        screen.blit(text_holding, (768 + (212 - (5 * 28))//2, y_offset + (96 * 3)))
        screen.blit(text_item_held, (768 + (212 - (5 * 28))//2, y_offset + (96 * 3 + 28)))

        # Restart button
        restart_btn = gameplay_text_button(768 + (212 - (4 * 40))//2, y_offset + (96 * 4), "RESTART", 40, white)

        if restart_btn.draw():
            # Restores the player attributes back to default
            player_index = MOTHERGRID.index('L')
            grid = list(MOTHERGRID)
            found_item = None
            item = []
            history = ['.']
            player_mushroom_count = 0
            drowned = False
        
        if menu_btn.draw():
            menu_btn_state = True
            controls_popup_state = False

        if menu_btn_state:
            pause_menu()

        if controls_popup_state:
            controls_popup()

    def win():
        ...

    def lose():
        found_item = None

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

    current_map = load_map(grid)
    def game_screen():
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
            lose()

    while True:
        if pygame.KEYDOWN and not menu_btn_state:
            current_map = load_map(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_btn_state == True:
                        menu_btn_state = False
                    else:
                        menu_btn_state = True
                    controls_popup_state = False
            if not menu_btn_state and not controls_popup_state:
                if not (LVL_MUSHROOMS == player_mushroom_count or drowned):
                    if event.type == pygame.KEYDOWN:
                        if event.unicode.upper() in moves:
                            print(event.unicode.upper())
                            move_player(event.unicode.upper())
        
        game_screen()
        
        pygame.display.flip()


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
        main_loop()