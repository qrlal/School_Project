import pygame
import sys
import pyautogui
import keyboard
import math
import time

##############################################################################################################################

class Node:
    def __init__(self,is_wall,x,y,g,h,mom):  #x,y는 정가운데위치
        self._is_wall = is_wall
        self._x = x
        self._y = y
        self._g = g
        self._h = h
        self._mom = mom
    def __str__(self):
        return '({},{},{},{},{},{})'.format(self._is_wall, self._x, self._y, self._g, self._h, self._mom)
    def Get_F(self):
        return int(self._g) + int(self._h)
    def GetMom(self):
        return self._mom
    def GetPosition(self):
        return [self._x, self._y]
    def Get_is_this_wall(self):
        return self._is_wall
    def Draw_This_Open_Node(self):
        pygame.draw.rect(screen, open_col, (self._x, self._y, grid_interval, grid_interval))
    def Draw_This_Closed_Node(self):
        pygame.draw.rect(screen, closed_col, (self._x, self._y, grid_interval, grid_interval))
    def Draw_This_Wall_Node(self):
        pygame.draw.rect(screen, white, (self._x, self._y, grid_interval, grid_interval))
    def Remove_This_Wall(self):
        pygame.draw.rect(screen, black, (self._x, self._y, grid_interval, grid_interval))

##############################################################################################################################

def init_wall():
    pygame.draw.rect(screen, black,(0, 0, screen_width, screen_height))
    Draw_start_end()
    for node_i in nodes:
        for node_j in node_i:
            node_j._is_wall = False

##############################################################################################################################

def init_search():
    pygame.draw.rect(screen, black,(0, 0, screen_width, screen_height))
    Draw_start_end()
    for wall_node in wall:
        this_wall = nodes[wall_node[0]//grid_interval][wall_node[1]//grid_interval]
        this_wall.Draw_This_Wall_Node()

def Draw_grid():
    for i in range(screen_width // grid_interval - 1):
        pygame.draw.line(screen, white, [(i+1)*grid_interval, 0], [(i+1)*grid_interval,screen_height])
    for j in range(screen_height // grid_interval -1):
        pygame.draw.line(screen, white, [0, (j+1)*grid_interval], [screen_width, (j+1)*grid_interval])

##############################################################################################################################

def Draw_start_end():
    pygame.draw.rect(screen, start_col, (int((screen_width/5)//grid_interval*grid_interval), int((screen_height/2)//grid_interval*grid_interval), grid_interval, grid_interval)) # 출발점 그리기
    pygame.draw.rect(screen, end_col, (int((screen_width/5*4)//grid_interval*grid_interval), int((screen_height/2)//grid_interval*grid_interval), grid_interval, grid_interval)) # 도착점 그리기


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

final_path_nodes = []
def PathFinding_Astar():
    start = time.time()
    global start_node
    global end_node

    start_node = Node(False, start_x, start_y, 0, abs(end_x-start_x)+abs(end_y-start_y), None) # 출발노드
    start_node._mom = Node(False, start_x, start_y, 0, abs(end_x-start_x)+abs(end_y-start_y), None)
    nodes[start_node._x // grid_interval][start_node._y // grid_interval] = start_node
    end_node = Node(False, end_x, end_y, 0, 0, None) # 도착노드
    nodes[end_node._x // grid_interval][end_node._y // grid_interval] = end_node

    global open_nodes
    global closed_nodes_visit

    open_nodes = []
    closed_nodes_visit = [] 
    open_nodes.append(nodes[start_node._x // grid_interval][start_node._y // grid_interval])

    while len(open_nodes) > 0:
        if keyboard.is_pressed("i"):
            break

        if 설명모드:
            while True:
                if keyboard.is_pressed("g"):
                    time.sleep(0.5)
                    break
                
        global cur_node
        cur_node = open_nodes[0]
        for i in range(len(open_nodes)):
            if open_nodes[i].Get_F() <= cur_node.Get_F() and open_nodes[i]._h < cur_node._h:
                cur_node = open_nodes[i]
        # print("cur_node", cur_node.GetPosition())
        open_nodes.remove(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])
        closed_nodes_visit.append(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])


        if cur_node == end_node:
            total_dis = 0
            target_node = end_node
            while target_node != start_node:
                final_path_nodes.append(target_node)
                target_node = target_node._mom
            final_path_nodes.append(start_node)
            final_path_nodes.reverse()

            for i in range(len(final_path_nodes)):
                total_dis += abs(final_path_nodes[i]._x-final_path_nodes[i]._mom._x)
                total_dis += abs(final_path_nodes[i]._y-final_path_nodes[i]._mom._y)
                pygame.draw.line(screen, blue, [final_path_nodes[i]._x+grid_interval/2, final_path_nodes[i]._y+grid_interval/2], [final_path_nodes[i]._mom._x+grid_interval/2, final_path_nodes[i]._mom._y+grid_interval/2], grid_interval//3)
            print("A* 이동거리:",total_dis)
            print("A* 걸리시간:",round((time.time()-start)*100)/100)
            text = sysfont.render("A* 이동거리: "+str(total_dis), True, (75, 198, 255))
            text2 = sysfont.render("걸린시간: "+str(round((time.time()-start)*100)/100)+"sec", True, (75, 198, 255))
            screen.blit(text, (0,0))
            screen.blit(text2, (0,30))
            break


        if allow_diagonal:
            Astar_Add_Open(cur_node._x - grid_interval, cur_node._y - grid_interval) # 상좌
            Astar_Add_Open(cur_node._x - grid_interval, cur_node._y + grid_interval) # 하좌
            Astar_Add_Open(cur_node._x - grid_interval, cur_node._y - grid_interval) # 좌상
            Astar_Add_Open(cur_node._x + grid_interval, cur_node._y + grid_interval) # 우하

        Astar_Add_Open(cur_node._x, cur_node._y - grid_interval) # 상
        Astar_Add_Open(cur_node._x, cur_node._y + grid_interval) # 하 
        Astar_Add_Open(cur_node._x - grid_interval, cur_node._y) # 좌
        Astar_Add_Open(cur_node._x + grid_interval, cur_node._y) # 우
        
        for node in open_nodes:
            node.Draw_This_Open_Node()
        for node in closed_nodes_visit:
            node.Draw_This_Closed_Node()
        Draw_start_end()
        # time.sleep(3)
        pygame.display.flip()

##############################################################################################################################

def Astar_Add_Open(check_x, check_y):
    this_node_i_index = check_x // grid_interval
    this_node_j_index = check_y // grid_interval
    if not allow_diagonal and 0 <= check_x < screen_width and 0 <= check_y < screen_height and not nodes[this_node_i_index][this_node_j_index]._is_wall and not nodes[this_node_i_index][this_node_j_index] in closed_nodes_visit:
        neighbor_node = nodes[this_node_i_index][this_node_j_index]
        movecost = cur_node._g + grid_interval  # F = G + H

        if movecost < neighbor_node._g or not neighbor_node in open_nodes:
            neighbor_node._g = movecost
            neighbor_node._h = abs(neighbor_node._x - end_node._x) + abs(neighbor_node._y - end_node._y)
            neighbor_node._mom = cur_node
            open_nodes.append(neighbor_node)
            # print(neighbor_node.GetPosition())

    elif allow_diagonal and 0 <= check_x < screen_width and 0 <= check_y < screen_height and not nodes[this_node_i_index][this_node_j_index]._is_wall and not nodes[this_node_i_index][this_node_j_index] in closed_nodes_visit and not nodes[this_node_i_index][cur_node._y // grid_interval]._is_wall and not nodes[cur_node._x // grid_interval][this_node_j_index]._is_wall :
        neighbor_node = nodes[this_node_i_index][this_node_j_index]
        if abs(check_x - cur_node._x) + abs(check_y - cur_node._y) > 11 :
            movecost = cur_node._g + grid_interval*1.4  # F = G + H
        else:
            movecost = cur_node._g + grid_interval  # F = G + H

        if movecost < neighbor_node._g or not neighbor_node in open_nodes:
            neighbor_node._g = movecost
            neighbor_node._h = abs(neighbor_node._x - end_node._x) + abs(neighbor_node._y - end_node._y)
            neighbor_node._mom = cur_node
            open_nodes.append(neighbor_node)
            # print(neighbor_node.GetPosition())

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def PathFinding_BestFistSearch():
    start = time.time()
    global start_node
    global end_node

    if BFS_def_dis_mode_sqrt:
        dis = math.sqrt((start_x-end_x)**2 + (start_y-end_y)**2)
    else:
        dis = abs(start_x-end_x) + abs(start_y-end_y)

    start_node = Node(False, start_x, start_y, -dis, None, None) # 출발노드
    start_node._mom = Node(False, start_x, start_y, None, None, None)
    nodes[start_node._x // grid_interval][start_node._y // grid_interval] = start_node
    end_node = Node(False, end_x, end_y, 0, 0, None) # 도착노드
    nodes[end_node._x // grid_interval][end_node._y // grid_interval] = end_node

    global open_nodes
    global closed_nodes_visit

    open_nodes = []
    closed_nodes_visit = [] 
    open_nodes.append(nodes[start_node._x // grid_interval][start_node._y // grid_interval])

    while len(open_nodes) > 0:
        if keyboard.is_pressed("i"):
            break

        if 설명모드:
            while True:
                if keyboard.is_pressed("g"):
                    time.sleep(0.5)
                    break

        global cur_node
        cur_node = open_nodes[0]
        for i in range(len(open_nodes)):
            if open_nodes[i]._g == cur_node._g and abs(abs(open_nodes[i]._x - end_node._x) - abs(open_nodes[i]._y - end_node._y)) < abs(abs(cur_node._x - end_node._x) - abs(cur_node._y - end_node._y)): # x,y 차이로 평가함수 정할때, 두 변 길이가 (1,5) 일때와 (2,4) 일때 평가함수 같게나옴(마약 두점 사이거리 공식 쓰면 (2,4)가 평가함수 더 큼.. 이 문제 잡기위해 빗변이 아닌 두 변의 길이의 합이 같은 두 삼각형은 산술기하평균에 의해(c^2 = a^2 + b^2, c^2의 최솟값) a,b가 같은 값일수록 빗변(실제거리)가 작음. 을 이용)
                cur_node = open_nodes[i]
            elif open_nodes[i]._g > cur_node._g:
                cur_node = open_nodes[i]
        open_nodes.remove(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])
        closed_nodes_visit.append(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])

        if cur_node == end_node:
            total_dis = 0
            target_node = end_node
            while target_node != start_node:
                final_path_nodes.append(target_node)
                target_node = target_node._mom
            final_path_nodes.append(start_node)
            final_path_nodes.reverse()

            for i in range(len(final_path_nodes)):
                total_dis += abs(final_path_nodes[i]._x-final_path_nodes[i]._mom._x)
                total_dis += abs(final_path_nodes[i]._y-final_path_nodes[i]._mom._y)
                pygame.draw.line(screen, blue, [final_path_nodes[i]._x+grid_interval/2, final_path_nodes[i]._y+grid_interval/2], [final_path_nodes[i]._mom._x+grid_interval/2, final_path_nodes[i]._mom._y+grid_interval/2], grid_interval//3)
            print("최고 우선 탐색 이동거리:",total_dis)
            print("최고 우선 탐색 걸린시간:",round((time.time()-start)*100)/100)
            text = sysfont.render("최고우선탐색 이동거리: "+str(total_dis), True, (75, 198, 255))
            text2 = sysfont.render("걸린시간: "+str(round((time.time()-start)*100)/100)+"sec", True, (75, 198, 255))
            screen.blit(text, (0,0))
            screen.blit(text2, (0,30))
            break

        ######노드 오픈하기 만들어야함
        Best_First_Search_Add_Open(cur_node._x, cur_node._y - grid_interval) # 상
        Best_First_Search_Add_Open(cur_node._x, cur_node._y + grid_interval) # 하 
        Best_First_Search_Add_Open(cur_node._x - grid_interval, cur_node._y) # 좌
        Best_First_Search_Add_Open(cur_node._x + grid_interval, cur_node._y) # 우
        ######노드 오픈하기 만들어야함

        for node in open_nodes:
            node.Draw_This_Open_Node()
        for node in closed_nodes_visit:
            node.Draw_This_Closed_Node()
        Draw_start_end()
        pygame.display.flip()

##############################################################################################################################

def Best_First_Search_Add_Open(check_x, check_y):
    this_node_i_index = check_x // grid_interval
    this_node_j_index = check_y // grid_interval
    if 0 <= check_x < screen_width and 0 <= check_y < screen_height and not nodes[this_node_i_index][this_node_j_index]._is_wall and not nodes[this_node_i_index][this_node_j_index] in closed_nodes_visit:
        neighbor_node = nodes[this_node_i_index][this_node_j_index]
        if not neighbor_node in open_nodes:
            neighbor_node._mom = cur_node

            if BFS_def_dis_mode_sqrt:
                neighbor_node._g = -(math.sqrt((neighbor_node._x-end_x)**2 + (neighbor_node._y-end_y)**2))
            else :
                neighbor_node._g = - abs(neighbor_node._x-end_x) - abs(neighbor_node._y-end_y)
            open_nodes.append(neighbor_node)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def PathFinding_BestFistSearch_PJW():
    start = time.time()
    global start_node
    global end_node

    if BFS_def_dis_mode_sqrt:
        dis = math.sqrt((start_x-end_x)**2 + (start_y-end_y)**2)
    else:
        dis = abs(start_x-end_x) + abs(start_y-end_y)

    start_node = Node(False, start_x, start_y, -dis, None, None) # 출발노드
    start_node._mom = Node(False, start_x, start_y, None, None, None)
    nodes[start_node._x // grid_interval][start_node._y // grid_interval] = start_node
    end_node = Node(False, end_x, end_y, 0, 0, None) # 도착노드
    nodes[end_node._x // grid_interval][end_node._y // grid_interval] = end_node

    global open_nodes
    global closed_nodes_visit

    open_nodes = []
    closed_nodes_visit = [] 
    open_nodes.append(nodes[start_node._x // grid_interval][start_node._y // grid_interval])

    while len(open_nodes) > 0:
        if keyboard.is_pressed("i"):
            break

        if 설명모드:
            while True:
                if keyboard.is_pressed("g"):
                    time.sleep(0.5)
                    break

        global cur_node
        cur_node = open_nodes[0]
        for i in range(len(open_nodes)):
            if open_nodes[i]._g == cur_node._g and abs(abs(open_nodes[i]._x - end_node._x) - abs(open_nodes[i]._y - end_node._y)) < abs(abs(cur_node._x - end_node._x) - abs(cur_node._y - end_node._y)): # x,y 차이로 평가함수 정할때, 두 변 길이가 (1,5) 일때와 (2,4) 일때 평가함수 같게나옴(마약 두점 사이거리 공식 쓰면 (2,4)가 평가함수 더 큼.. 이 문제 잡기위해 빗변이 아닌 두 변의 길이의 합이 같은 두 삼각형은 산술기하평균에 의해(c^2 = a^2 + b^2, c^2의 최솟값) a,b가 같은 값일수록 빗변(실제거리)가 작음. 을 이용)
                cur_node = open_nodes[i]
            elif open_nodes[i]._g > cur_node._g:
                cur_node = open_nodes[i]
        open_nodes.remove(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])
        closed_nodes_visit.append(nodes[cur_node._x // grid_interval][cur_node._y // grid_interval])

        if cur_node == end_node:
            total_dis = 0
            target_node = end_node
            while target_node != start_node:
                final_path_nodes.append(target_node)
                target_node = target_node._mom
            final_path_nodes.append(start_node)
            final_path_nodes.reverse()

            for i in range(len(final_path_nodes)):
                total_dis += abs(final_path_nodes[i]._x-final_path_nodes[i]._mom._x)
                total_dis += abs(final_path_nodes[i]._y-final_path_nodes[i]._mom._y)
                pygame.draw.line(screen, blue, [final_path_nodes[i]._x+grid_interval/2, final_path_nodes[i]._y+grid_interval/2], [final_path_nodes[i]._mom._x+grid_interval/2, final_path_nodes[i]._mom._y+grid_interval/2], grid_interval//3)
            
            print("내가만든탐색 이동거리:",total_dis)
            print("내가만든탐색 걸린시간:",round((time.time()-start)*100)/100)
            text = sysfont.render("내가만든탐색 이동거리: "+str(total_dis), True, (75, 198, 255))
            text2 = sysfont.render("걸린시간: "+str(round((time.time()-start)*100)/100)+"sec", True, (75, 198, 255))
            screen.blit(text, (0,0))
            screen.blit(text2, (0,30))
            break

        ######노드 오픈하기 만들어야함
        Best_First_Search_Add_Open_PJW(cur_node._x, cur_node._y - grid_interval) # 상
        Best_First_Search_Add_Open_PJW(cur_node._x, cur_node._y + grid_interval) # 하 
        Best_First_Search_Add_Open_PJW(cur_node._x - grid_interval, cur_node._y) # 좌
        Best_First_Search_Add_Open_PJW(cur_node._x + grid_interval, cur_node._y) # 우
        ######노드 오픈하기 만들어야함

        for node in open_nodes:
            node.Draw_This_Open_Node()
        for node in closed_nodes_visit:
            node.Draw_This_Closed_Node()
        Draw_start_end()
        pygame.display.flip()

##############################################################################################################################

def Best_First_Search_Add_Open_PJW(check_x, check_y):
    this_node_i_index = check_x // grid_interval
    this_node_j_index = check_y // grid_interval
    if 0 <= check_x < screen_width and 0 <= check_y < screen_height and not nodes[this_node_i_index][this_node_j_index]._is_wall and not nodes[this_node_i_index][this_node_j_index] in closed_nodes_visit:
        neighbor_node = nodes[this_node_i_index][this_node_j_index]
        if not neighbor_node in open_nodes:
            neighbor_node._mom = cur_node
            neighbor_node._g = - abs(neighbor_node._x-end_x) - abs(neighbor_node._y-end_y)

            if this_node_i_index-1 >= 0 and this_node_i_index+1 <= len(nodes)-1 and this_node_j_index-1 >= 0 and this_node_j_index+1 < len(nodes[this_node_i_index]) and this_node_j_index+1 < len(nodes[this_node_i_index-1]) and this_node_j_index+1 < len(nodes[this_node_i_index+1]):
                if nodes[this_node_i_index-1][this_node_j_index]._is_wall or nodes[this_node_i_index+1][this_node_j_index]._is_wall or nodes[this_node_i_index][this_node_j_index-1]._is_wall or nodes[this_node_i_index][this_node_j_index+1]._is_wall or nodes[this_node_i_index-1][this_node_j_index-1]._is_wall or nodes[this_node_i_index+1][this_node_j_index-1]._is_wall or nodes[this_node_i_index-1][this_node_j_index+1]._is_wall or nodes[this_node_i_index+1][this_node_j_index+1]._is_wall:
                    neighbor_node._g = neighbor_node._g / 2
                    # neighbor_node._g += 100

            open_nodes.append(neighbor_node)

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
BFS_def_dis_mode_sqrt = False
설명모드 = False
allow_diagonal = False
screen_width = 800
screen_height = 800
grid_interval = 10
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################


screen_start = [960-screen_width//2, 540-screen_height//2]  # pygame 창 왼쪽 모서리 위치

if 설명모드:
    screen_width = 800
    screen_height = 800
    grid_interval = 100


white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
start_col = (0, 255, 0)
end_col = (255, 0, 0)
open_col = (30, 90, 50)
closed_col = (200, 68, 85)


start_x = int((screen_width/5)//grid_interval*grid_interval)
start_y = int((screen_height/2)//grid_interval*grid_interval)
end_x = int((screen_width/5*4)//grid_interval*grid_interval)
end_y = int((screen_height/2)//grid_interval*grid_interval)


nodes = []
for i in range(screen_width//grid_interval):
    nodes.append([])
    for j in range(screen_height//grid_interval):
        nodes[i].append(Node(False, i*grid_interval, j*grid_interval, 0, None, None))


wall = []

##############################################################################################################################
pygame.init()

sysfont = pygame.font.SysFont('malgungothic', 30)
screen = pygame.display.set_mode((screen_width, screen_height))


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

##############################################################################################################################

    if keyboard.is_pressed("a"):
        local_x = pyautogui.position().x - screen_start[0]
        local_y = pyautogui.position().y - screen_start[1]
        if 0<local_x<screen_width and 0<local_y<screen_height and not nodes[local_x//grid_interval][local_y//grid_interval]._is_wall:
            nodes[local_x//grid_interval][local_y//grid_interval]._is_wall = True
            wall.append([local_x//grid_interval*grid_interval, local_y//grid_interval*grid_interval])
            nodes[local_x//grid_interval][local_y//grid_interval].Draw_This_Wall_Node()

    if keyboard.is_pressed("b"):
        local_x = pyautogui.position().x - screen_start[0]
        local_y = pyautogui.position().y - screen_start[1]
        if 0<local_x<screen_width and 0<local_y<screen_height and nodes[local_x//grid_interval][local_y//grid_interval]._is_wall:
            nodes[local_x//grid_interval][local_y//grid_interval]._is_wall = False
            nodes[local_x//grid_interval][local_y//grid_interval].Remove_This_Wall()
            wall.remove([local_x//grid_interval*grid_interval, local_y//grid_interval*grid_interval])


    if keyboard.is_pressed("c"):
        final_path_nodes = []
        wall = []
        init_wall()
        init_search


    if keyboard.is_pressed("i"):
        final_path_nodes = []
        init_search()


    if keyboard.is_pressed("1"):
        final_path_nodes = []
        init_search()
        PathFinding_Astar()
        if final_path_nodes == []:
            print("도착점이 막혀있음")
        time.sleep(0.2)


    if keyboard.is_pressed("2"):
        final_path_nodes = []
        init_search()
        PathFinding_BestFistSearch()
        if final_path_nodes == []:
            print("도착점이 막혀있음")
        time.sleep(0.2)


    if keyboard.is_pressed("3"):
        final_path_nodes = []
        init_search()
        PathFinding_BestFistSearch_PJW()
        if final_path_nodes == []:
            print("도착점이 막혀있음")
        time.sleep(0.2)

##############################################################################################################################

    Draw_start_end()
    if 설명모드:
        Draw_grid()

    pygame.display.flip()