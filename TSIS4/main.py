import pygame
import sys
from db import Database
from settings_manager import SettingsManager
from game import Game, Button, WIDTH, HEIGHT, WHITE, BLACK, CELL_SIZE

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48)
        
        self.db = Database()
        self.settings = SettingsManager()
        self.username = ""
        self.current_screen = "menu"
        self.typing = False
    
    def draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(surface, rect)
    
    def username_entry_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Enter Username:", self.title_font, WHITE, WIDTH//2 - 150, HEIGHT//2 - 100)
        
        # Draw input box
        input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, 2)
        
        username_surface = self.font.render(self.username + ("_" if self.typing else ""), True, WHITE)
        self.screen.blit(username_surface, (input_box.x + 5, input_box.y + 10))
        
        self.draw_text("Press ENTER to continue", self.font, WHITE, WIDTH//2 - 120, HEIGHT//2 + 60)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    if len(self.username) < 20:
                        self.username += event.unicode
        return None
    
    def main_menu(self):
        play_button = Button(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50, "PLAY", (0, 128, 0), (0, 255, 0))
        leaderboard_button = Button(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50, "LEADERBOARD", (0, 0, 128), (0, 0, 255))
        settings_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "SETTINGS", (128, 128, 0), (255, 255, 0))
        quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 125, 200, 50, "QUIT", (128, 0, 0), (255, 0, 0))
        
        while self.current_screen == "menu":
            self.screen.fill(BLACK)
            
            self.draw_text("SNAKE GAME", self.title_font, WHITE, WIDTH//2 - 120, 50)
            
            play_button.draw(self.screen, self.font)
            leaderboard_button.draw(self.screen, self.font)
            settings_button.draw(self.screen, self.font)
            quit_button.draw(self.screen, self.font)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif play_button.is_clicked(event):
                    self.current_screen = "game"
                    return True
                elif leaderboard_button.is_clicked(event):
                    self.current_screen = "leaderboard"
                elif settings_button.is_clicked(event):
                    self.current_screen = "settings"
                elif quit_button.is_clicked(event):
                    return False
            
            self.clock.tick(60)
        return True
    
    def leaderboard_screen(self):
        scores = self.db.get_top_scores()
        back_button = Button(WIDTH//2 - 50, HEIGHT - 80, 100, 40, "BACK", (128, 0, 0), (255, 0, 0))
        
        while self.current_screen == "leaderboard":
            self.screen.fill(BLACK)
            
            self.draw_text("TOP 10 LEADERBOARD", self.title_font, WHITE, WIDTH//2 - 150, 20)
            
            # Draw headers
            headers = ["Rank", "Username", "Score", "Level", "Date"]
            x_positions = [50, 150, 350, 500, 600]
            for i, header in enumerate(headers):
                self.draw_text(header, self.font, WHITE, x_positions[i], 80)
            
            # Draw scores
            y = 120
            for i, score in enumerate(scores, 1):
                username, score_val, level, played_at = score
                date_str = played_at.strftime("%Y-%m-%d")
                values = [str(i), username[:15], str(score_val), str(level), date_str]
                for j, value in enumerate(values):
                    self.draw_text(value, self.font, WHITE, x_positions[j], y)
                y += 30
                if y > HEIGHT - 100:
                    break
            
            back_button.draw(self.screen, self.font)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif back_button.is_clicked(event):
                    self.current_screen = "menu"
            
            self.clock.tick(60)
        return True
    
    def settings_screen(self):
        grid_button = Button(WIDTH//2 - 100, 100, 200, 50, 
                            f"Grid: {'ON' if self.settings.get('grid_overlay') else 'OFF'}", 
                            (0, 128, 0), (0, 255, 0))
        sound_button = Button(WIDTH//2 - 100, 170, 200, 50,
                             f"Sound: {'ON' if self.settings.get('sound') else 'OFF'}",
                             (0, 128, 0), (0, 255, 0))
        color_button = Button(WIDTH//2 - 100, 240, 200, 50,
                            "Change Color", (128, 0, 128), (255, 0, 255))
        back_button = Button(WIDTH//2 - 50, HEIGHT - 80, 100, 40, "SAVE & BACK", (0, 0, 128), (0, 0, 255))
        
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
        color_index = 0
        
        while self.current_screen == "settings":
            self.screen.fill(BLACK)
            
            self.draw_text("SETTINGS", self.title_font, WHITE, WIDTH//2 - 80, 20)
            
            grid_button.draw(self.screen, self.font)
            sound_button.draw(self.screen, self.font)
            color_button.draw(self.screen, self.font)
            
            # Show current color
            pygame.draw.rect(self.screen, tuple(self.settings.get("snake_color")), 
                           (WIDTH//2 - 30, 310, 60, 60))
            
            back_button.draw(self.screen, self.font)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif grid_button.is_clicked(event):
                    current = self.settings.get("grid_overlay")
                    self.settings.set("grid_overlay", not current)
                    grid_button.text = f"Grid: {'ON' if self.settings.get('grid_overlay') else 'OFF'}"
                elif sound_button.is_clicked(event):
                    current = self.settings.get("sound")
                    self.settings.set("sound", not current)
                    sound_button.text = f"Sound: {'ON' if self.settings.get('sound') else 'OFF'}"
                elif color_button.is_clicked(event):
                    color_index = (color_index + 1) % len(colors)
                    self.settings.set("snake_color", list(colors[color_index]))
                elif back_button.is_clicked(event):
                    self.current_screen = "menu"
            
            self.clock.tick(60)
        return True
    
    def game_over_screen(self, score, level, personal_best):
        retry_button = Button(WIDTH//2 - 120, HEIGHT//2 + 50, 100, 40, "RETRY", (0, 128, 0), (0, 255, 0))
        menu_button = Button(WIDTH//2 + 20, HEIGHT//2 + 50, 100, 40, "MENU", (128, 0, 0), (255, 0, 0))
        
        while True:
            self.screen.fill(BLACK)
            
            self.draw_text("GAME OVER", self.title_font, WHITE, WIDTH//2 - 100, HEIGHT//2 - 150)
            self.draw_text(f"Score: {score}", self.font, WHITE, WIDTH//2 - 50, HEIGHT//2 - 50)
            self.draw_text(f"Level: {level}", self.font, WHITE, WIDTH//2 - 50, HEIGHT//2 - 20)
            self.draw_text(f"Personal Best: {personal_best}", self.font, WHITE, WIDTH//2 - 80, HEIGHT//2 + 10)
            
            retry_button.draw(self.screen, self.font)
            menu_button.draw(self.screen, self.font)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif retry_button.is_clicked(event):
                    return True
                elif menu_button.is_clicked(event):
                    return False
            
            self.clock.tick(60)
    
    def run(self):
        # Get username
        while True:
            result = self.username_entry_screen()
            if result is False:
                return
            elif result is True:
                break
        
        running = True
        while running:
            if self.current_screen == "menu":
                running = self.main_menu()
            elif self.current_screen == "leaderboard":
                running = self.leaderboard_screen()
            elif self.current_screen == "settings":
                running = self.settings_screen()
            elif self.current_screen == "game":
                game = Game(self.db, self.settings, self.username)
                game_running = True
                
                while game_running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                game.snake.change_direction(0, -CELL_SIZE)
                            elif event.key == pygame.K_DOWN:
                                game.snake.change_direction(0, CELL_SIZE)
                            elif event.key == pygame.K_LEFT:
                                game.snake.change_direction(-CELL_SIZE, 0)
                            elif event.key == pygame.K_RIGHT:
                                game.snake.change_direction(CELL_SIZE, 0)
                    
                    if not game.update():
                        score, level, best = game.game_over()
                        if self.game_over_screen(score, level, best):
                            game = Game(self.db, self.settings, self.username)
                        else:
                            game_running = False
                            self.current_screen = "menu"
                        break
                    
                    game.draw(self.screen)
                    pygame.display.update()
                    self.clock.tick(game.speed)
        
        self.db.close()
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()