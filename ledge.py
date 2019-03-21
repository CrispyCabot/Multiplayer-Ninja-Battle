import pygame
from config import PATH
import os

grass = pygame.image.load(PATH+os.path.join('data', 'platform.png'))
wall1 = pygame.image.load(PATH+os.path.join('data', 'wall1.png'))
wall2 = pygame.image.load(PATH+os.path.join('data', 'wall2.png'))
class Platform:
    def __init__(self, x, y, w, h, typee):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = typee
        self.img = pygame.transform.scale(grass, (self.w, self.h))
    def draw(self, win):
        if self.type == 'floor':
            pass
        if self.type == 'plat':
            win.blit(self.img, (self.x, self.y))
           # pygame.draw.rect(win, (0,255,0), pygame.Rect(self.x, self.y, self.w, self.h))
    def hit(self, x, y, lastY):
        if x < self.x+self.w+10 and x > self.x-10 and y > self.y and lastY < self.y+10:
            return True, self.y+10
        return False, 0

class Wall:
    def __init__(self, x, y, w, h, typ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if typ == 'wall1':
            self.img = pygame.transform.scale(wall1, (self.w, self.h))
        else:
            self.img = pygame.transform.scale(wall2, (self.w, self.h))
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
    def hit(self, x, y):
        if self.x < x+30 and x-30 < self.x+self.w and self.y < y+75 and y-75 < self.y+self.h:
            return True