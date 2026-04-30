import pygame, sys
from racer import Game
from ui import *
from persistence import *

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

settings = load_settings()
leaderboard = load_leaderboard()

# Состояния игры
state = "NAME_INPUT"
name = ""

game = None

# Для анимации курсора
cursor_blink = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_settings(settings)
            pygame.quit()
            sys.exit()
        
        # Глобальный выход по Q
        if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
            save_settings(settings)
            pygame.quit()
            sys.exit()

        # Состояние ввода имени
        if state == "NAME_INPUT":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip():
                    # Создаем игру с именем игрока
                    game = Game(settings)
                    state = "MENU"
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Ограничиваем длину имени
                    if len(name) < 20 and e.unicode.isprintable():
                        name += e.unicode

        # Меню
        elif state == "MENU":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    game.reset()
                    state = "GAME"
                elif e.key == pygame.K_l:
                    state = "LEADERBOARD"
                elif e.key == pygame.K_s:
                    state = "SETTINGS"

        # Настройки
        elif state == "SETTINGS":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d:
                    settings["sound"] = not settings["sound"]
                    # Применяем настройки к игре
                    if game:
                        game.settings = settings
                elif e.key == pygame.K_ESCAPE:
                    state = "MENU"

        # Таблица лидеров
        elif state == "LEADERBOARD":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_m:
                    state = "MENU"

        # Игра - ВАЖНО! Здесь обновляем игру
        elif state == "GAME":
            # Обработка нажатий для игры (опционально)
            pass

        # Экран Game Over
        elif state == "GAME_OVER":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    game.reset()
                    state = "GAME"
                elif e.key == pygame.K_m:
                    state = "MENU"

    # ОТРИСОВКА (ВНЕ цикла событий)
    screen.fill((0, 0, 0))

    # Отрисовка разных состояний
    if state == "NAME_INPUT":
        draw_name_input(screen, name)
    
    elif state == "MENU":
        draw_menu(screen, name)
    
    elif state == "SETTINGS":
        draw_settings(screen, settings)
    
    elif state == "LEADERBOARD":
        draw_leaderboard(screen, leaderboard)
    
    elif state == "GAME":
        # ВАЖНО: Обновляем игру КАЖДЫЙ кадр
        game.update()
        
        # Проверяем Game Over
        if game.game_over:
            # Сохраняем результат
            leaderboard = add_score(leaderboard, name, game.score, game.distance)
            save_leaderboard(leaderboard)
            state = "GAME_OVER"
        
        # Рисуем игру
        game.draw(screen)
    
    elif state == "GAME_OVER":
        draw_game_over(screen, game, name)

    pygame.display.update()
    clock.tick(60)