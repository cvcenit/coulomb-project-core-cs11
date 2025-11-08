# Shroom Raider

## Table of Contents

* [User Manual](#user_manual)
  * [Startup](#start_up)
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
  - Create a text (.txt) file.
  - Open the file in a text editor.
  - Create a rectangular grid using the following characters:
    > Tiles:
    > 
    > Player tile ('L') - Required; Only one (1) may exist; Initial position of the player.
    > Mushroom Tile ('+') - Required; More than one (1) may exist; Main goal of the game: collect all mushrooms.
    > Empty Tile ('.') - Used to fill in gaps between non-empty tiles; The player can move to these tiles.
    > Tree Tile ('T') - Acts as a wall that the player can't pass through unless holding an item.
    > Rock Tile ('R') - Can be pushed by the player.
    > Water Tile ('~') - Hazardous tile; The player loses if they move into a water tile; Can be converted into a paved tile when a rock is pushed into a water tile.
    > Paved Tile ('_') - Created when a rock is pushed into a water tile; The player can move to these tiles.
    >
    > Items:
    > Axe ('x') - Used to cut down a tree the player moves to.
    > Flamethrower ('*') - Used to burn down all the trees connected to the one the player moves to.
    >
    > Sample:
    > TTTTTTTTT
    > T...+...T
    > T...~...T
    > T...R.T.T
    > T.T.LTT.T
    > T.x...*.T
    > T.......T
    > T.......T
    > TTTTTTTTT
  - Follow the initial steps as mentioned in the Raw Game section.
  - 


