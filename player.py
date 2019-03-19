import pygame
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, \
                            MOUSEBUTTONUP, QUIT, K_r
import os
from config import PATH, SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
def loadSprite2(folder, amt, char): #Left images, flips them
    for i in range(0, amt):
        img = pygame.transform.flip(pygame.image.load(PATH +
                                os.path.join('data', 'char', 'red', folder, 'tile00' + str(i)+'.png')), True, False)
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (int(SIZE * w), int(SIZE * h)))
        char[folder].append(img)

def loadSprite(folder, amt, char): #Right images
    for i in range(0, amt):
        img = pygame.image.load(PATH +
                                os.path.join('data', 'char', 'red', folder, 'tile00' + str(i)+'.png'))
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (int(SIZE * w), int(SIZE * h)))
        char[folder].append(img)

def loadR(char):
    loadSprite('death', 4, char)
    loadSprite('hurt', 5, char)
    loadSprite('idle', 4, char)
    loadSprite('longJump', 8, char)
    loadSprite('quickJump', 4, char)
    loadSprite('run', 3, char)
    loadSprite('slash', 4, char)
    loadSprite('sneak', 6, char)
    loadSprite('throw', 5, char)

def loadL(char):
    loadSprite2('death', 4, char)
    loadSprite2('hurt', 5, char)
    loadSprite2('idle', 4, char)
    loadSprite2('longJump', 8, char)
    loadSprite2('quickJump', 4, char)
    loadSprite2('run', 3, char)
    loadSprite2('slash', 4, char)
    loadSprite2('sneak', 6, char)
    loadSprite2('throw', 5, char)

charr = {
        'death': [],
        'hurt': [],
        'idle': [],
        'longJump': [],
        'quickJump': [],
        'run': [],
        'slash': [],
        'sneak': [],
        'throw': []
    }

charl = {
        'death': [],
        'hurt': [],
        'idle': [],
        'longJump': [],
        'quickJump': [],
        'run': [],
        'slash': [],
        'sneak': [],
        'throw': []
    }

loadR(charr)
loadL(charl)

width, height = charr['run'][0].get_rect().size

playerSpeed = 10

class Player:
    def __init__(self, x, y):
        self.x = x
        self.alive = True
        self.y = y
        self.health = 100
        self.damagedEnemy = False
        self.lastY = y
        self.height = height
        self.width = width
        self.health = 100
        self.frameCounter = 0
        self.jumpMax = 30
        self.jumpVel = self.jumpMax
        self.dir = 'right'
        self.jump = False
        self.action = 'idle'
        self.lastAction = 'idle' #used to detect a change in action
        self.reset = False
    def draw(self, win):
        if self.action == self.lastAction:
            self.frameCounter += .1
        else:
            self.frameCounter = 0
            self.lastAction = self.action
        if self.frameCounter >= len(charr[self.action]):
            self.frameCounter = 0

        if self.dir == 'right':
            img = charr[self.action][int(self.frameCounter)]
        elif self.dir == 'left':
            img = charl[self.action][int(self.frameCounter)]
        pos = img.get_rect()
        pos.center = self.x, self.y #Center anchor
        pygame.draw.rect(win, (0,255,0), pygame.Rect(self.x-50,self.y-50,self.health, 10))
        if self.health < 100:
            pygame.draw.rect(win, (255,0,0), pygame.Rect(self.x-50+self.health,self.y-50,100-self.health,10))
        win.blit(img, pos)

    def move(self, platforms, enemy):
        keys = pygame.key.get_pressed()
        if enemy.damagedEnemy:
            if self.alive:
                self.health -= 5
                if self.health <= 0:
                    self.alive = False
        self.lastY = self.y
        self.damagedEnemy = False
        if keys[K_ESCAPE]:
            pygame.quit() #Causes an error but good enough
        if keys[K_r]:
            self.reset = True
        self.action = 'idle'
        if self.alive:
            if self.jump:
                self.y -= self.jumpVel
                self.jumpVel -= 2
                if self.jumpVel < 0 and not keys[K_DOWN]:
                    for i in platforms:
                        check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                        if check:
                            print('hit')
                            self.jump = False
                            self.y = val-self.height/2
                            self.jumpVel = self.jumpMax
                            break
            if keys[K_UP] and not self.jump:
                self.jump = True
                self.y -= self.jumpVel
                self.action = 'run' #the jump action is bad so yeah
                if self.jumpVel <  -self.jumpMax:
                    self.jumpVel = self.jumpMax
                    self.jump = False
            if keys[K_RIGHT] and not keys[K_LEFT]:
                self.x += playerSpeed
                if self.x > SCREEN_WIDTH:
                    self.x = SCREEN_WIDTH
                self.action = 'run'
                self.dir = 'right'
                for i in platforms:
                    check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                    if not(check) and not(self.jump):
                        self.jump = True
                        self.jumpVel = 0
            if keys[K_LEFT] and not keys[K_RIGHT]:
                self.x -= playerSpeed
                if self.x < 0:
                    self.x = 0
                self.action = 'run'
                self.dir = 'left'
                for i in platforms:
                    check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                    if not(check) and not(self.jump):
                        self.jump = True
                        self.jumpVel = 0
            if keys[K_SPACE]:
                self.action = 'slash'
                #if p2 is in front
                if enemy.x - self.x < 50 and self.dir == 'right' and abs(enemy.y -self.y) < 50:
                    self.damagedEnemy = True
                if self.x - enemy.x < 50 and self.dir == 'left' and abs(enemy.y -self.y) < 50:
                    self.damagedEnemy = True
                
            if keys[K_DOWN] and not self.jump and self.y < 600:
                self.jump = True
                self.jumpVel = 0
                self.y += 50
                self.lastY = self.y
            self.frameCounter += .3
            if self.frameCounter >= 54:
                self.frameCounter = 0
            if self.y > 666: #For some reason down key let them go through floor so idk this fixed it
                    self.y = 666