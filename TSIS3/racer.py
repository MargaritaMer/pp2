import pygame, random, os

BASE = os.path.dirname(__file__)

def load(x):
    return pygame.image.load(os.path.join(BASE, "assets", x))

LANES = [80, 160, 240, 320]


# ================= КЛАСС МОНЕТЫ =================
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


# ================= КЛАСС ИГРОКА =================
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


# ================= КЛАСС ОБЪЕКТОВ =================
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


# ================= ОСНОВНОЙ КЛАСС ИГРЫ =================
class Game:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        # Игрок
        self.player = Player()

        # Группы спрайтов
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Загрузка изображений
        self.bg = load("AnimatedStreet.png")
        self.enemy_img = load("Enemy.png")
        
        # Монеты разного размера
        self.coin_imgs = {
            1: pygame.transform.scale(load("coin.png"), (20, 20)),
            2: pygame.transform.scale(load("coin.png"), (30, 30)),
            3: pygame.transform.scale(load("coin.png"), (40, 40))
        }
        
        self.oil_img = load("oil.png")
        self.nitro_img = load("nitro.png")
        self.shield_img = load("shield.png")
        self.repair_img = load("repair.png")

        # Таймеры спавна
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 800

        # Счетчики
        self.score = 0
        self.distance = 0
        self.coins_collected = 0

        # Скорость
        self.base_speed = 5
        self.current_speed = self.base_speed

        # Эффекты
        self.slowed = False
        self.slow_timer = 0
        self.shield = False
        self.active_power = None
        self.power_timer = 0

        # Состояние игры
        self.game_over = False

    # ================= СПАВН ОБЪЕКТОВ =================
    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn < self.spawn_delay:
            return

        self.last_spawn = now

        lanes = [0, 1, 2, 3]

        # Проверка безопасных полос (не спавним на игрока)
        safe_lanes = [l for l in lanes if abs(LANES[l] - self.player.rect.centerx) > 60]
        if not safe_lanes:
            return

        random.shuffle(safe_lanes)

        for lane in safe_lanes:
            if self.lane_busy(lane):
                continue

            roll = random.randint(1, 100)

            # 40% - враги
            if roll <= 40:
                self.enemies.add(Obj(self.enemy_img, lane))
            
            # 30% - монеты (разного номинала)
            elif roll <= 70:
                value = random.choice([1, 2, 3])
                coin = Coin(self.coin_imgs[value], lane, value)
                self.coins.add(coin)
            
            # 20% - препятствия (масло)
            elif roll <= 90:
                self.hazards.add(Obj(self.oil_img, lane, kind="oil", move_side=True))
            
            # 10% - усиления
            else:
                power_type = random.choice(["nitro", "shield", "repair"])
                if power_type == "nitro":
                    self.powerups.add(Obj(self.nitro_img, lane, kind="nitro"))
                elif power_type == "shield":
                    self.powerups.add(Obj(self.shield_img, lane, kind="shield"))
                else:
                    self.powerups.add(Obj(self.repair_img, lane, kind="repair"))

            break

    # ================= ПРОВЕРКА ЗАНЯТОСТИ ПОЛОСЫ =================
    def lane_busy(self, lane):
        for group in [self.enemies, self.coins, self.hazards]:
            for obj in group:
                if abs(obj.rect.centerx - LANES[lane]) < 10 and obj.rect.y < 150:
                    return True
        return False

    # ================= ОБНОВЛЕНИЕ ИГРЫ =================
    def update(self):
        if self.game_over:
            return
            
        # Обновляем игрока
        self.player.update()
        
        # Спавним новые объекты
        self.spawn()

        # Обновляем все группы объектов
        self.enemies.update()
        self.coins.update()
        self.hazards.update()
        self.powerups.update()

        now = pygame.time.get_ticks()

        # ===== СТОЛКНОВЕНИЕ С ВРАГАМИ =====
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            if self.shield:
                # Щит защищает от одного врага
                self.shield = False
                self.active_power = None
                # Удаляем врага, с которым столкнулись
                for enemy in self.enemies:
                    if self.player.rect.colliderect(enemy.rect):
                        enemy.kill()
                        break
            else:
                # Нет щита - игра окончена
                self.game_over = True
                return

        # ===== МАСЛО (ЗАМЕДЛЕНИЕ) =====
        oil_hit = pygame.sprite.spritecollideany(self.player, self.hazards)
        if oil_hit:
            self.slowed = True
            self.slow_timer = now
            oil_hit.kill()  # Масло исчезает после касания

        # Снимаем замедление через 2 секунды
        if self.slowed and now - self.slow_timer > 2000:
            self.slowed = False

        # ===== СБОР МОНЕТ =====
        coins_hit = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coins_hit:
            self.score += coin.value * 10
            self.coins_collected += coin.value

        # ===== СБОР УСИЛЕНИЙ =====
        power_hit = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for power in power_hit:
            self.active_power = power.kind
            self.power_timer = now

            if power.kind == "nitro":
                # Нитро активируется в расчете скорости
                pass
            elif power.kind == "shield":
                self.shield = True
            elif power.kind == "repair":
                # Ремонт убирает замедление
                self.slowed = False
                # Небольшое восстановление скорости
                self.base_speed = max(5, self.base_speed - 0.5)

        # ===== ТАЙМЕР УСИЛЕНИЙ =====
        if self.active_power and now - self.power_timer > 4000:
            if self.active_power == "shield":
                self.shield = False
            self.active_power = None

        # ===== РАСЧЕТ СКОРОСТИ =====
        speed = self.base_speed
        
        if self.slowed:
            speed = 3
        
        if self.active_power == "nitro":
            speed = 10
        
        self.current_speed = speed

        # Применяем скорость ко всем объектам
        for group in [self.enemies, self.coins, self.hazards, self.powerups]:
            for obj in group:
                obj.speed = self.current_speed

        # ===== НАЧИСЛЕНИЕ ОЧКОВ И ДИСТАНЦИИ =====
        self.distance += self.current_speed * 0.1

        # ===== УВЕЛИЧЕНИЕ СЛОЖНОСТИ =====
        if int(self.distance) % 200 == 0 and int(self.distance) > 0:
            self.spawn_delay = max(250, self.spawn_delay - 50)
            self.base_speed += 0.2

    # ================= ОТРИСОВКА ИГРЫ =================
    def draw(self, screen):
        # Рисуем фон
        screen.blit(self.bg, (0, 0))

        # Рисуем все объекты
        self.enemies.draw(screen)
        self.coins.draw(screen)
        self.hazards.draw(screen)
        self.powerups.draw(screen)

        # Рисуем игрока
        screen.blit(self.player.image, self.player.rect)

        # Шрифты
        font = pygame.font.SysFont("Arial", 20)
        font_big = pygame.font.SysFont("Arial", 24)

        # Статистика (левый верхний угол)
        screen.blit(font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Coins: {self.coins_collected}", True, (255, 215, 0)), (10, 30))
        screen.blit(font.render(f"Dist: {int(self.distance)}m", True, (255, 255, 255)), (10, 50))

        # Статус эффектов (правый верхний угол)
        y_offset = 10
        
        if self.shield:
            shield_text = font_big.render("🛡️ SHIELD", True, (0, 200, 255))
            screen.blit(shield_text, (280, y_offset))
            y_offset += 25
            
        if self.active_power == "nitro":
            nitro_text = font_big.render("⚡ NITRO", True, (255, 100, 0))
            screen.blit(nitro_text, (280, y_offset))
            y_offset += 25
            
        if self.slowed:
            slow_text = font_big.render("💧 OIL SLOW", True, (150, 150, 150))
            screen.blit(slow_text, (280, y_offset))
            y_offset += 25

        # Время действия активного усиления
        if self.active_power and self.active_power != "repair":
            now = pygame.time.get_ticks()
            remaining = max(0, 4 - (now - self.power_timer) / 1000)
            screen.blit(font.render(f"{remaining:.1f}s", True, (200, 200, 200)), (280, y_offset))