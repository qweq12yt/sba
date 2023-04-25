from pygame.constants import BUTTON_LEFT
from SpriteObject import SpriteObject
from Area import Area
from PPlay.mouse import Mouse
from MagicNumbers import *


def mouse_update_all_buttons(button_list: list, m: Mouse):
    for b in button_list:
        r = b.mouse_update(m)
        if r:
            return r

def add_buttons(button_list: list, area: Area, buttons: list):
    n = len(buttons)
    n_division = area.height // n
    division_middle = n_division // 2
    x_middle = area.width // 2

    for i in range(n):
        button = buttons[i]
        button.set_position(x_middle - button.width / 2, n_division * i + division_middle - button.height / 2)
        button_list.append(button)

def add_menu_buttons(button_list: list, area: Area):
    start = ActionButton(area, 'gfx/play_button.png', lambda: PLAYING)
    difficulty = ActionButton(area, 'gfx/difficulty_button.png', lambda: MENU_DIFFICULTY)
    ranking = ActionButton(area, 'gfx/rank_button.png', lambda: MENU_RANK)
    leave = ActionButton(area, 'gfx/exit_button.png', lambda: MENU_EXIT)  # exit() is already a thing

    l = [start, difficulty, ranking, leave]
    add_buttons(button_list, area, l)

def add_difficulty_buttons(button_list: list, area: Area):
    easy = ActionButton(area, 'gfx/button.png', lambda: SET_EASY)
    normal = ActionButton(area, 'gfx/button.png', lambda: SET_NORMAL)
    hard = ActionButton(area, 'gfx/button.png', lambda: SET_HARD)

    l = [easy, normal, hard]
    add_buttons(button_list, area, l)

def draw_all_buttons(button_list: list):
    for b in button_list:
        b.draw()

class Button(SpriteObject):

    mouse_state = 0 # 0 = no mouse, 1 = mouse over, 2 = mouse clicking
    
    freeze_timer = 1000 # prevents weird menu changing shenanigans

    def __init__(self, area: Area, image_file, frames=3):
        super().__init__(area, image_file, frames=frames)
    
    """Do something on mouse click"""
    def __on_mouse_click__(self):
        self.mouse_state = 2

    def __on_mouse_enter__(self):
        self.mouse_state = 1

    def __on_mouse_leave__(self):
        self.mouse_state = 0
    
    def mouse_update(self, m: Mouse):
        self.freeze_timer -= 1
        if m.is_over_object(self):
            self.__on_mouse_enter__()
            if m.is_button_pressed(BUTTON_LEFT) and self.freeze_timer < 0:
                return self.__on_mouse_click__()
        else:
            self.__on_mouse_leave__()
    
    """need to overwrite for mouse over and mouse leave stuff"""
    def draw(self):
        self.set_curr_frame(self.mouse_state)
        return super().draw()

class ActionButton(Button):
    action = None
    def __init__(self, area: Area, image_file, action):
        super().__init__(area, image_file=image_file, frames=3)
        self.action = action
    
    def __on_mouse_click__(self):
        super().__on_mouse_click__()
        if self.action:
            return self.action()
        