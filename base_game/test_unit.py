import shroom_raider

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


def test_pickup():
    test1, test2, test3 = 'x', '*', '.' 
    
    shroom_raider.item.clear()
    shroom_raider.pickup(test1)
    assert test1 in shroom_raider.item
    assert len(shroom_raider.item) == 1
    assert shroom_raider.pickup(test1) == '🪓'

    shroom_raider.item.clear()
    shroom_raider.pickup(test2)
    assert test2 in shroom_raider.item
    assert len(shroom_raider.item) == 1
    assert shroom_raider.pickup(test2) == '🔥'

    shroom_raider.item.clear()
    shroom_raider.pickup(test3)
    assert test3 in shroom_raider.item
    assert len(shroom_raider.item) == 1
    assert shroom_raider.pickup(test3) == '　'

def test_flame_spread():
    #jane: hindi q pa to natetest pero if may error prolly sa leading or trailing spaces. grid is same sa defined grid sa shroomraider.py
    assert ''.join(shroom_raider.flame_spread(0, 1)) == """\
....~~~~~.....
..L.~.xT~~~~~.
..R.~.~+~TTT~.
.~.~~T~.~T~T~.
.~~~~.~R~T~T~.
....~x~~~T~T~.
...T~.~.~T~T~.
.~+...~..*~+~.
.~~~~~~~~~~~~.
.............."""

    assert ''.join(shroom_raider.flame_spread(1, 7)) == """\
TTTT~~~~~TTTTT
T.L.~.x.~~~~~T
T.R.~.~+~TTT~T
T~.~~T~.~T~T~T
T~~~~.~R~T~T~T
T...~x~~~T~T~T
TT.T~.~.~T~T~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT"""
    assert ''.join(shroom_raider.flame_spread(5, 9)) == """\
TTTT~~~~~TTTTT
T.L.~.xT~~~~~T
T.R.~.~+~...~T
T~.~~T~.~.~.~T
T~~~~.~R~.~.~T
T...~x~~~.~.~T
TT.T~.~.~.~.~T
T~+...~..*~+~T
T~~~~~~~~~~~~T
TTTTTTTTTTTTTT"""
    assert ''.join(shroom_raider.flame_spread(5, 6)) == """\
TTTT~~~~~TTTTT
T.L.~.xT~~~~~T
T.R.~.~+~TTT~T
T~.~~T~.~T~T~T
T~~~~.~R~T~T~T
T...~x~~~T~T~T
TT.T~.~.~T~T~T
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