import subprocess
import sys
import os
import webbrowser
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from games import saper, tetris, kamn
from utilits import coordinat, durak, poker, BsEmpire, ball_game, snakeGame, arkanoid, avtomobils
from utilits import soft

from load_env import load_env

load_env()


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_dir()

def standart_games(root, lang, actives_programs, state_sound, start_time_,
                   volume, errors, global_bg, global_fg, GlobalAlpha):

    type_ = os.getenv("TYPE")

    actives_programs.append("Standart Games")

    Win = Toplevel(root)
    Win.attributes('-alpha', float(GlobalAlpha))
    Win.title(lang.get("standart_games", "Games"))
    Win.geometry('750x500')

    Win.images = {}

    def load_img(key, path):
        if not os.path.exists(path):
            return None

        img = ImageTk.PhotoImage(
            Image.open(path).resize((45, 45), Image.Resampling.LANCZOS)
        )

        Win.images[key] = img
        return img

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

    Label(
        frm_top,
        text=lang.get("standart_games", "Games"),
        font=("Arial", 15, "bold"),
        bg=global_bg,
        fg=global_fg
    ).pack()

    icons = {
        "tetris": load_img("tetris", os.path.join(BASE_DIR, 'icons/tetris.png')),
        "durak": load_img("durak", os.path.join(BASE_DIR, 'icons/interface/durak.png')),
        "coord": load_img("coord", os.path.join(BASE_DIR, 'icons/coordinat.png')),
        "grid3D": load_img("grid3D", os.path.join(BASE_DIR, 'games/coordinatGrid3D/coordinate.png')),
        "saper": load_img("saper", os.path.join(BASE_DIR, 'icons/saper.png')),
        "poker": load_img("poker", os.path.join(BASE_DIR, 'icons/poker.png')),
        "arc": load_img("arc", os.path.join(BASE_DIR, 'icons/asteroid.png')),
        "snake": load_img("snake", os.path.join(BASE_DIR, 'icons/snake.png')),
        "ball": load_img("ball", os.path.join(BASE_DIR, 'icons/ball.png')),
        "BE": load_img("BE", os.path.join(BASE_DIR, 'icons/BE.jpg')),
        "auto": load_img("auto", os.path.join(BASE_DIR, 'icons/Auto.png')),
        "fpv": load_img("fpv", os.path.join(BASE_DIR, 'games/fpvdrone/icon.png')),
        "tank": load_img("tank", os.path.join(BASE_DIR, 'games/tank/icon.png')),
        "checkers": load_img("checkers", os.path.join(BASE_DIR, 'games/checkers/icon.png')),
        "kamn": load_img("kamn", os.path.join(BASE_DIR, 'icons/rock_paper_scissors.png')),
        "mill": load_img("mill", os.path.join(BASE_DIR, 'icons/millionaire.png')),
        "horror": load_img("horror", os.path.join(BASE_DIR, 'icons/horror.png')),
    }

    names = [
        lang.get("tetris", "tetris"),
        lang.get("game_durak", "durak"),
        lang.get("coor_tre", "coord"),
        lang.get("coordinatGrid3D", "grid3D"),
        lang.get("saper", "saper"),
        lang.get("poker_na__", "poker"),
        lang.get("asteroids", "asteroids"),
        lang.get("snakeG", "snake"),
        lang.get("ballG", "ball"),
        lang.get("BEG", "BE"),
        lang.get("automobils", "auto"),
        lang.get("fpvgame", "fpv"),
        lang.get("gametank", "tank"),
        lang.get("checkers", "checkers"),
        lang.get("kamnozhbum", "kamn"),
        lang.get("mill", "mill"),
        lang.get("horror","horror")
    ]

    commands = [
        lambda: tetris(actives_programs, state_sound, volume, errors, root, start_time_, GlobalAlpha),
        lambda: durak.durak(root, lang, start_time_, global_bg, GlobalAlpha),
        lambda: coordinat.main_window(root, lang, start_time_, GlobalAlpha, global_bg),
        lambda: subprocess.Popen(
            [os.path.join(BASE_DIR, "games/coordinatGrid3D/coordinatGrid3D.exe")],
            cwd=os.path.join(BASE_DIR, "games/coordinatGrid3D")
        ),
        lambda: saper(actives_programs, state_sound, volume, errors, lang, root, start_time_, GlobalAlpha),
        lambda: poker.poker(root, lang, start_time_, global_bg, GlobalAlpha),
        lambda: arkanoid.startA(root, lang),
        lambda: snakeGame.start(root, lang),
        lambda: ball_game.startB(root, lang),
        lambda: BsEmpire.BSWin(root, lang),
        lambda: avtomobils.start_func(root, lang),
        lambda: subprocess.Popen(
            [os.path.join(BASE_DIR, "games/fpvdrone/fpvdrone.exe")],
            cwd=os.path.join(BASE_DIR, "games/fpvdrone")
        ),
        lambda: subprocess.Popen(
            [os.path.join(BASE_DIR, "games/tank/tank.exe")],
            cwd=os.path.join(BASE_DIR, "games/tank")
        ),
        lambda: subprocess.Popen(
            [os.path.join(BASE_DIR, "games/checkers/checkers.exe")],
            cwd=os.path.join(BASE_DIR, "games/checkers")
        ),
        lambda: kamn(root, lang, start_time_, global_bg, global_fg, GlobalAlpha),
        lambda: soft.millioner(lang, root, start_time_, global_bg, global_fg, GlobalAlpha),
        lambda: webbrowser.open(os.path.join(BASE_DIR, 'games/horror.html'))
    ]

    frames = [frm_left, frm_right, frm_right1, frm_right2]

    for i, (name, key, cmd) in enumerate(zip(names, icons.keys(), commands)):
        frm = frames[i // 5]

        if name in [lang.get("BEG"),lang.get("game_durak"),lang.get("asteroids"),lang.get("ballG"), lang.get("automobils"),
            lang.get("horror")] and type_ == "FREE":
            continue

        img = icons[key]

        if img:
            lbl = Label(frm, image=img, bg=global_bg)
            lbl.image = img
            lbl.pack()

        ttk.Button(frm, text=name, command=cmd).pack()