import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


SPEED = 5

SCORE = 0
COINS = 0


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


background = pygame.image.load("AnimatedStreet.png")


DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        
        self.value = random.choice([1, 2, 3])

        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()

        
        self.image = pygame.transform.scale(self.image, (20*self.value, 20*self.value))

        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)

        
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        
        self.value = random.choice([1, 2, 3])
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (20*self.value, 20*self.value))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()


C1 = Coin()
C2 = Coin()

coins = pygame.sprite.Group()
coins.add(C1,C2)

enemies = pygame.sprite.Group()
enemies.add(E1, )

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1,  C1, C2)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2  

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    
    DISPLAYSURF.blit(background, (0,0))

    
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (250, 10))

    
    hit_coin = pygame.sprite.spritecollideany(P1, coins)
    if hit_coin:
        COINS += hit_coin.value  
        hit_coin.reset()

        
        if COINS % 5 == 0:
            SPEED += 1
            print("Speed increased!")

    
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)