import math
import random

from area import Area
from boid import Boid
from quadtree import Quadtree


class Boids:
    def __init__(self, num_boids, screen, perception_radius=75, max_qt=4, min_accel=0, max_accel=10, min_velocity=0,
                 max_velocity=50, cohesion_weight=1, separation_weight=1, alignment_weight=1):
        self.num_boids = num_boids
        self.screen = screen
        self.perception_radius = perception_radius
        self.max_qt = max_qt
        self.max_accel = max_accel
        self.min_accel = min_accel
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.cohesion_weight = cohesion_weight
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight

        self.all_boids = []
        self.boids = Quadtree(0, 0, self.screen.get_width(), self.screen.get_height(), max_qt)
        # self.area = Area(0, 0, self.screen.get_width(), self.screen.get_height())
        self.create_boids()

    def create_boids(self):
        for i in range(self.num_boids):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            angle = random.uniform(0, math.tau)
            speed = random.randrange(20, 50)
            boid = Boid(x, y, angle, speed, self.screen, max_accel=self.max_accel, min_accel=self.min_accel,
                        max_vel=self.max_velocity, min_vel=self.min_velocity, cohesion_weight=self.cohesion_weight,
                        separation_weight=self.separation_weight, alignment_weight=self.alignment_weight)
            self.all_boids.append(boid)
            self.update_quadtree()

    def update_quadtree(self):
        self.boids = Quadtree(0, 0, self.screen.get_width(), self.screen.get_height(), self.max_qt)
        for boid in self.all_boids:
            self.boids.insert(boid)

    def update(self, dt):
        for boid in self.all_boids:
            r = self.perception_radius
            area = Area(boid.pos.x - r, boid.pos.y - r, r * 2, r * 2)
            boids = self.boids.query(area)
            # boid.calculate(dt, self.all_boids, r)
            boid.calculate(dt, boids, r)

        for boid in self.all_boids:
            boid.update_pos(dt)
            # if random.random() < .001:
            #     print(f'Velocity: {boid.vel.length():.2f}')
            #     print(f'Acceleration: {boid.acc.length():.2f}')

        self.update_quadtree()

    def show(self):
        for boid in self.all_boids:
            boid.show()

    def show_quadtree(self):
        self.boids.show(self.screen)

    def __len__(self):
        return len(self.all_boids)

    def __repr__(self):
        return f"Boids({self.num_boids})"
