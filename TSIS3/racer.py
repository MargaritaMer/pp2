import pygame, random, os

BASE = os.path.dirname(__file__)  

def load(x):
    return pygame.image.load(os.path.join(BASE, "assets", x))

LANES = [80, 160, 240, 320]

pygame.mixer.init()

try:
    crash_sound = pygame.mixer.Sound(os.path.join(BASE, "assets", "crash.wav"))
    crash_sound.set_volume(0.5)  
    print("crash.wav loaded successfully!") 
except Exception as e:
    crash_sound = None
    print(f"crash.wav not found. Error: {e}")

class Coin(pygame.sprite.Sprite):
    def __init__(self, img, lane, value):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(LANES[lane], -50))
        self.value = value
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("Player.png")
        self.rect = self.image.get_rect(center=(200, 500))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < 400:
            self.rect.x += self.speed


class Obj(pygame.sprite.Sprite):
    def __init__(self, img, lane, kind=None, move_side=False):
        super().__init__()
        self.image = pygame.transform.scale(img, (40, 60))
        self.rect = self.image.get_rect(center=(LANES[lane], -50))

        self.kind = kind
        self.move_side = move_side
        self.dir = random.choice([-1, 1])
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.move_side:
            self.rect.x += self.dir * 2
            if self.rect.left < 0 or self.rect.right > 400:
                self.dir *= -1

        if self.rect.top > 600:
            self.kill()


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        
        self.player = Player()

        
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        
        self.bg = load("AnimatedStreet.png")
        self.enemy_img = load("Enemy.png")
        
    
        self.coin_imgs = {
            1: pygame.transform.scale(load("coin.png"), (20, 20)),
            2: pygame.transform.scale(load("coin.png"), (30, 30)),
            3: pygame.transform.scale(load("coin.png"), (40, 40))
        }
        
        self.oil_img = load("oil.png")
        self.nitro_img = load("nitro.png")
        self.shield_img = load("shield.png")
        self.repair_img = load("repair.png")

        
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 800

        
        self.score = 0
        self.distance = 0
        self.coins_collected = 0

        
        self.base_speed = 5
        self.current_speed = self.base_speed

       
        self.slowed = False
        self.slow_timer = 0
        self.shield = False
        self.active_power = None
        self.power_timer = 0

        
        self.game_over = False

    
    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn < self.spawn_delay:
            return

        self.last_spawn = now

        lanes = [0, 1, 2, 3]

        safe_lanes = [l for l in lanes if abs(LANES[l] - self.player.rect.centerx) > 60]
        if not safe_lanes:
            return

        random.shuffle(safe_lanes)

        for lane in safe_lanes:
            if self.lane_busy(lane):
                continue

            roll = random.randint(1, 100)

            
            if roll <= 40:
                self.enemies.add(Obj(self.enemy_img, lane))
            
           
            elif roll <= 70:
                value = random.choice([1, 2, 3])
                coin = Coin(self.coin_imgs[value], lane, value)
                self.coins.add(coin)
            
            
            elif roll <= 90:
                self.hazards.add(Obj(self.oil_img, lane, kind="oil", move_side=True))
            
           
            else:
                power_type = random.choice(["nitro", "shield", "repair"])
                if power_type == "nitro":
                    self.powerups.add(Obj(self.nitro_img, lane, kind="nitro"))
                elif power_type == "shield":
                    self.powerups.add(Obj(self.shield_img, lane, kind="shield"))
                else:
                    self.powerups.add(Obj(self.repair_img, lane, kind="repair"))

            break


    def lane_busy(self, lane):
        for group in [self.enemies, self.coins, self.hazards]:
            for obj in group:
                if abs(obj.rect.centerx - LANES[lane]) < 10 and obj.rect.y < 150:
                    return True
        return False

  
    def update(self):
        if self.game_over:
            return
            
    
        self.player.update()
        

        self.spawn()

        
        self.enemies.update()
        self.coins.update()
        self.hazards.update()
        self.powerups.update()

        now = pygame.time.get_ticks()

       
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            if self.shield:
              
                self.shield = False
                self.active_power = None
               
                for enemy in self.enemies:
                    if self.player.rect.colliderect(enemy.rect):
                        enemy.kill()
                        break
            else:
               
                if crash_sound:
                    crash_sound.play()
                
                self.game_over = True
                return

      
        oil_hit = pygame.sprite.spritecollideany(self.player, self.hazards)
        if oil_hit:
            self.slowed = True
            self.slow_timer = now
            oil_hit.kill()  

       
        if self.slowed and now - self.slow_timer > 2000:
            self.slowed = False

        coins_hit = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coins_hit:
            self.score += coin.value * 10
            self.coins_collected += coin.value

    
        power_hit = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for power in power_hit:
            self.active_power = power.kind
            self.power_timer = now

            if power.kind == "nitro":
               
                pass
            elif power.kind == "shield":
                self.shield = True
            elif power.kind == "repair":
                
                self.slowed = False
               
                self.base_speed = max(5, self.base_speed - 0.5)

        
        if self.active_power and now - self.power_timer > 4000:
            if self.active_power == "shield":
                self.shield = False
            self.active_power = None

     
        speed = self.base_speed
        
        if self.slowed:
            speed = 3
        
        if self.active_power == "nitro":
            speed = 10
        
        self.current_speed = speed

        
        for group in [self.enemies, self.coins, self.hazards, self.powerups]:
            for obj in group:
                obj.speed = self.current_speed

       
        self.distance += self.current_speed * 0.1

       
        if int(self.distance) % 200 == 0 and int(self.distance) > 0:
            self.spawn_delay = max(250, self.spawn_delay - 50)
            self.base_speed += 0.2

   
    def draw(self, screen):
        
        screen.blit(self.bg, (0, 0))

      
        self.enemies.draw(screen)
        self.coins.draw(screen)
        self.hazards.draw(screen)
        self.powerups.draw(screen)

       
        screen.blit(self.player.image, self.player.rect)

        
        font = pygame.font.SysFont("Arial", 20)
        font_big = pygame.font.SysFont("Arial", 24)

       
        screen.blit(font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Coins: {self.coins_collected}", True, (255, 215, 0)), (10, 30))
        screen.blit(font.render(f"Dist: {int(self.distance)}m", True, (255, 255, 255)), (10, 50))

        
        y_offset = 10
        
        if self.shield:
            shield_text = font_big.render("SHIELD", True, (0, 200, 255))
            screen.blit(shield_text, (280, y_offset))
            y_offset += 25
            
        if self.active_power == "nitro":
            nitro_text = font_big.render("NITRO", True, (255, 100, 0))
            screen.blit(nitro_text, (280, y_offset))
            y_offset += 25
            
        if self.slowed:
            slow_text = font_big.render("OIL SLOW", True, (150, 150, 150))
            screen.blit(slow_text, (280, y_offset))
            y_offset += 25

        
        if self.active_power and self.active_power != "repair":
            now = pygame.time.get_ticks()
            remaining = max(0, 4 - (now - self.power_timer) / 1000)
            screen.blit(font.render(f"{remaining:.1f}s", True, (200, 200, 200)), (280, y_offset))