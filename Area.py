"""extensively used for final project, not so much for other things"""

class Area:
    x, y, width, height, maxX, maxY = 0, 0, 0, 0, 0, 0

    def __init__(self, x=0, y=0, width=0, height=0) -> None:
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
        self.maxY   = y + height
        self.maxX   = x + width
