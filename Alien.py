from Points import PointSystem
from SpriteObject import SpriteObject
from Area import Area
from Player import Shot
from MagicNumbers import *
from random import randint

class Alien(SpriteObject):
    max_step_timer = 2
    step_timer = max_step_timer
    step_distance = STEP_DISTANCE
    direction = 1
    dead = False
    multiplier = 1
    points = 0
    max_shot_timer = 5
    shot_timer = 0

    def __init__(self, area: Area, image_file="gfx/alien.png", frames=1):
        super().__init__(area, image_file, frames=frames)
        # modifier = 
    
    def move(self, d_time, dif, army):
        self.step_timer -= d_time + dif + army
        self.shot_timer -= d_time + army
        if(self.step_timer < 0):
            self.move_x(self.step_distance * self.direction)
            self.step_timer = self.max_step_timer
        
    
    def shoot(self, enemy_shot_list: list):
        new_shot = AlienShot(self.area)
        new_shot.set_position(self.x + self.width // 2, self.y + self.height // 1.5)
        enemy_shot_list.append(new_shot)
        self.shot_timer = self.max_shot_timer


    def hit_by_bullet(self, point_system: PointSystem):
        self.dead = True
        point_system.hit_alien(self)
    
    def check_side_limit(self):
        if self.x + self.width > self.area.maxX:
            return 1
        if self.x < self.area.x:
            return -1
        return 0

def remove_dead(alien_list: list):
    to_remove = []
    for alien in alien_list:
        if alien.dead:
            to_remove.append(alien)
    for alien in to_remove:
        alien_list.remove(alien)

def __build_row__(alien_type, alien_list: list, area: Area, row_n: int, speed_multi, mod):
    l = []
    for n in range(ALIEN_PER_ROW + mod):
        new_alien = alien_type(area)
        new_alien.multiplier = speed_multi
        new_alien.set_position(n * ALIEN_SEPARATION_HORIZONTAL + n * new_alien.width, row_n * ALIEN_SEPARATION_VERTICAL + row_n * new_alien.height + area.y)
        l.append(new_alien)
    
    lenght = (area.maxY // 2) - (((ALIEN_PER_ROW + mod) * new_alien.width + ALIEN_PER_ROW * ALIEN_SEPARATION_HORIZONTAL - 1) // 2)
    for alien in l:
        alien.move_x(lenght)
    
    alien_list.extend(l)

def build_army(alien_list: list, area: Area, difficulty):
    rows = 0
    mod = (int(difficulty) - SET_NORMAL)
    for n in range(ALIEN3_ROWS + mod):
        __build_row__(Alien3, alien_list, area, rows, 1, mod * 2 if mod < 0 else mod)
        rows += 1
    for n in range(ALIEN2_ROWS + mod):
        __build_row__(Alien2, alien_list, area, rows, 1, mod * 2 if mod < 0 else mod)
        rows += 1
    for n in range(ALIEN1_ROWS + mod):
        __build_row__(Alien1, alien_list, area, rows, 1, mod * 2 if mod < 0 else mod)
        rows += 1
    
def __check_army_limit__(alien_list: list):
    for alien in alien_list:
        limit = alien.check_side_limit()
        if limit != 0:
            return limit
    return 0

def set_alien_direction(alien_list: list):
    new_direction = __check_army_limit__(alien_list)
    if new_direction != 0:
        for alien in alien_list:
            alien.direction = -new_direction
            alien.x -= alien.step_distance * new_direction

def lower_army(alien_list: list):
    if(__check_army_limit__(alien_list)):
        lower_by = alien_list[0].height
        for alien in alien_list:
            alien.move_y(lower_by)

def move_army(alien_list: list, d_time, difficulty):
    dif_mod = (difficulty - SET_EASY) / 100
    army_mod = 0 if len(alien_list) > 5 else (-len(alien_list) + 5) / 10
    for alien in alien_list:
        alien.move(d_time, dif_mod, army_mod)

def collide_all_aliens(alien_list: list, shoot_list: list, point_system: PointSystem):
    for shoot in shoot_list:
        for alien in alien_list:
            if(shoot.collided(alien)):
                alien.hit_by_bullet(point_system)
                shoot.hit_alien()
                return

def shoot_army(alien_list: list, shot_list: list, timer, difficulty, sleep):
    if sleep > 0:
        return
    if(round(timer, 1) % 1 - ((-difficulty + SET_NORMAL) / 5) == 0):
        i = randint(0, len(alien_list) - 1)
        alien_list[i].shoot(shot_list)
        return True

def army_reached_bottom(alien_list: list, player):
    for alien in alien_list:
        if alien.y + alien.height > player.y:
            return True

def update_army(alien_list: list, d_time, shoot_list, point_system, difficulty, enemy_shoot_list, timer, sleep):
    if(len(alien_list) > 0):
        lower_army(alien_list)
        set_alien_direction(alien_list)
        move_army(alien_list, d_time, difficulty)
        collide_all_aliens(alien_list, shoot_list, point_system)
        remove_dead(alien_list)
        return shoot_army(alien_list, enemy_shoot_list, timer, difficulty, sleep)

def draw_all_aliens(alien_list: list):
    for alien in alien_list:
        alien.draw()

class Alien1(Alien):
    def __init__(self, area: Area, image_file="gfx/alien1.png", frames=1):
        super().__init__(area, image_file=image_file, frames=frames)
        self.points = ALIEN1_POINTS

class Alien2(Alien):
    def __init__(self, area: Area, image_file="gfx/alien2.png", frames=1):
        super().__init__(area, image_file=image_file, frames=frames)
        self.points = ALIEN2_POINTS

class Alien3(Alien):
    def __init__(self, area: Area, image_file="gfx/alien3.png", frames=1):
        super().__init__(area, image_file=image_file, frames=frames)
        self.points = ALIEN3_POINTS

class AlienShot(Shot):
    def move(self, d_time):
        self.move_y(self.speed * d_time)

    def __check_bot__(self):
        if(self.y > self.area.maxY):
            self.to_destroy = True
    
def remove_alien_shots(shot_list: list):
    l = []
    for s in shot_list:
        if s.to_destroy:
            l.append(s)
    for i in l:
        shot_list.remove(i)

def move_alien_shots(shot_list: list, d_time):
    for s in shot_list:
        s.move(d_time)