import pygame, sys
from racer import Game
from ui import *
from persistence import *

pygame.init()
pygame.mixer.init() 


WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

settings = load_settings()
leaderboard = load_leaderboard()


state = "NAME_INPUT"
name = ""

game = None


cursor_blink = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_settings(settings)
            pygame.quit()
            sys.exit()
        
        
        if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
            save_settings(settings)
            pygame.quit()
            sys.exit()

        
        if state == "NAME_INPUT":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip():
                    
                    game = Game(settings)
                    state = "MENU"
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    
                    if len(name) < 20 and e.unicode.isprintable():
                        name += e.unicode

       
        elif state == "MENU":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    game.reset()
                    state = "GAME"
                elif e.key == pygame.K_l:
                    state = "LEADERBOARD"
                elif e.key == pygame.K_s:
                    state = "SETTINGS"

        
        elif state == "SETTINGS":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d:
                    settings["sound"] = not settings["sound"]
                    
                    if game:
                        game.settings = settings
                elif e.key == pygame.K_ESCAPE:
                    state = "MENU"

        
        elif state == "LEADERBOARD":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_m:
                    state = "MENU"

       
        elif state == "GAME":
            
            pass

        
        elif state == "GAME_OVER":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    game.reset()
                    state = "GAME"
                elif e.key == pygame.K_m:
                    state = "MENU"

    
    screen.fill((0, 0, 0))

    
    if state == "NAME_INPUT":
        draw_name_input(screen, name)
    
    elif state == "MENU":
        draw_menu(screen, name)
    
    elif state == "SETTINGS":
        draw_settings(screen, settings)
    
    elif state == "LEADERBOARD":
        draw_leaderboard(screen, leaderboard)
    
    elif state == "GAME":
    
        game.update()
        
        
        if game.game_over:
            
            leaderboard = add_score(leaderboard, name, game.score, game.distance)
            save_leaderboard(leaderboard)
            state = "GAME_OVER"
        
        
        game.draw(screen)
    
    elif state == "GAME_OVER":
        draw_game_over(screen, game, name)

    pygame.display.update()
    clock.tick(60)