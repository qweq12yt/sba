from Block import Block
from Area import Area

class PlainBrick(Block):
    t = 'plain'
    points = 10
    subtypes = ['orange.png', 'brown.png', 'green.png', 'blue.png', 'pink.png', 'purple.png']
    def __init__(self, area: Area, x, y, sub_type=0, image_file='gfx/', frames=1):
        image_file += self.subtypes[sub_type]
        super().__init__(area, x, y, sub_type=sub_type, image_file=image_file, frames=frames)

class SturdyBrick(Block):
    t = 'sturdy'
    life = 3
    points = 15
    def __init__(self, area: Area, x, y, sub_type=1, image_file='gfx/sturdy.png', frames=4):
        self.life = sub_type
        super().__init__(area, x, y, sub_type=sub_type, image_file=image_file, frames=frames)
        self.set_curr_frame(sub_type - 1)