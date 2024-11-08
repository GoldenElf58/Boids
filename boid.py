import pygame
from pygame.math import Vector2


class Boid:
    def __init__(self, x, y, angle, speed, screen, min_accel=0, max_accel=10, min_vel=0, max_vel=50,
                 cohesion_weight=1.0, separation_weight=3.0, alignment_weight=1.0):
        self.pos = Vector2(x, y)
        self.vel = Vector2(speed, 0).rotate_rad(angle)
        self.acc = Vector2()
        self.screen = screen
        self.min_accel = min_accel
        self.max_accel = max_accel
        self.min_vel = min_vel
        self.max_vel = max_vel
        self.cohesion_weight = cohesion_weight
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight

    def show(self):
        angle = self.vel.as_polar()[1] + 90  # Angle in degrees
        points = [
            Vector2(0, -10).rotate(angle),
            Vector2(-5, 5).rotate(angle),
            Vector2(5, 5).rotate(angle),
        ]
        translated_points = [self.pos + point for point in points]
        pygame.draw.polygon(self.screen, "white", translated_points)

    def update_pos(self, dt):
        self.pos += self.vel * dt
        width, height = self.screen.get_size()
        self.pos.x %= width
        self.pos.y %= height

    # noinspection PyTypeChecker
    def calculate(self, dt, boids, perception_radius=50):
        cohesion = Vector2()
        separation = Vector2()
        alignment = Vector2()
        total = 0

        for boid in boids:
            if boid != self:
                offset = boid.pos - self.pos
                distance = offset.length()
                if 0 < distance < perception_radius:
                    # Cohesion
                    cohesion += boid.pos
                    # Separation
                    separation += (self.pos - boid.pos).normalize() / distance
                    # Alignment
                    alignment += boid.vel
                    total += 1

        if total > 0:
            # Cohesion
            center_of_mass = cohesion / total
            cohesion = (center_of_mass - self.pos)
            cohesion = cohesion.normalize() * self.max_accel if cohesion.length() > 0 else Vector2()

            # Separation
            separation = separation.normalize() * self.max_accel if separation.length() > 0 else Vector2()

            # Alignment
            avg_velocity = alignment / total
            alignment = (avg_velocity - self.vel)
            alignment = alignment.normalize() * self.max_accel if alignment.length() > 0 else Vector2()

            self.acc = (cohesion * self.cohesion_weight +
                        separation * self.separation_weight +
                        alignment * self.alignment_weight)

            # Limit acceleration
            if self.acc.length() > self.max_accel:
                self.acc.scale_to_length(self.max_accel)
            elif self.acc.length() < self.min_accel:
                self.acc.scale_to_length(self.min_accel)

        # Update velocity and limit it
        self.vel += self.acc * dt
        if self.vel.length() > self.max_vel:
            self.vel.scale_to_length(self.max_vel)
        elif self.vel.length() < self.min_vel:
            self.vel.scale_to_length(self.min_vel)

    def cohesion(self, boid):
        return boid.pos - self.pos

    def separate(self, boid, dist_squared: float, perception_radius: float = 50):
        # if dist_squared == 0:
        #     print("div by 0")
        #     return Vector2(0, 0)
        #     # return vector(phi=self.vel.phi, rho=0)
        return ((self.pos - boid.pos) / dist_squared) * perception_radius ** 2

    @staticmethod
    def align(boid: 'Boid') -> Vector2:
        return Vector2(boid.vel.x, boid.vel.y).normalize()
        # return vector(phi=boid.vel.phi, rho=1)

    def __repr__(self):
        return f"Boid(pos={self.pos}, vel={self.vel}, acc={self.acc})"
