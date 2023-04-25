from Points import PointSystem
from PPlay.gameimage import GameImage
from Item import remove_items
from PPlay.sound import Sound
from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from Block import Block, draw_all_blocks, remove_dead
from Area import Area
from Bricks import PlainBrick, SturdyBrick
from Paddle import Paddle, collect_all_items, collide_all_shots, draw_all_shots, update_all_shots
from Ball import Ball
from MagicNumbers import *
from Button import *
from Text import Text

debug = False

def save_level(block_dict: dict, name='noname'):
    s = ''
    for key in block_dict:
        block: Block = block_dict[key]
        b = '{} {} {} {}\n'.format(block.pos[0], block.pos[1], block.t, block.s)
        s += b
    
    save = open(name, 'w')
    save.write(s)

def load_level(level, area: Area, types):
    d = dict()
    file_path = 'levels/{}'.format(level)
    file = open(file_path, 'r')
    for line in file:
        line = line.split()
        x, y = int(line[0]), int(line[1])
        t = line[2]
        s = int(line[3])

        d[(x, y)] = types[t](area, x, y, s)
    
    return d

def draw_all_items(item_list: list):
    for item in item_list:
        item.draw()

def update_all_items(item_list: list, d_time):
    for item in item_list:
        item.move(d_time)

# defines
GAME = 1
BUILD = -456687

menu_area = Area(width=960, height=570)

w = Window(960, 570)
dbbg = Sprite("db/dbbg.png")
fundo = Sprite("gfx/fundo.png")
playArea = Area(24, 24, 700, 520)
scoreArea = Area(768, 24, 700, 520)
score = PointSystem()

fundo_menu = 1

types = {'plain': PlainBrick, 'sturdy': SturdyBrick}
level = 1
block_dict = load_level(level, playArea, types)

item_list = []
shot_list = []

pad = Paddle(playArea)
ball = Ball(playArea, pad, item_list)
pad.ball_reference = ball
kb = Keyboard()
mouse = Mouse()

ball.set_position(pad.x, pad.y)

s = 0
t = 'plain'

button_list = []

add_menu_buttons(button_list, menu_area)

state = MENU
shot = False
menu_music = Sound('sounds/title.ogg')
title_screen = GameImage('gfx/title_screen.png')

score_text = Text(scoreArea, w, score, size=32)
life_text = Text(scoreArea, w, None, size=32)
score_text.x += 20
score_text.y += 10
life_text.x += 20
life_text.y += 100


while True:
    d_time = w.delta_time()
    if state == MENU:
        if not menu_music.is_playing():
            menu_music.play()

        if kb.key_pressed('enter'):
            state = GAME
            pad.reset()
            ball.reset()
            pad.life = 3
            menu_music.stop()
        
        if kb.key_pressed('esc'):
            exit(0)
        
        title_screen.draw()

    if(state == GAME):
        # stage progression logic
        if len(block_dict.values()) == 0:
            level += 1
            level = (level % 8)
            block_dict = load_level(level, playArea, types)
            shot_list.clear()
            pad.reset()
            ball.reset()

        # game over
        if pad.life <= 0:
            state = MENU

        # capture controls
        pad_move = -1 if kb.key_pressed('a') else 0 + \
                    1 if kb.key_pressed('d') else 0
        speed_mult = 1 * 5 if kb.key_pressed('left_shift')   else 1 * \
                     10    if kb.key_pressed('left_control') else 1
        
        prev_shot = shot
        shot = kb.key_pressed('space')
        release = kb.key_pressed('space')
        
        # move logic
        ball.move(d_time)
        pad.move(d_time, pad_move * speed_mult)
        if release and ball.stuck: ball.release()
        update_all_shots(shot_list, d_time)
        collide_all_shots(shot_list, block_dict)
        if shot and not prev_shot and pad.shooting_paddle:
            pad.shoot(shot_list)

        # collision logic
        ball.check_walls()
        pad.check_walls()
        pad.ball_hit(ball)
        collect_all_items(item_list, pad)
        ball.check_fall()
        remove_dead(block_dict)
        ball.collide_all_bricks(block_dict, score)

        update_all_items(item_list, d_time)
        remove_items(item_list)

        # debug
        if debug:
            if kb.key_pressed('q'):
                ball.angle -= 0.01
            if kb.key_pressed('e'):
                ball.angle += 0.01

        # pre draw
        life_text.string = f'Lives = {pad.life}'

        # draws
        fundo.draw()
        draw_all_shots(shot_list)
        score_text.draw()
        life_text.draw()
        ball.draw()
        pad.draw()
        draw_all_blocks(block_dict)
        draw_all_items(item_list)

    if(state == BUILD):
        mx, my = mouse.get_position()
        gx, gy = (mx - 25) // 50, (my - 25) // 20
        
        if(mouse.is_button_pressed(1)):
            if (gx, gy) not in block_dict and 0 <= gx <= 13 and 0 <= gy <= 19:
                block_dict[(gx, gy)] = types[t](playArea, gx, gy, s)
        if(mouse.is_button_pressed(3)):
            if (gx, gy) in block_dict:
                block_dict.pop((gx, gy))
        
        if(kb.key_pressed('space')):
            save_level(block_dict)
        
        if(kb.key_pressed('a')): t = 'plain'
        if(kb.key_pressed('s')): t = 'sturdy'

        for n in range(0, 10):
            if(kb.key_pressed(str(n))):
                s = n
                break
        
        dbbg.draw()
        draw_all_blocks(block_dict)

        pass
    # final update
    w.update()
