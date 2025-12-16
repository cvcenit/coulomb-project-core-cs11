# TODO: check sa pyright if my type hints are accurate, especially those
#  no-return-funcs na nilagyan ko ng " -> None" if may error alisin nalang
#  +++ what does add_args return tama ba ginawa q??

import os
from argparse import ArgumentParser, Namespace
from posix import remove


# PREREQUISITE FUNCTIONS
def add_args() -> Namespace:
    """
    Parses arguments. This will only be called if __name__ == "__main__" below.

    Returns:
        argparse.Namespace: An object containing the parsed arguments
        with attributes `stage_file`, `movement`, and `output_file`.
    """

    parser = ArgumentParser(add_help=False)
    if __name__ == "__main__":
        parser.add_argument('-f', '--stage_file')
        parser.add_argument('-m', '--movement')
        parser.add_argument('-o', '--output_file')
    assert isinstance(parser.parse_args(), Namespace)
    return parser.parse_args()


def pick_map(stage_file: str | None = None) -> str:
    """
    Picks out the map depending on whether there is a stage_file or not

    Args:
        stage_file (str | None): stage to be played, which may have a file path of string type or None of None type

    Returns:
        str: If stage_file is a string, the map string in that file path is returned. If not, the default map string.
    """

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


def is_user_playing(output_file: str | None = None) -> bool:
    """
    Determines if the user will play, or output a file

    Args:
        output_file (str | None): path to the output file, which may have a
            file path in string format where output will be written or None of None type

    Returns:
        bool: True if -o has an argument, False otherwise
    """
    return True if output_file is None else False


def clear_terminal() -> None:
    """
    Clears the terminal, does not return anything
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Checks if the command is running from shroom_raider.py, and not as a module/from another file
if __name__ == "__main__":
    terminal_args: Namespace = add_args()
    is_playing: bool = is_user_playing(terminal_args.output_file)  # Mode if to play or to output
    lvlmap: str = pick_map(terminal_args.stage_file)  # Map as string/raw
else:
    terminal_args: Namespace = add_args()
    is_playing: bool = is_user_playing()  # Mode if to play or to output
    lvlmap: str = pick_map()  # Map as string/raw

# Determines if the player is still playing the game
playing_game: bool = True

# Makes a list with the tiles as its elements from "lvlmap" excluding the values for the height and width
lvlmapcontent: list = list(lvlmap[lvlmap.index('\n') + 1:])

# Takes the integer strings at their respective indices then converts them into integers
GRID_HEIGHT: int = int(lvlmap[:lvlmap.index(' ')])  # height is before ' '
GRID_WIDTH: int = int(lvlmap[lvlmap.index(' ') + 1: lvlmap.index('\n')])  # width is after ' ' and before the first \n

# Serves as the base grid for the level (will not be mutated)
MOTHERGRID: list = list(''.join(lvlmapcontent))

# Serves as the starting index for the level
START: int = MOTHERGRID.index("L")

# Serves as the working grid for the level (will be mutated)
global_grid: list = list(''.join(lvlmapcontent))

# Counts the amount of mushrooms needed to win the level
LVL_MUSHROOMS: int = 0
for x in lvlmap:
    if x == "+":
        LVL_MUSHROOMS += 1

# Lists the indices of '\n' characters
_n_indices: range = range(lvlmapcontent.index('\n'), len(lvlmapcontent), GRID_WIDTH + 1)


class Player:
    """The Player class contains all the necessary attributes and methods connected to the player input"""

    # Library of inputs with their corresponding change in index (+1 in width to accommodate for the '\n' characters)
    moves: dict[str, int] = {
        'W': -(GRID_WIDTH + 1),
        'S': GRID_WIDTH + 1,
        'A': -1,
        'D': 1,
        'P': 0
    }

    def __init__(self, starting_index: int) -> None:
        """
        Sets the default attributes, initiating the class

        Args:
            starting_index (int): starting position of player before any movements are done
        """
        super(Player, self).__init__()
        self.starting_index: int = starting_index
        self.item: list = []
        self.history: dict = {'player': ['.']}
        self.found_item: None | str = None
        self.drowned: bool = False
        self.player_mushroom_count: int = 0
        self.player_index: int = self.starting_index

    def reset(self) -> None:
        """Resets the attributes back to default"""
        self.item = []
        self.history = {'player': ['.']}
        self.found_item = None
        self.drowned = False
        self.player_mushroom_count = 0
        self.player_index = self.starting_index

    def pickup(self, tile: str | None) -> str | None:
        """
        Adds current tile to the list of items held by the player, then returns the picked up tile in emoji.

        Args:
            tile (str): single-character string of the object being picked up in ASCII format, or None

        Returns:
            str: emoji equivalent of the character argument if there is an
                object being picked up in the tile or else None is returned
        """

        self.item.append(tile)
        return tile if tile is None else char_to_emoji(tile)

    def move_self(self, direction: str, grid: list) -> list:
        """
        Takes the directional input of the player and moves the player accordingly

        Args:
            direction (str): movement of the player in string
            grid (list): 2D representation of the playing grid

        Returns:
            a list of characters representing the new grid after applying the directions
        """

        global playing_game


        def moveto(under_tile: str) -> None:
            """
            Mutates the grid

            Args:
                under_tile (str): single-character string of the tile where the player last moved from

            The function does not return anything but only changes the history
            """

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
                    col = (new_index % (GRID_WIDTH + 1))
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

                # Ensures the 'moveto' function appends the correct under_tile when the player moves
                if f"Rock {new_index}" in self.history:
                    rock_under_tile = self.history[f"Rock {new_index}"]  # Sets the tile under the rock to history.

                # Checks if it will go out of bounds or in a '\n' index
                if new_rock_index >= len(grid) or new_rock_index in _n_indices:
                    return grid

                # Converts a water tile into a paved tile
                elif grid[new_rock_index] == "~":
                    grid[new_rock_index] = "_"
                    moveto(rock_under_tile)

                # Moves the rock along an empty tile
                elif grid[new_rock_index] == ".":
                    grid[new_rock_index] = "R"
                    moveto(rock_under_tile)

                # Moves the rock along a paved tile
                elif grid[new_rock_index] == "_":
                    grid[new_rock_index] = "R"
                    self.history[f"Rock {new_rock_index}"] = "_"  # Takes note of the tile under the rock
                    moveto(rock_under_tile)

                # Checks if the player is trying to move two rocks at the same time or into a non-empty tile
                elif grid[new_rock_index] == "R" or 'x' or '*' or '+':
                    return grid

                # Removes the Rock at index new_index from history after it gets moved
                if f"Rock {new_index}" in self.history:
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
    def __init__(self, title: str) -> None:
        super(Leaderboard, self).__init__()
        self.title: str = title
        self.max_players: int = 10
        self.max_character: int = 12
        self.player_folder: list[str] = os.listdir(f'players')
        self.players: dict[str, int] = {}
        for player_file in self.player_folder:
            with open(f'players/{player_file}', 'r') as plr:
                self.players[player_file] = int(plr.read())

    def show_board(self) -> None:
        """
        Shows the leaderboard to the screen, returns None
        """
        print(f"\n{self.title}")
        print("|----Player----|--Wins--")
        for player in sorted(self.players, reverse=True, key=lambda x: self.players[x]):
            print(f"|{player[:-4]}",
            " " * (self.max_character - len(player[:-4])),
                f"|{self.players[player]}")
        print('\n')

    def add_player(self, player_name: str) -> bool:
        """
        Adds a player to player saves and the list
        
        Args:
            player_name (str): name of the player to be played as
        Returns:
            True if the player already exists (play as the existing) or
            the player does not exist and there are less than 10 players and 
            player_name have 1 to 12 characters and all characters are in the English alphabet

            False otherwise
        """

        if f'{player_name}.txt' in self.players:
            return True
        if len(self.player_folder) < self.max_players:
            if 0 < len(player_name) <= self.max_character:
                if not player_name.isalpha():
                    print("Invalid player name, only use the English alphabet")
                    return False
                if f'{player_name}.txt' not in self.players:
                    self.players[f'{player_name}.txt'] = 0  # updates current list
                    with open(f'players/{player_name}.txt', 'w') as plr:
                        plr.write("0")  # updates the file
                    print(f"Player: {player_name} created successfully!")
                    return True
                else:
                    return True
            else:
                print("Player name should have at least 1 and at most 12 characters")
                return False
        else:
            print("Maximum player number reached")
            return False

    def remove_player(self, player_name: str) -> bool:
        """
        Removes a player from the player saves and the list
        
        Args:
            player_name (str): name of the player to be removed
        Returns:
            Always returns True
        """
        if player_name in self.player_folder:
            self.player_folder.remove(player_name)
            self.players.pop(player_name)
            os.remove(f'players/{player_name}')
        else:
            print("Not a player")
        return True

    def add_player_win(self, player_name: str) -> None:
        """
        Adds a win to the player's save
        
        Args:
            player_name (str): name of the player that won
        Returns nothing
        """
        self.players[f'{player_name}.txt'] += 1
        with open(f'players/{player_name}.txt', 'w') as plr:
            plr.write(str(self.players[f'{player_name}.txt']))


def char_to_emoji(tiles: str | list) -> str:
    """
    Converts the grid from text characters in ASCII format to emoji

    Args:
        tiles (str): string of multiple lines or list of grid representing the map using ASCII characters

    Returns:
        str: emoji equivalent of each character in the grid
    """

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
    return ''.join(emoji.get(c, c) for c in tiles if c in emoji)


def flame_spread(start_row: int, start_col: int) -> list:
    """
    Returns the new map when flamethrower is used, or when player approaches tree while holding flamethrower

    Args:
        start_row (int): row of the position of tree being approached
        start_col (int): column of the position of tree being approached

    Returns:
        list: the resulting grid after flamethrower is used
    """

    global global_grid

    grid_string = ''.join(global_grid)
    grid_2d_list = [list(row) for row in grid_string.strip().split('\n')]
    row, col = len(grid_2d_list), len(grid_2d_list[0])

    def in_bounds(r: int, c: int) -> bool:
        """
        Determines if 2D index is within the range of row and column

        Args:
            r (int): row of the next adjacent tree's position
            c (int): column of the next adjacent tree's position

        Returns:
            bool: True if r and c is inside the grid and false otherwise
        """

        return 0 <= r < row and 0 <= c < col

    def apply_flamethrower(r: int, c: int) -> None:
        """
        Changes the grid as flamethrower is being applied to consecutive trees

        Args:
            r (int): row of the next adjacent tree's position
            c (int): column of the next adjacent tree's position

        Returns None. The function directly changes the grid.
        """

        if not in_bounds(r, c) or grid_2d_list[r][c] != 'T':
            return
        # Base of the recursion stops when there no longer exists an adjacent 'T' or r and c is out of bounds
        grid_2d_list[r][c] = '.'

        # Continuously calls itself for every direction
        for change_row, change_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            apply_flamethrower(r + change_row, c + change_col)

    # Will only recursively call apply_flamethrower if the player is approaching 'T'
    if grid_2d_list[start_row][start_col] == 'T':
        apply_flamethrower(start_row, start_col)

    new_grid_string = '\n'.join(''.join(row) for row in grid_2d_list)

    return list(new_grid_string)


def describe_tile(tile: str) -> str:
    """
    Converts the grid's ASCII character to its tile name

    Args:
        tile (str): single-character string of the grid's symbol

    Returns:
        str: description of the character argument
    """

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


def move_player_with_string(direction: str, name: Player, grid: list) -> list:
    """
    Takes the user input and proceeds accordingly

    Args:
        direction (str): movement of the player in string
        name (Player): instance of the Player class representing the current player
        grid (list): 2D representation of the playing grid

    Returns:
        list: updated grid in 2D list format after movement changes are applied to the initial playing grid
    """

    global playing_game, Leaderboard_opened

    # Processes each input in a string of inputs
    for inp in direction:
        inp = inp.upper()
        if playing_game:
            if inp == 'Q':
                playing_game = False
                return grid

            elif inp == 'P':
                # Picks up the found item
                if is_playing:
                    if not name.found_item or len(name.item) == 1:
                        continue
                    else:
                        name.pickup(name.found_item)
                        name.found_item = None
                        name.history['player'][-1] = '.'  # Sets the previous tile to empty tile after picking up item
                        name.move_self("P", grid)
                elif not name.found_item or len(name.item) == 1:
                    continue
                else:
                    name.pickup(name.found_item)
                    name.found_item = None
                    name.history['player'][-1] = '.'  # Sets the previous tile to empty tile after picking up item
                    return grid

            elif inp == "!":
                # Restarts the game
                name.reset()
                grid = list(MOTHERGRID)
                return grid

            elif inp == "L":
                Leaderboard_opened = False if Leaderboard_opened else True

            elif inp == "R": 
                Lb.show_board()  
                while True:
                    remove_this_player = input("Which one? (Type any number to exit deletion) ")
                    if remove_this_player != new_player:
                        if Lb.remove_player(f'{remove_this_player}.txt'):
                            break
                    else:
                        print("Can't delete current player!")
                break

            elif inp not in name.moves:
                break

            else:
                grid = name.move_self(inp, grid)
    return grid


if __name__ == "__main__":
    # Outputs args.output_file if -o was called, else run the game.
    if not is_playing:
        Laro = Player(START)
        with open(terminal_args.output_file, "w", encoding="utf-8") as output:
            move_player_with_string(terminal_args.movement, Laro, global_grid)

            # Contents of the output file: no/clear and grid
            if Laro.player_mushroom_count == LVL_MUSHROOMS:
                output.write(f"CLEAR\n{GRID_HEIGHT} {GRID_WIDTH}\n{"".join(global_grid)}")
            else:
                output.write(f"NO CLEAR\n{GRID_HEIGHT} {GRID_WIDTH}\n{"".join(global_grid)}")
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
                print(char_to_emoji(global_grid))

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
        [R] Delete a player
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
                    Lb.show_board()

                # Player input
                move = input("What will you do? ").strip().upper()
                global_grid = move_player_with_string(move, Laro, global_grid)

                clear_terminal()
            else:
                if Laro.player_mushroom_count == LVL_MUSHROOMS:
                    clear_terminal()
                    print(f"Won as {new_player} on:\n")
                    print(char_to_emoji(global_grid))
                    print("-" * GRID_WIDTH * 2)
                    print(" " * ((GRID_WIDTH // 2) + 1), "You Won!")
                    print("-" * GRID_WIDTH * 2, "\n")
                    Lb.add_player_win(new_player)
                    Lb.show_board()

                elif Laro.drowned:
                    clear_terminal()
                    print(f"Lost as {new_player} on:\n")
                    print(char_to_emoji(global_grid))
                    print("-----------------------------------")
                    print(f"Game Over! {new_player} can't swim!")
                    print("-----------------------------------")
                    print(f"{Laro.player_mushroom_count} out of {LVL_MUSHROOMS} mushroom/s collected\n")
                    Lb.show_board()
                else:
                    clear_terminal()
                    print("Grid:")
                    print(char_to_emoji(global_grid))
                    Lb.show_board()
                    print("Goodbye!")
                break