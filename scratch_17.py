from argparse import ArgumentParser
import os

parser = ArgumentParser(add_help=False)
parser.add_argument('-f', '--stage_file')
parser.add_argument('-m', '--movement')
parser.add_argument('-o', '--output_file')
args = parser.parse_args()

if args.stage_file == None:
    lvlmap = "99\nTTTTTTTTT\nT...++..T\nT...~...T\nT...R.T.T\nT.T.LTT.T\nT.x...*.T\nT.......T\nT.......T\nTTTTTTTTT"
else:
    with open(args.stage_file, "r", encoding="utf-8") as lvl:
      lvlmap = lvl.read()

lvlmapcontent = list(lvlmap)

if " " in lvlmapcontent:
  lvlmapcontent.remove(' ')

grid_height = int(lvlmapcontent[0])
grid_width = int(lvlmapcontent[1])

mothergrid = lvlmapcontent[3:]
grid = lvlmapcontent[3:]

main = 0
player_mushroom_count = 0
lvl_mushroom_count = 0

for x in mothergrid:
    if x == "+":
        lvl_mushroom_count += 1

item = []
history = ['.']
found_item = None

player_index = grid.index('L')

moves = {
    'W': -grid_width - 1,
    'S': grid_width + 1,
    'A': -1,
    'D': 1,
    'P': 0
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ascii_to_emoji(map):
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
  return ''.join(emoji.get(c, c) for c in map if c in emoji) #replaces ascii value from map to corresponding key from dict, but keeps '\n'

def pickup(tile):

    print(f"You picked up the {describe_tile(tile)}!")
    item.append(tile)
    return ascii_to_emoji(tile)

def flame_spread(start_row, start_col):
    #used for item flamethrower
    global grid

    grid_string = ''.join(grid)
    grid_2d_list = [list(row) for row in grid_string.strip().split('\n')]
    row, col = len(grid_2d_list), len(grid_2d_list[0])

    def in_bounds(r, c):
        return 0 <= r < row and 0 <= c < col

    def flamethrowed(r, c):
        if not in_bounds(r, c) or grid_2d_list[r][c] != 'T':
            return
        grid_2d_list[r][c] = '.'
        for change_row, change_col in [(-1,0), (1,0), (0,-1), (0,1)]:
            flamethrowed(r + change_row, c + change_col)

    if grid_2d_list[start_row][start_col] == 'T':
        flamethrowed(start_row, start_col)

    new_grid_string = '\n'.join(''.join(row) for row in grid_2d_list)

    return list(new_grid_string)


def describe_tile(tile):
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

def move_player(direction):

    global player_index, grid, mothergrid, main, player_mushroom_count, item, history, found_item

    def moveto(under_tile):

        global player_index, grid, mothergrid, main, player_mushroom_count, item, history

        print(f"You moved onto a {describe_tile(target_tile)} tile.")

        grid[player_index] = f"{history[-1]}"  # leave floor behind
        grid[new_index] = 'L'     # new position
        player_index = new_index

        history.append(under_tile)

        print(ascii_to_emoji(grid))

    direction = direction.upper()


    if direction == "!":

        print("Restart Successful:")
        print(ascii_to_emoji(mothergrid))

        player_index = mothergrid.index('L')
        grid = lvlmapcontent[3:]
        return

    elif direction not in moves:
        print("Invalid move. Use W, A, S, D.")
        return

    new_index = player_index + moves[direction]

    if not (0 <= new_index < len(grid)):
        print("You can't move outside the grid!")
        return

    target_tile = grid[new_index]

    if target_tile == 'T':
        remove_tree = new_index + moves[direction]
        if not item:
            print("You bumped into a tree!")
        elif item[0] == 'x':
            #grid[remove_tree] = "."
            moveto('.')
            item.clear()
        elif item[0] == '*':
            col = (new_index % (grid_width+1))
            row = (new_index - col) // grid_width
            grid = flame_spread(row, col)
            moveto('.')
            item.clear()
        print(ascii_to_emoji(grid))
        return

    elif target_tile == 'R':

        new_rock_index = new_index + moves[direction]

        if new_rock_index > len(grid):
            print("You can't move the rock there")
            print(ascii_to_emoji(grid))
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

    elif target_tile == '~':
        print("---------------------------------")
        print("Game Over! Laro Craft can't swim!")
        print("---------------------------------")
        main += 1

        return

    elif target_tile == "+":
        pickup(target_tile)
        player_mushroom_count += 1

        if player_mushroom_count == lvl_mushroom_count:

            print
            print("--------")
            print("You Won!")
            print("--------")
            main += 1

            return

        moveto('.')
        return

    elif target_tile == "x":
        found_item = 'x'
        if not item:
            moveto('x')
        elif len(item) == 1:
            #print('You already have an item, you can\'t pickup another')
            #input("Press Enter to continue: ")
            moveto('x')
        else:
            moveto('.')
        return

    elif target_tile == "*":
        found_item = '*'
        if not item:
            moveto('*')
        elif len(item) == 1:
            #print('You already have an item, you can\'t pickup another')
            #input("Press Enter to continue: ")
            moveto('*')
        else:
            moveto('.')
        return

    elif target_tile == "_":
        moveto('_')
        return

    moveto('.')

print(f"You need {lvl_mushroom_count} mushroom/s to win!")
print("Initial Grid:")
print(ascii_to_emoji(grid))


while main == 0:
    print(f"found item: {found_item}")
    print(f"item holding: {item}")

    print(f"{player_mushroom_count} out of {lvl_mushroom_count} mushroom/s collected")
    print('''
    [W] Move up
    [A] Move left
    [S] Move down
    [D] Move right
    [!] Reset
    ''')

    if not found_item:
        print("No items here")
    else:
        print(f"[P] Pick up {describe_tile(found_item)}")

    if not item:
        print("Not holding anything")
    else:
        print(f"Currently holding {ascii_to_emoji(item[0])}")
    move = input("What will you do? ").strip().upper()

    if move == 'Q':
        print("Goodbye!")
        break
    elif move == 'P':
        if len(item) == 1:
            print('You already have an item, you can\'t pickup another')
            # jane: d q pa naaayos dto if may hawak sha tas pinindot 'p', hnde nmn sha gagalaw sa map pero magdidisplay 'you moved onto a player tile' intentional b un ?
        else:
            pickup(found_item)

    found_item = None

    move_player(move)

if main > 1:
    print("Goodbye!")