from SpriteObject import SpriteObject
from Paddle import Paddle


class Item(SpriteObject):
    speed = 125
    to_destroy = False

    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item.png"):
        super().__init__(area, image_file, 1)
        self.ball_reference = ball_reference
        self.pad_reference = pad_reference

    def move(self, d_time):
        self.move_y(self.speed * d_time)
        if(self.y > self.area.maxY):
            self.to_destroy = True

    def do_effect(self):
        pass

class KillPaddle(Item):
    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item_kp.png"):
        super().__init__(area, ball_reference, pad_reference, image_file=image_file)

    def do_effect(self):
        self.pad_reference.lose_life()

class ThroughBall(Item):

    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item_tb.png"):
        super().__init__(area, ball_reference, pad_reference, image_file=image_file)

    def do_effect(self):
        self.ball_reference.through_ball = True

class FastBall(Item):
    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item_fb.png"):
        super().__init__(area, ball_reference, pad_reference, image_file=image_file)
    
    def do_effect(self):
        self.ball_reference.speed *= 1.75

class GlueBall(Item):
    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item_gb.png"):
        super().__init__(area, ball_reference, pad_reference, image_file=image_file)
    
    def do_effect(self):
        self.pad_reference.glue_ball = True

class ShootingPaddle(Item):
    def __init__(self, area, ball_reference, pad_reference: Paddle, image_file="gfx/item_sp.png"):
        super().__init__(area, ball_reference, pad_reference, image_file=image_file)
    
    def do_effect(self):
        self.pad_reference.shooting_paddle = True


def remove_items(item_list: list):
    to_remove = []
    for item in item_list:
        if item.to_destroy:
            to_remove.append(item)
    
    for i in to_remove:
        item_list.remove(i)


types = [ThroughBall, FastBall, GlueBall, ShootingPaddle, KillPaddle]