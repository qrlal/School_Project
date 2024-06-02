import math
import pygame
import sys
import pyautogui
import keyboard
import random

class Vector2D:   # 2차원 벡터 클래스 정의
    def __init__(self,x,y):
        self._x=x
        self._y=y
    def __str__(self): # 벡터 출력 형식
        return '({},{})'.format(self._x, self._y)
    def add(self, other):  # 벡터의 더하기 구현
        return Vector2D(self._x + other._x, self._y+other._y)
    def __sub__(self,other):  # 벡터의 뺼셈 구현
        return Vector2D(self._x - other._x, self._y-other._y)
    def __mul__(self,other):  #벡터의 곱셈 구현
        return Vector2D(self._x * other._x, self._y*other._y)
    def norm(self) :  # 벡터의 정규화
        magnitude = math.sqrt((self._x)**2 + (self._y)**2)  # 벡터의 크기
        if magnitude == 0:
            return Vector2D(1, 1)
        return Vector2D(self._x / magnitude, self._y /magnitude)  # x,y를 벡터의 크기로 나눠서 크기가 1인 벡터로 정규화

def ball2_ap() :
    rd_x = random.randint(0, 1800)
    rd_y = random.randint(0, 800)
    return {"position" : Vector2D(rd_x,rd_y), "r" : 10, "col" : blue}

screen_width = 1800
screen_height = 800
scren_start = [60, 140]  # pygame 창 왼쪽 모서리 위치

white = [255, 255, 255] # rgb 정보
red = [255, 0, 0]       # rgb 정보
blue = [50, 50, 255]    # rgb 정보

ball1 = {"position" : Vector2D(50,50) , "r" : 20, "col" : white}

ball1_speed = 2
view_angle = 20

radian_view_angle = math.radians(view_angle)
cos_half_FOV = math.cos(radian_view_angle)

line1_v = Vector2D(800,-math.sin(radian_view_angle)/math.cos(radian_view_angle)*800)
line2_v = Vector2D(800, math.sin(radian_view_angle)/math.cos(radian_view_angle)*800)

ball2_list = []
for i in range(50):
    ball2_list.append(ball2_ap())


pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    if keyboard.is_pressed("w") :
        ball1["position"]._y -= ball1_speed
    if keyboard.is_pressed("s") :
        ball1["position"]._y += ball1_speed
    if keyboard.is_pressed("a") :
        ball1["position"]._x -= ball1_speed
    if keyboard.is_pressed("d") :
        ball1["position"]._x += ball1_speed

    global_ball1 = Vector2D(scren_start[0]+ball1["position"]._x, scren_start[1]+ball1["position"]._y)
    global_mouse = Vector2D(pyautogui.position().x, pyautogui.position().y)
    ball1_mouse_vec = global_mouse - global_ball1
    ball1_mouse_vec = ball1_mouse_vec.norm()

    for ball2 in ball2_list:
        ball1_ball2_vec = ball2["position"] - ball1["position"]
        ball1_ball2_vec = ball1_ball2_vec.norm()

        if ball1_ball2_vec._x*ball1_mouse_vec._x + ball1_ball2_vec._y*ball1_mouse_vec._y > cos_half_FOV :
            ball2["col"] = red
        else :
            ball2["col"] = blue

    mat = [ball1_mouse_vec._x, ball1_mouse_vec._y, -ball1_mouse_vec._y, ball1_mouse_vec._x]
    new_line1_v = Vector2D(line1_v._x*mat[0] + line1_v._y*mat[2], line1_v._x*mat[1] + line1_v._y*mat[3])
    new_line2_v = Vector2D(line2_v._x*mat[0] + line2_v._y*mat[2], line2_v._x*mat[1] + line2_v._y*mat[3])


    screen.fill((0, 0, 0)) # 화면 계속 초기화 해서 과거를 잊기

    pygame.draw.circle(screen, ball1["col"], (ball1["position"]._x, ball1["position"]._y), ball1["r"])
    pygame.draw.line(screen, white, [ball1["position"]._x, ball1["position"]._y], [ball1["position"]._x + ball1_mouse_vec._x*100, ball1["position"]._y + ball1_mouse_vec._y*100])
    pygame.draw.line(screen, white, [ball1["position"]._x, ball1["position"]._y], [ball1["position"]._x + new_line1_v._x, ball1["position"]._y + new_line1_v._y])
    pygame.draw.line(screen, white, [ball1["position"]._x, ball1["position"]._y], [ball1["position"]._x + new_line2_v._x, ball1["position"]._y + new_line2_v._y])
###################################################################

    for ball2 in ball2_list:
        pygame.draw.circle(screen, ball2["col"], (ball2["position"]._x, ball2["position"]._y), ball2["r"])  # 모든 ball2 그리기


    # for ball2 in ball2_list:
    #     ball1_ball2_vec = ball2["position"] - ball1["position"]
    #     ball1_ball2_vec = ball1_ball2_vec.norm()
    #     if ball1_ball2_vec._x*ball1_mouse_vec._x + ball1_ball2_vec._y*ball1_mouse_vec._y > cos_half_FOV :
    #         pygame.draw.circle(screen, ball2["col"], (ball2["position"]._x, ball2["position"]._y), ball2["r"])  # 시야 안에있는 ball2만 그리기

##################################################################### (렉 차이 비교용 코드)

    # for ball2 in ball2_list :
    #     ball1_ball2_vec = ball2["position"] - ball1["position"]
    #     ball1_ball2_vec = ball1_ball2_vec.norm()

    #     rand_rgb = []
    #     for i in list(range(200, 0, -1)):

    #         r_r = random.randint(1,255)
    #         r_g = random.randint(1,255)
    #         r_b = random.randint(1,255)
    #         rand_rgb = [r_r, r_g, r_b]
    #         pygame.draw.circle(screen, rand_rgb, (ball2["position"]._x, ball2["position"]._y), i%30)
    #         rand_rgb[1] += 10
    #         if rand_rgb[1] > 250 :
    #             rand_rgb[1] = rand_rgb[1] % 250  #모든 ball2 렌더링


    # for ball2 in ball2_list :
    #     ball1_ball2_vec = ball2["position"] - ball1["position"]
    #     ball1_ball2_vec = ball1_ball2_vec.norm()
    #     if ball1_ball2_vec._x*ball1_mouse_vec._x + ball1_ball2_vec._y*ball1_mouse_vec._y > cos_half_FOV :
    #         rand_rgb = []
    #         for i in list(range(200, 0, -1)):

    #             r_r = random.randint(1,255)
    #             r_g = random.randint(1,255)
    #             r_b = random.randint(1,255)
    #             rand_rgb = [r_r, r_g, r_b]
    #             pygame.draw.circle(screen, rand_rgb, (ball2["position"]._x, ball2["position"]._y), i%30)
    #             rand_rgb[1] += 10
    #             if rand_rgb[1] > 250 :
    #                 rand_rgb[1] = rand_rgb[1] % 250  # 시야 안에 있는 ball2만 렌더링

########################################################################

    pygame.display.flip()