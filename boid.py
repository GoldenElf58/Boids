import math

import pygame

from vector import Point, PolarVector


class Boid:
    def __init__(self, x, y, angle, speed, screen):
        self.pos: Point = Point(x, y)
        self.vel: PolarVector = PolarVector(angle, speed)
        self.screen: pygame.Surface = screen
    
    def update(self, dt, boids):
        cohesion = PolarVector()
        separation = PolarVector()
        alignment = PolarVector()
        
        for boid in boids:
            if boid != self:
                cohesion += self.cohesion(boid)
                separation += self.separation(boid)
                alignment += self.alignment(boid)
        
        self.vel += cohesion
        self.vel += separation
        self.vel += alignment
        self.vel = self.vel.limit(5)
        self.pos += self.vel
        self.pos = self.pos.limit(self.screen.get_width(), self.screen.get_height())
    
    def update_pos(self, dt):
        self.pos += self.vel * dt
        if self.pos.x > self.screen.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.screen.get_width()
        if self.pos.y > self.screen.get_height():
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = self.screen.get_height()

    def show(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos.to_tuple(), 5)
