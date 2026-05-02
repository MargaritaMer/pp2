import pygame

import random


class Snake:
    def __init__(self, color):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.dx = CELL_SIZE
        self.dy = 0
        self.grow = False
        self.color = color
        self.shield_active = False
    
    def move(self):
        head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
        self.body.insert(0, head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (*segment, CELL_SIZE, CELL_SIZE))
    
    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx = dx
            self.dy = dy
    
    def collide_with_self(self):
        return self.body[0] in self.body[1:]
    
    def shorten(self, amount=2):
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()
    
    def get_length(self):
        return len(self.body)

class Food:
    def __init__(self, snake, obstacles):
        self.position = self.generate_position(snake, obstacles)
        self.value = random.choice([1, 2, 3])
        
        if self.value == 1:
            self.color = RED
        elif self.value == 2:
            self.color = (255, 165, 0) #оранжевый
        elif self.value == 3:
            self.color = (255, 255, 0) #желтый
        
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(3000, 7000)
    
    def generate_position(self, snake, obstacles):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = (x, y)
            if pos not in snake.body and pos not in obstacles:
                return pos
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))

class PoisonFood:
    def __init__(self, snake, obstacles, food_pos):
        self.position = self.generate_position(snake, obstacles, food_pos)
        self.color = (139, 0, 0)  # темно красный 
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000
    
    def generate_position(self, snake, obstacles, food_pos):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = (x, y)
            if pos not in snake.body and pos not in obstacles and pos != food_pos:
                return pos
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))

class PowerUp:
    def __init__(self, snake, obstacles, foods):
        self.type = random.choice(['speed_boost', 'slow_motion', 'shield'])
        self.position = self.generate_position(snake, obstacles, foods)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000
        
        if self.type == 'speed_boost':
            self.color = (0, 255, 255)  #голубой
        elif self.type == 'slow_motion':
            self.color = (255, 0, 255)  # фиолетовый 
        else:  #щит
            self.color = (0, 255, 0)  #зеленый
    
    def generate_position(self, snake, obstacles, foods):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = (x, y)
            if pos not in snake.body and pos not in obstacles:
                valid = True
                for food in foods:
                    if pos == food.position:
                        valid = False
                        break
                if valid:
                    return pos
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))

class Obstacle:
    def __init__(self, x, y):
        self.position = (x, y)
        self.color = (100, 100, 100) #серый
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
    
    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

class Game:
    def __init__(self, db, settings_manager, username):
        self.db = db
        self.settings = settings_manager
        self.username = username
        self.snake = Snake(tuple(self.settings.get("snake_color")))
        self.obstacles = []
        self.foods = []
        self.poison_foods = []
        self.powerups = []
        
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.speed = 7
        self.personal_best = db.get_personal_best(username)
        
        
        self.speed_boost_end = 0
        self.slow_motion_end = 0
        self.original_speed = self.speed
        
    
        self.foods.append(Food(self.snake, self.get_all_obstacle_positions()))
        
        
        if self.level >= 3:
            self.generate_obstacles()
    
    def get_all_obstacle_positions(self):
        return [obs.position for obs in self.obstacles]
    
    def generate_obstacles(self):
        self.obstacles = []
        num_obstacles = min(5 + self.level, 15)
        snake_head = self.snake.body[0]
        
        for _ in range(num_obstacles):
            while True:
                x = random.randrange(0, WIDTH, CELL_SIZE)
                y = random.randrange(0, HEIGHT, CELL_SIZE)
                pos = (x, y)
                
                
                if pos not in self.snake.body and abs(pos[0] - snake_head[0]) > CELL_SIZE * 3:
                    self.obstacles.append(Obstacle(x, y))
                    break
    
    def spawn_powerup(self):
        if len(self.powerups) == 0 and random.random() < 0.02:  
            all_foods = self.foods + self.poison_foods
            self.powerups.append(PowerUp(self.snake, self.get_all_obstacle_positions(), all_foods))
    
    def spawn_poison(self):
        if len(self.poison_foods) == 0 and random.random() < 0.01:  
            all_foods = self.foods
            self.poison_foods.append(PoisonFood(self.snake, self.get_all_obstacle_positions(), 
                                                self.foods[0].position if self.foods else (0,0)))
    
    def update_powerups(self):
        current_time = pygame.time.get_ticks()
        
        
        if current_time < self.speed_boost_end:
            self.speed = self.original_speed + 3
        elif current_time < self.slow_motion_end:
            self.speed = max(3, self.original_speed - 3)
        else:
            self.speed = self.original_speed
    
    def handle_collisions(self):
        head = self.snake.body[0]
        
       
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            if self.snake.shield_active:
                self.snake.shield_active = False
                return False
            return True
        
        
        if self.snake.collide_with_self():
            if self.snake.shield_active:
                self.snake.shield_active = False
                return False
            return True
        
        
        for obstacle in self.obstacles:
            if head == obstacle.position:
                if self.snake.shield_active:
                    self.snake.shield_active = False
                    return False
                return True
        
        return False
    
    def update(self):
        self.snake.move()
        
        
        if self.handle_collisions():
            return False
        
        head = self.snake.body[0]
        
        
        for food in self.foods[:]:
            if head == food.position:
                self.snake.grow = True
                self.score += food.value
                self.foods_eaten += 1
                self.foods.remove(food)
                self.foods.append(Food(self.snake, self.get_all_obstacle_positions()))
                
                
                if self.foods_eaten >= 4:
                    self.level += 1
                    self.foods_eaten = 0
                    self.original_speed += 2
                    if self.level >= 3:
                        self.generate_obstacles()
        
        
        for poison in self.poison_foods[:]:
            if head == poison.position:
                self.snake.shorten(2)
                self.poison_foods.remove(poison)
                if self.snake.get_length() <= 1:
                    return False
        
        
        for powerup in self.powerups[:]:
            if head == powerup.position:
                current_time = pygame.time.get_ticks()
                if powerup.type == 'speed_boost':
                    self.speed_boost_end = current_time + 5000
                elif powerup.type == 'slow_motion':
                    self.slow_motion_end = current_time + 5000
                elif powerup.type == 'shield':
                    self.snake.shield_active = True
                self.powerups.remove(powerup)
        
        
        self.update_powerups()
        
        
        self.spawn_powerup()
        self.spawn_poison()
        
        
        for food in self.foods[:]:
            if food.is_expired():
                self.foods.remove(food)
                self.foods.append(Food(self.snake, self.get_all_obstacle_positions()))
        
        for poison in self.poison_foods[:]:
            if poison.is_expired():
                self.poison_foods.remove(poison)
        
        for powerup in self.powerups[:]:
            if powerup.is_expired():
                self.powerups.remove(powerup)
        
        return True
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        
        if self.settings.get("grid_overlay"):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
        
        
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        
        for food in self.foods:
            food.draw(screen)
        
        
        for poison in self.poison_foods:
            poison.draw(screen)
        
        
        for powerup in self.powerups:
            powerup.draw(screen)
        
        
        self.snake.draw(screen)
        
        
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        best_text = font.render(f"Best: {self.personal_best}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(best_text, (10, 70))
        
        
        if self.snake.shield_active:
            shield_text = font.render("SHIELD ACTIVE", True, (255, 255, 0))
            screen.blit(shield_text, (WIDTH - 150, 10))
    
    def game_over(self):
        self.db.save_game_result(self.username, self.score, self.level)
        return self.score, self.level, self.personal_best