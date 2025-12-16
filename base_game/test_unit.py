from src import shroom_raider
from shroom_raider import move_player


def test_char_to_emoji():
    test1 = '''\
TTTTTTTTT
T...+...T
T...~...T
T...R.T.T
T.T.LTT.T
T.x...*.T
T.......T
T.......T
TTTTTTTTT'''

    test2 = '''\
...+...
...~..
...R.T.
..LTT.
.x...*.
T...Tqq
TTTTT**TT'''

    test3 = '''\
TTTTTTTTT.....................
T...+.RRRRRRRRRR+++++++____..T
T..~.~>~.~>~/~~,,~xxxxxx.~...T
T._____.****LLLL.______,xXXTTT'''

    assert shroom_raider.char_to_emoji(test1) == '''\
🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲　　　🍄　　　🌲
🌲　　　🟦　　　🌲
🌲　　　🪨　🌲　🌲
🌲　🌲　🧑🌲🌲　🌲
🌲　🪓　　　🔥　🌲
🌲　　　　　　　🌲
🌲　　　　　　　🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲'''

    assert shroom_raider.char_to_emoji(test2) == '''\
　　　🍄　　　
　　　🟦　　
　　　🪨　🌲　
　　🧑🌲🌲　
　🪓　　　🔥　
🌲　　　🌲
🌲🌲🌲🌲🌲🔥🔥🌲🌲'''

    assert shroom_raider.char_to_emoji(test3) == """\
🌲🌲🌲🌲🌲🌲🌲🌲🌲　　　　　　　　　　　　　　　　　　　　　
🌲　　　🍄　🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🍄🍄🍄🍄🍄🍄🍄⬜⬜⬜⬜　　🌲
🌲　　🟦　🟦🟦　🟦🟦🟦🟦🟦🪓🪓🪓🪓🪓🪓　🟦　　　🌲
🌲　⬜⬜⬜⬜⬜　🔥🔥🔥🔥🧑🧑🧑🧑　⬜⬜⬜⬜⬜⬜🪓🌲🌲🌲"""


class TestPlayer:

    def test_pickup(self):
        player = shroom_raider.Player(starting_index=0)

        test1, test2, test3 = 'x', '*', '.'

        player.item.clear()
        player.pickup(test1)
        assert test1 in player.item
        assert len(player.item) == 1
        assert player.pickup(test1) == '🪓'

        player.item.clear()
        player.pickup(test2)
        assert test2 in player.item
        assert len(player.item) == 1
        assert player.pickup(test2) == '🔥'

        player.item.clear()
        player.pickup(test3)
        assert test3 in player.item
        assert len(player.item) == 1
        assert player.pickup(test3) == '　'


def test_flame_spread():

    assert ''.join(shroom_raider.flame_spread(0, 1)) == """\
....~~~~~.....
..L.~.xT~~~~~.
..R.~.~+~TTT~.
.~.~~.~.~T~T~.
.~~~~.~R~T~T~.
....~x~~~T~T~.
...T~.~T~T~T~.
.~+...~..*~+~.
.~~~~~~~~~~~~.
.............."""

    assert ''.join(shroom_raider.flame_spread(1, 7)) == """\
TTTT~~~~~TTTTT
T.L.~.x.~~~~~T
T.R.~.~+~TTT~T
T~.~~.~.~T~T~T
T~~~~.~R~T~T~T
T...~x~~~T~T~T
TT.T~.~T~T~T~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT"""
    assert ''.join(shroom_raider.flame_spread(5, 9)) == """\
TTTT~~~~~TTTTT
T.L.~.xT~~~~~T
T.R.~.~+~...~T
T~.~~.~.~.~.~T
T~~~~.~R~.~.~T
T...~x~~~.~.~T
TT.T~.~T~.~.~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT"""
    assert ''.join(shroom_raider.flame_spread(5, 6)) == """\
TTTT~~~~~TTTTT
T.L.~.xT~~~~~T
T.R.~.~+~TTT~T
T~.~~.~.~T~T~T
T~~~~.~R~T~T~T
T...~x~~~T~T~T
TT.T~.~T~T~T~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT"""


def test_describe_tile():
    assert shroom_raider.describe_tile('.') == 'empty'
    assert shroom_raider.describe_tile('T') == 'tree'
    assert shroom_raider.describe_tile('+') == 'mushroom'
    assert shroom_raider.describe_tile('R') == 'rock'
    assert shroom_raider.describe_tile('L') == 'player'
    assert shroom_raider.describe_tile('`') == 'water'
    assert shroom_raider.describe_tile('_') == 'paved'
    assert shroom_raider.describe_tile('x') == 'axe'
    assert shroom_raider.describe_tile('*') == 'flamethrower'


def test_move_player_with_string():

    # Test case 1: moving to empty tile.
    shroom_raider.move_player_with_string('a')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', 'L', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 2: bumping onto a tree.
    shroom_raider.move_player_with_string('w')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', 'L', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 3: moving to empty tile.
    shroom_raider.move_player_with_string('s')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'L', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', 'R', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 4: pushing a rock.
    shroom_raider.move_player_with_string('d')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', 'L', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 5: walking towards a water tile. game ends.
    shroom_raider.move_player_with_string('dd')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', 'L', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    assert shroom_raider.main == 1
    shroom_raider.main = 0
    shroom_raider.move_player_with_string('!')

    # Test case 6: walking past a water tile. player should not move from the water tile. game ends.
    shroom_raider.move_player_with_string('ddd')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', 'L', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    assert shroom_raider.main == 1
    shroom_raider.main = 0
    shroom_raider.move_player_with_string('!')

    # Test case 7: walking past a tree. player should stop before tree.
    shroom_raider.move_player_with_string('sssssdd')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', 'L', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 8: player pushes rock to pavement.
    shroom_raider.move_player_with_string('ss')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', 'L', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 9: player walks on pavement.
    shroom_raider.move_player_with_string('sss')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', 'L', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 10: walking beyond the grid. player should not move further than grid.
    shroom_raider.move_player_with_string('aa')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', 'L', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', 'R', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '~', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '+', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 11: player walks on a mushroom.
    shroom_raider.move_player_with_string('ssssss')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', 'L', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 12: player walks past a mushroom.
    shroom_raider.move_player_with_string('ssssssdd')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', 'L', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 13: player walks to an axe.
    shroom_raider.move_player_with_string('ssssssdddww')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'L', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 14: player walks past an axe without picking up.
    shroom_raider.move_player_with_string('ssssssdddwww')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', 'L', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', 'x', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 15: player picks up axe then walks away.
    shroom_raider.move_player_with_string('ssssssdddwwpw')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', 'L', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 16: player uses axe on tree.
    shroom_raider.move_player_with_string('ssssssdddwwpssaaw')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'L', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 17: player uses axe then bumps on tree.
    shroom_raider.move_player_with_string('ssssssdddwwpssaawaa')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', 'x', 'T', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '+', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', 'R', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '~', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', 'L', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 18: player walks to flamethrower.
    shroom_raider.move_player_with_string('ssssssdddwwpwwwwddapdssssssdd')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', '.', '.', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '.', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '_', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', 'L', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 19: player walks past flamethrower without picking up.
    shroom_raider.move_player_with_string('ssssssdddwwpwwwwddapdssssssddaa')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', '.', '.', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '.', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '_', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', 'L', '.', '*', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 20: player picks up flamethrower then walks away.
    shroom_raider.move_player_with_string('ssssssdddwwpwwwwddapdssssssddpaa')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', '.', '.', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '.', '~', 'T', 'T', 'T', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '_', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', '.', '~', 'T', '~', 'T', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', 'L', '.', '.', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Test case 21: player uses flamethrower on tree.
    shroom_raider.move_player_with_string('ssssssdddwwpwwwwddapdssssssddpw')
    assert shroom_raider.grid == ['T', 'T', 'T', 'T', '~', '~', '~', '~', '~', 'T', 'T', 'T', 'T', 'T', '\n', 'T', '.', '.', '.', '~', '.', '.', '.', '~', '~', '~', '~', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '.', '~', '.', '.', '.', '~', 'T', '\n', 'T', '~', '.', '~', '~', '.', '~', '.', '~', '.', '~', '.', '~', 'T', '\n', 'T', '~', '_', '~', '~', '.', '~', '.', '~', '.', '~', '.', '~', 'T', '\n', 'T', '.', '.', '.', '~', '.', '~', '_', '~', '.', '~', '.', '~', 'T', '\n', 'T', 'T', '.', 'T', '~', '.', '~', '.', '~', 'L', '~', '.', '~', 'T', '\n', 'T', '~', '.', '.', '.', '.', '~', '.', '.', '.', '~', '+', '~', 'T', '\n', 'T', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', 'T', '\n', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
    shroom_raider.move_player_with_string('!')

    # Cases that uses a map different from the default map to showcase other possible moves
    TEST_MAP_1 = list("""\
R..R..R
...R.RT
xR...R*
RR.L.RR
~RR..R+
.._R...
R..R..R""")

    grid_1 = list(TEST_MAP_1)

    TEST_MAP_2 = list("""\
.......
.......
...x...
..xL*..
...*...
.......
......+""")

    grid_2 = list(TEST_MAP_2)

    # Map is TEST_MAP_1, set all the vars according to new map
    shroom_raider.GRID_HEIGHT, shroom_raider.GRID_WIDTH = 7, 7
    shroom_raider.MOTHERGRID = TEST_MAP_1
    shroom_raider.grid = grid_1

    # Lists the indices of '\n' characters
    shroom_raider._n_indices = range(TEST_MAP_1.index('\n'), len(TEST_MAP_1), 7 + 1)

    # Default player attributes
    shroom_raider.item = []
    shroom_raider.history = {'player': ['.']}
    shroom_raider.found_item = None
    shroom_raider.drowned = False
    shroom_raider.player_mushroom_count = 0
    shroom_raider.player_index = grid_1.index('L')
    shroom_raider.moves = {
    'W': -(7 + 1),
    'S': 7 + 1,
    'A': -1,
    'D': 1,
    'P': 0,
}

    # Test case 22: player try to push rock to axe.
    move_player('waaaa')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', 'L', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 23: player try to push rock to flamethrower.
    move_player('wdddd')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', 'L', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 24: player try to push rock to tree.
    move_player('dwwdddd')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', 'L', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 25.1: player try to push rock to edge (from leftwards then upwards).
    move_player('wawwaaaaaasaww')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', 'L', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 25.2: player try to push rock to edge (from rightwards then downwards).
    move_player('sdssddddddwdss')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', 'L', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 26: player try to push rock to another rock (upwards, leftwards, downwards, rightwards).
    move_player('wwwwwwsaaaaadssssswdddddawwwww')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', 'L', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 27: player try to push rock past pavement.
    move_player('asssa')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', '.', '.', '.', 'R', '+', '\n', '.', 'L', '_', 'R', '.', '.', '.', '\n', 'R', '.', 'R', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 28: player try to push rock to water
    move_player('asssadwaad')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '_', 'L', '.', '.', '.', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', 'R', 'R', '.', '.', 'R']
    move_player('!')

    # Test case 29: player try to push rock to mushroom
    move_player('sdddd')
    assert shroom_raider.grid == ['R', '.', '.', 'R', '.', '.', 'R', '\n', '.', '.', '.', 'R', '.', 'R', 'T', '\n', 'x', 'R', '.', '.', '.', 'R', '*', '\n', 'R', 'R', '.', '.', '.', 'R', 'R', '\n', '~', 'R', 'R', '.', 'L', 'R', '+', '\n', '.', '.', '_', 'R', '.', '.', '.', '\n', 'R', '.', '.', 'R', '.', '.', 'R']
    move_player('!')

    # Map is TEST_MAP_2, set all the vars according to new map
    shroom_raider.GRID_HEIGHT, shroom_raider.GRID_WIDTH = 7, 7
    shroom_raider.MOTHERGRID = TEST_MAP_2
    shroom_raider.grid = grid_2

    # Lists the indices of '\n' characters
    shroom_raider._n_indices = range(TEST_MAP_2.index('\n'), len(TEST_MAP_2), 7 + 1)

    # Default player attributes
    shroom_raider.item = []
    shroom_raider.history = {'player': ['.']}
    shroom_raider.found_item = None
    shroom_raider.drowned = False
    shroom_raider.player_mushroom_count = 0
    shroom_raider.player_index = grid_2.index('L')
    shroom_raider.moves = {
    'W': -(7 + 1),
    'S': 7 + 1,
    'A': -1,
    'D': 1,
    'P': 0,
}

    # Test case 30: player picks up axe while holding flamethrower.
    move_player('spwappppd')
    assert shroom_raider.grid == ['.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', 'x', '.', '.', '.', '\n', '.', '.', 'x', 'L', '*', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '+']
    move_player('!')

    # Test case 31: player picks up flamethrower while holding axe.
    move_player('wpsdppppa')
    assert shroom_raider.grid == ['.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', 'x', 'L', '*', '.', '.', '\n', '.', '.', '.', '*', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '+']
    move_player('!')

    # Test case 32: player picks up axe while holding axe.
    move_player('wpaspd')
    assert shroom_raider.grid == ['.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', 'x', 'L', '*', '.', '.', '\n', '.', '.', '.', '*', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '+']
    move_player('!')

    # Test case 33: player picks up flamethrower while holding flamethrower.
    move_player('spdwpa')
    assert shroom_raider.grid == ['.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', 'x', '.', '.', '.', '\n', '.', '.', 'x', 'L', '*', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '.', '\n', '.', '.', '.', '.', '.', '.', '+']
    move_player('!')
