# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# ���� ȭ�� ����
import os
import pygame

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

# ��� �̹��� �ҷ�����
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "./images/background.png"))

running = True # running�� true�� ������ ��� ������ ����

while running:
    clock.tick(60) # FPS 60���� ����

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.update()

pygame.quit()