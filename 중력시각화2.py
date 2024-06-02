import math
import pygame
import keyboard
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
    return 7 * 10**-11 * m1 * m2 / dis / dis



screen_width = 800
screen_height = 800
scren_start = [560, 140]  # pygame 창 왼쪽 모서리 위치

white = (255, 255, 255) # rgb 정보
red = (255, 0, 0)       # rgb 정보
blue = (50, 50, 255)    # rgb 정보

ball1 = {"x" : 200, "y" : 600 , "r" : 20, "mess" : 6*10**24} # 지구
ball2 = {"x" : 400, "y" : 400 , "r" : 40, "mess" : 2*10**30} # 태양

current_vec = Vector2D(0, 0) # 지구의 이동방향 방향벡터

scale = 10000000000000000  # 축척 비스무리

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    ball1_vec = Vector2D(ball1["x"], ball1["y"]) # 지구 위치벡터
    ball2_vec = Vector2D(ball2["x"], ball2["y"]) # 태양 위치벡터
    ball1_dir_vec = ball2_vec-ball1_vec # 태양의 위치벡터에서 지구의 위치벡터를 뺴서 지구가 태양를 바라보는 벡터(지구의 로컬 좌표계에서 태양의 위치벡터, 즉 지구가 태양을 바라보는 벡터)저장
    ball2_dir_vec = ball1_vec-ball2_vec # 지구의 위치벡터에서 태양의 위치벡터를 뺴서 태양이 지구를 바라보는 벡터(태양의 로컬 좌표계에서 지구의 위치벡터, 즉 태양이 지구를 바라보는 벡터)저장
    ball1_dir_vec = ball1_dir_vec.norm() # 크기가 일정하지 않으면 속도, 가속도가 변하기 떄문에 벡터의 정규화를 하여 크기가 1인 방향벡터로 변환
    ball2_dir_vec = ball2_dir_vec.norm() # 크기가 일정하지 않으면 속도, 가속도가 변하기 떄문에 벡터의 정규화를 하여 크기가 1인 방향벡터로 변환

    distance = math.sqrt((ball1["x"]-ball2["x"])**2 + (ball1["y"]-ball2["y"])**2) # 두 점 사이 거리 공식 사용


    g_F = G(ball1["mess"], ball2["mess"], distance) # 두 물체 사이 작용하는 중력 확인

    ball1_a = g_F / ball1["mess"] # F = ma (가속도는 힘 / 질량)
    ball2_a = g_F / ball2["mess"] # F = ma (가속도는 힘 / 질량)

    ball1_movevec = Vector2D(ball1_a/scale, ball1_a/scale) * ball1_dir_vec # scale로 나누어서 축소해서 보기
    ball2_movevec = Vector2D(ball2_a/scale, ball2_a/scale) * ball2_dir_vec # scale로 나누어서 축소해서 보기

    past = Vector2D(ball1["x"], ball1["y"]) # 과거 지구의 위치벡터
    ball1["x"] += ball1_movevec._x  # 중력으로 인한 지구 이동
    ball1["y"] += ball1_movevec._y  # 중력으로 인한 지구 이동
    ball2["x"] += ball2_movevec._x  # 중력으로 인한 태양 이동
    ball2["y"] += ball2_movevec._y  # 중력으로 인한 태양 이동

    ball1["x"] = round(ball1["x"],3)  # 컴퓨터를 위한 소수 3자리 밑 삭제
    ball1["y"] = round(ball1["y"],3)  # 컴퓨터를 위한 소수 3자리 밑 삭제
    ball2["x"] = round(ball2["x"],3)  # 컴퓨터를 위한 소수 3자리 밑 삭제
    ball2["y"] = round(ball2["y"],3)  # 컴퓨터를 위한 소수 3자리 밑 삭제

    global_ball1 = Vector2D(scren_start[0]+ball1["x"], scren_start[1]+ball1["y"]) # 화면 전체에서의 pygame창의 위치벡터와 pygame에서의 지구의 위치벡터를 더하여 화면 전체에서의 지구 위치벡터 저장
    global_mouse = Vector2D(pyautogui.position().x, pyautogui.position().y) # 화면 전체에서의 마우스의 위치벡터 저장
    ball1_mouse_vec = global_mouse - global_ball1 # 마우스의 위치벡터에서 지구의 위치벡터를 뺴서 지구의 로컬 좌표계에서의 마우스의 위치벡터 저장. 이번엔 방향벡터 말고 거리가 멀수록 크기가 큰 벡터로 저장하여 지구가 마우스를 부드럽게 따라가는거 구현
    #print(ball1_mouse_vec)
    ball1["x"] += ball1_mouse_vec._x / 1000 # 지구가 마우스 방향으로 이동
    ball1["y"] += ball1_mouse_vec._y / 1000 # 지구가 마우스 방향으로 이동

    # if keyboard.is_pressed("w"):  # 이거 이용 or 마우스로 이동 (이거 쓸거면 w로 태양 처박힘 탈출 비활성화)
    #     ball1["y"] -= speed 
    # if keyboard.is_pressed("s"):
    #     ball1["y"] += speed
    # if keyboard.is_pressed("a"):
    #     ball1["x"] -= speed
    # if keyboard.is_pressed("d"):
    #     ball1["x"] += speed

    if keyboard.is_pressed("w"):  # w눌러서 항성에 무한 처박힘 탈출
        ball1["x"] = ball1["x"] - ball1_movevec._x
        ball1["y"] = ball1["y"] - ball1_movevec._y

        
    current = Vector2D(ball1["x"], ball1["y"]) # 현재 지구의 위치벡터
    current_vec = current - past # 과거 지구의 위치와 현재 지구의 미세한 위치 차이 이용해서 지구의 "이동방향 방향벡터" 저장
    current_vec = current_vec.norm() # 방향벡터니깐 정규화
    

    if distance <= ball1["r"] + ball2["r"] : # 지구 태양에게 먹힘 방지
        if boo == False:
            sdf = ball1["x"]
            jkl = ball1["y"]
        ball1["x"] = sdf -20 * current_vec._x
        ball1["y"] = jkl -20 * current_vec._y
        boo = True
    else :
        boo = False


    if ball1["x"] < 0:   # 지구의 화면 이탈 방지 (태양은 거의 안움직여서 구현 x)
        ball1["x"] = 0
        current_vec = Vector2D(0, 0)
    elif ball1["x"] > 800:
        ball1["x"] = 800
        current_vec = Vector2D(0, 0)
    if ball1["y"] < 0:
        ball1["y"] = 0
        current_vec = Vector2D(0, 0)
    elif ball1["y"]> 800:
        ball1["y"] = 800
        current_vec = Vector2D(0, 0)


    screen.fill((0, 0, 0)) # 화면 계속 초기화 해서 과거를 잊기
    
    pygame.draw.circle(screen, white, (ball1["x"], ball1["y"]), ball1["r"]) # 지구 그리기
    pygame.draw.line(screen, blue, [ball1["x"], ball1["y"]], [ball1["x"]+current_vec._x*100, ball1["y"]+current_vec._y*100], 5) # 지구 이동 방향 그리기

    pygame.draw.circle(screen, red, (ball2["x"], ball2["y"]), ball2["r"]) # 태양 그리기
    
    pygame.display.flip()