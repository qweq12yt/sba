from pygame.image import load
from SpriteObject import SpriteObject
from Area import Area

class Player(SpriteObject):
    speed = 100
    lifes = 1
    i_frames = 0
    shots_fired = 0
    recharge = 0
    on_charge = False

    def __init__(self, area: Area, image_file='gfx/invaders_player.png', frames=1):
        super().__init__(area, image_file, frames=frames)
    
    def __check_walls__(self):
        if self.x + self.width > self.area.maxX:
            self.x = self.area.maxX - self.width
        if self.x < self.area.x:
            self.x = self.area.x
    
    def move(self, d_time, direction = 0):
        self.move_x(self.speed * d_time * direction)
        self.__check_walls__()
        self.i_frames -= d_time
        if self.on_charge:
            self.recharge -= d_time
        if self.recharge < 0:
            self.on_charge = False
            self.shots_fired = 0
            self.image = load("gfx/invaders_player.png").convert_alpha()
    
    def shoot(self, shot_list: list):
        if self.shots_fired <= 10:
            to_add = Shot(self.area)
            to_add.set_position(self.x + self.width // 2 - to_add.width // 2, self.y)
            shot_list.append(to_add)
            self.shots_fired += 1
        if self.shots_fired >= 10:
            self.on_charge = True
            self.recharge = 2
            self.image = load("gfx/invaders_player_recharge.png").convert_alpha()
    
    def apply_i_frames(self):
        self.i_frames = 2

    def check_alien_shots(self, alien_shot_list: list):
        if self.i_frames < 0:
            for shot in alien_shot_list:
                if self.collided(shot):
                    self.lifes -= 1
                    shot.to_destroy = True
                    self.apply_i_frames()
                    self.set_position(self.area.maxX // 2 - self.width // 2, self.y)
                    return self.lifes
        return False

    def reset(self):
        self.lifes = 3
        self.set_position(self.area.maxX // 2 - self.width // 2, self.y)
        self.i_frames = 0
        self.on_charge = False
        self.shots_fired = 0
    
    def draw(self):
        if (self.i_frames < 0):
            return super().draw()
        else:
            if((self.i_frames % 0.20) > 0.1):
                return super().draw()

    
class Shot(SpriteObject):
    speed = 350
    to_destroy = False
    def __init__(self, area: Area, image_file='gfx/shot.png', frames=1):
        super().__init__(area, image_file, frames=frames)
    
    def move(self, d_time):
        self.move_y(self.speed * d_time * -1)
        self.__check_top__()

    def __check_top__(self):
        if(self.y < self.area.y - self.y):
            self.to_destroy = True
    
    def hit_alien(self):
        self.to_destroy = True

def draw_all_shots(shot_list: list):
    for shot in shot_list:
        shot.draw()

def update_all_shots(shot_list: list, d_time):
    to_destroy = []
    for shot in shot_list:
        shot.move(d_time)

        if(shot.to_destroy):
            to_destroy.append(shot)
    
    for i in to_destroy:
        shot_list.remove(i)
