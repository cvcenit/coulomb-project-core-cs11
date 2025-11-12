# Shroom Raider

## Table of Contents

* [User Manual](#user-manual)
  * [Startup](#start-up)
  * [Main Menu](#main-menu)
  * [Controls](#controls)
    * [Movement](#movement)
    * [Pickup](#pickup)
    * [Restart and Exit](#restart-and-exit)
  * [Level Creation](#level-creation)
* [Code Organization](#code-organization)
  * [Graphical User Interface (GUI)](#graphical-user-interface-(GUI))
  * [Gameplay](#gameplay)
    * [Map](#map)
    * [Tiles](#tiles)
    * [Movement](#movement-1)
    * [Input](#input)
  * [Level Creation](#level-creation-1)
* [Unit Tests]
* [Bonus Features]
  * [Level Creation]

## User Manual

_Hello, aspiring adventurer. Welcome to Shroom Raider! Here's a quick rundown on how to embark on your adventure:_

### Start Up

_Here are the following ways you can run the game:_

* Pre-requisites
  - [Download python](https://realpython.com/installing-python/) in your computer.
  - Navigating the computer using the [terminal.](https://terminalcheatsheet.com/guides/navigate-terminal) 

* Raw Game - This method will run the game with its presets.
  - Download the whole game folder.
  - Open up your operating system's terminal by using the search bar.
  - Navigate through the computer's directory using the terminal until the directory that contains the game file.
  - Run the following command:
    > python3 shroom_raider.py

* Custom Map
  - Create a text (.txt) file in the same directory as the game file.
  - Open the file in a text editor.
  - Create a rectangular grid using the following characters:
    > Tiles:\
    > Player tile ('L') - Required; Only one (1) may exist; Initial position of the player.\
    > Mushroom Tile ('+') - Required; More than one (1) may exist; Main goal of the game: collect all mushrooms.\
    > Empty Tile ('.') - Used to fill in gaps between non-empty tiles; The player can move to these tiles.\
    > Tree Tile ('T') - Acts as a wall that the player can't pass through unless holding an item.\
    > Rock Tile ('R') - Can be pushed by the player.\
    > Water Tile ('~') - Hazardous tile; The player loses if they move into a water tile; Can be converted into a paved tile when a rock is pushed into a water tile.\
    > Paved Tile ('_') - Created when a rock is pushed into a water tile; The player can move to these tiles.
    >
    > Items:\
    > Axe ('x') - Used to cut down a tree the player moves to.\
    > Flamethrower ('*') - Used to burn down all the trees connected to the one the player moves to.
    >
    > Sample:\
    > TTTT~\~\~\~\~TTTTT\
    > T.L.\~.xT\~\~\~\~\~T\
    > T.R.\~.\~+\~TTT\~T\
    > T\~.\~\~.\~.\~T\~T\~T\
    > T\~\~\~\~T\~R\~T\~T\~T\
    > T...\~x\~\~\~T\~T\~T\
    > TT.T\~.\~.\~T\~T\~T\
    > T\~+...~..*\~+\~T\
    > T\~\~\~\~\~\~\~\~\~\~\~\~T\
    > TTTTTTTTTTTTTT
  - Count the number of rows and columns.
  - Insert the number of rows and columns respectively in the first line of the file.
    > 10 14\
    > TTTT~\~\~\~\~TTTTT\
    > T.L.\~.xT\~\~\~\~\~T\
    > T.R.\~.\~+\~TTT\~T\
    > T\~.\~\~.\~.\~T\~T\~T\
    > T\~\~\~\~.\~R\~T\~T\~T\
    > T...\~x\~\~\~T\~T\~T\
    > TT.T\~.\~T\~T\~T\~T\
    > T\~+...~..*\~+\~T\
    > T\~\~\~\~\~\~\~\~\~\~\~\~T\
    > TTTTTTTTTTTTTT
  - Save the file changes.
  - Open up your operating system's terminal by using the search bar.
  - Navigate through the computer's directory using the terminal until the directory that contains the game file.
  - Run the following command:
    > python3 shroom_raider.py -f map.txt

* With a Movement String and an Output File
  - Compile the sequence of moves you wish to perform.
  - Create an empty text (.txt) file that will serve as the output file in the same directory as the game file.
  - Open up your operating system's terminal by using the search bar.
  - Navigate through the computer's directory using the terminal until the directory that contains the game file.
  - Run the following command:
    > python3 shroom_raider.py -m (your sequence of moves) -o output.txt
  - For custom maps:
    > python3 shroom_raider.py -f map.txt -m (your sequence of moves) -o output.txt

### Main Menu

### Controls

_After arriving into location of your adventure, here's how to navigate around the area:_

#### Movement

* Directions - Moves the player accordingly.
  * W - Up
  * A - Left
  * S - Down
  * D - Right

* Tiles - Specific tile interactions.
  * Player to Water Tile - Player loses the game whenever they move to a water tile.
  * Player to Tree Tile - Player cannot pass through tree tiles unless holding an item.
  * Player to Rock Tile - Player can only push the rock to a non-empty tile, a water tile, or a paved tile.
  * Player to Mushroom Tile - Player will automatically pickup the mushroom upon stepping on it.
  * Rock Tile to Water Tile - Converts the water tile into a paved tile.

#### Pickup

_Press P to pick up the following items you can encounter during your journey:_

* Axe - Cuts down the tree along the player's path allowing them to pass through; Can only be used once.
* Flamethrower - Burns down all the trees connected to the one along the player's path; Can only be used once.\
  (_Note: For all mentioned items, only one can be equipped at a time._)

#### Restart and Exit

_Unfortunate events are unavoidable during an adventurer's journey, here are the controls if you wish to regroup for a while:_

* Restart ('!') - Immediately go back at the start of your journey; Resets the loaded level and undos all progress made.
* Exit ('Q') - Take some time off from your journey to regroup; Exits the program.

### Level Creation

## Code Organization

_In this section, you will get to learn about the secrets behind the world of Shroom Raider!_

### Start Up
* ArgumentParser from argparse

  This was done to implement the -f, -m, and -o flags for a custom map file, move sequnece, and outfile file respectively through the following functions:
  > add_args() - Creates the custom arguments: -f, -o, -m.
  > 
  > pick_map(stage_file=None) - If the user inputs a custom map file, the function will set the map file as 'lvlmap'; otherwise, 'lvlmap' will be the preset map.
  > 
  > choose_mode(output_file=None) - If the user inputs an output file, it will return the mode '', where the game file will take the player's move sequence and redirect its output towards the output file; otherwise, it will return the mode 'play', where the game will run and will be taking inputs throught the terminal.
  
### Graphical User Interface

### Gameplay
* Map and Map Attributes
  
   The map process starts from determining whether it will load a custom map or the preset map. Then the following attributes will be determined:
 * Map Height - Count of rows in 'lvlmap'; The first number string in a map file.
   > GRID_HEIGHT - Takes the second number string in a map file and converts to an integer.
 * Map Width - Count of columns in 'lvlmap'; The second number string in a map file.
   > GRID_WIDTH - Takes the second number string in a map file and converts to an integer.
 * Map Content - All tiles in 'lvlmap'.
   > lvlmapcontent - Converts the characters after the first new line character in a map file to a list of characters.
 * Base Grid - Default state of the map; will not be mutated.
   > MOTHERGRID - Converts the characters in the string from rejoining the tiles in 'lvlmapcontent' to a new list of characters; avoids accidental mutation of 'MOTHERGRID' when mutating 'grid'.
 * Active Grid - Current state of the map; mutated based on the player's input.
   > grid - Converts the characters in the string from rejoining the tiles in 'lvlmapcontent' to a new list of characters; avoids accidental mutation of 'MOTHERGRID' when mutating 'grid'.
 * Mushroom Count - Amount of mushrooms found within the map.
   > LVL_MUSHROOMS - A for loop will increase the count by one(1) for every '+' in 'lvlmap'.
 * New Line Character Indices - List of the indices of the new line characters in 'lvlmap'; Used as reference to avoid invalid mutation.
   > _n_indices - Starts from the index of the first new line character and jumps to the next index with 'GRID_WIDTH' distance.
 * Character to Emoji Conversion - The process of converting the active grid before being displayed is done by the function:
   > char_to_emoji(map) - Returns the map converted from text characters to their respective emojis.
* Player Attributes
  
   The player's default attributes when starting the map are the following:\
   > item = [] - The player will be holding no items.\
   > history = {'player': ['.'\]} - The tile under the player is set to an empty tile.\
   > found_item = None - The player isn't standing on any items.\
   > DROWNED = False - The player can't arrive on a water tile.\
   > player_mushroom_count = 0 - The player haven't found any mushrooms.\
   > player_index = grid.index('L') - The player's current position is the initial position in the grid.
* Main Loop - Loops the gameplay code while main = 0; Terminates the game otherwise.
* Inputs

   The valid inputs the user can use are the following:
  
  * Directional - Dictionary of inputs that changes the player's position
    > W - Moves the player up by one row; translates to the index change of -(GRID_WIDTH + 1).\
    > S - Moves the player down by one row; translates to the index change of GRID_WIDTH + 1.\
    > A - Moves the player left by one tile; translates to the index change of -1.\
    > D - Moves the player right by one tile; translates to the index change of 1.

  * Operational - Collection of inputs the makes changes in the game's state.
    > P - Picks up the item under the player if there is one.
    > Q - Exits the game.
    > ! - Restarts the current map; returns all player attributes to default.

  * Sequence of Moves
    - In a sequence of moves, the inputs will be processed individualy starting from the left; an invalid input will terminate the process prematurely.

* Movement and Tiles

  The movement functionalities and tile interactions are executed through the following functions and/or blocks of code:
  * Movement
    > a) move_player(direction) - Takes an input or a string of inputs and processes based on its functionality (Directional or Operational); breaks the input processing loop after encountering an invalid move.
    > 
    > b) _move_player(direction) - Gets called by move_player(direction) if the processed inpur is a directional move; checks whether the desired move of the player is valid, and will process player-tile and tile-tile interactions caused by the desired move; also calls and executes item functionalities if applicable.
    >
    > c) moveto(under_tile) - Sub function of _move_player(direction); gets called to mutate the active grid based on the player's move.
    >
    > d) describe_tile(tile) -  Describes the tile in the input.
 
* Items
  
  The functionality of the items are executed through the following functions and/or blocks of code:
  * Axe
    > if target_tile == 'T' and if item[0\] == 'x' - If the player is trying to move to a tree tile and is holding an axe, the tree tile will be replaced with an empty tile and the player will be able to move.
  * Flamethrower
    > flame_spread(start_row, start_col) - will call the sub function: flamethrowed(r, c) if the tile is a tree tile.
    > flamethrowed(r, c) - replaces the the tile at row r, col c to an empty tile (if it is a tree tile; breaks the recursion other wise.) and repeatedly calls itself for all adjacent tiles in all four(4) directions.
    
### Level Creation

## Unit Test

## Additional Features

In addition to the base game, the following features have been added in the following sections:

### Graphical User Interface (GUI)
* Main Menu - The main menu gives the following options to the player:
  * Play Menu
    - Allows the player to input their character's name; alternatively, the player can also delete existing character names.
      * Character Name
        - Contains the date of creation, number of mushrooms collected, and total amount of time played.
        - Updates after each game, win or lose.
    - The player can select from different level options:
      * Story
        - Contains ten(10) levels that are increasing in difficulty.
      * Bonus
        - Special level made by the creators.
      * User-made
        - Allows the player to create and edit their own level.
    - 
