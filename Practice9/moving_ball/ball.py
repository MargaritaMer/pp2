class Ball:
    def __init__(self, x, y, radius, speed, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.width = width
        self.height = height

    def move(self, direction):
        if direction == "LEFT" and self.x - self.speed - self.radius >= 0:
            self.x -= self.speed
        if direction == "RIGHT" and self.x + self.speed + self.radius <= self.width:
            self.x += self.speed
        if direction == "UP" and self.y - self.speed - self.radius >= 0:
            self.y -= self.speed
        if direction == "DOWN" and self.y + self.speed + self.radius <= self.height:
            self.y += self.speed