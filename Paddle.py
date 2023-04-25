from SpriteObject import SpriteObject
from Area import Area
from PPlay.sound import Sound

class Shot(SpriteObject):
    speed = 300
    to_destroy = False
    def __init__(self, area: Area, image_file='gfx/shot.png', frames=1):
        super().__init__(area, image_file, frames=frames)
    
    def move(self, d_time):
        self.move_y(self.speed * d_time * -1)
        self.__check_top__()

    def __check_top__(self):
        if(self.y < self.area.y):
            self.to_destroy = True
    
    def hit_block(self):
        self.to_destroy = True

def collide_all_shots(shot_list: list, block_dict: dict):
    for shot in shot_list:
        for key in block_dict:
            block = block_dict[key]
            if shot.collided(block):
                shot.hit_block()
                block.got_hit(deliver_item=False)

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

class Shooter(SpriteObject):
    def __init__(self, area: Area, image_file="gfx/shooter.png"):
        super().__init__(area, image_file)
    
    def shoot(self, shot_list: list):
        if len(shot_list) < 6:
            new = Shot(self.area)
            new.set_position(self.x, self.y)
            shot_list.append(new)

class Paddle(SpriteObject):
    speed = 150
    life = 3
    shoot_sound = Sound('sounds/shot.ogg')
    lose_sound = Sound('sounds/lose.ogg')
    glue_ball = False
    shooting_paddle = False
    paddle_sound = Sound('sounds/paddle.ogg')


    def __init__(self, area: Area, ball_reference=None, image_file="gfx/pad.png", frames=1):
        super().__init__(area, image_file, frames=frames)
        self.set_position(self.area.width / 2 - self.width / 2, self.area.maxY - 39)
        self.ball_reference = ball_reference
        self.shooters = (Shooter(self.area), Shooter(self.area))
        

    """move wraper. 1 = left, -1 = right"""
    def move(self, d_time, direction = 0):
        self.move_x(self.speed * d_time * direction)
        if self.ball_reference.stuck:
            self.ball_reference.move_x(self.speed * d_time * direction)
        self.shooters[0].set_position(self.x, self.y - self.shooters[0].height)
        self.shooters[1].set_position(self.x + self.width - self.shooters[1].width, self.y - self.shooters[1].height)
        
    
    """TODO, make mouse movement"""
    def move_mouse(self):
        pass

    def check_walls(self):
        if self.x + self.width > self.area.maxX:
            self.x = self.area.maxX - self.width
        if self.x < self.area.x:
            self.x = self.area.x

    def ball_hit(self, ball):
        if self.collided(ball):
            self.paddle_sound.play()
            ball.y = self.y - ball.height - 0.1
            # setting up areas of the pad
            left_corner = self.x    # and anything lesser than x
            left_gray_limit = left_corner + self.width / 10
            left_blue_limit = left_gray_limit + (self.width / 10) * 2

            white_limit = left_blue_limit + (self.width / 10) * 4
            right_blue_limit = white_limit + (self.width / 10) * 2
            right_gray_limit = right_blue_limit + self.width / 10

            # getting x center of the ball
            ball_middle = ball.x + ball.width / 2
            b_speedx, b_speedy = ball.__convert_angle2components__()
            b_speedy *= -1
            if ball_middle < left_corner or ball_middle < left_gray_limit:       # hit left gray area
                b_speedx = -ball.speed
            if ball_middle > right_gray_limit or ball_middle > right_blue_limit: # hit right gray area
                b_speedx = ball.speed
            ball.speed = ball.__convert_components2speed__(b_speedx, b_speedy) if ball.__convert_components2speed__(b_speedx, b_speedy) < 500 else 500
            
            if left_gray_limit < ball_middle < left_blue_limit:   # hit left blue area
                b_speedx += b_speedy / 2
            if white_limit < ball_middle < right_blue_limit:      # hit right blue area
                b_speedx += -b_speedy / 2

            ball.angle = ball.__convert_components2angle__(b_speedx, b_speedy)

            if self.glue_ball:
                ball.stuck = True

    def collect_item(self, item):
        if(self.collided(item)):
            item.to_destroy = True
            item.do_effect()
    
    def reset(self):
        self.set_position( self.area.x + self.area.maxX // 2 - self.width // 2, self.y)

        self.glue_ball = False
        self.shooting_paddle = False
    
    def shoot(self, shot_list: list):
        self.shoot_sound.play()
        for shooter in self.shooters:
            shooter.shoot(shot_list)
    
    def lose_life(self):
        self.reset()
        self.lose_sound.play()
        self.ball_reference.reset()
        self.life -= 1

    
    def draw(self):
        super().draw()
        if self.shooting_paddle:
            for s in self.shooters:
                s.draw()



def collect_all_items(item_list: list, paddle: Paddle):
    for item in item_list:
        paddle.collect_item(item)
