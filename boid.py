import pygame

from vector import Point, PolarVector


class Boid:
    def __init__(self, x, y, angle, speed, screen):
        self.pos: Point = Point(x, y)
        self.vel: PolarVector = PolarVector(angle, speed)
        self.screen: pygame.Surface = screen
    
    def show(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos.to_tuple(), 5)
    
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
    
    def calculate(self, dt, boids, perception_radius=35):
        cohesion = PolarVector()
        separation = PolarVector()
        alignment = PolarVector()
        total = 0
        
        for boid in boids:
            if boid != self and (d := self.pos.distance(boid.pos)) < perception_radius:
                cohesion += self.cohesion(boid)
                separation += self.separate(boid, d)
                alignment += self.align(boid)
                total += 1
        
        if total != 0:
            cohesion /= total
            separation /= total
            alignment /= total
        
        cohesion = cohesion.to_polar()
        
        cohesion = (cohesion * .1).limit(5)
        separation = (separation * 1).limit(5)
        alignment = (alignment * 1).limit(5)
        # print(cohesion, separation, alignment, total)
        
        self.vel += cohesion + separation + alignment
        self.vel = self.vel.limit(30)
        self.update_pos(dt)
    
    def cohesion(self, boid):
        return boid.pos - self.pos
    
    def separate(self, boid, dist: float):
        if dist == 0:
            return PolarVector()
        return (self.pos - boid.pos).to_polar() / dist
    
    def align(self, boid):
        return boid.vel
