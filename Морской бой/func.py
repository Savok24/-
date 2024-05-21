from sdl2 import *
from sdl2.ext import *
from sdl2.sdlgfx import *
import random


def draw_table( size_x, size_y, step_x, step_y, size_ip_y, size_ip_x,  windowsurface, offset_x = 0):
    for i in range (0, size_x+1):
        line(windowsurface, (255, 255, 255), ( offset_x +step_x * i,0, offset_x + step_x * i, size_ip_y))
        for i in range (0, size_y+1):
            line(windowsurface, (255, 255, 255), (offset_x, step_y * i, offset_x+ size_ip_x , step_y * i))


def generate_enemy_ships(ships, ship_1, ship_2, ship_3, ship_4, size_x, size_y):
    enemy_ships = []
    ships_list = []
    for i in range (0, ships):
        ships_list.append(random.choice([ship_1, ship_2, ship_3, ship_4 ]))
    #print (ships_list )
    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(size_x + 1)] for i in
                    range(size_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, size_x)
            if primerno_x + len > size_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, size_y)
            if primerno_y + len > size_y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= size_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                            enemy_ships[primerno_y][primerno_x + j] + \
                                            enemy_ships[primerno_y][primerno_x + j + 1] + \
                                            enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                            enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                            enemy_ships[primerno_y + 1][primerno_x + j - 1] + \
                                            enemy_ships[primerno_y - 1][primerno_x + j - 1] + \
                                            enemy_ships[primerno_y + 1][primerno_x + j] + \
                                            enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = len  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= size_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                            enemy_ships[primerno_y + j][primerno_x] + \
                                            enemy_ships[primerno_y + j + 1][primerno_x] + \
                                            enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                            enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                            enemy_ships[primerno_y + 1][primerno_x + j - 1] + \
                                            enemy_ships[primerno_y - 1][primerno_x + j - 1] + \
                                            enemy_ships[primerno_y + j][primerno_x + 1] + \
                                            enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = len  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, size_x):
            for j in range(0, size_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1
    #print(sum_1_enemy)
    #print(ships_list)
    #print(enemy_ships)
    return enemy_ships

def show_enemy(size_x, size_y, enemy_ships1, step_x, step_y, windowsurface):
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                color = Color(255,255,0)
                fill(windowsurface, color, (i * step_x, j * step_y, step_x, step_y))

def show_enemy2(size_x, size_y, enemy_ships2, step_x, step_y, size_ip_x, menu_x, windowsurface):
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                color = Color(255,255,0)
                fill(windowsurface, color, (size_ip_x + menu_x + i * step_x, j * step_y, step_x, step_y))

def draw_point(x, y, step_x, step_y, enemy_ships1, windowsurface, hit):
    #print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0:
        fill(windowsurface, (0, 0, 255), (x * step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
    if enemy_ships1[y][x] > 0:
        line(windowsurface, (255, 0, 0), (x * step_x, y * step_y, step_x * x + step_x, step_y* y + step_y))
        line(windowsurface, (255, 0, 0), (x * step_x + step_x , y  * step_y, step_x * x, step_y* y + step_y))  
        length = 0
        check_kill = 0
        length = enemy_ships1[y][x]
        hit[y][x] = 1
        for i in range(0, length):
            if hit[y + i][x] == 1:
                check_kill += 1
            elif hit[y][x + i] == 1:
                check_kill += 1
            elif hit[y - i][x] == 1:
                check_kill += 1
            elif hit[y][x - i] == 1:
                check_kill += 1
            else:
                i = 5
        print(length)                
        print(check_kill)
        if check_kill == length:
            for i in range(0, length):
                if hit[y + i][x] == 1:
                    fill(windowsurface, (255, 0, 0), (x * step_x + 1, (y + i) * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y][x + i] == 1:
                    fill(windowsurface, (255, 0, 0), ((x + i) *  step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y - i][x] == 1:
                    fill(windowsurface, (255, 0, 0), (x * step_x + 1, (y - i) * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y][x - i] == 1:
                    fill(windowsurface, (255, 0, 0), ((x - i) * step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
                else:
                    check_kill += 0
            check_kill = 0
        else:
            check_kill = 0

def draw_point2(x, y, step_x, step_y, enemy_ships2, windowsurface, size_ip_x, menu_x, hit):
    #print(enemy_ships2[y][x])
    if enemy_ships2[y][x] == 0:
        fill(windowsurface, (0, 0, 255), (size_ip_x + menu_x + x * step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
    if enemy_ships2[y][x] > 0:
        line(windowsurface, (255, 0, 0), (size_ip_x + menu_x + x * step_x, y * step_y, size_ip_x + menu_x + step_x * x + step_x, step_y* y + step_y))
        line(windowsurface, (255, 0, 0), (size_ip_x + menu_x + x * step_x + step_x , y  * step_y, size_ip_x + menu_x + step_x * x, step_y* y + step_y))
        length = 0
        check_kill = 0
        length = enemy_ships2[y][x]
        hit[y][x] = 1
        for i in range(0, length):
            if hit[y + i][x] == 1:
                check_kill += 1
            elif hit[y][x + i] == 1:
                check_kill += 1
            elif hit[y - i][x] == 1:
                check_kill += 1
            elif hit[y][x - i] == 1:
                check_kill += 1
            else:
                i = 5
        print(length)                
        print(check_kill)
        if check_kill == length:
            for i in range(0, length):
                if hit[y + i][x] == 1:
                    fill(windowsurface, (255, 0, 0), (size_ip_x + menu_x + x * step_x + 1, (y + i) * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y][x + i] == 1:
                    fill(windowsurface, (255, 0, 0), (size_ip_x + menu_x + (x + i) *  step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y - i][x] == 1:
                    fill(windowsurface, (255, 0, 0), (size_ip_x + menu_x + x * step_x + 1, (y - i) * step_y + 1, step_x - 1, step_y - 1))
                elif hit[y][x - i] == 1:
                    fill(windowsurface, (255, 0, 0), (size_ip_x + menu_x + (x - i) * step_x + 1, y * step_y + 1, step_x - 1, step_y - 1))
                else:
                    check_kill += 0
            check_kill = 0
        else:
            check_kill = 0


def check_winner(x, y, enemy_ships1, win, size_x, size_y, points1):
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    return win

def check_winner2(x, y, enemy_ships2, win, size_x, size_y, points2):
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    return win
    
def mark_igrok(igrok_mark_1, font_manager, windowsurface, size_ip_x, menu_x, menu_y, width, size_ip_y):
    fill(windowsurface, (0, 0, 0), (0, size_ip_y + 1, width, menu_y))
    player_color1 = Color(0, 0, 0)
    player_color2 = Color(0, 0, 0)
    if igrok_mark_1:
        player_color1 = Color(0, 0, 0)
        player_color2 = Color(0, 200, 200)
        hod_igroka2 = font_manager.render("Ход игрока 2")
        SDL_BlitSurface(hod_igroka2, None, windowsurface, SDL_Rect(width // 2 - hod_igroka2.w // 2, size_ip_y + 5, 0, 0)) 
    else:
        player_color2 = Color(0, 0, 0)
        player_color1 = Color(0, 200, 200)
        hod_igroka1 = font_manager.render("Ход игрока 1")
        SDL_BlitSurface(hod_igroka1, None, windowsurface, SDL_Rect(width // 2 - hod_igroka1.w // 2, size_ip_y + 5, 0, 0))
    player1 = font_manager.render("Игрок 1", bg_color=player_color1)
    player2 = font_manager.render("Игрок 2", bg_color=player_color2)
    SDL_BlitSurface(player1, None, windowsurface, SDL_Rect(size_ip_x // 2 - player1.w // 2, size_ip_y + 5, 0, 0)) 
    SDL_BlitSurface(player2, None, windowsurface, SDL_Rect(size_ip_x + menu_x + size_ip_x // 2 - player1.w // 2, size_ip_y + 5 , 0, 0))
