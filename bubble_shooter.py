# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# ���� ȭ�� ����
import pygame

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

running = True # running�� true�� ������ ��� ������ ����

while running:
    clock.tick(60) # FPS 60���� ����

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()