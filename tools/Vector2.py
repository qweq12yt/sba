from math import atan, cos, sin

class Vector2:
    x = None
    y = None
    lenght = None
    angle = None

    def __calcLenghtAngle__(self):
        self.lenght = ((self.x ** 2) + (self.y ** 2) ** (1/2))
        self.angle = atan(self.y/self.x)
    
    def __calcComponents__(self):
        self.x = self.lenght * cos(self.angle)
        self.y = self.lenght * sin(self.angle)

    def __init__(self, x_component, y_component):
        self.x = x_component
        self.y = y_component
        self.__calcLenghtAngle__()
    
    def __init__(self, lenght, angle):
        self.lenght = lenght
        self.angle = angle
        self.__calcComponents__()

    def sum(self, v):
        self.x += v.x
        self.y += v.y
        self.__calcLenghtAngle__()
    
    def reflect(self, v):
        self.x *= v.x
        self.y *= v.y
        self.__calcLenghtAngle__()