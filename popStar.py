# -*- coding: gbk -*-

import sys
import time
import pygame
from pygame.locals import *
import pygame.font

from star import Star, StarArray
from const import *
from data import level_score_data as LSD

pygame.init()
gameClock = pygame.time.Clock()
gameSurface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.display.set_caption("PopStar")

starArray = StarArray()

gameSurface.fill((0,0,0))
for starList in starArray:
    for star in starList:
        position = star.getPosition()
        top = SCREEN_SIZE_Y - (position[1] + 1) * STAR_SIZE + 2
        left = SCREEN_SIZE_X - (position[0] + 1) * STAR_SIZE + 2 - (SCREEN_SIZE_X - STAR_NUM * STAR_SIZE) / 2
        rect = pygame.Rect(left, top, STAR_SIZE-2, STAR_SIZE-2)
        color = star.getColor()
        pygame.draw.rect(gameSurface, color, rect)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            pressedArray = pygame.mouse.get_pressed()
            if pressedArray[0]:
                pos = pygame.mouse.get_pos()
                indexX = (SCREEN_SIZE_X - (SCREEN_SIZE_X - STAR_NUM * STAR_SIZE) / 2 - pos[0]) / STAR_SIZE
                indexY = (SCREEN_SIZE_Y - pos[1]) / STAR_SIZE
                if indexX < len(starArray) and indexY < len(starArray[indexX]):
                    star = starArray[indexX][indexY]
                    if star.state == STAR_STATE_ACTIVATED:
                        starArray.popStar()
                    else:
                        starArray.clearActivatedStars()
                        starArray.activateStars(star)
        gameSurface.fill((0,0,0))
        for starList in starArray:
            for star in starList:
                position = star.getPosition()
                top = SCREEN_SIZE_Y - (position[1] + 1) * STAR_SIZE + 2
                left = SCREEN_SIZE_X - (position[0] + 1) * STAR_SIZE + 2 - (SCREEN_SIZE_X - STAR_NUM * STAR_SIZE) / 2
                rect = pygame.Rect(left, top, STAR_SIZE-2, STAR_SIZE-2)
                color = star.getColor() if star.state == STAR_STATE_INIT else (255,255,255)
                pygame.draw.rect(gameSurface, color, rect)

        font = pygame.font.Font("res/STXINGKA.TTF", 40)
        textSurface=font.render(str(starArray.score), True, (255, 0, 0))
        gameSurface.blit(textSurface, (50,60))
        textSurface=font.render("Goal: "+str(LSD.data.get(starArray.level, 99999)), True, (255, 0, 0))
        gameSurface.blit(textSurface, (50,20))
        if starArray.isFinish:
            textSurface = font.render("GAME OVER!", True, (255, 255, 255))
            gameSurface.blit(textSurface, (100, 100))

        pygame.display.update()
