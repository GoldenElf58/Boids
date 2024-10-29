import math

import pygame


class Boid:
    def __init__(self, x, y, angle, speed, screen):
        self.x: int = x
        self.y: int = y
        self.screen: pygame.Surface = screen
        self.angle: float = angle
        self.speed: float = speed
    
    def update(self, dt):
        self.x += self.speed * math.cos(self.angle) * dt
        self.y += self.speed * math.sin(self.angle) * dt
        if self.x > self.screen.get_width():
            self.x = 0
        if self.x < 0:
            self.x = self.screen.get_width()
        if self.y > self.screen.get_height():
            self.y = 0
        if self.y < 0:
            self.y = self.screen.get_height()

    def show(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)
