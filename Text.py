from PPlay.window import Window
from Area import Area

class Text():
    w = None
    area = None
    x,y = None, None

    def __init__(self, area: Area, w: Window, obj, color=(255,255,255), size=12, pre_str=''):
        self.obj = obj
        self.area  = area
        self.w = w
        self.x = area.x
        self.y = area.y
        self.color = color
        self.size = size
        self.pre_str = pre_str
        self.string = '???'

    
    def draw(self):
        self.string = self.obj.__str__() if self.obj is not None else self.string
        self.w.draw_text(self.pre_str + self.string, self.x, self.y, self.size, self.color)
    
    def set_posistion(self, x: float, y: float):
        self.x = x
        self.y = y
