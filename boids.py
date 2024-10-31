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
            self.boids.insert(boid)

    def update(self, dt):
        for boid in self.boids.query(self.area):
            boid.calculate(dt, self.boids, self.perception_radius)
        for boid in self.boids.query(self.area):
            boid.update_pos(dt)

    def show(self):
        for boid in self.boids.query(self.area):
            boid.show()
