import pygame
from network import Network
from player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from ledge import Platform

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    platforms = [Platform(-50,SCREEN_HEIGHT-50, SCREEN_WIDTH+100, 100, 'floor'), 
                Platform(100,SCREEN_HEIGHT-200,200,30, 'plat'),
                Platform(100,SCREEN_HEIGHT-400,200,30, 'plat'),
                Platform(400, SCREEN_HEIGHT-600, 200, 30, 'plat')
                ]

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move(platforms)
        redrawWindow(win, p, p2)

main()