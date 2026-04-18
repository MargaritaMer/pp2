import pygame
from datetime import datetime

class MickeyClock:
    def __init__(self, bg_path, min_path, sec_path, center):
        self.bg = pygame.image.load(bg_path)
        self.min_hand = pygame.image.load(min_path).convert_alpha()
        self.sec_hand = pygame.image.load(sec_path).convert_alpha()

        
        self.min_hand = pygame.transform.scale(self.min_hand, (250, 250))
        self.sec_hand = pygame.transform.scale(self.sec_hand, (300, 300))

        self.center = center

    def get_angles(self):
        now = datetime.now()
        minutes = now.minute 
        seconds = now.second

        angle_min = minutes * 6
        angle_sec = seconds * 6

        return angle_min, angle_sec

    def draw_hand(self, screen, image, angle):
        rotated = pygame.transform.rotate(image, -angle)
        rect = rotated.get_rect(center=self.center)
        screen.blit(rotated, rect)

    def draw(self, screen):
        angle_min, angle_sec = self.get_angles()

        screen.blit(self.bg, (0, 0))

        
        self.draw_hand(screen, self.min_hand, angle_min)

       
        self.draw_hand(screen, self.sec_hand, angle_sec)