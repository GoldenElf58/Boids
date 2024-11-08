import time

import pygame

from boids import Boids


# noinspection PyTypeChecker
def main() -> None:
    show_fps = True
    show_quadtree = False
    update = True
    width, height = 800, 800
    num_boids = 100
    perception_radius = 75
    cohesion_weight = 1
    separation_weight = 3
    alignment_weight = 2

    min_acceleration = 20
    max_acceleration = 75
    min_velocity = 50
    max_velocity = 150

    max_qt = 4
    frame_eval = 300
    fps = 60

    pygame.init()
    pygame.font.init()

    screen: pygame.Surface = pygame.display.set_mode((width, height))

    font = pygame.font.SysFont(None, 32)
    clock: pygame.time.Clock = pygame.time.Clock()

    boids: Boids = Boids(
        num_boids,
        screen,
        perception_radius=perception_radius,
        min_accel=min_acceleration,
        max_accel=max_acceleration,
        max_qt=max_qt,
        min_velocity=min_velocity,
        max_velocity=max_velocity,
        cohesion_weight=cohesion_weight,
        separation_weight=separation_weight,
        alignment_weight=alignment_weight
    )

    t0 = time.perf_counter()
    fps_total = 0
    frames = 0
    running = True
    while running:
        dt = clock.tick(fps) / 1000
        fps_total += 1 / dt
        frames += 1

        if frames == frame_eval:
            t1 = time.perf_counter()
            print(t1 - t0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_f:
                    show_fps = not show_fps
                if event.key == pygame.K_q:
                    show_quadtree = not show_quadtree
                if event.key == pygame.K_u:
                    update = not update

        screen.fill((0, 0, 0))

        if show_fps:
            text = font.render(f'{1 / dt:.0f}', True, (255, 255, 255))
            # text_rect = text.get_rect(center=(50, 50))
            screen.blit(text, (10, 10))

        if show_quadtree:
            boids.show_quadtree()

        if update:
            boids.update(dt)
        boids.show()

        pygame.display.flip()


if __name__ == '__main__':
    main()
