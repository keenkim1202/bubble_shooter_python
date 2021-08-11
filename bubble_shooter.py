# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# ���� ��Ʈ����
import os, random, math
import pygame
from pygame import image

# ���� Ŭ���� ����
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position = (0, 0),  row_idx = -1, col_idx = -1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18 # �߻�ӵ�
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle) # ȣ�������� ������ ��
    
    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

    # current bubble�� �浹�ؼ� ��� ��ġ�� ���� ��, ���� �������� ��� ��ġ�� �־��־������ �� �� �ִ�.
    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

# �߻�� Ŭ���� ����
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

        # ������ �ּ� �ִ밪 ����
        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.position)

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
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
                
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))

# ������ ��ġ ������ ���ϴ� �Լ�
def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)

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
        return bubble_images[-1]

# �� ���� ���� �غ� �ϴ� �Լ�
def prepare_bubbles():
    global curr_bubble, next_bubble

    if next_bubble:
        curr_bubble = next_bubble
    else:
        curr_bubble = create_bubble()

    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

# �߻��� ���� �������� �����ϴ� �Լ�
def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

# �������� ������ ���� ����ִ� �Լ�
def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    return random.choice(colors)

# �浹 ó�� �Լ�
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

# �ʿ����� ��ġ������ �������� �Լ�
def get_map_index(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE

    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2)) // CELL_SIZE

        if col_idx < 0: # ������ ȭ���� ���� ��� ���¿��� �浹�� ���.
            col_idx = 0
        elif col_idx > MAP_COL_COUNT - 2:
            col_idx = MAP_COL_COUNT - 2

    return row_idx, col_idx

# ��ġ������ �������� ������ ��ġ�ϴ� �Լ�
def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)

# dfs�� �̿��Ͽ� ���� ���� ������� ������ ���� ��Ʈ����!
def remove_adjacent_bubbles(row_idx, col_idx, color):
    visited.clear()
    visit(row_idx, col_idx, color)
    # ���ӵ� ������ 3�� �̻��̸� ���ֱ�
    if len(visited) >= 3:
        remove_visited_bubbles()
        remove_hanging_bubbles()

def visit(row_idx, col_idx, color = None):
    # ���� ������ ������� Ȯ��
    if row_idx < 0 or row_idx >= MAP_ROW_COUNT or col_idx < 0 or col_idx >= MAP_COL_COUNT:
        return
    # ���� cell�� ������ color�� ������ Ȯ��
    if color and map[row_idx][col_idx] != color:
        return
    # ������ �� �����̰ų�, ������ �� ���� ��ġ���� Ȯ�� -> �湮���� ����
    if map[row_idx][col_idx] in [".", "/"]:
        return
    # �̹� �湮 ���θ� Ȯ��
    if (row_idx, col_idx) in visited:
        return
    #  �湮 ó��
    visited.append((row_idx, col_idx))

    # ���� ��ġ�� �������� �湮 ������ ��ǥ ����
    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]

    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]
    
    for i in range(len(rows)):
        visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
    # ����� �߿��� �湮�� �� ��ġ�� �Ȱ��� ��ġ(row_idx, col_idx)�� �ִ� ���� �����ָ� �ȴ�.
    # bubble group�� row_idx�� col_idx�� visited�� �ִ� �͵��� �����´�.
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

# �湮���� ���� ����, �� ���߿� ���δ� ������� �����
def remove_not_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)
    
# ������ ���� �پ��ִ� ���� ���ֱ�. (õ��� ����Ǿ����� �ʰ� ���ִ� ����� ó��)
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

# �߻�� �̹��� �ҷ�����
pointer_image = pygame.image.load(os.path.join(current_path, "./images/pointer.png")) 
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

# ���� ���� ����
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
MAP_ROW_COUNT = 11
MAP_COL_COUNT = 8

# ȭ��ǥ ���� ����
to_angle_left = 0 # ���� ���� ����
to_angle_right = 0 # ���� ���� ����
angle_speed = 1.5 # 1.5���� �����̰� �ȴ�.

curr_bubble = None # �̹��� �� ����
next_bubble = None # ������ �� ����
fire = False # �߻� ���� (���� ������ �߻� ���̸� �߻���� �ʵ����ϱ� ���ؼ�.)

map = [] # ���� ��
visited = []
bubble_group = pygame.sprite.Group()

# �Լ� ȣ��
setup()

# ���� ���� ����
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ����Ű�� ���� �̺�Ʈ ����
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # ȭ��ǥ ���� ����
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT: # ȭ��ǥ ���� ����
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE: # ���� �߻�
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)
        
        # ���� ������ ���� ȭ��ǥ�� �̵��� ����� �ϴ� �κ� ����
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
    pointer.rotate(to_angle_left + to_angle_right) # �߻���� �ڿ������� �������� ���ؼ�
    pointer.draw(screen)

    if curr_bubble:
        if fire:
            curr_bubble.move() # �߻���¸� ������ �̵��ϵ���.
        curr_bubble.draw(screen)

    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()