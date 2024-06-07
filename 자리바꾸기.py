import math
import pygame
import sys
import pyautogui
import keyboard
import win32api
import win32con
import random
import time
import os

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

# pygame.draw.rect(screen, black, (self._x, self._y, grid_interval, grid_interval))
def draw_grid():
    for i in range(9):
        pygame.draw.line(screen, white, [start_x+i*horizontal_spacing,start_y], [start_x+i*horizontal_spacing,start_y+vertical_spacing*4], 2)
    for j in range(5):
        for i in range(3):
            pygame.draw.line(screen, white, [start_x+i*horizontal_spacing*3,start_y+j*vertical_spacing], [start_x+i*horizontal_spacing*3+2*horizontal_spacing,start_y+j*vertical_spacing], 2)

def draw_StartButton():
    global a
    a = 80
    pygame.draw.rect(screen, red, (screen_width//2-a, 700, 2*a, 60))

sound_file = "C:\\Users\\User\\Desktop\\vscode\\sound.wav"



horizontal_spacing = 150
vertical_spacing = 100


screen_width = 1800
screen_height = 800
screen_start = [960-screen_width//2, 540-screen_height//2]

start_x = (screen_width-horizontal_spacing*8)//2
start_y = (screen_height-vertical_spacing*4)//2

white = (255, 255, 255) # rgb 정보
red = (255, 0, 0)       # rgb 정보
blue = (50, 50, 255)    # rgb 정보
black = (0, 0, 0)

sit = []
for i in range(4):
    sit.append([(start_x//horizontal_spacing), (start_y//vertical_spacing)+i])
for i in range(4):
    sit.append([(start_x//horizontal_spacing)+1, (start_y//vertical_spacing)+i])
for i in range(4):
    sit.append([(start_x//horizontal_spacing)+3, (start_y//vertical_spacing)+i])
for i in range(4):
    sit.append([(start_x//horizontal_spacing)+4, (start_y//vertical_spacing)+i])
for i in range(4):
    sit.append([(start_x//horizontal_spacing)+6, (start_y//vertical_spacing)+i])
for i in range(4):
    sit.append([(start_x//horizontal_spacing)+7, (start_y//vertical_spacing)+i])
# print(sit)
# sit.remove([1,3])
# print(sit)

no_sit = []

students = ["박조완", "김정우", "김민우", "김지훈", "하나경", "강윤구", "문성원", "박준한", "박지수", "곽상백", "오채연", "오영묵", "윤동환", "윤예서", "이승민", "이진우", "임성윤", "임지효", "전아라", "조민규", "조윤서", "한승혜", "황지섭"]

start = False

pygame.init()
myFont = pygame.font.SysFont(None, 50)
font = pygame.font.SysFont("malgungothic", 50)
font1 = pygame.font.SysFont("malgungothic", 30)
student_font = pygame.font.SysFont("malgungothic", 40)

screen = pygame.display.set_mode((screen_width, screen_height))
sound = pygame.mixer.Sound(sound_file)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and screen_width//2-a < pyautogui.position().x - screen_start[0] < screen_width//2+a and 700 < pyautogui.position().y - screen_start[1] < 760:  # 1은 마우스 왼쪽 버튼을 의미합니다
                start = True

    if keyboard.is_pressed("a"):
        local_x = pyautogui.position().x - screen_start[0]
        local_y = pyautogui.position().y - screen_start[1]
        x_index = local_x//horizontal_spacing
        y_index = local_y//vertical_spacing
        if [x_index, y_index] in no_sit:
            pygame.draw.line(screen, black, [x_index*horizontal_spacing, y_index*vertical_spacing], [(x_index+1)*horizontal_spacing, (y_index+1)*vertical_spacing],1)
            pygame.draw.line(screen, black, [x_index*horizontal_spacing, (y_index+1)*vertical_spacing], [(x_index+1)*horizontal_spacing, (y_index)*vertical_spacing],1)
            if not [x_index, y_index] in sit:
                sit.append([x_index, y_index])

    if keyboard.is_pressed("b"):
        local_x = pyautogui.position().x - screen_start[0]
        local_y = pyautogui.position().y - screen_start[1]
        x_index = local_x//horizontal_spacing
        y_index = local_y//vertical_spacing
        if [x_index, y_index] in sit:
            pygame.draw.line(screen, white, [x_index*horizontal_spacing, y_index*vertical_spacing], [(x_index+1)*horizontal_spacing, (y_index+1)*vertical_spacing],1)
            pygame.draw.line(screen, white, [x_index*horizontal_spacing, (y_index+1)*vertical_spacing], [(x_index+1)*horizontal_spacing, (y_index)*vertical_spacing],1)
            sit.remove([x_index, y_index])
            no_sit.append([x_index, y_index])


    state_left = win32api.GetKeyState(win32con.VK_LBUTTON)
    new_state_left = win32api.GetKeyState(win32con.VK_LBUTTON)
    
    if new_state_left != state_left:  # 상태 변경 감지
        state_left = new_state_left
        
        if new_state_left < 0:
            print("Hello World")


    draw_grid()
    draw_StartButton()
    myText = myFont.render("START", True, (0,0,0)) #(Text,anti-alias, color)
    myText2 = font.render("B + 마우스 : 자리제거", True, (255,255,255))
    myText3 = font.render("A + 마우스 : 자리제거 취소", True, (255,255,255))
    myText4 = font1.render("경고: 자릿수와 학생수 다름", True, (255,0,0))
    screen.blit(myText, (screen_width//2-a+23,700+13)) #(글자변수, 위치)
    screen.blit(myText2, (30,60)) #(글자변수, 위치)
    screen.blit(myText3, (30,0)) #(글자변수, 위치)
    if len(students) != len(sit):
        screen.blit(myText4, (screen_width//2-180,630))
    elif len(students) == len(sit):
        pygame.draw.rect(screen, black, (700,620,400,50))


    if start:
        random.shuffle(sit)
        random.shuffle(students)

        name_texts = []
        for name in students:
            name_text = student_font.render(name, True, (255, 255, 255))
            name_texts.append(name_text)

        for sits,name in zip(sit,name_texts):
            screen.blit(name, (sits[0]*horizontal_spacing+17, sits[1]*vertical_spacing+24))
            pygame.display.flip()
            sound.play()
            time.sleep(1)
        
        time.sleep(100000000)
        

    pygame.display.flip()
