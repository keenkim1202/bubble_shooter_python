# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# �߻��( ȭ��ǥ ) ����
import os
import pygame
from pygame import image

# ���� Ŭ���� ����
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

# �߻�� Ŭ���� ����
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# �� �����
# / : ������ �� �� ���� ������ �ǹ�.
# . : ����ִ� ����.
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

    # ���� ����� �ֱ�.
    # map�� ���ڿ��� �־������Ƿ� 2��for������ 2�������� ��ȸ
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]: # ������ ����� �ϴ� �����̸� continue.
                continue
                
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))

# ������ ��ġ ������ ���ϴ� �Լ�
def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)

    # ¦������ ���� Ȧ����° �ٺ��� �ణ ġ���� �ִ� ����̹Ƿ�, CELL_SIZE�� �ݸ�ŭ �Ű��ش�.
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2
    return pos_x, pos_y

# ������ ���� �´� �̹��� ������ ���ϴ� �Լ�
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
        return bubble_images[-1] # -1�� �־��ָ� list�� ���� ������ ���Ҹ� �ǹ��Ѵ�.
    

pygame.init()

screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Puzzle Bubble")

clock = pygame.time.Clock()

# ��� �̹��� �ҷ�����
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "./images/background.png"))

# ���� �̹��� �ҷ�����
bubble_images = [
    pygame.image.load(os.path.join(current_path, "./images/red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "./images/black.png")).convert_alpha()
]

# ���� ���� ����
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
map = [] # ���� ��
bubble_group = pygame.sprite.Group()

# �Լ� ȣ��
setup()

running = True # running�� true�� ������ ��� ������ ����

while running:
    clock.tick(60) # FPS 60���� ����

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    bubble_group.draw(screen) # bubble_group�� ��� ���Ҹ� screen�� �׷��ش�.
    pygame.display.update()

pygame.quit()