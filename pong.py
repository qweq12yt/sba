from PPlay.gameimage import GameImage
from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import Keyboard
from math import cos, sin, radians, atan, ceil, pi
from random import randint
from time import time


class Boost(Sprite):
    def pick_position(self):
        y_range = 600 // self.height
        x_range = 800 // self.width
        x, y = randint(1, x_range - 1), randint(1, y_range - 1)
        self.set_position(x * self.width, y * self.height)


class Ball(Sprite):
    # both of those are in frames
    wait_time = 200  # for whenever the ball spawns
    disable_collision = 100   # for stopping funny collision behavior

    speed = 200
    # vector angle implementation because i will need for my game project
    # yes i know it's bad
    angle = radians(randint(0, 3) * 90 + 45) # pick random angle to start the ball

    boost = False

    """Reset ball"""
    def reset(self):
        self.set_position(w.width / 2 - self.width / 2, w.height / 2 - self.height - 2)
        self.wait_time = 300
        self.disable_collision = 100
        self.speed = 200 if self.speed / 3 < 200 else self.speed / 3
        self.boost = False
    
    """Move wraper"""
    def move(self, d_time):
        if self.wait_time > 0:
            self.wait_time -= 1
            return
        
        if self.disable_collision > 0:
            self.disable_collision -= 1

        speedx, speedy = self.__convert_angle2components__()
        boost = 1
        
        if(self.boost):
            boost = 2
        self.move_x(speedx * d_time * boost)
        self.move_y(speedy * d_time * boost)
    
    """Check collision with top and bottom"""
    def check_wall(self, y):
        speedx, speedy = self.__convert_angle2components__()
        if self.y > y - self.height - 7 or self.y < 7:
            self.y = self.y + 1 if self.y < 7 else self.y - 1
            speedy *= -1
            self.y += ceil(speedy) / abs(ceil(speedy))
            self.speed += 25

        self.angle = self.__convert_components2angle__(speedx, speedy)
    
    """Check if ball went past a paddle"""
    def check_score(self, x):
        if ceil(self.x) > x or ceil(self.x) < -self.width:
            if self.x < 0:
                return -1
            if self.x > x:
                return 1
        return 0          
    
    def check_boost(self, boost: Boost):
        if self.collided(boost):
            self.boost = True
            boost.pick_position()

    """Private Trigonometry functions"""        
    def __convert_angle2components__(self):
        speedx = cos(self.angle) * self.speed
        speedy = sin(self.angle) * self.speed
        return speedx, speedy
    def __convert_components2angle__(self, x, y):
        if x > 0:
            return atan(y / x)
        return atan(y / x) + pi


class Pad(Sprite):
    speed = 100

    """Move wraper. direction 1 = Down, -1 = up, 0 = stay"""
    def move(self, d_time, direction=0):
        self.move_y(self.speed * d_time * direction)
    
    """Check if collides with top or bottom"""
    def check_wall(self, y):
        if ceil(self.y) > y - self.height - 9:
            return 1
        if ceil(self.y) < 9:
            return -1
        return 0

    """Check collision with ball"""
    def ball_hit(self, ball: Ball):
        if self.collided(ball) and ball.disable_collision <= 0:
            b_speedx, b_speedy = ball.__convert_angle2components__()
            b_speedx *= -1

            ball_middle = ball.y + ball.height / 2
            a_third = self.height / 3
            if self.y < ball_middle < self.y + a_third:
                    b_speedy -= abs(ball.speed) / 1.5
            if self.y + a_third * 2 < ball_middle < self.y + self.height:
                    b_speedy += abs(ball.speed) / 1.5


            ball.angle = ball.__convert_components2angle__(b_speedx, b_speedy)
            ball.disable_collision = 100
            ball.boost = False


class CPUPad(Pad):

    state_timer = 300
    state = 1

    def __pick_state__(self):
        n = randint(1, 20)
        if 11 <= n <= 20:
            return 2    # inspired
        if 2 <= n <= 10:
            return 1    # tired
        if n == 20:
            return 4    # master
        if n == 1:
            return 0.5  # brain dead
    
    def __lookup_ball_direction__(self, ball: Ball):
        pad_middle = self.y + self.height / 2
        ball_middle = ball.y + ball.height / 2
        if ball_middle > pad_middle:
            return 1
        if ball_middle < pad_middle:
            return -1
        return 0

    def inteligence(self, d_time, ball: Ball):
        if self.state_timer > 0:
            direction = self.__lookup_ball_direction__(ball)
            self.move(d_time, self.state * direction)
            if self.y < 7:
                self.y = 7
            if self.y + self.height > 600 - 7:
                self.y = 600 - 7 - self.height
            
            self.state_timer -= 1
        
        else:
            self.state = self.__pick_state__()
            self.state_timer = randint(self.state * 10, self.state * 20) * 10   


class FPSCounter():
    c_frames = 0
    t = None
    fps = 0
    def __init__(self) -> None:
        self.t = time()
    
    def update(self):
        self.c_frames += 1
        self.s = time() - self.t
        if self.s > 1:
            self.fps = self.c_frames
            self.c_frames = 0
            self.t = time()
    
    def __str__(self) -> str:
        return str(self.fps)


# init
w = Window(800, 600)
ball = Ball("gfx/ball.png")
player = Pad("gfx/paddle.png")
cpu = CPUPad("gfx/paddle2.png")
player2 = Pad("gfx/paddle2.png")
bg = GameImage("gfx/background.png")
boost = Boost('gfx/speed.png')
left_score = 0
right_score = 0
fps = FPSCounter()

p2 = False   # 2 player mode, else, 1 player mode (vs cpu)

kb = Keyboard()

# post init
ball.set_position(w.width / 2 - ball.width / 2, w.height / 2 - ball.height - 2)
boost.pick_position()
player.set_position(0, -player.height / 2 + w.height / 2)
cpu.set_position(w.width - cpu.width, -cpu.height / 2 + w.height / 2)
player2.set_position(w.width - player2.width, -player2.height / 2 + w.height / 2)

while True:
    score_check = ball.check_score(w.width)

    # collision area
    ball.check_wall(w.height)
    ball.check_boost(boost)

    # ball collision
    player.ball_hit(ball)
    player2.ball_hit(ball) if p2 else cpu.ball_hit(ball)


    # score area
    if score_check > 0: # left scored
        left_score += 1
        ball.reset()
    if score_check < 0: # right scored
        right_score += 1
        ball.reset()

    # movement area
    ball.move(w.delta_time())
    

    # controll area
        # p1
    speed_multi = 5 if kb.key_pressed('left_shift') else 1
    if(kb.key_pressed('w') and player.check_wall(w.height) != -1):
        player.move(w.delta_time(), -1 * speed_multi)
    if(kb.key_pressed('s') and player.check_wall(w.height) != 1):
        player.move(w.delta_time(), 1 * speed_multi)

    if(p2): # p2
        speed_multi = 5 if kb.key_pressed('enter') else 1
        if(kb.key_pressed('i') and player2.check_wall(w.height) != -1):
            player2.move(w.delta_time(), -1 * speed_multi)
        if(kb.key_pressed('k') and player2.check_wall(w.height) != 1):
            player2.move(w.delta_time(), 1 * speed_multi)
    
    else:   # cpu
        if left_score - right_score > 2:
            cpu.state = 2
            cpu.state_timer = 100
        else:
            cpu.inteligence(w.delta_time(), ball)
        

    # drawing area
    bg.draw()
    ball.draw()
    player.draw()
    player2.draw() if p2 else cpu.draw()
    boost.draw()
    w.draw_text(str(left_score), w.width / 2 - 20, 10, 20, (255, 255, 255))
    w.draw_text(str(right_score), w.width / 2 + 20, 10, 20, (255, 255, 255))
    fps.update()
    w.draw_text(str(fps), 0, 0, 20, (255, 255, 255))


    # final update
    w.update()
