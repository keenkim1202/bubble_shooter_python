# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# 게임 화면 설정
import pygame

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

running = True # running이 true일 동안은 계속 게임이 실행

while running:
    clock.tick(60) # FPS 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()