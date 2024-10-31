import pygame

from boids import Boids


def main() -> None:
    pygame.init()
    # pygame.font.init()
    
    width, height = 1920, 1080
    # font = pygame.font.SysFont(None, 32)
    screen: pygame.Surface = pygame.display.set_mode((width, height))
    clock: pygame.time.Clock = pygame.time.Clock()
    
    boids: Boids = Boids(200, screen, 80)
    
    fps = 0
    total = 0
    running = True
    i = 0
    while running:
        dt = clock.tick(60) / 1000
        i += dt
        fps += 1/dt
        total += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        
        # text = font.render(str(1/dt), True, (255,255,255))
        # text_rect = text.get_rect(center=(50,50))
        # screen.blit(text, text_rect)
        
        
        boids.update(dt)
        boids.show()
        
        if i > 1:
            print(fps/total)
            i = 0
        
        
        pygame.display.flip()


if __name__ == '__main__':
    main()
