import pygame
from config import PATH
import os

grass = pygame.image.load(PATH+os.path.join('data', 'grassPlatform.png'))
w, h = grass.get_rect().size
class Platform:
    def __init__(self, x, y, w, h, typee):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = typee
        self.img = pygame.transform.scale(grass, (self.w, self.h))
    def update(self, win):
        if self.type == 'floor':
            pass
        if self.type == 'plat':
            win.blit(self.img, (self.x, self.y))
           # pygame.draw.rect(win, (0,255,0), pygame.Rect(self.x, self.y, self.w, self.h))
    def hit(self, x, y, lastY):
        if x < self.x+self.w+10 and x > self.x-10 and y > self.y+10 and lastY < self.y+10:
            return True, self.y+10
        return False, 0