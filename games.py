import sqlite3
import time
from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk
from logtofile import log_to_file
from play_sound import play_sound

WIDTH = 1200
number = 0
value = 0.0
fps_s = 1
HEIGHT = 900
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
NUM_STARS = 1000
SPEED = 0.01
ROWS, COLS, MINES = 9, 9, 10
WIDTH = 10
HEIGHT = 20
BLOCK_SIZE = 30
current_position = [0, 0]
GAME_SPEED = 1000
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # Т-образная
    [[1, 1], [1, 1]],        # Квадрат
    [[1, 1, 0], [0, 1, 1]],  # Z-образная
    [[0, 1, 1], [1, 1, 0]],  # S-образная
    # и так далее...
]

COLORS = ["red", "blue", "green", "yellow", "purple", "cyan", "orange"]
buttons = []
board = []
timer_running = False
start_time = None
game_over = False
current_shape = None
current_color = None
current_step = 50
background_color = "white"
main_line_color = "black"
line_color = "grey"
text_color = "black"
fill_line = "red"
fill_text = "blue"
color_dot = "blue"
global_color = None
color = None
main_theme = "White"
chif_x = True
chif_y = True
level = "2"
booster_active = False
last_booster_activation_time = None
flag = False

ident = ""
call_count = 0
turn = 0
dice_canvas_ids = []
check_vars = []
roll_count = 0
players = []
scores = []
obligatory_scores = []
matches_played = []
chosen_nominals = []
chosen_combinations = []
phase = "obligatory"
background_color_ = "White"
color_dice = "Red"
activefill_dice = "Yellow"
color__ = None
last_booster_activation_time_ = None
booster_active_ = False
dialog_roll = None
dialog_combination = None
dice_values = [random.randint(1, 6) for _ in range(5)]
points0 = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
conn = sqlite3.connect("configurations.db")
cursor = conn.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT
        )
""")
conn.commit()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

if users:
    user = users[0]
    n, ln, e = user[1], user[2], user[3]
else:
    n = ln = e = "Unknown"

username = n
score_pc = 0
score_user = 0

def tetris(actives_programs,state_sound,volume,errors,root,start_time_,GlobalAlpha):
    actives_programs.append("Tetris")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    global game_over, score, current_shape, current_position, current_color, board
    game_over = False
    score = 0
    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    current_shape = None
    current_position = [0, 0]
    current_color = None

    log_to_file("Tetris launch",start_time_=start_time_)
    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title("Tetris")
    Win.focus_set()
    img = Image.open("icons/tetris.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    canvas = Canvas(Win, width=WIDTH * BLOCK_SIZE, height=HEIGHT * BLOCK_SIZE)
    canvas.pack()

    def new_shape():
        global current_shape, current_position, current_color
        current_shape = random.choice(SHAPES)
        current_color = random.choice(COLORS)
        current_position = [0, WIDTH // 2 - len(current_shape[0]) // 2]

        if check_collision():
            global game_over
            game_over = True
            canvas.create_text(WIDTH * BLOCK_SIZE // 2, HEIGHT * BLOCK_SIZE // 2, text="GAME OVER", fill="red",
                               font=('Arial', 24))
    def check_collision():
        """Проверка столкновений с границами или другими фигурами"""
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pos_x = current_position[1] + x
                    pos_y = current_position[0] + y
                    if pos_x < 0 or pos_x >= WIDTH or pos_y >= HEIGHT or (pos_y >= 0 and board[pos_y][pos_x]):
                        return True
        return False
    def freeze():
        global score
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    board[current_position[0] + y][current_position[1] + x] = current_color
        remove_full_lines()
        new_shape()
        if check_collision():
            global game_over
            game_over = True
            canvas.create_text(WIDTH * BLOCK_SIZE // 2, HEIGHT * BLOCK_SIZE // 2, text="GAME OVER", fill="red",
                               font=('Arial', 24))
    def remove_full_lines():
        global score
        lines_to_remove = [i for i, row in enumerate(board) if all(cell != 0 for cell in row)]
        lines_removed = len(lines_to_remove)

        for i in lines_to_remove:
            del board[i]
            board.insert(0, [0] * WIDTH)
        score += lines_removed
    def move_left(event=None):
        """Передвижение фигуры влево"""
        current_position[1] -= 1
        if check_collision():
            current_position[1] += 1
    def move_right(event=None):
        """Передвижение фигуры вправо"""
        current_position[1] += 1
        if check_collision():
            current_position[1] -= 1
    def move_down(event=None):
        """Передвижение фигуры вниз"""
        current_position[0] += 1
        if check_collision():
            current_position[0] -= 1
            freeze()
    def rotate(event=None):
        global current_shape
        current_shape = [list(row) for row in zip(*current_shape[::-1])]
        if check_collision():
            current_shape = [list(row) for row in zip(*current_shape[::-1])][::-1]
    def draw_board():
        canvas.delete("all")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if board[y][x]:
                    canvas.create_rectangle(
                        x * BLOCK_SIZE, y * BLOCK_SIZE,
                        (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                        fill=board[y][x], outline="black"
                    )
    def draw_current_shape():
        """Отрисовка текущей фигуры"""
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    canvas.create_rectangle(
                        (current_position[1] + x) * BLOCK_SIZE,
                        (current_position[0] + y) * BLOCK_SIZE,
                        (current_position[1] + x + 1) * BLOCK_SIZE,
                        (current_position[0] + y + 1) * BLOCK_SIZE,
                        fill=current_color,
                        outline="black"
                    )
    def update_game():
        if not game_over:
            move_down()
            draw_board()
            draw_current_shape()
            canvas.create_text(50, 10, text=f"Score: {score}", fill="black", font=('Arial', 14))
            Win.after(GAME_SPEED, update_game)
    Win.bind("<Left>", move_left)
    Win.bind("<Right>", move_right)
    Win.bind("<Down>", move_down)
    Win.bind("<Up>", rotate)

    new_shape()
    update_game()
def saper(actives_programs,state_sound,volume,errors,lang,root,start_time_,GlobalAlpha):
    actives_programs.append("Saper")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    def create_board():
        global board
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        mines_placed = 0
        while mines_placed < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if board[r][c] != 'M':
                board[r][c] = 'M'
                mines_placed += 1
                for i in range(r - 1, r + 2):
                    for j in range(c - 1, c + 2):
                        if 0 <= i < ROWS and 0 <= j < COLS and board[i][j] != 'M':
                            board[i][j] += 1
    def update_mine_count():
        count = MINES - len(flags)
        mine_label.config(text=lang["mins-10"] + str(count))
    def update_timer():
        if timer_running:
            elapsed = int(time.time() - start_time)
            timer_label.config(text=f"{lang['time']}: {elapsed} сек")
            roott.after(1000, update_timer)
    def flag(event, r, c):
        try:
            if buttons[r][c]["state"] == "disabled":
                return
        except IndexError:
            return

        if (r, c) in flags:
            buttons[r][c].config(text="")
            flags.remove((r, c))
        else:
            buttons[r][c].config(text="⚑", fg="blue")
            flags.add((r, c))
        update_mine_count()
    def reveal(r, c):
        try:
            if buttons[r][c]["state"] == "disabled" or (r, c) in flags:
                return
        except IndexError:
            return

        buttons[r][c].config(state="disabled")
        val = board[r][c]
        if val == 'M':
            buttons[r][c].config(text="*", bg="red")
            game_over(False)
        else:
            buttons[r][c].config(text=str(val) if val > 0 else "", bg="lightgray")
            if val == 0:
                for i in range(r - 1, r + 2):
                    for j in range(c - 1, c + 2):
                        if 0 <= i < ROWS and 0 <= j < COLS:
                            reveal(i, j)
        check_win()
    def check_win():
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] != 'M' and buttons[i][j]["state"] != "disabled":
                    return
        game_over(True)
    def game_over(won):
        global timer_running
        timer_running = False
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] == 'M':
                    buttons[i][j].config(text="*", bg="red")
                buttons[i][j].config(state="disabled")
        msg = lang["you-win"] if won else lang['you-lose']
        log_to_file("Game over",start_time_=start_time_)
        log_to_file(msg,start_time_=start_time_)
        result_label.config(text=msg)
    def restart():
        play_sound("sound//click.mp3",volume,state_sound,start_time_)
        log_to_file("Saper has been restarted",start_time_=start_time_)

        global flags, start_time, timer_running, buttons

        for row in buttons:
            for btn in row:
                btn.destroy()
        flags = set()
        create_board()

        buttons = []
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                btn = Button(grid_frame, width=3, height=1, font=("Arial", 10),
                             command=lambda r=i, c=j: reveal(r, c))
                btn.grid(row=i, column=j)
                btn.bind("<Button-3>", lambda e, r=i, c=j: flag(e, r, c))
                row.append(btn)
            buttons.append(row)

        result_label.config(text="")
        update_mine_count()
        start_time = time.time()
        timer_running = True
        update_timer()
    log_to_file('Saper launch',start_time_=start_time_)
    global buttons, flags, timer_running, start_time, board
    roott = Toplevel(root)
    roott.attributes("-alpha",float(GlobalAlpha))
    roott.title(lang["saper"])
    img = Image.open("icons/saper.png")
    icon_image = ImageTk.PhotoImage(img)
    roott.iconphoto(False, icon_image)
    top_frame = Frame(roott)
    top_frame.pack()

    mine_label = Label(top_frame, text=lang['mins-10'], font=("Arial", 12))
    mine_label.pack(side="left", padx=10)

    timer_label = Label(top_frame, text=lang["time-0sec"], font=("Arial", 12))
    timer_label.pack(side="left", padx=10)

    restart_btn = Button(top_frame, text=lang["restart_"], command=restart)
    restart_btn.pack(side="left", padx=10)

    grid_frame = Frame(roott)
    grid_frame.pack()

    for i in range(ROWS):
        row = []
        for j in range(COLS):
            btn = Button(grid_frame, width=3, height=1, font=("Arial", 10),
                         command=lambda r=i, c=j: reveal(r, c))
            btn.grid(row=i, column=j)
            btn.bind("<Button-3>", lambda e, r=i, c=j: flag(e, r, c))
            row.append(btn)
        buttons.append(row)

    result_label = Label(roott, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    restart()
def kamn(root,lang,start_time_,global_bg,global_fg,GlobalAlpha):
    def game(hod, lbl,sp):
        global score_user, score_pc
        pc = random.choice(sp)

        if hod == sp[0] and pc == sp[0]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["nic3"]))
        elif hod == sp[1] and pc == sp[1]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["nic2"]))
        elif hod == sp[2] and pc == sp[2]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["nic1"]))
        elif hod == sp[0] and pc == sp[1]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["you_win4"]))
            score_user += 1
        elif hod == sp[0] and pc == sp[2]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["pc_win3"]))
            score_pc += 1
        elif hod == sp[1] and pc == sp[0]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["pc_win2"]))
            score_pc += 1
        elif hod == sp[1] and pc == sp[2]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["you_win2"]))

            score_user += 1
        elif hod == sp[2] and pc == sp[0]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["you_win1"]))
            score_user += 1
        elif hod == sp[2] and pc == sp[1]:
            lbl.config(text=lang["pc_vib"])
            Win.after(1000, lambda: lbl.config(text=lang["pc_win1"]))
            score_pc += 1
        Win.after(1000,
                  lambda: score.config(text=f"{lang['sccore']}: {lang['PC']}-{score_pc}     {lang['USER']}-{score_user}", font=("Arial", 14, "bold")))


    sp = [lang["nozh"],lang['bumaga'],lang["kamen"]]

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.title(lang["kamnozhbum"])
    Win.geometry("400x300")
    img = Image.open("icons/kamn.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    btn1 = ttk.Button(Win,text=lang["kamen"], command=lambda: game(sp[2], lbl,sp)).pack()
    btn2 = ttk.Button(Win,text=lang['bumaga'], command=lambda: game(sp[0], lbl,sp)).pack()
    btn3 = ttk.Button(Win,text=lang["nozh"], command=lambda: game(sp[1], lbl,sp)).pack()

    lbl = Label(Win,text="",fg = global_fg,bg = global_bg)
    lbl.pack()
    score = Label(Win,fg = global_fg,bg = global_bg,text=f"{lang['sccore']}: {lang['PC']}-{score_pc}     {lang['USER']}-{score_user}", font=("Arial", 14, "bold"))
    score.pack()
    Win.mainloop()