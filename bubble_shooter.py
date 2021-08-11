# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# 발사대( 화살표 ) 생성
import os
import pygame
from pygame import image

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

    # 버블 만들어 넣기.
    # map에 문자열을 넣어줬으므로 2중for문으로 2차원으로 순회
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]: # 버블이 없어야 하는 원소이면 continue.
                continue
                
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))

# 버블의 위치 정보를 구하는 함수
def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)

    # 짝수번쨰 줄은 홀수본째 줄보다 약간 치우져 있는 모양이므로, CELL_SIZE의 반만큼 옮겨준다.
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2
    return pos_x, pos_y

# 버블의 색에 맞는 이미지 정보를 구하는 함수
def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[-1] # -1을 넣어주면 list의 가장 마지막 원소를 의미한다.
    

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "./images/background.png"))

# 버블 이미지 불러오기
bubble_images = [
    pygame.image.load(os.path.join(current_path, "./images/red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/black.png")).convert_alpha()
]

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
map = [] # 게임 맵
bubble_group = pygame.sprite.Group()

# 함수 호출
setup()

running = True # running이 true일 동안은 계속 게임이 실행

while running:
    clock.tick(60) # FPS 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    bubble_group.draw(screen) # bubble_group의 모든 원소를 screen에 그려준다.
    pygame.display.update()

pygame.quit()