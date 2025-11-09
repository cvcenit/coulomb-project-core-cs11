# Shroom Raider

## Table of Contents

* [User Manual](#user_manual)
  * [Startup](#start_up)
  * [Main Menu]
  * [Controls]
    * [Movement]
    * [Pickup]
    * [Restart and Exit]
  * [Level Creator]
* [Code Organization]
  * [Graphical User Interface (GUI)]
  * [Main Menu]
  * [Gameplay]
    * [Map]
    * [Tiles]
    * [Movement]
    * [Input]
  * [Level Creation]
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

### Level Creator

## Code Organization

_In this section, you will get to learn about the secrets behind the world of Shroom Raider!_

### Start Up
* ArgumentParser from argparse\
   This was done to implement the -f, -m, and -o flags for a custom map file, move sequnece, and outfile file respectively through the following functions:
  > add_args() - Creates the custom arguments: -f, -o, -m.\
  > 
### Graphical User Interface
### Gameplay
### Level Creation
