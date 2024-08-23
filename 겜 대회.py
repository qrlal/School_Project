import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isometric Tilemap Game")

# FPS 설정
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 타일맵 설정
tile_width = 40 # →→→
tile_height = 20 # ↓↓↓
map_width = 10 # ↘↘↘
map_height = 10 # ↙↙↙

# 타일맵 예시 데이터
tilemap = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Y축 오프셋 상수
Y_OFFSET = 100  # 이 값을 조정하여 타일을 아래로 이동시킬 수 있음

# 카르테시안 좌표를 아이소메트릭 좌표로 변환
def cart_to_iso(cart_x, cart_y, tile_width, tile_height):
    iso_x = (cart_x - cart_y) * (tile_width // 2)
    iso_y = (cart_x + cart_y) * (tile_height // 2)
    return iso_x, iso_y

# 타일 그리기 함수
def draw_tile(screen, x, y, tile_width, tile_height, color):
    points = [
        (x, y),
        (x + tile_width // 2, y + tile_height // 2),
        (x, y + tile_height),
        (x - tile_width // 2, y + tile_height // 2)
    ]
    pygame.draw.polygon(screen, color, points)

# 격자 그리기 함수
def draw_grid(screen, map_width, map_height, tile_width, tile_height):
    for row in range(map_width):
        for col in range(map_height):
            iso_x, iso_y = cart_to_iso(col, row, tile_width, tile_height)
            # 중심점 보정 및 Y축 위치 조정
            iso_x += WIDTH // 2
            iso_y += HEIGHT // 4 + Y_OFFSET  # 타일을 아래로 Y_OFFSET만큼 내림
            points = [
                (iso_x, iso_y),
                (iso_x + tile_width // 2, iso_y + tile_height // 2),
                (iso_x, iso_y + tile_height),
                (iso_x - tile_width // 2, iso_y + tile_height // 2)
            ]
            pygame.draw.polygon(screen, BLACK, points, 1)  # 검은색 선으로 격자 그리기

# 타일맵 그리기 함수
def draw_tilemap(screen, tilemap, map_width, map_height, tile_width, tile_height):
    for row in range(map_height):
        for col in range(map_width):
            iso_x, iso_y = cart_to_iso(col, row, tile_width, tile_height)
            # 중심점 보정 및 Y축 위치 조정
            iso_x += WIDTH // 2
            iso_y += HEIGHT // 4 + Y_OFFSET  # 타일을 아래로 Y_OFFSET만큼 내림
            color = GREEN if tilemap[row][col] == 1 else GRAY
            draw_tile(screen, iso_x, iso_y, tile_width, tile_height, color)

# 플레이어 그리기 함수
def draw_player(screen, player_pos, tile_width, tile_height):
    # 타일의 중앙에 정육면체를 그리기 위해 좌표 계산
    iso_x, iso_y = cart_to_iso(player_pos[0], player_pos[1], tile_width, tile_height)
    iso_x += WIDTH // 2
    iso_y += HEIGHT // 4 + Y_OFFSET
    iso_player_pos = (iso_x, iso_y)
    # 정육면체의 각 꼭짓점 좌표 계산 (정확한 중심점을 기준으로)
    top = (iso_x, iso_y - tile_height)  # 윗면 중앙점
    front_left = (iso_x - tile_width // 2, iso_y - tile_height//2)  # 앞면 좌측 하단
    front_right = (iso_x + tile_width // 2, iso_y - tile_height//2)  # 앞면 우측 하단
    back_left = (iso_x - tile_width // 2, iso_y + tile_height//2)  # 후면 좌측 하단
    back_right = (iso_x + tile_width // 2, iso_y + tile_height//2)  # 후면 우측 하단
    bottom = (iso_x, iso_y + tile_height)  # 아랫면 중앙점

    pygame.draw.polygon(screen, RED, [top, front_left, back_left, bottom, back_right, front_right])
    pygame.draw.polygon(screen, BLACK, [top, front_left, iso_player_pos, front_right], 1)
    pygame.draw.line(screen, BLACK, iso_player_pos, bottom, 1)
    pygame.draw.line(screen, BLACK, front_left, back_left, 1)
    pygame.draw.line(screen, BLACK, front_right, back_right, 1)
    pygame.draw.line(screen, BLACK, back_left, bottom, 1)
    pygame.draw.line(screen, BLACK, bottom, back_right, 1)


# 플레이어 초기 위치
player_pos = [0, 9]

# 메인 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_pos[0] != 0:
                player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and player_pos[0] != 9:
                player_pos[0] += 1
            elif event.key == pygame.K_UP and player_pos[1] != 0:
                player_pos[1] -= 1
            elif event.key == pygame.K_DOWN and player_pos[1] != 9:
                player_pos[1] += 1

    screen.fill(WHITE)

    # 타일맵 그리기
    draw_tilemap(screen, tilemap, map_width, map_height, tile_width, tile_height)

    # 격자 그리기
    draw_grid(screen, map_width, map_height, tile_width, tile_height)

    # 플레이어 그리기
    if player_pos[0] >= map_width or player_pos[1] >= map_height:
        print("플레이어 위치 맵 벗어남")
        break
    draw_player(screen, player_pos, tile_width, tile_height)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
