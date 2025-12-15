import os
from argparse import ArgumentParser

# PREREQUISITE FUNCTIONS
def add_args():
    """Returns parsed arguments, will only be called if __name__ == "__main__" below."""
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-f', '--stage_file')
    parser.add_argument('-m', '--movement')
    parser.add_argument('-o', '--output_file')
    return parser.parse_args()


def pick_map(stage_file=None) -> str:
    """Returns default map if there's no stage_file, else returns the stage file."""
    if stage_file is None:
        return '''10 14
TTTT~~~~~TTTTT
T.L.~.xT~~~~~T
T.R.~.~+~TTT~T
T~.~~.~.~T~T~T
T~~~~.~R~T~T~T
T...~x~~~T~T~T
TT.T~.~T~T~T~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT'''
    else:
        with open(stage_file, encoding="utf-8") as lvl:
          return lvl.read()


def is_user_playing(output_file=None) -> bool:
    """
    Determines if the user will play, or output a file
    
    Returns:
        True if -o has an argument
        False otherwise
    """
    return True if output_file is None else False

def clear_terminal():
    """
    Clears the terminal, does not return anything
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Checks if the command is running from shroom_raider.py, and not as a module/from another file
if __name__ == "__main__":
    args = add_args()
    is_playing: bool = is_user_playing(args.output_file)  # Mode if to play or to output
    lvlmap = pick_map(args.stage_file)  # Map as string/raw
else:
    is_playing: bool = is_user_playing()  # Mode if to play or to output
    lvlmap = pick_map()  # Map as string/raw

# Determines if the player is still playing the game
playing_game: bool = True

# Makes a list with the tiles as its elements from "lvlmap" excluding the values for the height and width
lvlmapcontent: list = list(lvlmap[lvlmap.index('\n')+1:])

# Takes the integer strings at their respective indices (height before ' '; width after ' ' and before the first \n) and converts into integers
GRID_HEIGHT = int(lvlmap[:lvlmap.index(' ')])
GRID_WIDTH = int(lvlmap[lvlmap.index(' ')+1: lvlmap.index('\n')])

# Serves as the base grid for the level (will not be mutated)
MOTHERGRID = list(''.join(lvlmapcontent))

#Serves as the starting index for the level
START = MOTHERGRID.index("L")

# Serves as the working grid for the level (will be mutated)
grid = list(''.join(lvlmapcontent))

# Counts the amount of mushrooms needed to win the level
LVL_MUSHROOMS = 0
for x in lvlmap:
    if x == "+":
        LVL_MUSHROOMS += 1

# Lists the indices of '\n' characters
_n_indices = range(lvlmapcontent.index('\n'), len(lvlmapcontent), GRID_WIDTH + 1)

class Player:
    """The Player class contains all the necessary attributes and methods connected to the player input"""

    # Library of inputs with their corresponding change in index (+1 in width to accommodate for the '\n' characters)
    moves = {
        'W': -(GRID_WIDTH + 1),
        'S': GRID_WIDTH + 1,
        'A': -1,
        'D': 1,
        'P': 0,
        'L': 0,
    }

    def __init__(self, start):
        """Sets the default attributes"""
        super(Player, self).__init__()
        self.start = start
        self.item = []
        self.history = {'player': ['.']}
        self.found_item = None
        self.drowned = False
        self.player_mushroom_count = 0
        self.player_index = self.start

    def reset(self):
        """Resets the addributes back to default"""
        self.item = []
        self.history = {'player': ['.']}
        self.found_item = None
        self.drowned = False
        self.player_mushroom_count = 0
        self.player_index = self.start

    def pickup(self, tile):
        """Adds current tile to the list of items held by the player. Returns the current tile in emoji form"""
        self.item.append(tile)
        return char_to_emoji(tile)

    def _move_player(self, direction, grid):
        """Takes the directional input of the player and moves the player accordingly"""
        global playing_game

        grid = grid

        def moveto(under_tile):
            """Mutates the grid; Doesn't return anything"""

            # Sets the tile left behind by the player as the tile it previously was based on the history list
            grid[self.player_index] = f"{self.history['player'][0]}"
            self.history['player'].pop()

            # Sets the tile at new_index as the player tile
            grid[new_index] = 'L'

            # Updates the current player_index
            self.player_index = new_index

            # Appends the under_tile(the tile the player moved to) into the history list
            self.history['player'].append(under_tile)

        # The targeted index of the player based on the move
        new_index = self.player_index + self.moves[direction]

        # Checks if either the targeted index is out of bounds
        if not (0 <= new_index < len(grid)) or new_index in _n_indices:  # Avoids the mutation of \n indices:
            return grid

        else:
            # Gets the tile of the targeted index
            target_tile = grid[new_index]

            # Checks the nature of the targeted tile
            if target_tile == 'T':
                if not self.item:  # Player will not move anywhere if not holding an axe/flamethrower
                    pass
                elif self.item[0] == 'x':  # Tree will turn into empty space if player is holding an axe
                    moveto('.')
                    self.item.clear()  # Item is cleared every time after used
                    self.found_item = None

                elif self.item[0] == '*':  # flame_spread function is called when player is holding flamethrower
                    col = (new_index % (GRID_WIDTH+1))
                    row = (new_index - col) // GRID_WIDTH
                    grid = flame_spread(row, col)
                    moveto('.')
                    self.item.clear()  # Item is cleared every time after used
                    self.found_item = None

                return grid

            elif target_tile == 'R':

                # New position of the rock as it moves along with the player
                new_rock_index = new_index + self.moves[direction]

                # Checks if it is possible to move the rock to the new index
                rock_under_tile = '.'

                if f"Rock {new_index}" in self.history:  # Sets the tile under the rock based on history, so that the 'moveto' function appends the correct under_tile when the player moves
                    rock_under_tile = self.history[f"Rock {new_index}"]

                if new_rock_index >= len(grid) or new_rock_index in _n_indices:  # Checks if it will go out of bounds or in a '\n' index
                    return grid

                elif grid[new_rock_index] == "~":   # Converts a water tile into a paved tile
                    grid[new_rock_index] = "_"
                    moveto(rock_under_tile)

                elif grid[new_rock_index] == ".":    # Moves the rock along an empty tile
                    grid[new_rock_index] = "R"
                    moveto(rock_under_tile)

                elif grid[new_rock_index] == "_":   # Moves the rock along a paved tile
                    grid[new_rock_index] = "R"
                    self.history[f"Rock {new_rock_index}"] = "_"  # Takes note of the tile under the rock
                    moveto(rock_under_tile)

                elif grid[new_rock_index] == "R" or 'x' or '*' or '+':   # Checks if the player is trying to move two rocks at the same time or into a non-empty tile
                    return grid

                if f"Rock {new_index}" in self.history:    # Removes the Rock at index new_index from history after it gets moved
                    del self.history[f"Rock {new_index}"]

                return grid

            elif target_tile == '~':

                # Moves the player into the water
                moveto('~')

                # Changes the following player attributes
                self.drowned = True
                playing_game = False

                return grid

            elif target_tile == "+":

                # Increases the collected mushroom count of the player
                self.player_mushroom_count += 1

                # Checks if the player has reached the required amount of mushrooms
                if self.player_mushroom_count == LVL_MUSHROOMS:
                    moveto('+')
                    playing_game = False

                # Moves the player and leaves an empty tile
                moveto('.')
                return grid

            elif target_tile == "x":

                # Updates the found item as an axe
                self.found_item = 'x'
                moveto('x')

                return grid

            elif target_tile == "*":

                # Updates the found item as a flamethrower
                self.found_item = '*'
                moveto('*')

                return grid

            elif target_tile == "_":

                # No items in a paved tile
                self.found_item = None
                moveto('_')

                return grid

            else:

                # No items in an empty tile
                self.found_item = None
                moveto('.')

                return grid

class Leaderboard:
    def __init__(self, title):
        super(Leaderboard, self).__init__()
        self.title = title
        self.max_players = 10
        self.max_character = 12
        self.player_folder = os.listdir(f'players')
        self.players = {}
        for player_file in self.player_folder:
            with open(f'players/{player_file}', 'r') as plr:
                self.players[player_file] = plr.read()

    def draw_board(self):
        print("\nWin Leaderboard")
        print("|----Player----|Wins")
        for player in self.players:
            print(f"|{player[:-4]}", " " * (self.max_character - len(player[:-4])), f"|{self.players[player]}")
        print('\n')

    def add_player(self, player_name):
        if len(self.player_folder) < self.max_players:
            if 0 < len(player_name) <= self.max_character:
                for ch in player_name:
                    if ch.lower() not in "qwertyuiopasdfghjklzxcvbnm":
                        print("Invalid player name, only use the English alphabet")
                        return
                if f'{player_name}.txt' not in self.players:
                    self.players[f'{player_name}.txt'] = 0 # updates current list
                    with open(f'players/{player_name}.txt', 'w') as plr:
                        plr.write("0") # updates the file
                    print(f"Player: {player_name} created successfully!")
                    return True
                else:
                    return True
            else:
                print("Player name should have at least 1 and at most 12 characters")
        else:
            print("Maximum player number reached")

    def remove_player(self, player_name):
        if player_name in self.player_folder:
            self.player_folder.remove(player_name)
            self.players.pop(player_name)
            os.remove(f'players/{player_name}')
        else:
            print("Not a player")

    def add_player_win(self, player_name):
        pass

def char_to_emoji(map):
    """Returns the map converted from text characters to emoji"""
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
        '\n': '\n',
        }
    return ''.join(emoji.get(c, c) for c in map if c in emoji)

def flame_spread(start_row, start_col):
    """Returns the new map when flamethrower is used, or when player approaches tree while holding flamethrower"""
    global grid

    grid_string = ''.join(grid)
    grid_2d_list = [list(row) for row in grid_string.strip().split('\n')]
    row, col = len(grid_2d_list), len(grid_2d_list[0])

    def in_bounds(r, c):
        """Returns True if 2d index is within the range of row and column"""
        return 0 <= r < row and 0 <= c < col

    def flamethrowed(r, c):
        # Replaces 'T' to '.' if another 'T' shares the same side with the initial approached 'T' and is within the bounds else the recursion stops
        if not in_bounds(r, c) or grid_2d_list[r][c] != 'T':
            return
        grid_2d_list[r][c] = '.'

        # Continously calls itself for every direction
        for change_row, change_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            flamethrowed(r + change_row, c + change_col)

    # Will only call flamethrowed if the player is approaching 'T'
    if grid_2d_list[start_row][start_col] == 'T':
        flamethrowed(start_row, start_col)

    new_grid_string = '\n'.join(''.join(row) for row in grid_2d_list)

    return list(new_grid_string)

def describe_tile(tile):
    """Returns a tile converted from ASCII character to its tile name"""
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
    }.get(tile, 'unknown')

Leaderboard_opened = False
Lb = Leaderboard("Win Leaderboard")

def move_player(direction, Name, grid):

    # Takes the user input and proceeds accordingly
    global playing_game, Leaderboard_opened

    '''Processes each input in a string of inputs'''
    for inp in direction:
        inp = inp.upper()
        if playing_game:
            if inp == 'Q':
                playing_game = False
                return grid

            elif inp == 'P':
                # Picks up the found item
                if is_playing:
                    if not Name.found_item or len(Name.item) == 1:
                        continue
                    else:
                        Name.pickup(Name.found_item)
                        Name.found_item = None
                        Name.history['player'][-1] = '.'  # Sets the previous tile as an empty tile after picking up the item
                        Name._move_player("P", grid)
                elif not Name.found_item or len(Name.item) == 1:
                    continue
                else:
                    Name.pickup(Name.found_item)
                    Name.found_item = None
                    Name.history['player'][-1] = '.'  # Sets the previous tile as an empty tile after picking up the item
                    return grid
 
            elif inp == "!":
                # Restarts the game
                Name.reset()
                grid = list(MOTHERGRID)
                return grid

            elif inp == "L":
                Leaderboard_opened = False if Leaderboard_opened else True

            elif inp not in Name.moves:
                return Name._move_player(inp, grid)

            grid = Name._move_player(inp, grid)
    return grid

if __name__ == "__main__":
    # Outputs args.output_file if -o was called, else run the game.
    if not is_playing:
        Laro = Player(START)
        with open(args.output_file, "w", encoding="utf-8") as output:
            move_player(args.movement, Laro, grid)

            # Contents of the output file: no/clear and grid
            if Laro.player_mushroom_count == LVL_MUSHROOMS:
                output.write(f"CLEAR\n{GRID_HEIGHT} {GRID_WIDTH}\n{"".join(grid)}")
            else:
                output.write(f"NO CLEAR\n{GRID_HEIGHT} {GRID_WIDTH}\n{"".join(grid)}")
    else:
        Laro = Player(START)
        while True:
            new_player = input("\nPlayer, enter your name: ")
            if Lb.add_player(new_player):
                break
        while True:
            if playing_game:
                # Clears the terminal at the start, and after inputs
                clear_terminal()

                # Prints the map and mushroom count of the level
                print(f"Playing as: {new_player}\n")
                print(f"You need {LVL_MUSHROOMS} mushroom/s to win!")
                print("Grid:")
                print(char_to_emoji(grid))

                # Prints the collected mushroom count, and the valid moves
                print(f"{Laro.player_mushroom_count} out of {LVL_MUSHROOMS} mushroom/s collected")
                print('''
        [W] Move up
        [A] Move left
        [S] Move down
        [D] Move right
        [!] Reset
        [Q] Quit
        [L] Show/Hide leaderboard
                ''')

                # Prints the available item beneath the player, if any or none
                if not Laro.found_item:
                    print("No items here")
                elif len(Laro.item) == 1:
                    print('You already have an item, you can\'t pickup another')
                else:
                    print(f"[P] Pick up {describe_tile(Laro.found_item)}")

                # Prints the item currently held by the player, if any or none
                if not Laro.item:
                    print("Not holding anything")
                else:
                    print(f"Currently holding {char_to_emoji(Laro.item[0])}")

                if Leaderboard_opened:
                    Lb.draw_board()

                # Player input
                move = input("What will you do? ").strip().upper()
                grid = move_player(move, Laro, grid)

                if Laro.player_mushroom_count == LVL_MUSHROOMS:
                    clear_terminal()
                    print("Grid:")
                    print(char_to_emoji(grid))
                    print("-" * GRID_WIDTH * 2)
                    print(" " * ((GRID_WIDTH // 2) + 1), "You Won!")
                    print("-" * GRID_WIDTH * 2, "\n")

                if Laro.drowned:
                    clear_terminal()
                    print(f"You need {LVL_MUSHROOMS} mushroom/s to win!")
                    print("Grid:")
                    print(char_to_emoji(grid))
                    print("---------------------------------")
                    print("Game Over! Laro Craft can't swim!")
                    print("---------------------------------")
                    print(f"{Laro.player_mushroom_count} out of {LVL_MUSHROOMS} mushroom/s collected\n")

                clear_terminal()
            else:
                print(char_to_emoji(grid))
                print("Goodbye!")
                break
