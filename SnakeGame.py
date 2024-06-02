import os
import random
import time
import keyboard
import threading

wall_rotn = 15  # 벽 개수

up_bool = False
down_bool = False
left_bool = False
right_bool = True

found_dup = False
hit_wall = False

snake_unit = [[wall_rotn//2, wall_rotn//2]]
direction = "right"

score = 0

apple = [wall_rotn//2, wall_rotn//2]
while apple == snake_unit[0]:
    apple = [random.randint(1, wall_rotn), random.randint(1, wall_rotn)]

a = "ㅁㅁ"+"ㅁ"*wall_rotn
b = "ㅁ" + "ㅤ"*wall_rotn + "ㅁ"
wall = [a]
for i in range(wall_rotn):
    wall.append(b)
wall.append(a)

def change_dir():
    global direction

    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"
    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"
    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"
    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"
    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"
    if keyboard.is_pressed("w") and direction != "down":  # 방향
        direction = "up"

    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"
    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"
    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"
    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"
    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"
    if keyboard.is_pressed("s") and direction != "up":
        direction = "down"

    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"
    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"
    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"
    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"
    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"
    if keyboard.is_pressed("a") and direction != "right":
        direction = "left"

    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"
    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"
    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"
    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"
    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"
    if keyboard.is_pressed("d") and direction != "left":
        direction = "right"


for i in [3,2,1]:
    print(i)
    time.sleep(1)

while True:
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향

    print("점수:",score)
    snake_add_wall = []
    sanke_apple_add_wall = []
    
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향

    for i in range(len(wall)): # 스네이크 그리기
        part_count = 0
        part_x_list = []

        for snake_part in snake_unit:
            if snake_part[1] == i :
                part_count += 1 
                part_x_list.append(snake_part[0])
        
        if not part_x_list == []:
            asw = wall[i][:min(part_x_list)]+"ㅇ"+wall[i][min(part_x_list)+1:]
            part_x_list.remove(min(part_x_list))
            part_count -= 1

            part_x_list.sort()
            for i in range(part_count):
                asw = asw[:part_x_list[i]]+"ㅇ"+asw[part_x_list[i]+1:]

            snake_add_wall.append(asw)

        else:
            snake_add_wall.append(wall[i])


    for i in range(len(snake_add_wall)): # 사과 그리기
        if apple[1] == i:
            saaw = snake_add_wall[i][:apple[0]]+"ㅅ"+snake_add_wall[i][apple[0]+1:]
            print(saaw)
            sanke_apple_add_wall.append(saaw)

        else:
            print(snake_add_wall[i])   
            sanke_apple_add_wall.append(snake_add_wall[i])         


    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향


    if snake_unit[0] == apple: # 사과 먹음
        last_tail = snake_unit[-1][:]
        snake_unit.append(last_tail)
        score += 1

        while any(apple == part for part in snake_unit):
            apple = [random.randint(1+1, wall_rotn-1), random.randint(1+1, wall_rotn-1)]


    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향


    snake_unit_ex = snake_unit[:]  # 대가리 이후파트 이동
    for i in range(len(snake_unit)-1): 
        snake_unit[i+1] = snake_unit_ex[i][:] 

    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향

    
    if direction == "up" and not down_bool: # 대가리 이동
        snake_unit[0][1] -= 1
        up_bool = True
        down_bool = False
        left_bool = False
        right_bool = False
    elif direction == "down" and not up_bool:
        snake_unit[0][1] += 1
        up_bool = False
        down_bool = True
        left_bool = False
        right_bool = False
    elif direction == "left" and not right_bool:
        snake_unit[0][0] -= 1
        up_bool = False
        down_bool = False
        left_bool = True
        right_bool = False
    elif direction == "right" and not left_bool:
        snake_unit[0][0] += 1
        up_bool = False
        down_bool = False
        left_bool = False
        right_bool = True
    else:
        if up_bool:
            snake_unit[0][1] -= 1
        elif down_bool:
            snake_unit[0][1] += 1
        elif left_bool:
            snake_unit[0][0] -= 1
        elif right_bool:
            snake_unit[0][0] += 1

    # if direction == "up": # 대가리 이동
    #     snake_unit[0][1] -= 1
    # elif direction == "down":
    #     snake_unit[0][1] += 1
    # elif direction == "left":
    #     snake_unit[0][0] -= 1
    # elif direction == "right":
    #     snake_unit[0][0] += 1

    
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향


    for i in range(len(snake_unit)): # 게임오버 조건1 (지가 지몸에 부딧힘)
        for j in range(len(snake_unit)):
            if i!=j and snake_unit[i] == snake_unit[j]:
                found_dup = True
                break

        if found_dup:
            break
    
    if found_dup:
        break   

    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향

    if snake_unit[0][0] <= 0 or snake_unit[0][0] >= wall_rotn+1 or snake_unit[0][1] <= 0 or snake_unit[0][1] >= wall_rotn+1: # 게임오버 조건2 (벽에 부딧힘)
        hit_wall = True
        break


    time.sleep(0.1)
    os.system('cls')


    change_dir() # 방향
    change_dir()
    change_dir() 
    change_dir() # 방향
    change_dir() # 방향
    change_dir() # 방향

    
if hit_wall:
    print("GAME OVER(벽에 부딧힘)")
elif found_dup:
    print("GAME OVER(지몸에 부딧힘)")