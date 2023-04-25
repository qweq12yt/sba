from Item import ThroughBall
from SpriteObject import SpriteObject
from math import radians, atan2, cos, sin
from Block import Block
from Area import Area
from PPlay.sound import Sound

class Ball(SpriteObject):
    speed = 100
    angle = radians(60)
    collide_timer = 0
    stuck = False
    wall_sound = Sound('sounds/wall.ogg')

    # item effects
    through_ball = False

    def __init__(self, area: Area, pad_reference, item_list: list, image_file="gfx/ball.png", frames=1):
        super().__init__(area, image_file, frames=frames)
        self.pad_reference = pad_reference
        self.item_list = item_list
    
    """Move wraper"""
    def move(self, d_time):
        if self.stuck:
            self.set_position(self.x, self.pad_reference.y - self.height)
        else:
            speedx, speedy = self.__convert_angle2components__()
            self.move_x(speedx * d_time)
            self.move_y(speedy * d_time)
    
    """Tri-wall Collision"""
    def check_walls(self):
        speedx, speedy = self.__convert_angle2components__()
        if self.x + self.width > self.area.maxX or self.x < self.area.x:
            speedx *= -1
            self.x = self.area.x if self.x < self.area.x else self.area.maxX - self.width
            self.wall_sound.play()
        if self.y < self.area.y:
            speedy *= -1
            self.y = self.area.y
            self.speed += 0.03
            self.wall_sound.play()
        self.angle = self.__convert_components2angle__(speedx, speedy)
    
    # need different approach
    # jesus this is disgusting! but it sort of works
    def __collide_brick__(self, brick: Block):
        if self.collided(brick) and self.collide_timer < 0:
                self.collide_timer = 0
                speedx, speedy = self.__convert_angle2components__()

                brick_middle_x, brick_middle_y = brick.x + brick.width / 2, brick.y + brick.height / 2
                ball_middle_x, ball_middle_y = self.x + self.width / 2, self.y + self.height / 2
                
                h = brick_middle_y - ball_middle_y
                l = brick_middle_x - ball_middle_x
                
                ball_angle = atan2(h, l)
                short_angle = atan2(brick.height, brick.width)  # both of those are halves
                long_angle = atan2(brick.width, brick.height)

                if (ball_angle < short_angle and ball_angle > -short_angle):
                    if not (self.through_ball):
                        speedx *= -1
                    #self.set_position(brick.x - self.width, self.y)
                    self.angle = self.__convert_components2angle__(speedx,speedy)
                    brick.got_hit(self.pad_reference, self, self.item_list)
                    return brick.points

                if (ball_angle < long_angle * 2 + short_angle and ball_angle < -long_angle * 2 - short_angle): # from the right b
                    if not (self.through_ball):
                        speedx *= -1
                    #self.set_position(brick.x + brick.width, self.y)
                    self.angle = self.__convert_components2angle__(speedx,speedy)
                    brick.got_hit(self.pad_reference, self, self.item_list)
                    return brick.points
                
                if (ball_angle < long_angle * 2 + short_angle and ball_angle > short_angle):
                    if not (self.through_ball):
                        speedy *= -1
                    #self.set_position(self.x, brick.y - self.width)
                    self.angle = self.__convert_components2angle__(speedx,speedy)
                    brick.got_hit(self.pad_reference, self, self.item_list)
                    return brick.points

                if (ball_angle > -long_angle * 2 - short_angle and ball_angle < -short_angle):
                    if not (self.through_ball):
                        speedy *= -1
                    #self.set_position(self.x, brick.y + brick.height)
                    self.angle = self.__convert_components2angle__(speedx,speedy)
                    brick.got_hit(self.pad_reference, self, self.item_list)
                    return brick.points
                
                # UUUUUUUUGH?
                if not (self.through_ball):
                    speedx *= -1
                    #self.set_position(brick.x + brick.width, self.y)
                    self.angle = self.__convert_components2angle__(speedx,speedy)
                    brick.got_hit(self.pad_reference, self, self.item_list)
                    return brick.points

        else:
            self.collide_timer -= 1
            return 0
        return 0

    # doesn't work
    def __collide_brick_2__(self, brick: Block):
        if(self.collided(brick)):
            brick.got_hit(self.pad_reference, self, self.item_list)
            speedx, speedy = self.__convert_angle2components__()

            tl, tr, bl, br = (brick.x - self.width, brick.y), (brick.x + brick.width + self.width, brick.y), (brick.x  - self.width, brick.y + brick.height), (brick.x + brick.width + self.width, brick.y + brick.height)
            
            collided_t = self.rect.clipline(tl, tr)
            collided_b = self.rect.clipline(bl, br)
            collided_r = self.rect.clipline(tr, br)
            collided_l = self.rect.clipline(tl, bl)


            s = 'ball hit on brick\'s '
            if(collided_t):
                s += 't '
            if(collided_r):
                s += 'r '
            if(collided_l):
                s += 'l '
            if(collided_b):
                s += 'b '
            
            print(s)
            print(collided_t, collided_r, collided_b, collided_l)

            self.angle = self.__convert_components2angle__(speedx, speedy)
            return True
        
        else:
            return False

    # make this only check the closest one to save resources + fix stuff
    def collide_all_bricks(self, block_dict: dict, point_system):
        for key in block_dict:
            point_system.add_points(self.__collide_brick__(block_dict[key]))

    def reset(self):
        print('reset')
        self.speed = 100
        self.angle = radians(60)
        self.stuck = True
        self.set_position(self.pad_reference.x + self.width * 2, self.pad_reference.y - self.height)
        
        self.through_ball = False
    
    def check_fall(self):
        if self.y > self.area.maxY + 20:
            self.pad_reference.lose_life()

    
    def release(self):
        self.stuck = False

    """Private Trigonometry functions"""        
    def __convert_angle2components__(self):
        speedx = cos(self.angle) * self.speed
        speedy = sin(self.angle) * self.speed
        return speedx, speedy
    def __convert_components2angle__(self, x, y):
        return atan2(y , x)
    def __convert_components2speed__(self, x, y):
        return ((x ** 2) + (y ** 2)) ** 0.5
