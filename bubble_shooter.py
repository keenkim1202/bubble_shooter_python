# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# 발사대 겨냥 ( 방향키로 움직이기 )
import os, random, math
import pygame
from pygame import image

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position = (0, 0)):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18 # 발사속도

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle) # 호도법으로 변경한 값
    
    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1 # 방향을 위로 하기 위해서 -1 곱해주기.

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, angle):
        self.angle += angle

        # 각도의 최소 최대값 고정
        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        # 원본 이미지를 변하는 각도정보를 반영하여 original 이미지를 업데이트해준다.
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        # image의 중심 좌표를 고정하여 center를 기준으로 회전되도록.
        self.rect = self.image.get_rect(center = self.position)

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
        return bubble_images[-1]

# 쏠 버블에 대한 준비를 하는 함수
def prepare_bubbles():
    global curr_bubble
    curr_bubble = create_bubble() # 새 버블 생성 함수
    curr_bubble.set_rect((screen_width // 2, 624))

# 발사할 버블 랜덤으로 생성하는 함수
def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

# 랜덤으로 버블의 색을 골라주는 함수
def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    return random.choice(colors)

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

# 발사대 이미지 불러오기
pointer_image = pygame.image.load(os.path.join(current_path, "./images/pointer.png")) 
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62

# 화살표 관련 변수
# to_angle = 0 # 좌우 각도 정보
# 키 이벤트가 들어오는 속도가 빠를 때를 대응하기 위해서 좌우의 각도 변수를 나눈다.
to_angle_left = 0 # 좌측 각도 정보
to_angle_right = 0 # 우측 각도 정보
angle_speed = 1.5 # 1.5도씩 움직이게 된다.

curr_bubble = None # 이번에 쏠 버블
fire = False # 발사 여부 (현재 버블이 발사 중이면 발사되지 않도록하기 위해서.)

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

            # 방향키에 따른 이벤트 생성
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 좌측키 -> 화살표 각도가 점점 증가함.
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT: # 우측키 -> 화살표 각도가 점점 감소함.
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE: # 스페이스 -> 버블 발사
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)
        
        # 위를 눌렀을 떄는 화살표의 이동이 멈춰야 하는 부분 설정.
        if event.type == pygame.KEYUP:
            # 좌측 혹은 우측 방향키에서 손을 때었을 때
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not curr_bubble:
        prepare_bubbles()

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right) # 발사대의 자연스러운 움직임을 위해서
    pointer.draw(screen)

    if curr_bubble:
        if fire:
            curr_bubble.move() # 발사상태면 버블이 이동하도록.
        curr_bubble.draw(screen)

        if curr_bubble.rect.top <= 0: # 발사한 버블이 꼭대기에 닿으면 없어지고 새로운 버블이 생기도록.
            curr_bubble = None
            fire = False
            
    pygame.display.update()

pygame.quit()