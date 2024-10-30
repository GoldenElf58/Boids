import math
import random

import pygame

from vector import Point, PolarVector


class Boid:
    def __init__(self, x, y, angle, speed, screen):
        self.pos: Point = Point(x, y)
        self.vel: PolarVector = PolarVector(angle, speed)
        self.acc: PolarVector = PolarVector()
        self.screen: pygame.Surface = screen
    
    def show(self):
        x = self.pos.x
        y = self.pos.y
        theta = self.vel.angle + math.pi / 2  # The angle to rotate by
        
        # Define the triangle points relative to (x, y)
        points = [(0, 0), (-4, 10), (4, 10)]  # Apex at (0, 0)
        
        # Rotate the points around (0, 0) by theta
        rotated_points = []
        for point in points:
            x_prime, y_prime = point
            x_rot = x_prime * math.cos(theta) - y_prime * math.sin(theta)
            y_rot = x_prime * math.sin(theta) + y_prime * math.cos(theta)
            # Translate the points back to the original position
            x_abs = x + x_rot
            y_abs = y + y_rot
            rotated_points.append([x_abs, y_abs])
        
        # Draw the rotated triangle
        pygame.draw.polygon(self.screen, "white", rotated_points)
        # pygame.draw.circle(self.screen, (255, 255, 255), self.pos.to_tuple(), 5)
    
    def update_pos(self, dt):
        self.pos += PolarVector(self.vel.angle, self.vel.speed * dt)
        if self.pos.x > self.screen.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.screen.get_width()
        if self.pos.y > self.screen.get_height():
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = self.screen.get_height()
    
    def calculate(self, dt, boids, perception_radius: float = 50):
        cohesion = PolarVector(self.vel.angle, 0)
        separation = PolarVector(self.vel.angle, 0)
        alignment = PolarVector(self.vel.angle, 0)
        total = 0
        
        for boid in boids:
            if boid != self and (d := self.pos.distance(boid.pos)) < perception_radius:
                cohesion += self.cohesion(boid)
                separation += self.separate(boid, d, perception_radius)
                alignment += self.align(boid)
                total += 1
        
        if total != 0:
            cohesion /= total
            separation /= total
            alignment /= total
        
        cohesion = cohesion.to_polar()
        
        cohesion = (cohesion * 1).limit(10)
        separation = (separation * 1).limit(10.07)
        alignment = (alignment * 1).limit(10)
        # r = PolarVector(random.uniform(-math.pi / 12, math.pi / 12), 0)
        # print(cohesion, separation, alignment, total)
        
        self.acc = cohesion + separation + alignment
        self.acc.speed = 250 * dt
        self.vel += self.acc
        self.vel.speed = 50
    
    def cohesion(self, boid):
        return boid.pos - self.pos
    
    def separate(self, boid, dist: float, perception_radius: float = 50):
        if dist == 0:
            return PolarVector()
        return ((self.pos - boid.pos).to_polar() / dist) * perception_radius
    
    def align(self, boid):
        return PolarVector(boid.vel.angle, 1)
