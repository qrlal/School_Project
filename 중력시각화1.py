import math
import pygame
import sys
import pyautogui

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

def G (m1, m2, dis):   # 두 물체의 질량, 거리 받아서 만류인력 return (만류인력의 법칙 공식 사용)
    if dis == 0:
        return 0
    return 7 * 10**-11 * m1 * m2 / dis / dis


screen_width = 1800
screen_height = 800
scren_start = [60, 140]  # pygame 창 왼쪽 모서리 위치

rksrur = 50 # 간격

lines = []
for i in range(1800 // rksrur - 1):
    for j in range(800//rksrur - 1):
        lines.append({"x" : rksrur*(i+1), "y" :rksrur*(j+1), "mess" : 1, "g" : 0, "dir" : Vector2D(0,0), "dis" : 0})

ball1 = {"x" : 200, "y" : 600 , "r" : 20, "mess" : 6*10**18}


white = (255, 255, 255) # rgb 정보
red = (255, 0, 0)       # rgb 정보
blue = (50, 50, 255)    # rgb 정보

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    for line in lines:
        dis = math.sqrt((line["x"]-ball1["x"])**2 + (line["y"]-ball1["y"])**2)
        line["dis"] = dis
        line["g"] = G(line["mess"], ball1["mess"], dis)

        line_loc_vec = Vector2D(line["x"], line["y"])
        ball1_loc_vec = Vector2D(ball1["x"], ball1["y"])
        line_dir_vec = ball1_loc_vec - line_loc_vec
        line_dir_vec = line_dir_vec.norm()
        scale_vec = Vector2D(line["g"], line["g"])
        line_dir_vec = scale_vec * line_dir_vec
        line["dir"] = line_dir_vec


    global_ball1 = Vector2D(scren_start[0]+ball1["x"], scren_start[1]+ball1["y"])
    global_mouse = Vector2D(pyautogui.position().x, pyautogui.position().y)
    ball1_mouse_vec = global_mouse - global_ball1
    # ball1_mouse_vec = ball1_mouse_vec.norm()
    ball1["x"] += ball1_mouse_vec._x / 300
    ball1["y"] += ball1_mouse_vec._y / 300

    screen.fill((0, 0, 0))
    ###################################
    for line in lines:
        if line["dis"] < math.sqrt((line["x"]-(line["x"]+line["dir"]._x/100))**2 + (line["y"]-(line["y"]+line["dir"]._y/100))**2):
            dirvec = line["dir"].norm()
            dirvec = Vector2D(line["dis"], line["dis"])*dirvec
            pygame.draw.line(screen, white, [line["x"], line["y"]], [line["x"]+dirvec._x, line["y"]+dirvec._y], 5)
            continue
        pygame.draw.line(screen, white, [line["x"], line["y"]], [line["x"]+line["dir"]._x/100, line["y"]+line["dir"]._y/100], 5)
    pygame.draw.circle(screen, red, (ball1["x"], ball1["y"]), ball1["r"])
    ###################################
    pygame.display.flip()