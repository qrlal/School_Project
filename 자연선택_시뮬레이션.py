import pygame
import sys
import random
import random
import matplotlib.pyplot as plt
import keyboard

pygame.init()

screen_width = 1800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


average_x_speeds = []
average_y_speeds = []
average_sizes = []


white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 55, 0)

#########################시뮬 세팅#######################
safe_bool = True     # 안전지대 yes or not
food_bool = 1        # 먹이존재 yes or not (1 or 0)
red_bool  = 1        # 천적(빨갱이) 존재 y or n

food_limit = 100        # 먹이 개수 제한(하양이 상한: 먹이 개수* 2)
white_limit = 100        # 하양이 시작 개수
red_limit = 5          # 빨강이 시작 개수 
########################################################

white_squares = []
red_squares = []
food_squares = []


def create_small_white_square():  # 먹이 생존 모드 하양이
    square_size = 60
    square_x = random.randint(0, screen_width - square_size)
    square_y = random.randint(0, screen_height - square_size)
    speed_x = random.uniform(1, 3)
    speed_y = random.uniform(1, 3)
    return {"x": square_x, "y": square_y, "speed_x": speed_x, "speed_y": speed_y, "square_size": 60, "eat_food": 0}

def create_white_square():  # 하양이 생성
    square_size = 60
    square_x = random.randint(0, screen_width - square_size)
    square_y = random.randint(0, screen_height - square_size)
    speed_x = random.uniform(4, 6)
    speed_y = random.uniform(4, 6)
    return {"x": square_x, "y": square_y, "speed_x": speed_x, "speed_y": speed_y, "square_size": 60, "eat_food": 0}

def create_red_square():    # 빨강이 생성
    mlist = [-1, 1]
    a = random.randint(0,1)
    square_size = 20
    square_x = random.randint(0, screen_width - square_size)
    square_y = random.randint(0, screen_height - square_size)
    speed_x = mlist[a] * random.uniform(4, 6)
    speed_y = mlist[a] * random.uniform(4, 6)
    return {"x": square_x, "y": square_y, "speed_x": speed_x, "speed_y": speed_y, "square_size": 20}

def create_food_square():   # 먹이 생성
    square_size = 10
    square_x = random.randint(0, screen_width - square_size)
    square_y = random.randint(0, screen_height - square_size)
    return {"x": square_x, "y": square_y, "square_size": 10}


if food_bool :
    for i in range(white_limit) :   # 먹이 생존 모드 하양이 생성
        white_squares.append(create_small_white_square())
else :
    for i in range(white_limit) :   # 하양이 생성 
        white_squares.append(create_white_square())

for i in range(food_bool*food_limit) :    # 먹이 생성
    food_squares.append(create_food_square())

if red_bool:
    for i in range(red_limit) :     # 빨강이 생성
        red_squares.append(create_red_square())


running = True
clock = pygame.time.Clock()
timer = 0


while running:
    for event in pygame.event.get():  # 러닝
        if event.type == pygame.QUIT:
            running = False

    for square in white_squares:  # 하양이 이동 and 벽튕김
        square["x"] += square["speed_x"]
        square["y"] += square["speed_y"]

        if square["x"] < 0:
            square["x"] = 0
            square["speed_x"] = abs(square["speed_x"])
        elif square["x"] + square["square_size"] > screen_width:
            square["x"] = screen_width - square["square_size"]
            square["speed_x"] = -abs(square["speed_x"])

        if square["y"] < 0:
            square["y"] = 0
            square["speed_y"] = abs(square["speed_y"])
        elif square["y"] + square["square_size"] > screen_height:
            square["y"] = screen_height - square["square_size"]
            square["speed_y"] = -abs(square["speed_y"])

    if red_bool :
        for square in red_squares:  # 빨강이 이동 and 벽튕김
            square["x"] += square["speed_x"]
            square["y"] += square["speed_y"]

            if square["x"] < 0 or square["x"] + square["square_size"] > screen_width:
                square["speed_x"] = -square["speed_x"]
            if square["y"] < 0 or square["y"] + square["square_size"] > screen_height:
                square["speed_y"] = -square["speed_y"]

    for wh_rect in white_squares:  # 하양이 삭제
        wh_x = wh_rect["x"]
        wh_y = wh_rect["y"]
        wh_width = wh_rect["square_size"]
        wh_height = wh_rect["square_size"]

        for red_rect in red_squares:
            red_x = red_rect["x"]
            red_y = red_rect["y"]
            red_width = red_rect["square_size"]
            red_height = red_rect["square_size"]

            if wh_x < red_x + red_width and wh_x + wh_width > red_x and wh_y < red_y + red_height and wh_y + wh_height > red_y:
                if wh_rect in white_squares :

                    white_squares.remove(wh_rect)

    if safe_bool and red_bool:
        for wh_rect in red_squares:  # 빨강이 안전지대 못들어옴
            wh_x = wh_rect["x"]
            wh_y = wh_rect["y"]
            wh_width = wh_rect["square_size"]
            wh_height = wh_rect["square_size"]

            red_x = 850
            red_y = 350
            red_width = 100
            red_height = 100

            if wh_x < red_x + red_width and wh_x + wh_width > red_x and wh_y < red_y + red_height and wh_y + wh_height > red_y:
                if wh_rect in red_squares:
                    # 충돌 위치 계산
                    collision_x = max(wh_x, red_x) - min(wh_x + wh_width, red_x + red_width)
                    collision_y = max(wh_y, red_y) - min(wh_y + wh_height, red_y + red_height)

                    if collision_x > collision_y:
                        wh_rect["speed_x"] = -wh_rect["speed_x"]
                    else:
                        wh_rect["speed_y"] = -wh_rect["speed_y"]


    if food_bool : 
        for food_rect in food_squares :  # 먹이 먹히면 삭제, 먹은애는 배부름
            fo_x = food_rect["x"]
            fo_y = food_rect["y"]
            fo_width = food_rect["square_size"]
            fo_height = food_rect["square_size"]

            for wh_rect in white_squares :
                wh_x = wh_rect["x"]
                wh_y = wh_rect["y"]
                wh_width = wh_rect["square_size"]
                wh_height = wh_rect["square_size"]

                if fo_x < wh_x + wh_width and fo_x + fo_width > wh_x and fo_y < wh_y + wh_height and fo_y + fo_height > wh_y:
                    if food_rect in food_squares and not wh_rect["eat_food"]:
                        food_squares.remove(food_rect)
                        wh_rect["eat_food"] = 1



    # for wh_rect in white_squares :
    #     for red_rect in red_squares :
    #         for i in range( int(red_rect["x"]) , int(red_rect["x"]+red_rect["square_size"]+1) ) :
    #             for j in range(int( red_rect["y"] ),int(red_rect["y"]+red_rect["square_size"]+1)) :
    #                 for w_i in range(int(wh_rect["x"]), int(wh_rect["x"]+wh_rect["square_size"]+1), 20) :
    #                     for w_j in range(int(wh_rect["y"]), int(wh_rect["y"]+wh_rect["square_size"]+1), 20) :
    #                         if wh_rect in white_squares :
    #                             if -0.1 < w_i - i < 0.1 and -0.1< w_j-j< 0.1 :
    #                                 white_squares.remove(wh_rect)


    screen.fill((0, 0, 0))
    if safe_bool:
        pygame.draw.rect(screen, (50,50,50), (850, 350, 100, 100))  # 안전지대 그리기
    for square in white_squares:    # 하양이 그리기
        pygame.draw.rect(screen, white, (square["x"], square["y"], square["square_size"], square["square_size"]))
        pygame.draw.rect(screen, blue, (square["x"], square["y"], square["square_size"], square["square_size"]), width=3)
    if red_bool:
        for square in red_squares:      # 빨강이 그리기
            pygame.draw.rect(screen, red, (square["x"], square["y"], square["square_size"], square["square_size"]))   
    if food_bool:
        for square in food_squares :    # 먹이 그리기
            pygame.draw.rect(screen, green, (square["x"], square["y"], square["square_size"], square["square_size"]))
    

    pygame.display.flip()


    if keyboard.is_pressed('space'):  # 배속
        a = 800
    else: 
        a = 200    
    timer  += clock.tick(a)
    if timer >= 200000//a:  #############################################################주기###################

        print("하양이 개채수:",len(white_squares)) 

        if food_bool:
            nn_squares = white_squares[:]
            for wh_rect in nn_squares :  # 먹이 못먹은애 삭제
                if wh_rect["eat_food"] == 0:
                    white_squares.remove(wh_rect)

            for wh_rect in white_squares :  # 다시 배고파짐
                wh_rect["eat_food"] = 0

        n_squares = white_squares[:]
        for rect in n_squares :  #  자식 낳음
            a = random.randint(0,1)
            b = random.randint(0,1)
            plus = [-1,1]
            speed = random.uniform(0.95, 1.05) # 변이 구현
            white_squares.append({"x": rect["x"], "y": rect["y"], "speed_x": speed*plus[a]*(rect["speed_x"]), "speed_y": speed*plus[b]*(rect["speed_y"]), "square_size": abs(rect["square_size"]+random.uniform(-1, 1)), "eat_food": 0})

        # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ통계

        total_x = 0
        total_y = 0
        total_size = 0

        for rect in white_squares :  # 속도, 사이즈 수집
            total_x += abs(rect["speed_x"])
            total_y += abs(rect["speed_y"])
            total_size += rect["square_size"]

        if len(white_squares) != 0 :
            print("평균 x속도 :",total_x/len(white_squares))
            print("평균 y속도 :",total_y/len(white_squares))
            print("평균 사이즈 :",total_size/len(white_squares))
            print("--------------------------------------")


            average_x_speed = total_x / len(white_squares)
            average_y_speed = total_y / len(white_squares)
            average_size = total_size / len(white_squares)

        average_x_speeds.append(average_x_speed)
        average_y_speeds.append(average_y_speed)
        average_sizes.append(average_size)

        total_x = 0
        total_y = 0
        total_size = 0

        # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        timer = 0
        n_squares = []


        if food_bool:
            n_food_squares = food_squares[:]
            for fo_rect in n_food_squares :  # 기존 먹이 삭제
                food_squares.remove(fo_rect)

            for i in range(food_limit) :  # 새 먹이 생성
                food_squares.append(create_food_square())

    if not food_bool :
        if len(white_squares)>800 : #  개체수 제한
            for i in range(len(white_squares)-800) :
                del white_squares[i]


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

plt.figure(figsize=(10, 5))

plt.subplot(131)
plt.plot(average_x_speeds)
plt.title('Average X Speed')
plt.xlabel('Time')
plt.ylabel('Speed')

plt.subplot(132)
plt.plot(average_y_speeds)
plt.title('Average Y Speed')
plt.xlabel('Time')
plt.ylabel('Speed')

plt.subplot(133)
plt.plot(average_sizes)
plt.title('Average Size')
plt.xlabel('Time')
plt.ylabel('Size')

plt.tight_layout()

# 그래프 표시
plt.show()

pygame.quit()
sys.exit()