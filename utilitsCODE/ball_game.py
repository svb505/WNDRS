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
def safe_destroy(app):
    for child in app.winfo_children():
        if isinstance(child, ctk.CTkButton):
            if hasattr(child, "_click_animation") and child._click_animation is not None:
                try:
                    child.after_cancel(child._click_animation)
                except Exception:
                    pass
    app.after(50, app.destroy)


WIDTH,HEIGHT = 600,600
FPS = 100
game_over = False
target_size = 20
target_pos = [WIDTH // 4, HEIGHT // 4]
speed_coof = 0.999
ball_radius = 7.0
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_speed = [4.0,0.0]
wall_bounces = 0
target_update = 500
levl = ""
logged = False
show = False

def show_tournament(lang,root):
    rows = connectingDB.get_top_scores("ball",10)
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

    headers = [lang["place"], lang['nameG'], lang['scoreG']]
    for i, header in enumerate(headers):
        label = ctk.CTkLabel(frm, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=i, padx=10, pady=5)

    # Таблица данных
    for index, row in enumerate(rows):
        place = index + 1
        print(f"place - {place} | rowN - {row['name']} | score - {row['score']}")
        ctk.CTkLabel(frm, text=str(place)).grid(row=index + 1, column=0, padx=10, pady=2)
        ctk.CTkLabel(frm, text=row['name']).grid(row=index + 1, column=1, padx=10, pady=2)
        ctk.CTkLabel(frm, text=str(row['score'])).grid(row=index + 1, column=2, padx=10, pady=2)

    btn = ctk.CTkButton(app, text="OK", command=lambda: app.after(50, app.destroy))
    btn.pack()

def logging(data):
    timestamp = datetime.now().strftime('%d_%m_%Y_%H:%M:%S')

    if os.path.exists("games/OpenGLgames/ball/log.txt"):
        with open('games/OpenGLgames/ball/log.txt',"a",encoding='utf-8') as f:
            f.write(f"{timestamp} - {data}\n")
    else:
        with open('games/OpenGLgames/ball/log.txt',"w",encoding='utf-8') as f:
            f.write(f"{timestamp} - {data}\n")
def main_func(name,score,lang,root):
    def render_text(text, x, y,size = 20):
        global WIDTH, HEIGHT
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
        global ball_speed,speed_coof
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[K_UP] and keys[K_LEFT]:
            logging(f"[info] Change direction. Current direction: Up - Left")
            dx = -1
            dy = 1
        elif keys[K_UP] and keys[K_RIGHT]:
            logging(f"[info] Change direction. Current direction: Up - Right")
            dx = 1
            dy = 1
        elif keys[K_DOWN] and keys[K_LEFT]:
            logging(f"[info] Change direction. Current direction: Down - Left")
            dx = -1
            dy = -1
        elif keys[K_DOWN] and keys[K_RIGHT]:
            logging(f"[info] Change direction. Current direction: Down - Right")
            dx = 1
            dy = -1
        # Одиночные стрелки
        elif key == K_LEFT:
            logging(f"[info] ИChange direction. Current direction: Left")
            dx = -1
            dy = 0
        elif key == K_RIGHT:
            logging(f"[info] Change direction. Current direction: Right")
            dx = 1
            dy = 0
        elif key == K_UP:
            logging(f"[info] Change direction. Current direction: Up")
            dx = 0
            dy = 1
        elif key == K_DOWN:
            logging(f"[info] Change direction. Current direction: Down")
            dx = 0
            dy = -1

        if dx == 0 and dy == 0:
            return

        speed = math.hypot(ball_speed[0], ball_speed[1])
        if speed == 0:
            speed = 4.0
        norm = math.hypot(dx, dy)
        ball_speed[0] = dx / norm * speed
        ball_speed[1] = dy / norm * speed
    def init_gl():
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gluOrtho2D(0, WIDTH, 0, HEIGHT)
    def draw_ball(x, y, radius):
        glColor4f(1, 0.5, 0, 1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(37):
            angle = math.radians(i * 10)
            glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
        glEnd()
    def draw_target(x, y, size):

        glColor4f(0, 1, 0, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(x - size / 2, y - size / 2)
        glVertex2f(x + size / 2, y - size / 2)
        glVertex2f(x + size / 2, y + size / 2)
        glVertex2f(x - size / 2, y + size / 2)
        glEnd()
    def restart():
        global target_pos, ball_pos, ball_speed, wall_bounces, game_over,logged
        connectingDB.save_score(name,wall_bounces,"ball")
        logged = False
        target_pos = [WIDTH // 4, HEIGHT // 4]
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_speed = [4.0, 0.0]
        if levl == "1":
            ball_speed[0] = 7.0
        if levl == "2":
            ball_speed[0] = 4.0
        if levl == "3":
            ball_speed[0] = 3.0
        wall_bounces = 0
        game_over = False
    def check_collision(pos, v, r):
        global wall_bounces
        bounced = False
        if pos[0] - r <= 0 or pos[0] + r >= WIDTH:
            v[0] *= -1
            wall_bounces += 1
            bounced = True
        if pos[1] - r <= 0 or pos[1] + r >= HEIGHT:
            v[1] *= -1
            wall_bounces += 1
            bounced = True
        return bounced
    def check_target_hit(ball_pos, target_pos, ball_radius, target_size):
        bx, by = ball_pos
        tx, ty = target_pos
        return (tx - target_size / 2 <= bx <= tx + target_size / 2 and
                ty - target_size / 2 <= by <= ty + target_size / 2)
    def main():
        logging(f"[info] game launch")
        global ball_speed, wall_bounces, game_over,levl,target_update,logged,show
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
        init_gl()
        clock = pygame.time.Clock()
        running = True

        count = 0

        while running:
            count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    connectingDB.save_score(name, wall_bounces,"ball")
                    running = False
                    logging(f"[info] Exit from game")
                elif event.type == KEYDOWN:
                    handle_key(event.key)
                    if event.key == pygame.K_r:
                        restart()
                        logging(f"[info] Restart game")
                    elif event.key == pygame.K_e:
                        connectingDB.save_score(name, wall_bounces,"ball")
                        running = False
                        logging(f"[info] Exit from game")
            if not game_over:
                ball_pos[0] += ball_speed[0]
                ball_speed[0] *= speed_coof
                ball_pos[1] += ball_speed[1]
                ball_speed[1] *= speed_coof
                check_collision(ball_pos, ball_speed, ball_radius)

                if abs(ball_speed[0]) < 0.01 and abs(ball_speed[1]) < 0.01:
                    game_over = True
                if check_target_hit(ball_pos, target_pos, ball_radius, target_size):
                    game_over = True
            glClear(GL_COLOR_BUFFER_BIT)
            draw_ball(ball_pos[0], ball_pos[1], ball_radius)
            draw_target(target_pos[0], target_pos[1], target_size)
            render_text(f"{lang['kolvo_bounced']}: {wall_bounces}",-0.95, 0.9)
            render_text(f"{lang['OPENGL_lvl']}: {levl}", -0.95, 0.80, size=14)
            render_text(f"{lang['OPENGL_speed']}: {math.hypot(ball_speed[0],ball_speed[1]):.2f}", -0.95, 0.85, size=14)
            if count % target_update == 0:
                logging(f"[info] Update target position")
                target_pos[0] = randint(0, WIDTH)
                target_pos[1] = randint(0, HEIGHT)
            if game_over:
                if not logged:
                    logging(f"[info] Score: {wall_bounces}")
                    logging(f"[info] Game over")
                    logged = True
                render_text(f"{lang['game_over:score']}: {wall_bounces}", -0.6, 0.0)
                render_text(f"{lang['OPENGL_GAMES_COPYRIGHT']}", -0.6, -0.1)
                render_text(f"{lang['R_restart']}", -0.6, -0.2)
                render_text(f"{lang['E_exit']}", -0.6, -0.3)
                if not show:
                    show_tournament(lang,root)
                    show = True
                pygame.display.flip()
                pygame.time.wait(100)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
    main()
def startB(root,lang):
    def on_submit(level,name):
        def set_info(lvl,name):
            global ball_speed,target_update,levl
            logging(f"[info] Selected {lvl} level")
            if lvl == "1":
                ball_speed[0] = 7.0
                target_update = 700
            if lvl == "2":
                ball_speed[0] = 4.0
                target_update = 500
            if lvl == "3":
                ball_speed[0] = 3.0
                target_update = 300
            levl = lvl
            app.destroy()
            main_func(name,0,lang,root)
        set_info(level,name)
    def set_info(lvl):
        mes = ""
        if lvl == "1":
            mes = lang["BM_1"]
        if lvl == "2":
            mes = lang['BM_2']
        if lvl == "3":
            mes = lang['BM_2']
        label.configure(frm,text = mes)
    global name_db
    ctk.set_appearance_mode("dark")
    app = ctk.CTkToplevel(root)
    app.title(lang["vhod"])

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
    lbl = ctk.CTkLabel(app,text = lang["B_selectLEVL"])
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
