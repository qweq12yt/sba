class PointSystem:
    points = 0

    def add_points(self, points: int):
        self.points += points if points else 0
    
    def __str__(self) -> str:
        return str(self.points)