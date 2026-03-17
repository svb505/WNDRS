import subprocess
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from games import saper, tetris,kamn
from utilits import coordinat, durak, poker, BsEmpire, ball_game, snakeGame, arkanoid, avtomobils
from utilits import soft
import os
from load_env import load_env

load_env()

def standart_games(root, lang, actives_programs, state_sound, start_time_, volume, errors, global_bg, global_fg,
                   GlobalAlpha):
    type = os.getenv("TYPE")

    actives_programs.append("Standart Games")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    Win = Toplevel(root)
    Win.attributes('-alpha', float(GlobalAlpha))
    Win.geometry('750x500')

    img = Image.open(os.path.join(BASE_DIR, "icons/interface/games.png"))
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    frm_top = Frame(Win)
    frm_top.pack(fill=X, side=TOP)
    frm_left = Frame(Win)
    frm_left.pack(side=LEFT)
    frm_right = Frame(Win)
    frm_right.pack(side=LEFT)
    frm_right1 = Frame(Win)
    frm_right1.pack(side=LEFT)
    frm_right2 = Frame(Win)
    frm_right2.pack(side=LEFT)

    Win.tetris = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/tetris.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.durak = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/interface/durak.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.coord = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/coordinat.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.saper = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/saper.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.poker = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/poker.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.arc = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/asteroid.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.snake = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/snake.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.ball = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/ball.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.BE = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/BE.jpg')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.Auto = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/Auto.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.fpv = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'games/fpvdrone/icon.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.tank = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'games/tank/icon.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.checkers = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'games/checkers/icon.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.grid3D = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'games/coordinatGrid3D/coordinate.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )
    Win.kamn = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/rock_paper_scissors.png')).resize((45, 45),Image.Resampling.LANCZOS)
    )
    Win.mill = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/millionaire.png')).resize((45, 45), Image.Resampling.LANCZOS)
    )

    images = [Win.tetris, Win.durak, Win.coord,Win.grid3D, Win.saper, Win.poker,Win.arc, Win.snake, Win.ball, Win.BE, Win.Auto,
              Win.fpv, Win.tank,Win.checkers,Win.kamn,Win.mill]
    names = [lang["tetris"], lang["game_durak"], lang["coor_tre"],lang["coordinatGrid3D"], lang["saper"], lang["poker_na__"],
             lang["asteroids"], lang["snakeG"], lang["ballG"], lang["BEG"], lang['automobils'],
             lang["fpvgame"], lang["gametank"],lang["checkers"],lang["kamnozhbum"],lang["mill"]]
    commands = [lambda: tetris(actives_programs, state_sound, volume, errors, root, start_time_, GlobalAlpha),
                lambda: durak.durak(root, lang, start_time_, global_bg, GlobalAlpha),
                lambda: coordinat.main_window(root, lang, start_time_, GlobalAlpha, global_bg),
                lambda: subprocess.Popen(
                    [os.path.join(BASE_DIR, "games/coordinatGrid3D/coordinatGrid3D.exe")],
                    cwd=os.path.join(BASE_DIR, "games/coordinatGrid3D")
                ),
                lambda: saper(actives_programs, state_sound, volume, errors, lang, root, start_time_, GlobalAlpha),
                lambda: poker.poker(root, lang, start_time_, global_bg,GlobalAlpha),
                lambda: arkanoid.startA(root, lang),
                lambda: snakeGame.start(root, lang),
                lambda: ball_game.startB(root, lang),
                lambda: BsEmpire.BSWin(root, lang),
                lambda: avtomobils.start_func(root, lang),
                lambda: subprocess.Popen([os.path.join(BASE_DIR, "games/fpvdrone/fpvdrone.exe")],
                        cwd=os.path.join(BASE_DIR, "games/fpvdrone")),
                lambda: subprocess.Popen(
                [os.path.join(BASE_DIR, "games/tank/tank.exe")],
                cwd=os.path.join(BASE_DIR, "games/tank")),
                lambda: subprocess.Popen([os.path.join(BASE_DIR, "games/checkers/checkers.exe")],
                     cwd=os.path.join(BASE_DIR, "games/checkers")),
                lambda:kamn(root, lang, start_time_, global_bg, global_fg, GlobalAlpha),
                lambda:soft.millioner(lang, root,start_time_, global_bg, global_fg, GlobalAlpha)
        ]

    Label(frm_top, text=lang["standart_games"], font=("Arial", 15, "bold"), bg=global_bg, fg=global_fg).pack()

    for i, (name, image, com) in enumerate(zip(names, images, commands)):
        frm = ""
        if i < 5:
            frm = frm_left
        elif i < 10:
            frm = frm_right
        elif i < 15:
            frm = frm_right1
        elif i < 20:
            frm = frm_right2
        if name in [lang["BEG"],lang["game_durak"],lang["asteroids"],lang["ballG"],lang['automobils']] and type == "FREE":
            pass
        else:
            Label(frm, image=image, bg=global_bg, fg=global_fg).pack()
            ttk.Button(frm, text=name, command=com).pack()
