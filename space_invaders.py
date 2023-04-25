from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.window import Window
from Area import Area
from Button import add_difficulty_buttons, add_menu_buttons, mouse_update_all_buttons, draw_all_buttons
from MagicNumbers import *
from Player import *
from Alien import build_army, draw_all_aliens, move_alien_shots, remove_alien_shots, update_army, army_reached_bottom
from Points import PointSystem, load_file_to_list, save_list_to_file, sort_ranking

# general init
state = MENU
w = Window(651,744)
m = Mouse()
kb = Keyboard()

# other vars
difficulty = SET_NORMAL

# game areas
life_area = Area(0, 696, 651, 48)
score_area = Area(0, 0, 651, 75)
play_area = Area(0, 75, 651, 621)

# menu areas
menu_area = Area(0, 0, 651, 744)

# menu init
s_menu = MENU
button_list = []
add_menu_buttons(button_list, menu_area)

# game objects
player = Player(play_area)
player_shot_list = []
enemy_list = []
enemy_shot_list = []
ui_cover = GameImage('gfx/ui_cover.png')

# game sets
player.set_position(play_area.maxX // 2 - player.width // 2, play_area.maxY - player.height)

# controller control var
shoot_prev = False
shoot_now = False

# stage vars
no_aliens = True
sleep = 3

# point system
p = PointSystem()
file = None
ranking = load_file_to_list()

# global timer
timer = 0

while state > 0:
    d_time = w.delta_time()
    timer += d_time
    sleep -= d_time
    if state == MENU:
        # mouse updates
        action = mouse_update_all_buttons(button_list, m)

        if(kb.key_pressed('esc')):
            action = MENU
        
        # draw
        draw_all_buttons(button_list)

        # early final update for convenience
        w.update()

        # parse action buttons
        if action:
            if action == PLAYING:
                state = PLAYING
                player.reset()
                enemy_list = []
                no_aliens = True
                enemy_shot_list = []
                player_shot_list = []
                p = PointSystem()

            if action == MENU_EXIT:
                w.close()
                exit(0) # just in case

            if action == MENU:
                s_menu = MENU
            
            if action == MENU_DIFFICULTY:
                s_menu = MENU_DIFFICULTY
            if action == SET_EASY:
                difficulty = SET_EASY
                s_menu = MENU
            if action == SET_NORMAL:
                difficulty = SET_NORMAL
                s_menu = MENU
            if action == SET_HARD:
                difficulty = SET_HARD
                s_menu = MENU
            
            if action == MENU_RANK:
                s_menu = MENU_RANK
                ranking = load_file_to_list()

        # menu setups
        if action:
            button_list.clear()
            w.set_background_color((0,0,0))
            if s_menu == MENU:
                add_menu_buttons(button_list, menu_area)
            if s_menu == MENU_DIFFICULTY:
                add_difficulty_buttons(button_list, menu_area)
            if s_menu == MENU_RANK:
                text = []
                ranking.sort(reverse=True, key=lambda x: x[1])
                for entry in ranking:
                    text.append('{} - {}'.format(entry[0], entry[1]))
                space = 0
                for line in text:
                    w.draw_text(line, w.width // 3, space + (w.height // 3), 32, (255,255,255))
                    space += 32
    
    if state == PLAYING:
        if(no_aliens):
            build_army(enemy_list, play_area, difficulty)
            no_aliens = False
        if(len(enemy_list) == 0):
            no_aliens = True
            difficulty += 0.333
            difficulty = round(difficulty) if difficulty < SET_HARD + 1 else SET_HARD + 1

        if(kb.key_pressed('esc')):
            state = MENU

        # controls
        movement = 0
        if(kb.key_pressed('a')):
            movement += -1
        if(kb.key_pressed('d')):
            movement += 1
        
        # didn't want to use cooldown, too lazy and simple
        shoot_prev = shoot_now
        if(kb.key_pressed('space')):
            shoot_now = True
        else:
            shoot_now = False
        shoot_down = shoot_now and not shoot_prev if shoot_now else False   # like this, the player can't hold the key, but must press multiple times for multiple shots
        
        if(shoot_down):
            # difficulty sets how many shots at once can exist on the screen. Easy = 2, normal and hard = 1
            # later difficulty will also affect the enemies
            max_shots =  SET_NORMAL - difficulty + 1 if difficulty <= SET_NORMAL else 1
            if len(player_shot_list) < max_shots:
                player.shoot(player_shot_list)

        # movement
        player.move(d_time, movement)
        
        # logic updates
        update_all_shots(player_shot_list, d_time)
        if(update_army(enemy_list, d_time, player_shot_list, p, difficulty, enemy_shot_list, timer, sleep)):
            sleep = (3 * (len(enemy_list) / 55)) + 0.3
        move_alien_shots(enemy_shot_list, d_time)
        player.check_alien_shots(enemy_shot_list)

        remove_alien_shots(enemy_shot_list)

        # draws
        w.set_background_color((0,0,0))
        draw_all_shots(player_shot_list)
        draw_all_shots(enemy_shot_list)
        draw_all_aliens(enemy_list)
        player.draw()
        ui_cover.draw()
        w.draw_text(str(int(p.points)), score_area.x, (score_area.y + score_area.height) // 2 - 24 / 2, 24, (255, 255, 255), "Consolas")

        # final update
        w.update()

        if(army_reached_bottom(enemy_list, player)):
            player.lifes = 0

        if(player.lifes == 0):
            state = MENU
            w.set_background_color((0,0,0))
            name = input('Type your name: ')
            ranking.append([name if name != '' else '???' , int(p.points)])
            sort_ranking(ranking)
            save_list_to_file(ranking)
        


