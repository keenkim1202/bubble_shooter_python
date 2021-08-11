# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# 버블 터트리기
import os, random, math
import pygame
from pygame import image

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position = (0, 0),  row_idx = -1, col_idx = -1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18 # 발사속도
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle) # 호도법으로 변경한 값
    
    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

    # current bubble이 충돌해서 어느 위치에 들어갔을 때, 맵을 기준으로 어느 위치에 넣어주어야할지 알 수 있다.
    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

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

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
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
            if col in [".", "/"]:
                continue
                
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))

# 버블의 위치 정보를 구하는 함수
def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)

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
    global curr_bubble, next_bubble

    if next_bubble:
        curr_bubble = next_bubble
    else:
        curr_bubble = create_bubble()

    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

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

# 충돌 처리 함수
def process_collision():
    global curr_bubble, fire
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)

    if hit_bubble or curr_bubble.rect.top <= 0:
        row_idx, col_idx = get_map_index(*curr_bubble.rect.center) # (x, y)
        print(row_idx, col_idx)
        place_bubble(curr_bubble, row_idx, col_idx)
        remove_adjacent_bubbles(row_idx, col_idx, curr_bubble.color)
        curr_bubble = None
        fire = False

# 맵에서의 위치정보를 가져오는 함수
def get_map_index(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE

    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2)) // CELL_SIZE

        if col_idx < 0: # 버블이 화면을 조금 벗어난 상태에서 충돌한 경우.
            col_idx = 0
        elif col_idx > MAP_COL_COUNT - 2:
            col_idx = MAP_COL_COUNT - 2

    return row_idx, col_idx

# 위치정보를 바탕으로 버블을 배치하는 함수
def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)

# dfs를 이용하여 같은 색깔 버블들의 개수를 세어 터트리기!
def remove_adjacent_bubbles(row_idx, col_idx, color):
    visited.clear()
    visit(row_idx, col_idx, color)
    # 연속된 버블이 3개 이상이면 없애기
    if len(visited) >= 3:
        remove_visited_bubbles()
        remove_hanging_bubbles()

def visit(row_idx, col_idx, color = None):
    # 맵의 범위를 벗어는지 확인
    if row_idx < 0 or row_idx >= MAP_ROW_COUNT or col_idx < 0 or col_idx >= MAP_COL_COUNT:
        return
    # 현재 cell의 색상이 color와 같은지 확인
    if color and map[row_idx][col_idx] != color:
        return
    # 버블이 빈 공간이거나, 존재할 수 없는 위치인지 확인 -> 방문하지 않음
    if map[row_idx][col_idx] in [".", "/"]:
        return
    # 이미 방문 여부를 확인
    if (row_idx, col_idx) in visited:
        return
    #  방문 처리
    visited.append((row_idx, col_idx))

    # 현재 위치를 기준으로 방문 가능한 좌표 정보
    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]

    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]
    
    for i in range(len(rows)):
        visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
    # 버블들 중에서 방문한 곳 위치와 똑같은 위치(row_idx, col_idx)에 있는 버블만 지워주면 된다.
    # bubble group중 row_idx와 col_idx가 visited에 있는 것들을 가져온다.
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

# 방문하지 않은 버블, 즉 공중에 떠인는 버블들을 지우기
def remove_not_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)
    
# 지워진 버블에 붙어있던 버블 없애기. (천장과 연결되어있지 않고 떠있는 버블들 처리)
def remove_hanging_bubbles():
    visited.clear()
    for col_idx in range(MAP_COL_COUNT):
        if map[0][col_idx] != ".":
            visit(0, col_idx)
    remove_not_visited_bubbles()

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
MAP_ROW_COUNT = 11
MAP_COL_COUNT = 8

# 화살표 관련 변수
to_angle_left = 0 # 좌측 각도 정보
to_angle_right = 0 # 우측 각도 정보
angle_speed = 1.5 # 1.5도씩 움직이게 된다.

curr_bubble = None # 이번에 쏠 버블
next_bubble = None # 다음에 쏠 버블
fire = False # 발사 여부 (현재 버블이 발사 중이면 발사되지 않도록하기 위해서.)

map = [] # 게임 맵
visited = []
bubble_group = pygame.sprite.Group()

# 함수 호출
setup()

# 게임 실행 관련
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 방향키에 따른 이벤트 생성
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 화살표 각도 증가
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT: # 화살표 각도 감소
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE: # 버블 발사
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)
        
        # 위를 눌렀을 떄는 화살표의 이동이 멈춰야 하는 부분 설정
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not curr_bubble:
        prepare_bubbles()

    if fire:
        process_collision()

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right) # 발사대의 자연스러운 움직임을 위해서
    pointer.draw(screen)

    if curr_bubble:
        if fire:
            curr_bubble.move() # 발사상태면 버블이 이동하도록.
        curr_bubble.draw(screen)

    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()