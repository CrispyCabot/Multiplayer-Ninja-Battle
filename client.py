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

        p.move(platforms, p2)
        redrawWindow(win, p, p2, platforms)

main()