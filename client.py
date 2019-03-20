import pygame
from network import Network
from player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PATH
from ledge import Platform
import os

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NINJA BATTLE")

pygame.init()

font = pygame.font.SysFont('', 68)
smallFont = pygame.font.SysFont('', 24)
chatFont = pygame.font.SysFont('', 18)

bg = [1]
for i in range(0, 54):
    bg.append(pygame.transform.scale(pygame.image.load(PATH+os.path.join('data', 'bg', 'tile'+str(i)+'.png')), (SCREEN_WIDTH, SCREEN_HEIGHT)))


def redrawWindow(win,player, player2, plats):
    win.blit(bg[bg[0]], (0,0))
    bg[0] += 1
    if bg[0] > 54:
        bg[0] = 1
    for i in plats:
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
            text = chatFont.render(val[0][0], True, (255,0,0))
        pos = text.get_rect()
        pos.topleft = (10, yloc)
        win.blit(text, pos)
        yloc -= 20

    '''
    for i in player.pastMsgs:
        text = chatFont.render(i[0], True, (255,255,255))
        pos = text.get_rect()
        pos.topleft = (10,yloc)
        yloc += 20
        win.blit(text, pos)
    for i in player2.pastMsgs:
        text = chatFont.render(i[0], True, (255,100,100))
        pos = text.get_rect()
        pos.topleft = (10,yloc)
        yloc += 20
        win.blit(text, pos)
    '''
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


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'), 
                Platform(100,SCREEN_HEIGHT-150,200,30, 'plat'),
                Platform(600,SCREEN_HEIGHT-150,200,30, 'plat')
                ]

    while run:
        clock.tick(60)
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

        p.move(platforms, p2)
        redrawWindow(win, p, p2, platforms)

main()