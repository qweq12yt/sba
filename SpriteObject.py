from Area import Area
from PPlay.sprite import Sprite

class SpriteObject(Sprite):
    area = None
    def __init__(self,area: Area, image_file, frames=1):
        super().__init__(image_file, frames)
        super().set_position(area.x, area.y)
        self.area = area
    
    """This area is NOT the .area atribute!!!!, just a easy way to get the bounds of a sprite for use with mouse.is_over_area().
    Gets [start_point, end_point]"""
    def get_area(self):
        return (self.x, self.y), (self.x + self.width, self.x + self.height)