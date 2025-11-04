from argparse import ArgumentParser
import os

# Add arguments for the command
parser = ArgumentParser(add_help=False)
parser.add_argument('-f', '--stage_file')
parser.add_argument('-m', '--movement')
parser.add_argument('-o', '--output_file')
args = parser.parse_args()

# Checks if stage_file will be loaded, else load default map
if args.stage_file == None:
    # Default map
    lvlmap = '10 14\nTTTT~~~~~TTTTT\nT.L.~.xT~~~~~T\nT.R.~.~+~TTT~T\nT~.~~T~.~T~T~T\nT~~~~.~R~T~T~T\nT...~x~~~T~T~T\nTT.T~.~.~T~T~T\nT~+...~..*~+~T\nT~~~~~~~~~~~~T\nTTTTTTTTTTTTTT'
else:
    # Load stage_file
    with open(args.stage_file, "r", encoding="utf-8") as lvl:
      lvlmap = lvl.read()

# Mode whether the player will "play" or will output a file
mode = ""
if args.output_file == None:
    mode = "play"

# DUSTIN KIM JOSEP AUSIN M SINASABI Q SAU :ANGRY:
lvlmapcontent = list(lvlmap)

GRID_HEIGHT = int(lvlmap[:lvlmap.index(' ')])
GRID_WIDTH = int(lvlmap[lvlmap.index(' ')+1: lvlmap.index('\n')])

MOTHERGRID = lvlmapcontent[lvlmapcontent.index('\n') + 1:]

LVL_MUSHROOMS = 0
DROWNED = False

grid = lvlmapcontent[lvlmapcontent.index('\n') + 1:]
main = 0

player_mushroom_count = 0
for x in lvlmap:
    if x == "+":
        LVL_MUSHROOMS += 1

item = []
history = ['.']
found_item = None

player_index = grid.index('L')

moves = {
    'W': -GRID_WIDTH - 1,
    'S': GRID_WIDTH + 1,
    'A': -1,
    'D': 1,
    'P': 0
}

def clear():
    """This function clears the terminal, it does not return anything"""
    os.system('cls' if os.name == 'nt' else 'clear')

def char_to_emoji(map):
    # Returns the map converted from text characters to emoji
    emoji = {
        '.': '⬛',
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
    return ''.join(emoji.get(c, c) for c in map if c in emoji)

def pickup(tile):
    # Adds current tile to the list of items held by the player
    print(f"You picked up the {describe_tile(tile)}!")
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
        '*': 'flamethrower'
    }.get(tile, 'unknown')

def _move_player(direction):

    global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item, DROWNED, mode

    def moveto(under_tile):

        global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history

        grid[player_index] = f"{history[-1]}"  # leave floor behind
        grid[new_index] = 'L'     # new position
        player_index = new_index

        history.append(under_tile)

    new_index = player_index + moves[direction]

    if not ((0 <= new_index < len(grid))):
        if mode == "play":
            print("You can't move outside the grid!")
        return
    else:
        target_tile = grid[new_index]

        if target_tile == 'T':
            remove_tree = new_index + moves[direction]
            if not item:
                if mode == "play":
                    print("You bumped into a tree!")
            elif item[0] == 'x':
                moveto('.')
                item.clear()
            elif item[0] == '*':
                col = (new_index % (GRID_WIDTH+1))
                row = (new_index - col) // GRID_WIDTH
                grid = flame_spread(row, col)
                moveto('.')
                item.clear()
            return

        elif target_tile == 'R':

            new_rock_index = new_index + moves[direction]

            if mode == "play":
                if new_rock_index > len(grid):
                    print("You can't move the rock there")
                    return

                elif grid[new_rock_index] == "~":
                    grid[new_rock_index] = "_"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "." or grid[new_rock_index] == "_":
                    grid[new_rock_index] = "R"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "R":
                    print("You don't have the strength to push more than one rocks!")
                    return

                else:
                    print("You can't move the rock there!")
                    return
            else:
                if grid[new_rock_index] == "~":
                    grid[new_rock_index] = "_"
                    moveto('.')
                    return

                elif grid[new_rock_index] == "." or grid[new_rock_index] == "_":
                    grid[new_rock_index] = "R"
                    moveto('.')
                    return

        elif target_tile == '~':
            moveto('~')
            DROWNED = True
            main += 1
            return

        elif target_tile == "+":
            player_mushroom_count += 1

            if player_mushroom_count == LVL_MUSHROOMS:
                moveto('+')
                main += 1

            moveto('.')
            return

        elif target_tile == "x":
            found_item = 'x'
            if not item:
                moveto('x')
            elif len(item) == 1:
                moveto('x')
            else:
                moveto('.')
            return

        elif target_tile == "*":
            found_item = '*'
            if not item:
                moveto('*')
            elif len(item) == 1:
                moveto('*')
            else:
                moveto('.')
            return

        elif target_tile == "_":
            moveto('_')
            return

        else:
            found_item = None
            moveto('.')

def move_player(direction):
    global player_index, grid, MOTHERGRID, main, player_mushroom_count, item, history, found_item

    for inp in direction:
        inp = inp.upper()
        if main == 0:
            if inp == 'Q':
                main += 1

            elif inp == 'P':
                if mode == "play":
                    if not found_item:
                        print("Invalid move. Use W, A, S, D.")
                    elif len(item) == 1:
                        print('You already have an item, you can\'t pickup another')
                    else:
                        pickup(found_item)
                        found_item = None
                        history[-1] = '.'
                else:
                    if found_item and len(item) != 1:
                        pickup(found_item)
                        found_item = None
                        history[-1] = '.'

            elif inp == "!":

                if mode == "play":
                    print("Restart Successful:")

                player_index = MOTHERGRID.index('L')
                grid = lvlmapcontent[lvlmapcontent.index("\n") + 1:]
                found_item = None
                item = []
                history = ['.']
                player_mushroom_count = 0

            elif inp in moves:
                _move_player(inp)

            else:
                break
        else:
            break

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
    while main == 0:
        # Clears the terminal at the start, and after inputs
        clear()

        # Prints the map and mushroom count of the level
        print(f"You need {LVL_MUSHROOMS} mushroom/s to win!")
        print("Grid:")
        print(char_to_emoji(grid))

        # Prints the collected mushroom count, and the valid moves
        print(f"{player_mushroom_count} out of {LVL_MUSHROOMS} mushroom/s collected")
        print('''
        [W] Move up
        [A] Move left
        [S] Move down
        [D] Move right
        [!] Reset
        ''')

        # Prints the available item beneath the player, if any or none
        if not found_item:
            print("No items here")
        else:
            print(f"[P] Pick up {describe_tile(found_item)}")

        # Prints the item currently held by the player, if any or none
        if not item:
            print("Not holding anything")
        else:
            print(f"Currently holding {char_to_emoji(item[0])}")

        # Player input
        move = input("What will you do? ").strip().upper()
        move_player(move)

        if player_mushroom_count == LVL_MUSHROOMS:
            clear()
            print("Grid:")
            print(char_to_emoji(grid))
            print("-" * GRID_WIDTH * 2)
            print(" " * ((GRID_WIDTH // 2) + 1), "You Won!")
            print("-" * GRID_WIDTH * 2, "\n")

        if DROWNED:
            clear()
            print(f"You need {LVL_MUSHROOMS} mushroom/s to win!")
            print("Grid:")
            print(char_to_emoji(grid))
            print("---------------------------------")
            print("Game Over! Laro Craft can't swim!")
            print("---------------------------------")
            print(f"{player_mushroom_count} out of {LVL_MUSHROOMS} mushroom/s collected\n")

        if main > 0:
            print("Goodbye!")
