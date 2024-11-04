import math

import pygame

from vector import Point, PolarVector


class Boid:
    def __init__(self, x, y, angle, speed, screen, max_accel: float = 10, max_vel: float = 50):
        self.pos: Point = Point(x, y)
        self.vel: PolarVector = PolarVector(angle, speed)
        self.acc: PolarVector = PolarVector()
        self.screen: pygame.Surface = screen
        self.max_accel = max_accel
        self.max_vel = max_vel
    
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
        self.pos += self.vel * dt
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
            if boid != self and (d_sq := self.pos.distance_squared(boid.pos)) < perception_radius ** 2:
                cohesion += self.cohesion(boid)
                separation += self.separate(boid, d_sq, perception_radius)
                alignment += self.align(boid)
                total += 1
        
        if total != 0:
            cohesion /= total
            separation /= total
            alignment /= total
        
        cohesion = cohesion.to_polar()
        
        cohesion = (cohesion * 1).limit(self.max_accel * 2) * 1
        separation = (separation * 1).limit(self.max_accel * 2) * 200
        alignment = (alignment * 1).limit(self.max_accel * 2) * 1
        # r = PolarVector(random.uniform(-math.pi / 12, math.pi / 12), 0)
        # print(cohesion, separation, alignment, total)
        print(cohesion, separation, alignment)
        
        self.acc = cohesion + separation + alignment
        self.acc.limit(self.max_accel)
        self.acc.magnitude = self.max_accel
        self.vel += self.acc * dt
        self.vel.limit(self.max_vel)
        self.vel.magnitude = self.max_vel

    def cohesion(self, boid):
        return boid.pos - self.pos
    
    def separate(self, boid, dist_squared: float, perception_radius: float = 50):
        if dist_squared == 0:
            return PolarVector(self.vel.angle, 0)
        return ((self.pos - boid.pos).to_polar() / dist_squared) * perception_radius ** 2
    
    def align(self, boid):
        return PolarVector(boid.vel.angle, 1)
    
    def __repr__(self):
        return f"Boid(pos={self.pos}, vel={self.vel}, acc={self.acc})"
