import pygame
import time
from random import randint
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_ESCAPE, \
                            MOUSEBUTTONUP, QUIT, K_r, K_t, K_RETURN
import os
from config import PATH, SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
def loadSprite2(folder, amt, char, col): #Left images, flips them
    for i in range(0, amt):
        img = pygame.transform.flip(pygame.image.load(PATH +
                                os.path.join('data', 'char', col, folder, 'tile00' + str(i)+'.png')), True, False)
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (int(SIZE * w), int(SIZE * h)))
        char[folder].append(img)

def loadSprite(folder, amt, char, col): #Right images
    for i in range(0, amt):
        img = pygame.image.load(PATH +
                                os.path.join('data', 'char', col, folder, 'tile00' + str(i)+'.png'))
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (int(SIZE * w), int(SIZE * h)))
        char[folder].append(img)

def loadR(char, col):
    loadSprite('death', 4, char, col)
    loadSprite('hurt', 5, char, col)
    loadSprite('idle', 4, char, col)
  #  loadSprite('longJump', 8, char, col)
  #  loadSprite('quickJump', 4, char, col)
    loadSprite('run', 3, char, col)
    loadSprite('slash', 4, char, col)
  #  loadSprite('sneak', 6, char, col)
  #  loadSprite('throw', 5, char, col)

def loadL(char, col):
    loadSprite2('death', 4, char, col)
    loadSprite2('hurt', 5, char, col)
    loadSprite2('idle', 4, char, col)
   # loadSprite2('longJump', 8, char, col)
   # loadSprite2('quickJump', 4, char, col)
    loadSprite2('run', 3, char, col)
    loadSprite2('slash', 4, char, col)
   # loadSprite2('sneak', 6, char, col)
   # loadSprite2('throw', 5, char, col)

rcharr = {
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

rcharl = {
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

bcharr = {
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

bcharl = {
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

loadR(rcharr, 'red')
loadL(rcharl, 'red')

loadR(bcharr, 'blue')
loadL(bcharl, 'blue')

rcolors = {
            'red': rcharr,
            'blue': bcharr
}
lcolors = {
            'red': rcharl,
            'blue': bcharl
}

width, height = rcharr['run'][0].get_rect().size

playerSpeed = 10

class Player:
    def __init__(self, num):
        if num == 0:
            self.x = SCREEN_WIDTH/2-200
            self.col = 'red'
        else:
            self.x = SCREEN_WIDTH/2+200
            self.col = 'blue'
        self.y = SCREEN_HEIGHT-700
        self.alive = True
        self.id = num
        self.health = 100
        self.platLayout = randint(1,6)
        self.damagedEnemy = False
        self.lastY = self.y
        self.height = height
        self.width = width
        self.frameCounter = 0
        self.dir = 'right'
        self.action = 'idle'
        self.lastAction = 'idle' #used to detect a change in action
        
        self.jumpMax = 30
        self.jumpVel = self.jumpMax 
        self.jump = False
        self.canJump2 = True
        self.doubleJumpMax = 10
        self.doubleJumpDelay = self.doubleJumpMax

        self.reset = False

        self.knocked = False
        self.knockedVelMax = 6
        self.knockedVel = self.knockedVelMax
        self.knockedDir = ''
        self.knockXVel = 16

        self.chatActive = False
        self.msg = ''
        self.pastMsgs = []
    def resetVals(self):
        self.__init__(self.id)
        time.sleep(.2) #So it doesn't immediately register another press of r
    def draw(self, win):
        if self.action == self.lastAction:
            self.frameCounter += .1
        else:
            self.frameCounter = 0
            self.lastAction = self.action
        if self.frameCounter >= len(rcharr[self.action]):
            self.frameCounter = 0

        if self.dir == 'right':
            img = rcolors[self.col][self.action][int(self.frameCounter)]
        elif self.dir == 'left':
            img = lcolors[self.col][self.action][int(self.frameCounter)]
        pos = img.get_rect()
        pos.center = self.x, self.y #Center anchor
        pygame.draw.rect(win, (0,255,0), pygame.Rect(self.x-50,self.y-50,self.health, 10))
        if self.health < 100:
            pygame.draw.rect(win, (255,0,0), pygame.Rect(self.x-50+self.health,self.y-50,100-self.health,10))
        win.blit(img, pos)

    def move(self, platforms, walls, enemy):
        keys = pygame.key.get_pressed()
        if self.knocked:
            self.y -= self.knockedVel
            self.knockedVel -= 1
            if self.knockedVel < -self.knockedVelMax:
                self.knocked = False
                self.knockedVel = self.knockedVelMax
        if not enemy.platLayout == self.platLayout:
            x = randint(0,10)
            if x == 1:
                self.platLayout = enemy.platLayout
        if enemy.reset and self.reset:
            self.resetVals()
            self.platLayout = randint(1,6)
        if enemy.damagedEnemy: 
            if self.alive:
                self.health -= 1
                if not self.knocked:
                    self.knocked = True
                    if enemy.x < self.x:
                        self.knockedDir = 'right'
                    else:
                        self.knockedDir = 'left'
                    self.jump = True
                if self.health <= 0:
                    self.alive = False
        self.lastY = self.y
        self.damagedEnemy = False
        if keys[K_ESCAPE]:
            pygame.quit() #Causes an error but good enough
        if keys[K_r] and not self.chatActive:
            self.reset = True
        self.action = 'idle'
        if keys[K_RETURN] and self.chatActive and len(self.msg) > 1:
            self.pastMsgs.append([self.msg, time.time()])
            self.chatActive = False
            self.msg = ''
        if keys[K_t] and not self.chatActive:
            self.chatActive = True
            
        if self.alive:
            if self.jump: 
                self.doubleJumpDelay -= 1
                if self.knockedDir == 'right':    
                    self.x += self.knockXVel
                    for i in walls:
                        if i.hit(self.x, self.y):
                            self.x -= self.knockXVel
                            break
                if self.knockedDir == 'left':
                    self.x -= self.knockXVel
                    for i in walls:
                        if i.hit(self.x, self.y):
                            self.x += self.knockXVel
                            break
                self.y -= self.jumpVel
                self.jumpVel -= 2
                if self.jumpVel < 0 and not keys[K_DOWN]:
                    for i in platforms:
                        check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                        if check:
                            self.jump = False
                            self.canJump2 = True
                            self.y = val-self.height/2
                            self.jumpVel = self.jumpMax
                            break
            else:
                self.knockedDir = ''
                self.canJump2 = True
            if keys[K_UP] and not self.jump: #Single jump
                self.jump = True
                self.action = 'run' #the jump action is bad so yeah
                self.doubleJumpDelay = self.doubleJumpMax
            elif keys[K_UP] and self.canJump2 and self.doubleJumpDelay <= 0: #double jump
                self.jump = True
                self.jumpVel = self.jumpMax
                self.knockedDir = ''
                self.canJump2 = False
                self.doubleJumpDelay = self.doubleJumpMax
                self.action = 'run'
            if keys[K_RIGHT] and not keys[K_LEFT]:
                self.x += playerSpeed
                self.action = 'run'
                self.dir = 'right'
                for i in platforms:
                    check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                    if not(check) and not(self.jump):
                        self.jump = True
                        self.jumpVel = 0
                for i in walls:
                    if i.hit(self.x, self.y):
                        self.x -= playerSpeed
                        break
            if keys[K_LEFT] and not keys[K_RIGHT]:
                self.x -= playerSpeed
                self.action = 'run'
                self.dir = 'left'
                for i in platforms:
                    check, val = i.hit(self.x, self.y+self.height/2-10, self.lastY)
                    if not(check) and not(self.jump):
                        self.jump = True
                        self.jumpVel = 0
                for i in walls:
                    if i.hit(self.x, self.y):
                        self.x += playerSpeed
                        break
            if keys[K_SPACE] and not self.chatActive:
                self.action = 'slash'
                #if p2 is in front
                if 0 <  enemy.x - self.x < 75 and abs(enemy.y-self.y) < 50 and self.dir == 'right':
                    self.damagedEnemy = True
                if 0 <  self.x - enemy.x < 75 and abs(enemy.y-self.y) < 50 and self.dir == 'left':
                    self.damagedEnemy = True
                
            if keys[K_DOWN] and not self.jump and self.y < 600:
                self.jump = True
                self.jumpVel = 0
                self.y += 50
                self.lastY = self.y
            self.frameCounter += .3
            if self.frameCounter >= 54:
                self.frameCounter = 0
            if self.y > 1000: #For some reason down key let them go through floor so idk this fixed it
                    self.alive = False
                    self. y = 1000