import pygame
import time

from boids import Boids


def main() -> None:
    show_fps = True
    num_boids = 150
    perception_radius = 50
    max_qt = 4
    frame_eval = 300
    fps = 60
    
    pygame.init()
    pygame.font.init()
    
    width, height = 700, 600
    screen: pygame.Surface = pygame.display.set_mode((width, height))
    
    font = pygame.font.SysFont(None, 32)
    clock: pygame.time.Clock = pygame.time.Clock()
    
    boids: Boids = Boids(num_boids, screen, perception_radius, max_qt)
    
    t0 = time.perf_counter()
    fps_total = 0
    frames = 0
    running = True
    # i = 0
    while running:
        dt = clock.tick(fps) / 1000
        # i += dt
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
        
        screen.fill((0, 0, 0))
        
        if show_fps:
            text = font.render(f'{fps_total / frames:.1f}', True, (255, 255, 255))
            # text_rect = text.get_rect(center=(50, 50))
            screen.blit(text, (10, 10))
        
        boids.update(dt)
        boids.show()
        
        # if i > 1:
        #     print(fps / total)
        #     i = 0
        
        pygame.display.flip()


if __name__ == '__main__':
    main()
