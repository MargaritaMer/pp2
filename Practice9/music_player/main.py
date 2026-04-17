import pygame
import sys
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("comicsansms", 24)

player = MusicPlayer("music")

clock = pygame.time.Clock()

def draw():
    screen.fill((20, 20, 20))

    title = font.render("Music Player", True, (255, 255, 255))
    track = font.render(f"Track: {player.get_current_track_name()}", True, (255, 0, 255))

    controls = font.render(
        "P=Play S=Stop N=Next B=Back Q=Quit",
        True,
        (200, 200, 200)
    )

    screen.blit(title, (20, 20))
    screen.blit(track, (20, 80))
    screen.blit(controls, (20, 150))

    pygame.display.update()


while True:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.prev_track()

    clock.tick(30)