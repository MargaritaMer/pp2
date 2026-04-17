import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

ball = Ball(WIDTH // 2, HEIGHT // 2, 25, 1, WIDTH, HEIGHT)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]: 
            ball.move("RIGHT")
    if keys[pygame.K_LEFT]: 
            ball.move("LEFT")
    if keys[pygame.K_DOWN]:
            ball.move("DOWN")
    if keys[pygame.K_UP]:
           ball.move("UP")

        

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (160, 32, 208), (ball.x, ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()