import math
import random

from area import Area
from boid import Boid
from quadtree import Quadtree


class Boids:
    def __init__(self, num_boids, screen, perception_radius=75):
        self.num_boids = num_boids
        self.screen = screen
        self.perception_radius = perception_radius
        
        self.all_boids = []
        self.boids = Quadtree(0, 0, self.screen.get_width(), self.screen.get_height(), 4)
        self.area = Area(0, 0, self.screen.get_width(), self.screen.get_height())
        self.create_boids()

    def create_boids(self):
        for i in range(self.num_boids):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            angle = random.uniform(0, math.tau)
            speed = random.randrange(20, 50)
            boid = Boid(x, y, angle, speed, self.screen)
            self.all_boids.append(boid)
            self.update_quadtree()
        
    def update_quadtree(self):
        self.boids = Quadtree(0, 0, self.screen.get_width(), self.screen.get_height(), 4)
        for boid in self.all_boids:
            self.boids.insert(boid)

    def update(self, dt):
        for boid in self.all_boids:
            r = self.perception_radius
            area = Area(boid.pos.x - r, boid.pos.y - r, r * 2, r * 2)
            boids = self.boids.query(area)
            boid.calculate(dt, boids, r)
        
        for boid in self.all_boids:
            boid.update_pos(dt)
        
        self.update_quadtree()
    
    def show(self):
        for boid in self.all_boids:
            boid.show()
