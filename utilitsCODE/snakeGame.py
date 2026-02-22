import math
import pygame
from customtkinter import CTkLabel
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint
import customtkinter as ctk
import os
from datetime import datetime
from utilitsCODE import connectingDB

WIDTH,HEIGHT = 600,600
FPS = 100
game_over = False
target_size = 7
target_pos = [WIDTH // 4, HEIGHT // 4]
snake_pos = [WIDTH / 2, HEIGHT / 2]
snake_speed = [2.0,0.0]
segment_count = 1
snake_segments = [[WIDTH / 2, HEIGHT / 2] for _ in range(segment_count)]
levl = ""
logged = False
logged_collision = False
snake_size = 20
show = False
count_score = 0
delay = 10
segment_path = []


def show_tournament(lang,root):
    rows = connectingDB.get_top_scores("snake",10)
    ctk.set_appearance_mode("dark")
    app = ctk.CTkToplevel(root)
    app.title(lang['tournament_table'])

    sc_width = app.winfo_screenwidth()
    sc_height = app.winfo_screenheight()
    x = sc_width // 2
    y = sc_height // 2
    app.resizable(False, False)
    app.geometry(f"450x450+{x}+{y}")

    frm = ctk.CTkFrame(app)
    frm.pack(fill = "both",expand = True)

    headers = [lang['place'], lang["nameG"], lang["scoreG"]]
    for i, header in enumerate(headers):
        label = ctk.CTkLabel(frm, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=i, padx=10, pady=5)

    for index, row in enumerate(rows):
        place = index + 1
        ctk.CTkLabel(frm, text=str(place)).grid(row=index + 1, column=0, padx=10, pady=2)
        ctk.CTkLabel(frm, text=row['name']).grid(row=index + 1, column=1, padx=10, pady=2)
        ctk.CTkLabel(frm, text=str(row['score'])).grid(row=index + 1, column=2, padx=10, pady=2)

    btn = ctk.CTkButton(app, text="OK", command=lambda: app.destroy())
    btn.pack()

    app.mainloop()
def logging(data):
    timestamp = datetime.now().strftime('%d_%m_%Y_%H:%M:%S')

    if os.path.exists("games/OpenGLgames/snake/log_snake.txt"):
        with open('games/OpenGLgames/snake/log_snake.txt',"a",encoding='utf-8') as f:
            f.write(f"{timestamp} - {data}\n")
    else:
        with open('games/OpenGLgames/snake/log_snake.txt',"w",encoding='utf-8') as f:
            f.write(f"{timestamp} - {data}\n")
def main_func(name,score,lang,root):
    global segment_count, delay, segment_path, snake_segments
    def check_hit_himself():
        global snake_pos,snake_segments
        if segment_count > 1:
            if snake_pos in snake_segments[1:]:
                return True
    def render_text(text, x, y, size=20):
        font = pygame.font.SysFont('Courier', size)
        text_surface = font.render(text, True, (1, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        glWindowPos2f((x + 1) * (WIDTH / 2), (y + 1) * (HEIGHT / 2))
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glDisable(GL_BLEND)
    def handle_key(key):
        global snake_speed
        dx = dy = 0
        if key == K_LEFT:
            dx = -1
        elif key == K_RIGHT:
            dx = 1
        elif key == K_UP:
            dy = 1
        elif key == K_DOWN:
            dy = -1

        if dx == 0 and dy == 0:
            return

        speed = math.hypot(snake_speed[0], snake_speed[1])
        if speed == 0:
            speed = 4.0
        norm = math.hypot(dx, dy)
        snake_speed[0] = dx / norm * speed
        snake_speed[1] = dy / norm * speed
    def init_gl():
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gluOrtho2D(0, WIDTH, 0, HEIGHT)
    def draw_target(x, y, radius):
        glColor4f(1, 0.5, 0, 1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(37):
            angle = math.radians(i * 10)
            glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
        glEnd()
    def draw_snake_segments():
        global snake_segments
        for i, (x, y) in enumerate(snake_segments):
            if i == 0:
                glColor4f(0.7, 1, 0, 1)  # Голова
            else:
                glColor4f(0, 1, 0, 1)  # Хвост
            glBegin(GL_QUADS)
            glVertex2f(x - snake_size / 2, y - snake_size / 2)
            glVertex2f(x + snake_size / 2, y - snake_size / 2)
            glVertex2f(x + snake_size / 2, y + snake_size / 2)
            glVertex2f(x - snake_size / 2, y + snake_size / 2)
            glEnd()
    def restart():
        global target_pos, target_size,snake_pos, snake_speed, game_over, logged, segment_path, snake_segments,count_score,segment_count
        logged = False
        count_score = 0
        target_pos = [WIDTH // 4, HEIGHT // 4]
        snake_pos[0], snake_pos[1] = WIDTH / 2, HEIGHT / 2
        snake_speed[0] = 2.0
        snake_speed[1] = 0.0
        if levl == "1":
            snake_speed = [1.0, 0.0]
            target_size = 9
        if levl == "2":
            snake_speed = [2.0, 0.0]
            target_size = 7
        if levl == "3":
            snake_speed = [4.0, 0.0]
            target_size = 5
        game_over = False
        segment_path.clear()
        segment_path.append(snake_pos[:])
        segment_count = 1
        snake_segments = [[WIDTH / 2, HEIGHT / 2] for _ in range(segment_count)]
    def check_collision(pos, v):
        bounced = False
        if pos[0] <= 0 or pos[0] >= WIDTH:
            v[0] *= -1
            bounced = True
        if pos[1] <= 0 or pos[1] >= HEIGHT:
            v[1] *= -1
            bounced = True
        return bounced
    def check_target_hit(snake_pos, target_pos, target_size, snake_size):
        bx, by = snake_pos
        tx, ty = target_pos
        return (tx - snake_size - 10 <= bx <= tx + snake_size + 10 and ty - snake_size - 10 <= by <= ty + snake_size + 10)
    def update_segments():
        for i in range(segment_count):
            index = len(segment_path) - 1 - i * delay
            if index >= 0:
                snake_segments[i] = segment_path[index]
    def main():
        logging(f"[info] Game launch")
        global snake_speed, game_over, levl, logged,logged_collision, show, count_score,segment_count
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
        init_gl()
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    connectingDB.save_score(name,count_score,"snake")
                    running = False
                    logging(f"[info] Exit from game")
                elif event.type == KEYDOWN:
                    handle_key(event.key)
                    if event.key == pygame.K_r:
                        restart()
                        logging(f"[info] Restart game")
                    elif event.key == pygame.K_e:
                        running = False
                        logging(f"[info] Exist from game")
            if check_collision(snake_pos, snake_speed) or check_hit_himself():
                game_over = True
                if not logged_collision:
                    logging("[info] Collision with a wall or with oneself")
                    logged_collision = True

            if not game_over:
                snake_pos[0] += snake_speed[0]
                snake_pos[1] += snake_speed[1]

                # Обновление пути головы
                segment_path.append(snake_pos[:])
                if len(segment_path) > segment_count * delay + 1:
                    segment_path.pop(0)

                update_segments()
                if check_target_hit(snake_pos, target_pos, snake_size, target_size):
                    count_score += 1
                    segment_count += 1
                    logging("[info] 1 apple eaten")
                    global snake_segments
                    snake_segments = [[WIDTH / 2, HEIGHT / 2] for _ in range(segment_count)]
                    update_segments()
                    target_pos[0] = randint(1, WIDTH)
                    target_pos[1] = randint(1, HEIGHT)

            glClear(GL_COLOR_BUFFER_BIT)
            draw_snake_segments()
            draw_target(target_pos[0], target_pos[1], target_size)
            render_text(f"{lang['OPENGL_lvl']}: {levl}", -0.95, 0.80, size=14)
            render_text(f"{lang['OPENGL_speed']}: {math.hypot(snake_speed[0],snake_speed[1]):.2f}", -0.95, 0.85, size=14)

            if game_over:
                if not logged:
                    logging(f"[info] Game over")
                    logged = True
                render_text(f"{lang['kolvoSCORE']}: {count_score}",-0.6,0.0)
                render_text(lang['OPENGL_GAMES_COPYRIGHT'], -0.6, -0.1)
                render_text(f"{lang['R_restart']}", -0.6, -0.2)
                render_text(f"{lang['E_exit']}", -0.6, -0.3)
                connectingDB.save_score(name,count_score,"snake")
                if not show:
                    show_tournament(lang,root)
                    show = True

                pygame.display.flip()
                pygame.time.wait(100)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    main()
def start(root,lang):
    def on_submit(level,name):
        def set_info(lvl,name):
            global snake_speed,levl,target_size
            logging(f"[info] Selected {lvl} level")
            if lvl == "1":
                snake_speed = [1.0,0.0]
                target_size = 9
            if lvl == "2":
                snake_speed = [2.0,0.0]
                target_size = 7
            if lvl == "3":
                snake_speed = [4.0,0.0]
                target_size = 5
            levl = lvl
            app.destroy()
            main_func(name,0,lang,root)
        set_info(level,name)
    def set_info(lvl):
        mes = ""
        if lvl == "1":
            mes = lang['SM_1']
        if lvl == "2":
            mes = lang["SM_2"]
        if lvl == "3":
            mes = lang["SM_3"]
        label.configure(frm,text = mes)
    global name_db
    ctk.set_appearance_mode("dark")
    app = ctk.CTkToplevel(root)
    app.title(lang['vhod'])

    sc_width = app.winfo_screenwidth()
    sc_height = app.winfo_screenheight()
    x = sc_width // 2
    y = sc_height // 2
    app.resizable(False,False)
    app.geometry(f"350x300+{x}+{y}")
    user_name = ""
    lbl = ctk.CTkLabel(app, text=lang['enter_name'])
    lbl.pack()
    name = ctk.CTkEntry(app, placeholder_text=lang['enter_name'], width=100)
    name.pack(pady=20)
    name.insert(0,user_name)
    lbl = ctk.CTkLabel(app,text = lang['B_selectLEVL'])
    lbl.pack()
    level = ctk.CTkComboBox(app,values = ["1","2","3"],command=lambda event:set_info(level.get()))
    level.pack(pady=20)
    level.configure(state="readonly")
    frm = ctk.CTkFrame(app)
    frm.pack(fill = "x")
    label = CTkLabel(frm,text = "")
    label.pack()
    set_info(level.get())
    btn = ctk.CTkButton(app, text="OK", command=lambda:on_submit(level.get(),name.get()))
    btn.pack()

    app.mainloop()
