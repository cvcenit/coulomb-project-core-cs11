from shroom_raider import char_to_emoji, flame_spread, pickup, describe_tile, item

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
TTTTTTTTT
'''

    test2 = '''\
...+...
...~..
...R.T.
..LTT.
.x...*.
T...Tqq
TTTTT**TT
'''

    test3 = '''\
TTTTTTTTT.....................
T...+.RRRRRRRRRR+++++++____..T
T..~.~>~.~>~/~~,,~xxxxxx.~...T
T._____.****LLLL.______,xXXTTT
'''

    assert char_to_emoji(test1) == '''\
🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲　　　🍄　　　🌲
🌲　　　🟦　　　🌲
🌲　　　🪨　🌲　🌲
🌲　🌲　🧑🌲🌲　🌲
🌲　🪓　　　🔥　🌲
🌲　　　　　　　🌲
🌲　　　　　　　🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲'''

    assert char_to_emoji(test2) == '''\
　　　🍄　　　
　　　🟦　　
　　　🪨　🌲　
　　🧑🌲🌲　
　🪓　　　🔥　
🌲　　　🌲
🌲🌲🌲🌲🌲🔥🔥🌲🌲'''
    
    assert char_to_emoji(test3) == """\
🌲🌲🌲🌲🌲🌲🌲🌲🌲　　　　　　　　　　　　　　　　　　　　　
🌲　　　🍄　🪨🪨🪨🪨🪨🪨🪨🪨🪨🪨🍄🍄🍄🍄🍄🍄🍄⬜⬜⬜⬜　　🌲
🌲　　🟦　🟦🟦　🟦🟦🟦🟦🟦🪓🪓🪓🪓🪓🪓　🟦　　　🌲
🌲　⬜⬜⬜⬜⬜　🔥🔥🔥🔥🧑🧑🧑🧑　⬜⬜⬜⬜⬜⬜🪓🌲🌲🌲"""


def test_pickup():
    test1, test2, test3 = 'x', '*', '.' 
    
    item.clear()
    pickup(test1)
    assert test1 in item
    assert len(item) == 1
    assert pickup(test1) == '🪓'

    item.clear()
    pickup(test2)
    assert test2 in item
    assert len(item) == 1
    assert pickup(test2) == '🔥'

    item.clear()
    pickup(test3)
    assert test3 in item
    assert len(item) == 1
    assert pickup(test3) == '　'

def test_flame_spread():
    #jane: hindi q pa to natetest pero if may error prolly sa leading or trailing spaces. grid is same sa defined grid sa shroomraider.py
    assert ''.join(flame_spread(0, 1)) == """\
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
    assert ''.join(flame_spread(1, 7)) == """\
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
    assert ''.join(flame_spread(5, 9)) == """\
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
    assert ''.join(flame_spread(5, 6)) == """\
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
    assert describe_tile('.') == 'empty'
    assert describe_tile('T') == 'tree'
    assert describe_tile('+') == 'mushroom'
    assert describe_tile('R') == 'rock'
    assert describe_tile('L') == 'player'
    assert describe_tile('`') == 'water'
    assert describe_tile('_') == 'paved'
    assert describe_tile('x') == 'axe'
    assert describe_tile('*') == 'flamethrower'
