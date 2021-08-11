# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# 버블 이미지 설정 / map 설정
import os
import pygame

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

# 맵 만들기
# / : 버블이 들어갈 수 없는 공간을 의미.
# . : 비어있는 공간.
def setup():
    global map
    map = [
        list("RRYYBBGG"),
        list("RRYYBBG/"),
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")
    ]

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "./images/background.png"))

running = True # running이 true일 동안은 계속 게임이 실행

while running:
    clock.tick(60) # FPS 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.update()

pygame.quit()