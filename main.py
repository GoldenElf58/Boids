import pygame

from boids import Boids


def main() -> None:
    pygame.init()
    
    width, height = 1920, 1080
    screen: pygame.Surface = pygame.display.set_mode((width, height))
    clock: pygame.time.Clock = pygame.time.Clock()
    
    boids: Boids = Boids(150, screen, 80)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        
        boids.update(dt)
        boids.show()

        pygame.display.flip()


if __name__ == '__main__':
    main()
