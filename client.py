import pygame
from network import Network
from random import randint
from player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PATH
from ledge import Platform, Wall
import os
import time

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("NINJA BATTLE")

pygame.init()

font = pygame.font.SysFont('', 68)
smallFont = pygame.font.SysFont('', 24)
chatFont = pygame.font.SysFont('', 18)

bg = [1]
for i in range(0, 54):
    bg.append(pygame.transform.scale(pygame.image.load(PATH+os.path.join('data', 'bg', 'tile'+str(i)+'.png')), (SCREEN_WIDTH, SCREEN_HEIGHT)))


def redrawWindow(win,player, player2, plats, walls):
    win.blit(bg[bg[0]], (0,0))
    bg[0] += 1
    if bg[0] > 54:
        bg[0] = 1
    for i in plats:
        i.draw(win)
    for i in walls:
        i.draw(win)
    player.draw(win)
    player2.draw(win)
    if not player.alive:
            text = font.render("You died", True, (255,0,0))
            pos = text.get_rect()
            pos.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            win.blit(text, pos)
    if player.reset:
        text = smallFont.render('Waiting for other player to reset', True, (255,0,0))
        pos = text.get_rect()
        pos.topright = (SCREEN_WIDTH-10,10)
        win.blit(text, pos)
    elif player2.reset:
        text = smallFont.render('Other player waiting to reset. Press \'R\'', True, (255,0,0))
        pos = text.get_rect()
        pos.topright = (SCREEN_WIDTH-10,10)
        win.blit(text, pos)
    #chat background
    back = pygame.Surface((300,200))
    back.set_alpha(100)
    back.fill((100,100,100))
    win.blit(back, (8,8))
    yloc = 190
    msgs = []
    for i in player.pastMsgs:
        msgs.append([i, 0])
    for i in player2.pastMsgs:
        msgs.append([i, 1])
    msgs.sort(key = lambda x: x[0][1]) #I don't know how this works
    for i in range(len(msgs)-1, -1, -1):
        val = msgs[i]
        if val[1] == 0:
            text = chatFont.render(val[0][0], True, (255,255,255))
        else:
            text = chatFont.render(val[0][0], True, (0,255,0))
        pos = text.get_rect()
        pos.topleft = (10, yloc)
        win.blit(text, pos)
        yloc -= 20
    if player.chatActive:
        text = chatFont.render(player.msg, True, (0,0,0))
        pygame.draw.rect(win, (255,255,255), pygame.Rect(8,206, 300, 20))
        pos = text.get_rect()
        pos.topleft = (10, 208)
        win.blit(text, pos)
    if not player2.alive:
            text = font.render("You Win", True, (0,255,0))
            pos = text.get_rect()
            pos.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            win.blit(text, pos)
    pygame.display.update()

def getPlatforms(x):
    platforms = []
    walls = []
    if x == 1:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(100,SCREEN_HEIGHT-150,200,30, 'plat'),
                    Platform(600,SCREEN_HEIGHT-150,200,30, 'plat')
                    ]
    elif x == 2:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(100,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(600,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(1100,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(350,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(850,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(400,SCREEN_HEIGHT-650,600,30, 'plat')
                    ]
    elif x == 3:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(100,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(1100,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(350,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(850,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(400,SCREEN_HEIGHT-250,600,30, 'plat')
                    ]
    
    elif x == 4:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(200,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(1000,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(50,SCREEN_HEIGHT-250,500,30, 'plat'),
                    Platform(850,SCREEN_HEIGHT-250,500,30, 'plat'),
                    Platform(600,SCREEN_HEIGHT-450,200,30, 'plat')
                    ]
    elif x == 5:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(200,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(1000,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(600,SCREEN_HEIGHT-450,200,30, 'plat'),
                    Platform(0,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(800,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(400,SCREEN_HEIGHT-250,200,30, 'plat'),
                    Platform(1200,SCREEN_HEIGHT-250,200,30, 'plat')
                    ]
    elif x == 6:
        platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'),
                    Platform(150,SCREEN_HEIGHT-200,250,20, 'plat'),
                    Platform(900,SCREEN_HEIGHT-200,250,20, 'plat'),
                    Platform(650,SCREEN_HEIGHT-300,80,20, 'plat'),
                    Platform(150,SCREEN_HEIGHT-400,480,20, 'plat'),
                    Platform(0,SCREEN_HEIGHT-380,150,20, 'plat'),
                    Platform(1150,SCREEN_HEIGHT-300,250,20, 'plat'),
                    Platform(1150,SCREEN_HEIGHT-550,250,20, 'plat'),
                    Platform(600,SCREEN_HEIGHT-550,450,20, 'plat'),
                    Platform(1130,SCREEN_HEIGHT-600,20,20, 'plat'),
                    Platform(-50,SCREEN_HEIGHT-25, SCREEN_WIDTH+100, 100, 'floor'),
                    ]
        walls = [Wall(150,SCREEN_HEIGHT-400,20,200, 'wall1'),
                Wall(1130,SCREEN_HEIGHT-600,20,400, 'wall2'),
                Wall(550,SCREEN_HEIGHT-400,20,200, 'wall1'),
                Wall(730,SCREEN_HEIGHT-550,20,350, 'wall2')
                ]
    elif x == 7:
        platforms = [
                    Platform(0,SCREEN_HEIGHT-300,450,20, 'plat'),
                    Platform(915,SCREEN_HEIGHT-300,450,20, 'plat'),
                    Platform(550,SCREEN_HEIGHT-200,250,20, 'plat'),
                    Platform(620,SCREEN_HEIGHT-530,120,20, 'plat'),
                    Platform(200,SCREEN_HEIGHT-630,250,20, 'plat'),
                    Platform(950,SCREEN_HEIGHT-630,250,20, 'plat'),
                    Platform(670,SCREEN_HEIGHT-600,20,20, 'plat'),
                    ]
        walls = [Wall(670,SCREEN_HEIGHT-600,20,200, 'wall1'),
                Wall(915,SCREEN_HEIGHT-300,20,400, 'wall2'),
                Wall(440,SCREEN_HEIGHT-300,20,400, 'wall1'),
                ]
    elif x == 8:
        platforms = [
                    Platform(600,SCREEN_HEIGHT-100,200,20, 'plat'),
                    Platform(300,SCREEN_HEIGHT-150,200,20, 'plat'),
                    Platform(0,SCREEN_HEIGHT-200,200,20, 'plat'),
                    Platform(900,SCREEN_HEIGHT-150,200,20, 'plat'),
                    Platform(1200,SCREEN_HEIGHT-200,200,20, 'plat'),
                    Platform(550,SCREEN_HEIGHT-400,300,20, 'plat'),
                    Platform(350,SCREEN_HEIGHT-450,100,20, 'plat'),
                    Platform(100,SCREEN_HEIGHT-500,200,20, 'plat'),
                    Platform(950,SCREEN_HEIGHT-450,100,20, 'plat'),
                    Platform(1100,SCREEN_HEIGHT-500,200,20, 'plat'),
                    ]
        walls = [
                ]
    elif x == 9:
        platforms = [
                Platform(400,SCREEN_HEIGHT-200,550,20, 'plat'),
                Platform(400,SCREEN_HEIGHT-400,200,20, 'plat'),
                Platform(770,SCREEN_HEIGHT-400,200,20, 'plat'),
                Platform(580,SCREEN_HEIGHT-600,20,20, 'plat'),
                Platform(770,SCREEN_HEIGHT-600,20,20, 'plat'),
                Platform(100,SCREEN_HEIGHT-300,200,20, 'plat'),
                Platform(1100,SCREEN_HEIGHT-300,200,20, 'plat'),
                ]

        walls = [
            Wall(400,SCREEN_HEIGHT-400,20,400, 'wall1'),
            Wall(950,SCREEN_HEIGHT-400,20,400, 'wall2'),
            Wall(580,SCREEN_HEIGHT-600,20,200, 'wall1'),
            Wall(770,SCREEN_HEIGHT-600,20,200, 'wall2'),
                ]
    
    return platforms, walls
def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    platforms, walls = getPlatforms(randint(1,6))
    counter = 0

    while run:
        clock.tick(80)
        counter += 1
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if p.chatActive:
                if event.type == pygame.KEYDOWN:
                    if event.key != 13:
                        if event.key == 8: #backspace
                            p.msg = p.msg[0:-1]
                        else:
                            p.msg = p.msg + chr(event.key)

        p.move(platforms, walls, p2)
        if counter < 200:
            platforms, walls = getPlatforms(p.platLayout)
        redrawWindow(win, p, p2, platforms, walls)

main()