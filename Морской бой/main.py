from sdl2 import *
from sdl2.ext import *
from sdl2.sdlgfx import *
import random
import func


def main():
    init()

    size_ip_x = 600
    size_ip_y = 600
    size_x = size_y = 10 # Размер игрового поля
    step_x= size_ip_x // size_x # шаг по горизонтали
    step_y= size_ip_y // size_y # шаг по вертикали
    delta_menu_x = 3
    menu_x = step_x * delta_menu_x
    menu_y = 50
    size_ip_x = 600
    size_ip_y = 600
    width = size_ip_x + menu_x + size_ip_x
    height = size_ip_y + menu_y

    window = Window("Морской бой", (width, height), flags=SDL_WINDOW_SHOWN)
    window.show()
    # Создание рендера
    renderer = Renderer(window, backend=-1)
    set_texture_scale_quality(method="best")
    factory = SpriteFactory(TEXTURE, renderer=renderer)

    windowsurface = window.get_surface()
    selected_y = -1
    selected_x = -1
    ships = size_x // 2 # определяем количество кораблей
    ship_1 = 1
    ship_2 = 2
    ship_3 = 3
    ship_4 = 4
    enemy_ships1 = [[0 for i in range (size_x + 1)] for i in range (size_y + 1)]
    enemy_ships2 = [[0 for i in range (size_x + 1)] for i in range (size_y + 1)]
    points1 = [[-1 for i in range(size_x)] for i in range(size_y)] # список куда мы кликнули мышкой
    points2 = [[-1 for i in range(size_x)] for i in range(size_y)]
    hit = [[5 for i in range(15)] for i in range(15)] # список попаданий по кораблям противника
    win = False
    hod_igrovomu_polu_1 = False #если Истина - то ходит игрок 2, иначе ходит игрок 1
    computer_vs_human = True # computer_vs_human - если Истина - то играем против компьютера
    running = True
    enemy_ships1 = func.generate_enemy_ships(ships, ship_1, ship_2, ship_3, ship_4, size_x, size_y)
    enemy_ships2 = func.generate_enemy_ships(ships, ship_1, ship_2, ship_3, ship_4, size_x, size_y)

    font_manager = FontManager(font_path="./Prosto_Sans_Bold.ttf", size=32, color=(255, 255, 255))
    win_player = font_manager.render("Победил игрок 1!", bg_color=(148, 0, 211), size=100)
    win_player2 = font_manager.render("Победил игрок 2!", bg_color=(148, 0, 211), size=100)


    #func.show_enemy(size_x, size_y, enemy_ships1, step_x, step_y, windowsurface, )
    #func.show_enemy2(size_x, size_y, enemy_ships2, step_x, step_y, size_ip_x, menu_x, windowsurface)
    func.draw_table( size_x, size_y, step_x, step_y, size_ip_y, size_ip_x, windowsurface)
    func.draw_table( size_x, size_y, step_x, step_y, size_ip_y, size_ip_x, windowsurface, size_ip_x + menu_x)
    func.mark_igrok(hod_igrovomu_polu_1, font_manager, windowsurface, size_ip_x, menu_x, menu_y, width, size_ip_y)

    while running:
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if event.button.button == SDL_BUTTON_LEFT:
                    selected_y = event.button.y // step_y
                    selected_x = event.button.x // step_x
                    #print(f"Выбрана клетка: [{selected_x}, {selected_y}]")
                    if selected_x < size_x and selected_y < size_y and hod_igrovomu_polu_1:
                        if points1[selected_y][selected_x] == -1:
                            points1[selected_y][selected_x] = 1
                            hod_igrovomu_polu_1 = False
                            func.draw_point(selected_x, selected_y, step_x, step_y, enemy_ships1, windowsurface, hit)
                            if func.check_winner(selected_x, selected_y, enemy_ships1, win, size_x, size_y,points1):
                                hod_igrovomu_polu_1 = True
                                print ('Победил игрок 2')
                                SDL_BlitSurface(win_player2, None, windowsurface, SDL_Rect(width // 2 -win_player2.w // 2 , height // 2 - win_player2.h, 0, 0)) 
                                points1 = [[10 for i in range(size_x)] for i in range(size_y)]
                                points2 = [[10 for i in range(size_x)] for i in range(size_y)]  

                    if selected_x >= size_x + delta_menu_x and selected_y < size_y and not hod_igrovomu_polu_1:
                        if points2[selected_y][selected_x -  size_x - delta_menu_x] == -1:
                            points2[selected_y][selected_x  - size_x - delta_menu_x] = 1
                            hod_igrovomu_polu_1 = True
                            func.draw_point2(selected_x - size_x - delta_menu_x, selected_y, step_x, step_y, enemy_ships2, windowsurface, size_ip_x, menu_x, hit)
                            if func.check_winner2(selected_x, selected_y, enemy_ships2, win, size_x, size_y, points2):
                                hod_igrovomu_polu_1 = False
                                print ('Победил игрок 1')
                                SDL_BlitSurface(win_player, None, windowsurface, SDL_Rect(width // 2 -win_player.w // 2 , height // 2 - win_player.h, 0, 0)) 
                                points2 = [[10 for i in range(size_x)] for i in range(size_y)]
                                points1 = [[10 for i in range(size_x)] for i in range(size_y)]
                            elif computer_vs_human:
                                func.mark_igrok(hod_igrovomu_polu_1, font_manager, windowsurface, size_ip_x, menu_x, menu_y,  width, size_ip_y)
                                hod_igrovomu_polu_1 = False
                                selected_x = random.randint(0, size_x - 1)
                                selected_y = random.randint(0, size_y - 1)
                                while not points1[selected_y][selected_x] == -1:
                                    selected_x = random.randint(0, size_x-1)
                                    selected_y = random.randint(0, size_y-1)
                                points1[selected_y][selected_x] = 7
                                func.draw_point(selected_x, selected_y, step_x, step_y, enemy_ships1, windowsurface, hit)
                                if func.check_winner(selected_x, selected_y, enemy_ships1, win, size_x, size_y, points1):
                                    print ('Победил игрок 2')
                                    SDL_BlitSurface(win_player2, None, windowsurface, SDL_Rect(width // 2 -win_player2.w // 2 , height // 2 - win_player2.h, 0, 0)) 
                                    points1 = [[10 for i in range(size_x)] for i in range(size_y)]
                                    points2 = [[10 for i in range(size_x)] for i in range(size_y)]  
                func.mark_igrok(hod_igrovomu_polu_1, font_manager, windowsurface, size_ip_x, menu_x, menu_y,  width, size_ip_y)

        window.refresh()
if __name__ == "__main__":
    main()
