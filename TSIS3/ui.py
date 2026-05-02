import pygame

def draw_name_input(screen, current_name):
    """Экран ввода имени"""
    font_big = pygame.font.SysFont("Arial", 36)
    font_small = pygame.font.SysFont("Arial", 24)
    font_name = pygame.font.SysFont("Arial", 32)
    
    
    screen.fill((50, 50, 100))
    
    
    title = font_big.render("ENTER YOUR NAME", True, (255, 255, 255))
    screen.blit(title, (WIDTH(screen) // 2 - title.get_width() // 2, 150))
    
    
    input_rect = pygame.Rect(100, 250, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 0)
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
    
    
    name_text = font_name.render(current_name + ("_" if pygame.time.get_ticks() % 1000 < 500 else " "), True, (0, 0, 0))
    screen.blit(name_text, (input_rect.x + 10, input_rect.y + 12))
    
    
    instruction = font_small.render("Press ENTER to continue", True, (255, 255, 200))
    screen.blit(instruction, (WIDTH(screen) // 2 - instruction.get_width() // 2, 350))
    
    
    hint = font_small.render("Use keyboard to type your name", True, (200, 200, 200))
    screen.blit(hint, (WIDTH(screen) // 2 - hint.get_width() // 2, 400))

def draw_menu(screen, player_name):
    """Главное меню с именем игрока"""
    font_big = pygame.font.SysFont("Arial", 50)
    font_medium = pygame.font.SysFont("Arial", 30)
    font_small = pygame.font.SysFont("Arial", 20)
    
    screen.fill((255, 255, 255))
    
    
    title = font_big.render("HIGHWAY RACER", True, (0, 0, 0))
    screen.blit(title, (WIDTH(screen) // 2 - title.get_width() // 2, 100))

    
    name_text = font_medium.render(f"Player: {player_name}", True, (100, 100, 100))
    screen.blit(name_text, (WIDTH(screen) // 2 - name_text.get_width() // 2, 180))
    
    
    y_pos = 280
    buttons = [
        ("PLAY", pygame.K_RETURN),
        ("SETTINGS", pygame.K_s),
        ("LEADERBOARD", pygame.K_l),
        ("QUIT", pygame.K_q)
    ]
    
    for btn_text, key in buttons:
        
        btn_surface = font_medium.render(btn_text, True, (0, 0, 0))
        btn_rect = btn_surface.get_rect(center=(WIDTH(screen) // 2, y_pos))
        screen.blit(btn_surface, btn_rect)
        
        
        hint = font_small.render(f"Press {pygame.key.name(key).upper()}", True, (150, 150, 150))
        screen.blit(hint, (WIDTH(screen) // 2 - hint.get_width() // 2, y_pos + 25))
        
        y_pos += 70
    
    
    quit_hint = font_small.render("Press Q to quit anywhere", True, (200, 0, 0))
    screen.blit(quit_hint, (WIDTH(screen) // 2 - quit_hint.get_width() // 2, 550))

def draw_settings(screen, settings):
    """Экран настроек"""
    font_big = pygame.font.SysFont("Arial", 40)
    font_medium = pygame.font.SysFont("Arial", 28)
    font_small = pygame.font.SysFont("Arial", 20)

    screen.fill((200, 200, 200))
    
    
    title = font_big.render("SETTINGS", True, (0, 0, 0))
    screen.blit(title, (WIDTH(screen) // 2 - title.get_width() // 2, 100))
    
    
    sound_text = font_medium.render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, (0, 0, 0))
    screen.blit(sound_text, (WIDTH(screen) // 2 - sound_text.get_width() // 2, 220))
    
    
    controls = font_medium.render("Controls:", True, (0, 0, 0))
    screen.blit(controls, (WIDTH(screen) // 2 - controls.get_width() // 2, 280))
    
    controls_info = font_small.render("← → arrows to move", True, (50, 50, 50))
    screen.blit(controls_info, (WIDTH(screen) // 2 - controls_info.get_width() // 2, 310))
    
    
    screen.blit(font_small.render("D - Toggle sound", True, (0, 0, 0)), (100, 400))
    screen.blit(font_small.render("ESC - Back to menu", True, (0, 0, 0)), (100, 430))

def draw_leaderboard(screen, board):
    """Таблица лидеров"""
    font_big = pygame.font.SysFont("Arial", 36)
    font_medium = pygame.font.SysFont("Arial", 24)
    font_small = pygame.font.SysFont("Arial", 18)

    screen.fill((30, 30, 30))
    
   
    title = font_big.render("TOP 10 RACERS", True, (255, 255, 255))
    screen.blit(title, (WIDTH(screen) // 2 - title.get_width() // 2, 50))
    
    
    rank_header = font_medium.render("RANK", True, (255, 200, 0))
    name_header = font_medium.render("NAME", True, (255, 200, 0))
    score_header = font_medium.render("SCORE", True, (255, 200, 0))
    dist_header = font_medium.render("DIST", True, (255, 200, 0))
    
    screen.blit(rank_header, (30, 110))
    screen.blit(name_header, (90, 110))
    screen.blit(score_header, (250, 110))
    screen.blit(dist_header, (330, 110))
    
    
    pygame.draw.line(screen, (100, 100, 100), (20, 135), (380, 135), 2)
    
   
    y = 150
    for i, entry in enumerate(board[:10]):
        rank = font_medium.render(str(i + 1), True, (255, 255, 255))
        name = font_small.render(entry['name'][:15], True, (255, 255, 255))
        score = font_small.render(str(entry['score']), True, (255, 255, 0))
        distance = font_small.render(str(int(entry['distance'])), True, (200, 200, 200))
        
        screen.blit(rank, (35, y))
        screen.blit(name, (90, y))
        screen.blit(score, (250, y))
        screen.blit(distance, (330, y))
        
        y += 35
        if y > 550:
            break
    
   
    back_text = font_small.render("Press ESC or M to return", True, (150, 150, 150))
    screen.blit(back_text, (WIDTH(screen) // 2 - back_text.get_width() // 2, 570))

def draw_game_over(screen, game, player_name):
    """Экран Game Over"""
    font_big = pygame.font.SysFont("Arial", 48)
    font_medium = pygame.font.SysFont("Arial", 32)
    font_small = pygame.font.SysFont("Arial", 24)

    screen.fill((50, 0, 0))
    
  
    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH(screen) // 2 - game_over_text.get_width() // 2, 100))
    
   
    name_text = font_medium.render(f"Racer: {player_name}", True, (255, 255, 255))
    screen.blit(name_text, (WIDTH(screen) // 2 - name_text.get_width() // 2, 180))
    
    
    score_text = font_medium.render(f"Score: {game.score}", True, (255, 255, 0))
    screen.blit(score_text, (WIDTH(screen) // 2 - score_text.get_width() // 2, 250))
    
    dist_text = font_medium.render(f"Distance: {int(game.distance)}m", True, (200, 200, 255))
    screen.blit(dist_text, (WIDTH(screen) // 2 - dist_text.get_width() // 2, 290))
    
    coins_text = font_medium.render(f"Coins: {game.coins_collected}", True, (255, 215, 0))
    screen.blit(coins_text, (WIDTH(screen) // 2 - coins_text.get_width() // 2, 330))
    
    
    retry_text = font_small.render("Press R to RETRY", True, (0, 255, 0))
    screen.blit(retry_text, (WIDTH(screen) // 2 - retry_text.get_width() // 2, 420))
    
    menu_text = font_small.render("Press M for MAIN MENU", True, (255, 255, 255))
    screen.blit(menu_text, (WIDTH(screen) // 2 - menu_text.get_width() // 2, 460))

def WIDTH(screen):
    """Вспомогательная функция для получения ширины экрана"""
    return screen.get_width()