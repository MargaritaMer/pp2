import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20 # kлетка 20 пикселей


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 24)



class Snake:
    def __init__(self):
        
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.dx = CELL_SIZE # движение в право
        self.dy = 0 #вверх вниз
        self.grow = False #рост после еды
        #Змейка список координаn,nачинается в центре

    def move(self):
        
        head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
#Создаём новую голову:берём старую + добавляем движение
        
        self.body.insert(0, head) # новая голова в начале списка

        
        if not self.grow:
            self.body.pop()# удаляем хвост
        else:
            self.grow = False

    def draw(self):
        
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    def change_direction(self, dx, dy):
        
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx = dx
            self.dy = dy  #запрет идти назад

    def collide_with_self(self):
        
        return self.body[0] in self.body[1:] #Столкновение с собой



class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            if (x, y) not in snake.body: #не должна появляться на змейке
                return (x, y)

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))



def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))



def main():
    snake = Snake()
    food = Food(snake)

    score = 0
    level = 1
    foods_eaten = 0

    speed = 7  

    while True:
        screen.fill(BLACK)
        draw_grid()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, CELL_SIZE)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(CELL_SIZE, 0)

        
        snake.move()

        head_x, head_y = snake.body[0]

        
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            print("Game Over! Hit wall.") #вышли за экран
            pygame.quit()
            sys.exit()

        
        if snake.collide_with_self(): #Столкновение с собой
            print("Game Over! Hit yourself.")
            pygame.quit()
            sys.exit()

        
        if snake.body[0] == food.position:
            snake.grow = True
            score += 1
            foods_eaten += 1
            food = Food(snake)

       
        if foods_eaten == 4:  
            level += 1
            foods_eaten = 0
            speed += 2  

        
        snake.draw()
        food.draw()

        
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.update()

        
        clock.tick(speed)



if __name__ == "__main__":
    main()