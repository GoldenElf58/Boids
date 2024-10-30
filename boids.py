import random

from boid import Boid


class Boids:
    def __init__(self, num_boids, screen):
        self.num_boids = num_boids
        self.screen = screen
        self.boids = []
        self.create_boids()

    def create_boids(self):
        for i in range(self.num_boids):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            angle = random.randrange(0, 360)
            speed = random.randrange(20, 50)
            boid = Boid(x, y, angle, speed, self.screen)
            self.boids.append(boid)

    def update(self, dt):
        for boid in self.boids:
            boid.calculate(dt, self.boids)
        for boid in self.boids:
            boid.update_pos(dt)

    def show(self):
        for boid in self.boids:
            boid.show()
