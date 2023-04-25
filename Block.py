from Area import Area
from SpriteObject import SpriteObject
from random import randint, shuffle
from Item import Item, types
from PPlay.sound import Sound


class Block(SpriteObject):
    pos = None
    t = 'block'
    s = 0
    life = 1
    points = 1
    hit_sound = Sound('sounds/hit.ogg')
    break_sound = [Sound('sounds/break1.ogg'), Sound('sounds/break2.ogg'), Sound('sounds/break3.ogg')]

    def __init__(self, area: Area, x, y, sub_type=0, image_file='gfx/generic.png', frames=1):
        super().__init__(area, image_file, frames=frames)
        self.pos = (x, y)
        self.width = 50
        self.height = 20
        self.s = sub_type
        self.x = area.x + x * self.width
        self.y = area.y + 1 + y * self.height
    
    def got_hit(self, pad=None, ball=None, item_list: list = None, deliver_item=True):
        self.life -= 1
        self.set_curr_frame(self.life - 1)
        
        if(self.life == 0):
            shuffle(self.break_sound)
            self.break_sound[0].play()
        else:
            self.hit_sound.play()

        if (self.life == 0 and randint(0, 2) == 0 and deliver_item):
            shuffle(types)
            new_item = types[0](self.area, ball, pad)
            new_item.set_position(self.x, self.y)
            item_list.append(new_item)


def draw_all_blocks(block_dict: dict):
    for key in block_dict:
        block_dict[key].draw()

def remove_dead(block_dict: dict):
    to_remove = []
    for key in block_dict:
        block = block_dict[key]
        if block.life <= 0:
            to_remove.append(key)
    for key in to_remove:
        block_dict.pop(key)
