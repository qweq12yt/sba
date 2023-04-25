import Vector2
from math import radians

class Line2Angle:
    lenght = None
    max_angle = None
    max_speed_boost = None

    def __init__(self, lenght, max_angle, max_speed=0):
        self.lenght = lenght
        self.max_angle = radians(max_angle + 90)
        self.max_speed_boost = max_speed
    
    def __findMultiplier__(self, x,y):
        
        pass

    def calculateRebound(self, v: Vector2, contact_point):
        pass