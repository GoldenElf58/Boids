import pygame

from boids import Boids


def main() -> None:
    pygame.init()
    
    width, height = 400, 400
    screen: pygame.Surface = pygame.display.set_mode((width, height))
    clock: pygame.time.Clock = pygame.time.Clock()
    
    boids: Boids = Boids(10, screen)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        
        boids.update(dt)
        boids.show()

        pygame.display.flip()
    
    pass


if __name__ == '__main__':
    main()
