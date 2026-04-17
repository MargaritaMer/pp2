import pygame
import sys
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

center = (WIDTH // 2, HEIGHT // 2)


mickey = MickeyClock(
    "images/clock.png",
    "images/right_hand.png",
    "images/left_hand.png",
    center
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    
    mickey.draw(screen)

    pygame.display.flip()
    clock.tick(60)