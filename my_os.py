import json
import win32gui
import win32process
import win32api
import winreg
import ecran_block
from show_error import show_error
import shutil
from show_screenshoots import OpenWindow
from show_screenrecords import OpenWindowRec
from utilits import user_send_email
import sys
from create_window import create_window
from pass_manager import manager
from excos import shutdown_animation
from achievements import ach
from speedtest import speedtest
from photoviewer import photo_viewer
import pyautogui
from videplayer import video_player
from wlps import draw_galaxy, draw_night_sky, draw_gradient, anim_galaxy
import threading
import numpy as np
from dateutil.relativedelta import relativedelta
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog,Scale,simpledialog
from datetime import datetime, date, timedelta
import random
import os
from send_email import send_email
import time
from PIL import Image, ImageTk, ImageGrab
from runinthread import run_in_thread
from server_statistick import update_file,update_elpsed
from logtofile import log_to_file,log_system
from github import Github
from play_sound import play_sound
from crypto_work import generate_key,load_key,encrypt_message,decrypt_message,read_encrypted_file,write_encrypted_file
from copy_file_to_folder import copy_file_to_folder
import logging
from readandwrite_to_files import read_file,write_file
from load_env import load_env
import importlib
from transactions import transactions
from create_change_log import win_changelogs
from view_change_logs import WinDow
from tkcalendar import Calendar
from download_sdk import download_funcs
from load_cursor import load_cursor
from hwid_work import check_did
from fadeinout import fade_in,fade_out
from autostartconfigs import remove_exe_from_autostart,add_exe_to_autostart
from save_and_load_balance import save_balance,load_balance
from validate_hashes import check

start_time_ = time.time()
module_folder = "utilits"
for file in os.listdir(module_folder):
    if file.endswith((".py", ".pyd")) and not file.startswith("__"):
        name = file.split(".")[0]
        try:
            globals()[name] = importlib.import_module(f"utilits.{name}")
        except Exception as e:
            print(f"MODULE NOT FOUND: {e}")
            log_to_file(f"MODULE NOT FOUND: {e}",start_time_,level = "error")
t0 = time.perf_counter()

if False:
    from utilits import soft
    from utilits import commandConsole
    from utilits import standart_games
    from utilits import settings_funcs
    from utilits import bsod
    from utilits import browser
    from utilits import antvrs
    from utilits import SVBantvrs
    from utilits import bank
    from utilits import globalchat
    from utilits import messanger
    from utilits import techSupport
    from utilits import ides
    from utilits import file_manager
    from utilits import activity_center
    from utilits import cloud
    from utilits import t_manager
    from utilits import clocks
    from utilits import VPN
    from utilits import GetWifiInfo
    from utilits import activity_control
    from utilits import archivator
    from utilits import BookMaker
    from utilits import buy_num
    from utilits import book
    from utilits import cleaning
    from utilits import casino
    from utilits import cases
    from utilits import hotels
    from utilits import historys
    from utilits import gos
    from utilits import photo_editor
    from utilits import SVBStore
    from utilits import svbtube
    from utilits import deliv
    from utilits import os_diagnost
    from utilits import trade
    from utilits import svbred

load_env()

token = os.getenv('TOKEN_FOR_USERS')
repo_name = os.getenv('STAT_REPO')
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_GIST_ID = os.getenv("GIST_ID")
GITHUB_GIST_FILENAME = os.getenv("GIST_FNAME")

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
try: base_dir = os.path.dirname(os.path.realpath(__file__))
except NameError: base_dir = os.getcwd()

user_langs = []
user_color = []
user_icons = []
ll_n = []
paths = []
names = []

def state_cache(data):
    if os.path.exists("state/logs.cache"):
        try: write_file("state/logs.cache", "a", f"{data}\n")
        except Exception as e: log_to_file(str(e), level="error", start_time_=start_time_)
    else:
        try: write_file("state/logs.cache","w",f"{data}\n")
        except Exception as e: log_to_file(str(e), level="error", start_time_=start_time_)

if not os.path.exists("syst_comp/syst.key"): generate_key()
else: key = load_key()

errors = ["80010X10","80020X10","80030X10","80040X10","80050X10","80060x10"]
errors_bsod = ["AZ0001x001","AZ0020x001","FZ0001x001","TY0001x001"]
def load_valid_languages_encrypted(filepath="syst_comp/valids/vld_l.cfg"):
    global user_langs
    decrypted_lines = read_encrypted_file(filepath)
    base_langs = {"RU", "EN", "FR", "UA", "IT", "ES", "DE","PT","PL","ALB","SRB","BY","TUR",
                  'BG',"HU","RO","CN","CS","JP"}

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line and clean_line not in base_langs:
            user_langs.append(clean_line)
    return set(line.strip() for line in decrypted_lines.splitlines() if line.strip())
def load_valid_colors_encrypted(filepath="syst_comp/valids/vld_c.cfg"):
    global user_color

    decrypted_lines = read_encrypted_file(filepath)

    base_langs ={"#2C3E50","red","yellow","green","#808000","#D2691E","#00BFFF","#DAA520","#FF6347","#FF1493","#800080","FFA500","#00FF00"}

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line and clean_line not in base_langs:
            user_color.append(clean_line)
    return set(line.strip() for line in decrypted_lines.splitlines() if line.strip())
def load_valid_icons_encrypted(filepath="syst_comp/valids/vld_wlp.cfg"):
    global ll_n
    decrypted_lines = read_encrypted_file(filepath)

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line:
            ll_n.append(clean_line)
    return set(line.strip() for line in decrypted_lines.splitlines() if line.strip())
def load_paths_encrypted(filepath="syst_comp/valids/vld_path_wlp.cfg"):
    global paths
    decrypted_lines = read_encrypted_file(filepath)

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line:
            paths.append(clean_line)
    return paths
def load_names_encrypted(filepath="syst_comp/valids/vld_wlp.cfg"):
    global names
    decrypted_lines = read_encrypted_file(filepath)

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line:
            names.append(clean_line)
    return names
def load_images_icons_encrypted(filepath="syst_comp/valids/vld_icons.cfg"):
    global user_icons
    decrypted_lines = read_encrypted_file(filepath)

    base_langs ={"icons//acc3.png","icons//acc1.png","icons//myacc.png","icons//acc8.png","icons//acc2.png","icons//acc4.png","icons//acc5.png","icons//acc6.png","icons//acc7.png"}

    for line in decrypted_lines.splitlines():
        clean_line = line.strip()
        if clean_line and clean_line not in base_langs:
            user_icons.append(clean_line)
    return set(line.strip() for line in decrypted_lines.splitlines() if line.strip())

valid_lang = load_valid_languages_encrypted()
valid_colors = load_valid_colors_encrypted()
valid_icons = load_images_icons_encrypted()
valid_wlp_paths = load_names_encrypted()
valid_wlp_names = load_paths_encrypted()

valid_region = {"netherlans","usa","france","russia","hungry","italia",'australia',"canada"}
valid_size = {"32","42","52","64","76","84"}

flags = set()

with open("versions/current_version.txt",'r') as f: ver = f.read()

VERSION = f"{ver}"
nebo = False
ban_time = 0
totalAttemps = 3
currentAttemp = 0
all_programs_list = ["Photo Generator",'SVB PhotoEditor','SVB Hotels',"SVB History's",'SVB Bookmaker',"Internet Store","SVB Archiver",
                         "Book reader","SVB TxT Redactor","Password Manager","Trade","Promocodes","Lottery","State Services","Auto plate",
                         "Delivery", "Telephone", "Telegrom", "VPN", "Paint", "Casino", "SVB Antivirus", "Translator",
                         "IDE Universal", "IDE Python", "IDE C++", "IDE C", "IDE C#", "IDE HTML CSS",
                         "IDE JavaScript", "IDE Java", "IDE SQL", "IDE GO", "IDE Kotlin", "IDE Rust",
                         "IDE Ruby", "IDE Swift", "IDE PHP", "IDE TypeScript"]
ban_timer = False
shortcut_frame = None
timer_running = False
stopwatch_running = False
stopwatch_time = timedelta()
exclusive_bac = False
galaxy = False
galaxy_ = False
paused = False
is_on = False
showed = False
is_recording = False
state_sound = False
update_button_added = False
mes_count = False
blinking = False
progress_window = None
progress_bar = None
invisible_pass = False
current_song = None
vpn_win = None
vpn_label = None
email_state = True
wifi_button = None
canvas_icon = None
lang_win = None
layout_label = None
cursor_id = None
block_state = False
change_state = False
recording_thread = None
recording_indicator = None
recording_window = None
img = None
tooltip = None
photo = None
antvrs_state = True
aut = None
active_wifi_win = False
wifi_win = None
sound_win = None
sound_but = None
clock_win = None
bat_win = None
battery_bt = None
battery_label = None
clock_label = None
calendar_win = None
date_label = None
auto_update_enabled = False
image_wallpeper = False
timeoutEcran = 300000
GlobalAlpha = 100
timer_id = None
img_path_pass = ""
image_wallpeper_pass = False
paths_pass = []
level_svb = 0
night_state = 0
RAM = 16
ROM=1024
svb_coins = 0
count = 0
count_casino = 5
LoggingSett = 0
MAX_ROWS = 0
taskbar_height = 0
timer_time = 0
active_bg = "#34495e"
mute_state = ''
user_volume = ''
current_playlist = ""
TASKBAR_CONFIG_FILE = "syst_comp/taskbar_config.json"
img_path = ""
account_img = "icons//myacc.png"
edition = ""
clock_type = ""
tema = ""
lang = ""
gl_police = ""
preview_sys = ""
preview_clock = ""
color = ""
last_layout = ""
global_bg = ""
global_fg = ""
tbColor = ""
taskbar_bg = ''
taskbar_fg = ''
path_wlp = ""
win_theme = ""
clock = ""
icon_refs = {}
config = {}
setting_key = {}
icons = {}
LANGUAGES = {
    0x419: 'RU',         # Russian
    0x409: 'ENG(US)',    # English (United States)
    0x809: 'ENG(UK)',    # English (United Kingdom)
    0x40c: 'FR',         # French
    0x422: 'UA',         # Ukrainian
    0x41c: 'ALB',        # Albanian
    0x816: 'PRTG(PT)',   # Portuguese (Portugal)
    0x416: 'PRTG(BR)',   # Portuguese (Brazil)
    0x40a: 'SP(TR)',     # Spanish (Traditional Sort)
    0x0c0a: 'SP(MD)',    # Spanish (Mexico)
    0x410: 'IT',         # Italian
    0x401: 'ARB',        # Arabic (Saudi Arabia)
    0x403: 'DE',         # German (Germany)
    0x407: 'IT(CH)',     # Italian (Switzerland)
    0x1004: 'ZH(CHT)',   # Chinese Traditional
    0x813: 'PTG',        # Portuguese (General)
    0x414: 'SV',         # Swedish
    0x412: 'NL',         # Dutch
    0x40d: 'HE',         # Hebrew
    0x424: 'BE',         # Belarusian
    0x425: 'BG',         # Bulgarian
    0x426: 'CS',         # Czech
    0x427: 'DA',         # Danish
    0x428: 'DE',         # German (Austria)
    0x429: 'ET',         # Estonian
    0x42a: 'FI',         # Finnish
    0x42b: 'FR',         # French (Belgium)
    0x42c: 'FR',         # French (Canada)
    0x42d: 'HU',         # Hungarian
    0x42e: 'IS',         # Icelandic
    0x42f: 'IT',         # Italian (Switzerland)
    0x430: 'KO',         # Korean
    0x431: 'LV',         # Latvian
    0x432: 'LT',         # Lithuanian
    0x433: 'NO',         # Norwegian (Bokmål)
    0x434: 'PL',         # Polish
    0x435: 'PT',         # Portuguese (Brazil)
    0x436: 'RO',         # Romanian
    0x437: 'RU',         # Russian
    0x438: 'HR',         # Croatian
    0x439: 'SK',         # Slovak
    0x440: 'SL',         # Slovenian
    0x441: 'SQ',         # Albanian
    0x442: 'SR',         # Serbian (Latin)
    0x443: 'SV',         # Swedish
    0x444: 'TH',         # Thai
    0x445: 'TR',         # Turkish
    0x446: 'UK',         # Ukrainian
    0x447: 'BE',         # Belarusian
    0x800: 'CY',         # Welsh
    0x804: 'ZH',         # Chinese Simplified
    0x808: 'ZH',         # Chinese Traditional
}
playlist = {}
ROWS_MAP = {"32": 9, "42": 9, "52": 9, "64": 8, "76": 6, "84": 5}
labels = []
special_frames = []
actives_programs = []
taskbar_buttons = []

clock = str(read_encrypted_file("syst_comp/plc_clk.cfg"))

if os.path.exists("icons"): pass
else: messagebox.showerror(f'Error {errors[1]}',"No folder 'icons' in dirrectory!")
def set_rows(size_sh):
    global MAX_ROWS
    MAX_ROWS = ROWS_MAP.get(size_sh, 9)
log_system(f"START TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",start_time_)
log_system("All Global Variables (AGV) initialized",start_time_)
def init_database():
    global wifi, bluetooth, vpn, state_sound, log_inform,aut

    with sqlite3.connect("configurations.db") as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS states (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                vpn TEXT, wifi TEXT, bluetooth TEXT
            )
        ''')
        cursor.execute("INSERT INTO states (vpn, wifi, bluetooth) VALUES (?, ?, ?)", ("on", "on", "on"))
        conn.commit()

        cursor.execute("SELECT wifi FROM states")
        wifi = cursor.fetchone()[0]
        cursor.execute("SELECT bluetooth FROM states")
        bluetooth = cursor.fetchone()[0]
        cursor.execute("SELECT vpn FROM states")
        vpn = cursor.fetchone()[0]

        cursor.execute('''CREATE TABLE if not EXISTS SOUND_STATE(sound INTEGER)''')
        conn.commit()
        cursor.execute("SELECT sound FROM SOUND_STATE")
        result = cursor.fetchone()
        s = result[0] if result else 1
        state_sound = (s == 0)

        try:
            cursor.execute("SELECT * FROM LOG_INFO")
            log_inform = cursor.fetchone()
        except sqlite3.Error as e:
            log_to_file(f"Database error: {e}", level="error",start_time_ = start_time_)
            log_inform = None
        try:
            cursor.execute("SELECT * FROM AUT_STATE")
            aut = cursor.fetchone()
        except sqlite3.Error as e:
            log_to_file(f"Database error: {e}", level="error",start_time_ = start_time_)
            aut = None

        try:
            cursor.execute("SELECT * FROM night")
            row = cursor.fetchone()
            handle_night_mode(row[0])
        except Exception as e:
            log_to_file(str(e),level="error",start_time_=start_time_)
            handle_night_mode(0)

    copy_file_to_folder("configurations.db", "backup_data",start_time_)
    log_system("DB Disconnect",start_time_)
def load_config_files():
    global size_sh, edition,value,fps_s,tema,account_img,clock_type,mute_state,user_volume,LoggingSett
    try:
        LoggingSett = int(read_encrypted_file("syst_comp/log_set.cfg"))
    except:
        write_encrypted_file("syst_comp/log_set.cfg", "0")
        LoggingSett = int(read_encrypted_file("syst_comp/log_set.cfg"))
    try:
        mute_state = str(read_encrypted_file("syst_comp/mute.cfg"))
    except:
        write_encrypted_file("syst_comp/mute.cfg", "False")
        mute_state = str(read_encrypted_file("syst_comp/mute.cfg"))
    try:
        user_volume = str(read_encrypted_file("syst_comp/user_v.cfg"))
    except:
        write_encrypted_file("syst_comp/user_v.cfg", "0")
        user_volume = str(read_encrypted_file("syst_comp/user_v.cfg"))
    try:
        clock_type = str(read_encrypted_file("syst_comp/format_clk.cfg"))
    except:
        write_encrypted_file("syst_comp/format_clk.cfg", "hhmmss")
        clock_type = str(read_encrypted_file("syst_comp/format_clk.cfg"))
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/format_clk.cfg", "backup_data",start_time_)

    try:
        value = float(read_encrypted_file("syst_comp/gamebar_settings/gamebar_p.cfg"))
    except:
        write_encrypted_file("syst_comp/gamebar_settings/gamebar_p", "1.0")
        value = float(read_encrypted_file("syst_comp/gamebar_settings/gamebar_p.cfg"))
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/gamebar_settings/gamebar_p.cfg", "backup_data",start_time_)
    try:
        fps_s = int(read_encrypted_file("syst_comp/gamebar_settings/gamebar_shw_inf.cfg"))
    except:
        write_encrypted_file("syst_comp/gamebar_settings/gamebar_shw_inf", "1")
        fps_s = 1
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/gamebar_settings/gamebar_shw_inf.cfg", "backup_data",start_time_)
    try:
        tema = int(read_encrypted_file("syst_comp/gamebar_settings/gamebar_theme.cfg"))
    except:
        write_encrypted_file("syst_comp/gamebar_settings/gamebar_theme.cfg", "d")
        tema = 'd'
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/gamebar_settings/gamebar_theme.cfg", "backup_data",start_time_)
    try:
        size_sh = read_file("syst_comp/size.cfg",'r').strip()
    except:
        write_file("syst_comp/size.cfg",'w','52')
        size_sh = "52"
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/size.cfg", "backup_data",start_time_)

    try:
        account_img = read_file("syst_comp/icons.cfg", 'r').strip()
        log_to_file(f'Account image: {account_img}',start_time_ = start_time_)
    except Exception as e:
        log_to_file(str(e), level="error", start_time_=start_time_)
    try:
        decrypted_text = read_encrypted_file("syst_comp/parametrs.bin")
        config = dict(line.strip().split("=") for line in decrypted_text.strip().splitlines())
        edition = config.get("EDITION", "N/A")
    except Exception as e:
        log_to_file(f'Error with open or decode parametrs.bin: {e}', level="error",start_time_ = start_time_)
def validate_log_size():
    import logger_setup as lsetup
    global system_handler
    if log_inform and log_inform[0] == 1:
        if os.path.exists("syst_comp/system_log.log"):
            size_mb = os.path.getsize('syst_comp/system_log.log') / (1024 * 1024)
            if size_mb > 4.0:
                try:
                    lsetup.system_logger.removeHandler(system_handler)
                    system_handler.close()
                    write_file("syst_comp/system_log.log",'w',"")
                    new_handler = logging.FileHandler("syst_comp/system_log.logh", encoding='utf-8')
                    new_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
                    lsetup.system_logger.addHandler(new_handler)
                    system_handler = new_handler
                    lsetup.system_logger.info("System log file was cleared due to large size.")
                except Exception as e:
                    lsetup.system_logger.error(f"Error clearing system log: {e}")
            else: lsetup.system_logger.info(f"Log size OK: {size_mb:.2f} MB")
        else: lsetup.system_logger.warning("System log file does not exist.")
def set_device_states():
    global wifi_state, bluetooth_state

    wifi_state = (wifi == "on")
    bluetooth_state = (bluetooth == "on")

    log_system(f"WIFI --> {wifi_state}",start_time_)
    log_system(f"BLUETOOTH --> {bluetooth_state}",start_time_)
def load_secure_configs():
    global custom_wallpeper, gl_police,preview_sys

    try:
        decrypted_data = read_encrypted_file("exclusive.wndrs").strip()
        custom_wallpeper = (decrypted_data == "YES")
    except:
        custom_wallpeper = False

    try:
        gl_police = read_encrypted_file("syst_comp/plc_sys.cfg")
        preview_sys = gl_police = read_encrypted_file("syst_comp/plc_sys.cfg")
    except:
        gl_police = "Arial"
        preview_sys = "Arial"
def validate_cfg_files():
    def validate(value, valid_set, filename):
        if value not in valid_set:
            show_error(f"Error {errors[2]}: invalid data in {filename}")
            bsod.open_bsod(errors_bsod[2], 'ERROR WITH FILES')
    def str_to_bool(value):
        return value == "True"
    def safe_read(func, *args, default=None, fatal=True):
        try:
            return func(*args)
        except Exception as e:
            if fatal:
                show_error(str(e))
                bsod.open_bsod(errors_bsod[2], f'ERROR WITH FILES: {e}')
            else:
                log_to_file(str(e), level="error", start_time_=start_time_)
            return default

    global number, color, image_wallpeper, img_path, auto_update_enabled
    global win_theme, antvrs_state, email_state, showed
    global block_state, change_state, GlobalAlpha, tbColor, invisible_pass

    key = load_key()

    invisible_pass = str_to_bool(safe_read(read_encrypted_file, "syst_comp/invisible_pass.cfg"))

    tbColor = safe_read(read_encrypted_file, "syst_comp/tb_color.cfg")

    GlobalAlpha = int(float(safe_read(read_encrypted_file, "syst_comp/alpha.cfg"))) / 100

    block_state = str_to_bool(safe_read(read_encrypted_file, "syst_comp/block_ecran.cfg"))

    change_state = str_to_bool(safe_read(read_encrypted_file, "syst_comp/change_wlp_state.cfg"))

    showed = str_to_bool(safe_read(read_encrypted_file, "syst_comp/showed.cfg"))

    antvrs_state = str_to_bool(safe_read(read_encrypted_file, "syst_comp/antvrs_state.cfg"))

    auto_update_enabled = str_to_bool(safe_read(read_file, "syst_comp/auto_upd.cfg", 'r').strip())

    win_theme = decrypt_message(safe_read(read_file, "syst_comp/win_theme.cfg", 'rb').strip(),key)

    email_state = str_to_bool(safe_read(read_encrypted_file, "syst_comp/email_state.cfg"))

    color = safe_read(read_file, "syst_comp/color.cfg", 'r').strip()
    validate(color, valid_colors, "color.cfg")

    image_wallpeper = safe_read(read_encrypted_file, "syst_comp/img_wlp.cfg", fatal=False) != "FALSE"

    img_path = safe_read(read_encrypted_file, "syst_comp/path_wlp.cfg", fatal=False)

    size = safe_read(read_file, "syst_comp/size.cfg", 'r').strip()
    validate(size, valid_size, "size.cfg")

    number = float(safe_read(read_encrypted_file, "syst_comp/volume.cfg"))
def initialize_system_state():
    log_system("Connect to states.db",start_time_)
    init_database()
    load_config_files()
    set_device_states()
    load_secure_configs()
    validate_log_size()
    validate_cfg_files()
def load_activity_control():
    try:
        max_minutes = int(read_encrypted_file("syst_comp/max_minutes.cfg"))
    except:
        max_minutes = None

    try:
        next_date = read_encrypted_file("syst_comp/control_nxt_date.cfg")
    except:
        next_date = None

    try:
        updation_days = read_encrypted_file("syst_comp/updation_days.cfg")
    except:
        updation_days = None

    return max_minutes, next_date, updation_days
def initialize_system_state_async():
    import threading
    threading.Thread(target=initialize_system_state, daemon=True).start()
def handle_night_mode(night_value):
    global night_state, global_bg, global_fg,taskbar_bg,taskbar_fg,tbColor
    if night_value == 0:
        night_state = 0
        global_bg = "white"
        global_fg = "black"
        taskbar_bg = tbColor
        taskbar_fg = "#3e5870"
    else:
        night_state = 1
        global_bg = "black"
        global_fg = "white"
        taskbar_bg = "#000000"
        taskbar_fg = '#2a2929'

initialize_system_state_async()
log_system("ALL SYSTEMS FILES READS",start_time_)
def return_user_info():
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
    else: n = ln = e = "Unknown"
    return n,ln,e
def is_blocked():
    try:
        unblock_time = read_encrypted_file("syst_comp/control_nxt_date.cfg")
        unblock_time = datetime.strptime(unblock_time, "%d-%m-%Y %H:%M:%S")
        if datetime.now() < unblock_time: return True

    except:
        return False
    return False
def main():
    global shortcut_frame,ROWS_MAP,antvrs_state,LoggingSett,win_theme,vpn_win,stopwatch_time,stopwatch_running,valid_wlp_names,valid_wlp_paths,\
        taskbar_fg,taskbar_bg,taskbar_buttons,auto_update_enabled,img_path,image_wallpeper,user_langs,nebo,global_bg,\
        blinking,cursor_id,global_fg, exclusive_bac,state_sound, galaxy, galaxy_, edition, custom_wallpeper, wifi_state, \
        size_sh, number, lang,bluetooth_state,clock,night_state,GlobalAlpha,is_recording,recording_thread,showed,icons,module_folder, \
    invisible_pass
    def block_user():
        try:
            days = int(read_encrypted_file("syst_comp/updation_days.cfg"))
        except:
            days = 1
        unblock_time = datetime.now() + timedelta(days=days)
        write_encrypted_file("syst_comp/control_nxt_date.cfg",
                             unblock_time.strftime("%d-%m-%Y %H:%M:%S"))

        messagebox.showwarning("Time limit", f"{lang['limit!2']} {days} {lang['dn']}.")
        root.destroy()
    def set_icons():
        global icons
        icons = {
            "file_manager": "icons//filemanager.png",
            "cleaning": "icons/cleaning.png",
            "video_player": 'icons//videoread.png',
            "photov": "icons/svb_photo.png",
            "globalchat": "icons/interface/glchat.png",
            "CMD": "icons//cmd.png",
            "standart_games": "icons/interface/games.png",
            "SVB SpeedTest": "icons/interface/speed.png",
            "calculator": "icons//calculator.png",
            "browser": "icons//browser.png",
            "store": "icons//store.png",
            "antivirus": "icons//antivirus.png",
            "notepad": "icons//notebook.png",
            "case": "icons//cases.png",
            "pod1": "icons//tech_support.png",
            "task_manager": "icons//disp.png",
            "mus_pl1":"icons//mediaplayer.png",
            "bank": "icons/bank.png",
            "SVBTube": "icons//svbtube.png",
        }
    def on_activity(event=None):
        global timer_id
        if timer_id is not None: root.after_cancel(timer_id)

        start_timer()
    def block_ecran_no_act():
        global timeoutEcran
        Win = create_window(root,"",'#170E0E',float(GlobalAlpha),100,100,None,True)
        Label(Win,text=f"{lang['you_bee_inactivited']} {timeoutEcran//1000} {lang['sec']}\n{lang['press_any_key_to_continue']}",
              bg='#170E0E', fg="white",font=("Arial", 40, "bold")).pack()
        Win.bind_all("<KeyPress>", lambda event: Win.destroy())
    def start_timer():
        global timer_id
        timer_id = root.after(timeoutEcran,block_ecran_no_act)
    def check_activity_limit():
        global start_time_

        max_minutes, next_date, upd_days = load_activity_control()
        if max_minutes:
            elapsed_minutes = int((time.time() - start_time_) / 60)
            if elapsed_minutes >= max_minutes:
                messagebox.showwarning("Time limit", lang["limit!"])
                block_user()
        root.after(60000, check_activity_limit)
    def load_language(lang_code=""):
        try:
            with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
                langs = json.load(file)
            if lang_code not in langs:
                log_to_file(f"Error: language {lang_code} not found, use RU",start_time_ = start_time_)
                return langs["RU"]
        except Exception as e:
            messagebox.showerror(f"Error {errors[0]}",f"Error with lang.json! {e}")
            log_to_file("No file lang.json",level="error",start_time_ = start_time_)
        return langs[lang_code]
    def check_ach():
        global svb_coins
        svb_coins = load_balance(start_time_)

        conn = sqlite3.connect("achievements.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name, status, max, prize FROM achievements")
        rows = cursor.fetchall()

        for name, status, max_val, prize in rows:
            if status == "no" and svb_coins >= max_val:
                svb_coins += int(prize)
                transactions(f"-{prize} SVB Coins",start_time_)
                update_file("count_svbcoins.txt",int(prize))
                save_balance(svb_coins,start_time_)
                cursor.execute(
                    "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                    (svb_coins, "yes", name)
                )
                conn.commit()
                messagebox.showinfo(lang["success"],lang["ach_tr"] + str(prize))

        conn.close()
    log_system("----START OS----",start_time_)
    log_system(f'VERSION OS --> {VERSION}',start_time_)
    SETTINGS_FILE = "syst_comp/gamebar_settings/settings.json"
    c = ""
    try:
        selected_lang = read_encrypted_file("syst_comp/lang.cfg").strip()
    except Exception:
        messagebox.showerror(f'Error {errors[0]}',
                             "No file lang.cfg in directory! We created this file, or you can copy this file from folder 'backup_data'")
        log_to_file("No file lang.cfg in directory", level="error",start_time_ = start_time_)
        selected_lang = "EN"
        write_encrypted_file("syst_comp/lang.cfg", selected_lang)
        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/lang.cfg", "backup_data",start_time_)

    lang = load_language(selected_lang)
    set_icons()
    news_list_ = [
        lang["news1"], lang["news2"], lang["news3"], lang["news4"], lang["news5"],
        lang["news6"], lang["news7"], lang["news8"], lang["news9"], lang["news10"],
        lang["news11"], lang["news12"], lang["news13"], lang["news14"], lang["news15"],
        lang["news16"], lang["news17"], lang["news18"], lang["news19"], lang["news20"],
    ]
    volume = max(0.0, min(1.0, number / 100))
    log_system(f"CURRENT LANGUE --> {selected_lang}",start_time_)
    log_system(f'VOLUME --> {volume}',start_time_)


    def create_database():
        log_system('CREATE "CONFIGURATIONS.DB"',start_time_)
        if not os.path.exists('configurations.db'):
            log_system('DB not EXIST',start_time_)
            conn = sqlite3.connect('configurations.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              rarity TEXT NOT NULL)''')

            conn.commit()
            conn.close()
            log_system("DB Created",start_time_)
            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("configurations.db", "backup_data",start_time_)
                log_system("Copy file: configurations.db",start_time_)

        else:
            conn = sqlite3.connect('configurations.db')
            cursor = conn.cursor()
            log_system("Connect to configurations.db",start_time_)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory';")
            table_exists = cursor.fetchone()
            if not table_exists:
                cursor.execute('''CREATE TABLE inventory (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT NOT NULL,
                                  rarity TEXT NOT NULL)''')
                conn.commit()
            conn.close()
    create_database()
    def read_inventory_from_db():
        log_to_file("READ INVENTORY",start_time_ = start_time_)
        conn = sqlite3.connect('configurations.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["theme_"],))
        result_nebo = cursor.fetchone()
        cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["galaxy"],))
        result_galaxy = cursor.fetchone()
        cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["galaxy_"],))
        result_galaxy_ = cursor.fetchone()
        nebo = result_nebo is not None
        galaxy = result_galaxy is not None
        galaxy_ = result_galaxy_ is not None
        conn.close()
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
        return galaxy, nebo,galaxy_

    if os.path.exists('configurations.db'): galaxy, nebo,galaxy_ = read_inventory_from_db()
    try:
        reg = read_file("syst_comp/region.cfg", 'r').strip()
    except:
        reg = "usa"
    if reg == "usa":
        reg = lang["usa"]
        log_system("Region SET 'USA'",start_time_)
    elif reg == "netherlans":
        reg = lang["netherlans"]
        log_system("Region SET 'NETHERLANDS'",start_time_)
    elif reg == "france":
        reg = lang["france"]
        log_system("Region SET 'FRANCE'",start_time_)
    elif reg == "russia":
        reg = lang["russia"]
        log_system("Region SET 'RUSSIA'",start_time_)
    elif reg == "hungry":
        reg = lang["hungry"]
        log_system("Region SET 'HUNGRY'",start_time_)
    elif reg == "italia":
        reg = lang["italia"]
        log_system("Region SET 'ITALIA'",start_time_)
    elif reg == "canada":
        reg = lang["canada"]
        log_system("Region SET 'CANADA'",start_time_)
    else:
        reg = lang['australia']
        log_system("Region SET 'AUSTRALIA'",start_time_)
    def update_time():
        global clock,clock_type
        if clock_type == "hhmm": current_time = datetime.now().strftime("%H:%M")
        else: current_time = datetime.now().strftime("%H:%M:%S")

        clock_label.config(text=current_time,font = (clock,18,"bold"))
        root.after(1000, update_time)
    def remove_shortcut(program_name):
        pass
    def open_store():
        global all_programs_list
        run_in_thread(play_sound("sound//click.mp3",volume,state_sound,start_time_))
        actives_programs.append("Store")
        log_to_file('Store launch',start_time_ = start_time_)

        win = create_window(root,lang["store"], global_bg, float(GlobalAlpha), 1200, 600, "icons/store.png")
        Label(win, text=lang["select_program"], font=("Arial", 14, "bold"),bg=global_bg,fg=global_fg).pack(pady=10)

        canvas_frame = Frame(win,bg=global_bg)
        canvas_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        canvas = Canvas(canvas_frame,bg=global_bg)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        main_frame = Frame(canvas,bg = global_bg,padx=10, pady=10)
        canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        installed_frame = Frame(win, bg="#dff0d8", padx=10, pady=10, relief=RIDGE, bd=2)
        installed_frame.pack(padx=10, pady=10, fill=BOTH)

        Label(installed_frame, text=lang["downloaded"], font=("Arial", 12, "bold"), bg="#dff0d8").pack(pady=5)

        def download(program_name):
            if program_name not in installed_programs:
                if program_name == "SVB Antivirus":
                    global svb_coins
                    svb_coins = load_balance(start_time_)
                    if svb_coins > 2000:
                        svb_coins -= 2000
                        transactions("-2.000 SVb Coins"+f" {datetime.now()}",start_time_)
                        save_balance(svb_coins,start_time_)
                        log_to_file(f'Program {program_name} downloaded',start_time_ = start_time_)
                        write_file(installed_programs_file,"a",program_name)
                        messagebox.showinfo(lang["success"], lang['program'] + " " + program_name + " " + lang["downloaded"],parent=win)
                        log_to_file(f'Message: {lang["program"] + " " + program_name + " " + lang["downloaded"]}',start_time_ = start_time_)

                        installed_programs.append(program_name)
                        icons[program_name] = f"icons//{program_name.lower()}.png"

                        place_shortcuts(size_sh,MAX_ROWS,color)
                        refresh_buttons()
                    else:
                        messagebox.showerror(lang["error"],"Your balace is less than 2000 SVB Coins",parent=win)
                        log_to_file(f"Message: Your balance is less than 2000 SVB Coins", level="warning",start_time_ = start_time_)
                log_to_file(f'Program {program_name} downloaded',start_time_ = start_time_)
                write_file(installed_programs_file,"a",program_name)
                messagebox.showinfo(lang["success"], lang['program'] + " " + program_name + " " + lang["downloaded"],parent=win)
                log_to_file(f'Message: {lang["program"] + " " + program_name + " " + lang["downloaded"]}',start_time_ = start_time_)

                installed_programs.append(program_name)
                icons[program_name] = f"icons//{program_name.lower()}.png"

                place_shortcuts(size_sh,MAX_ROWS,color)
                refresh_buttons()
        def remove_program(program_name):
            global svb_coins
            run_in_thread(play_sound("sound//no.mp3", volume, state_sound, start_time_))
            if program_name in installed_programs:
                if program_name == "SVB Antivirus" or program_name == "Translator":
                    svb_coins = load_balance(start_time_)
                    svb_coins += 2000
                    update_file("count_svbcoins.txt", 2000)
                    transactions("+2.000 SVb Coins"+f" {datetime.now()}",start_time_)
                    save_balance(svb_coins,start_time_)
                    check_ach()
                log_to_file(f'Program {program_name} removed',start_time_ = start_time_)
                installed_programs.remove(program_name)
                write_file(installed_programs_file,"w","\n".join(installed_programs)+"\n")
                icons.pop(program_name, None)

                remove_shortcut(program_name)
                place_shortcuts(size_sh,MAX_ROWS,color)
                refresh_buttons()

                messagebox.showinfo(lang['deleted'], lang["program"] + " " + program_name + " " + lang["deleted"],parent=win)
                log_to_file(f'Message: {lang["program"] + " " + program_name + " " + lang["deleted"]}',start_time_ = start_time_)
        def refresh_buttons():
            for widget in main_frame.winfo_children():
                widget.destroy()

            column_count = 2
            row, col = 0, 0

            for name in all_programs_list:
                path = f"icons//{name.lower()}.png"
                try:
                    if os.path.exists(path):
                        img = Image.open(path)
                        img = img.resize((64, 64), Image.Resampling.LANCZOS)
                        icon = ImageTk.PhotoImage(img)
                    else: icon = None

                except Exception as e:
                    icon = None
                    log_to_file(f"Load Image Error {name}: {e}",level="warning",start_time_ = start_time_)

                frame = Frame(main_frame,bg = global_bg, padx=10, pady=5)
                frame.grid(row=row, column=col, padx=5, pady=5, sticky="w")

                if icon:
                    lbl = Label(frame, image=icon, fg = global_fg,bg = global_bg)
                    lbl.image = icon
                    lbl.pack(side="left", padx=5)

                label_text = f"{lang['downloaded']}" if name in installed_programs else name
                btn = Label(frame, text=label_text, fg="green" if name in installed_programs else "black",
                            font=("Arial", 11, "bold"), bg="white")
                btn.pack(side="right", padx=5)

                if name in installed_programs:
                    remove_btn = Button(frame, text=f"{lang['delete']} {name}", font=("Arial", 10),
                                        bg="#f44336", fg="white",
                                        command=lambda n=name: remove_program(n))
                    remove_btn.pack(side="right", padx=5)
                else:
                    download_btn = Button(frame, text=f"{lang['download']} {name}" + (
                        " 2000 SVB Coins" if name in ["SVB Antivirus", "Translator"] else ""),
                                          font=("Arial", 10), bg="#007bff", fg="white",
                                          command=lambda n=name: download(n))
                    download_btn.pack(side="right", padx=5)

                col += 1
                if col >= column_count:
                    col = 0
                    row += 1
        refresh_buttons()
    def on_closing():
        log_system("----SHUT DOWN OS----",start_time_)
        global is_recording, recording_thread
        if is_recording:
            is_recording = False
            recording_thread = False
        for i in actives_programs:
            log_to_file(f'Program {i} close',start_time_ = start_time_)
        try:
            elapsed = time.time() - start_time_
        except NameError:
            elapsed = 0
        n,ln,e = return_user_info()
        update_file("time_in_windoors.txt",int(elapsed))
        update_file(f"time_{e}.txt", int(elapsed))
        update_elpsed("max_time.txt", int(elapsed))
        root.destroy()
    def toggle_wifi_window():
        global wifi_win, wifi_button

        if wifi_win and wifi_win.winfo_exists():
            fade_out(wifi_win)
            wifi_button.config(bg=taskbar_bg)
            wifi_win = None
        else: open_network_simulator()
    def toggle_vpn():
        global vpn_win, vpn_label

        if vpn_win and vpn_win.winfo_exists():
            vpn_win.destroy()
            vpn_win = None
            vpn_label.config(bg=taskbar_bg)
        else:
            vpn_label.config(bg = taskbar_fg)
            VPN.open_vpn(root,lang,actives_programs,start_time_,volume,state_sound,edition,global_bg,global_fg,reg,GlobalAlpha)
    def toggle_sound_window():
        global sound_win, sound_but

        if sound_win and sound_win.winfo_exists():
            fade_out(sound_win)
            sound_win = None
            sound_but.config(bg=taskbar_bg)
        else: sound_bar()
    def toggle_clock():
        global clock_win, clock_label

        if clock_win and clock_win.winfo_exists():
            clock_win.destroy()
            clock_win = None
            clock_label.config(bg=taskbar_bg)
        else:
            clock_label.config(bg=taskbar_fg)
            clocks.open_clocks(root,lang,clock_type, gl_police, global_bg, global_fg, clock_win)
    def toggle_bat():
        global bat_win, battery_bt,battery_label

        if bat_win and bat_win.winfo_exists():
            fade_out(bat_win)
            bat_win = None
            battery_label.config(bg=taskbar_bg)
            battery_bt.config(bg=taskbar_bg)
        else:
            show_battery_info()
    def show_lang():
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        global lang_win, layout_label, LANGUAGES,taskbar_height
        layout_label.config(bg=taskbar_fg)

        lang_win = Toplevel(root)
        lang_win.attributes('-alpha',0.0)
        fade_in(lang_win)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 650 - 100
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset - 250
        lang_win.geometry(f"650x350+{x}+{y}")
        lang_win.overrideredirect(True)
        lang_win.title(lang["raskl"])

        img = Image.open("icons/interface/raskl.png")
        icon_image = ImageTk.PhotoImage(img)
        lang_win.iconphoto(False, icon_image)

        def get_keyboard_layouts():
            """Получить список доступных раскладок из реестра"""
            layouts = {}
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r"SYSTEM\CurrentControlSet\Control\Keyboard Layouts")
                i = 0
                while True:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        layout_text, _ = winreg.QueryValueEx(subkey, "Layout Text")
                        layouts[subkey_name] = layout_text
                    except FileNotFoundError:
                        layouts[subkey_name] = "Unknown"
                    i += 1
            except OSError:
                pass
            return layouts
        def switch_layout(hkl_str):
            hkl = user32.LoadKeyboardLayoutW(hkl_str, 1)
            if hkl == 0:
                pass
            else:
                res = user32.ActivateKeyboardLayout(hkl, 0)
                if res == 0:
                    log_to_file(f"Failed to switch layout {hkl_str}",level="error",start_time_ = start_time_)
                else:
                    log_to_file(f"Layout switched to {layouts[hkl_str]}",start_time_ = start_time_)
        def on_radio_change_update():
            hkl_str = var.get()
            switch_layout(hkl_str)
            layout_label.config(text=layouts[hkl_str])
            current_label.config(text=f"{lang['tek-ras']}: {layouts[hkl_str]}")
        layouts = get_keyboard_layouts()
        var = StringVar()

        current_hkl_int = user32.GetKeyboardLayout(0)
        current_hkl_str = f"{current_hkl_int & 0xFFFFFFFF:08x}".upper()
        header_label = ttk.Label(lang_win, text=lang["raskl"], font=("Segoe UI", 16, "bold"))
        header_label.pack(pady=(10, 5))
        current_label = ttk.Label(lang_win, text=lang['tek-ras_n'], font=("Segoe UI", 12))
        current_label.pack(pady=(0, 10))

        frame = ttk.Frame(lang_win, padding=10)
        frame.pack(fill='both', expand=True)

        canvas = Canvas(frame)
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        radio_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=radio_frame, anchor='nw')

        if current_hkl_str in layouts:
            var.set(current_hkl_str)
            current_label.config(text=f"{lang['tek-ras']} {layouts[current_hkl_str]}")
            layout_label.config(text=layouts[current_hkl_str])
        else:
            current_label.config(text=lang["tek-ras-not-found"])

        for hkl_str, name in layouts.items():
            rb = ttk.Radiobutton(radio_frame, text=name, variable=var, value=hkl_str, command=on_radio_change_update)
            rb.pack(anchor='w', pady=3)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        radio_frame.bind("<Configure>", on_frame_configure)

        close_btn = ttk.Button(lang_win, text=lang["zakr"], command=lang_win.destroy)
        close_btn.pack(pady=10)

        lang_win.update_idletasks()
        x = (lang_win.winfo_screenwidth() - lang_win.winfo_width()) // 2
        y = (lang_win.winfo_screenheight() - lang_win.winfo_height()) // 2
        lang_win.geometry(f"+{x}+{y}")
    def toggle_lang():
        global lang_win,layout_label

        if lang_win and lang_win.winfo_exists():
            fade_out(lang_win)
            lang_win = None
            layout_label.config(bg=taskbar_bg)
        else:
            show_lang()
    def toggle_calendar():
        global calendar_win, date_label

        if calendar_win and calendar_win.winfo_exists():
            fade_out(calendar_win)
            calendar_win = None
            date_label.config(bg=taskbar_bg)
        else:
            date_c()
    def open_network_simulator():
        run_in_thread(play_sound("sound//click.mp3", volume, state_sound, start_time_))

        global taskbar_height,wifi_state, bluetooth_state, wifi_label, bluetooth_label, wifi_toggle, bluetooth_toggle,gl_police,active_wifi_win,wifi_win
        wifi_button.config(bg = taskbar_fg)
        wifi_win = Toplevel()
        wifi_win.title("Wifi & Bluetooth")
        wifi_win.attributes('-alpha',0.0)

        fade_in(wifi_win)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 300 - 100
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset - 250
        wifi_win.geometry(f"300x300+{x}+{y}")
        wifi_win.configure(bg=global_bg)
        wifi_win.overrideredirect(True)
        img = Image.open("icons/interface/w.png")
        icon_image = ImageTk.PhotoImage(img)
        wifi_win.iconphoto(False, icon_image)
        style = ttk.Style()
        style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 12))

        wifi_label = Label(wifi_win, text="Wifi: " + lang['wifi_off'],font = (gl_police,10),bg=global_bg,fg=global_fg)
        wifi_label.pack(pady=10)

        wifi_toggle = create_toggle(wifi_win, toggle_wifi, "icons/interface/on_image.png", "icons/interface/off_image.png")
        wifi_toggle.pack(pady=5)

        bluetooth_label = Label(wifi_win, text="Bluetooth: " + lang['bt_off'],font = (gl_police,10),bg=global_bg,fg=global_fg)
        bluetooth_label.pack(pady=10)

        bluetooth_toggle = create_toggle(wifi_win, toggle_bluetooth, "icons/interface/on_image.png", "icons/interface/off_image.png")
        bluetooth_toggle.pack(pady=5)

        check_current_state()
    def create_toggle(parent, command, on_image_path, off_image_path):
        frame = Frame(parent, bg=global_bg)
        toggle_data = {"is_on": False}

        on_image = ImageTk.PhotoImage(Image.open(on_image_path).resize((60, 60)))
        off_image = ImageTk.PhotoImage(Image.open(off_image_path).resize((60, 60)))

        toggle_data["on_image"] = on_image
        toggle_data["off_image"] = off_image

        label = Label(frame, image=off_image, bg=global_bg)
        label.pack()

        def toggle(event=None):
            toggle_data["is_on"] = not toggle_data["is_on"]
            if toggle_data["is_on"]:
                label.config(image=on_image)
                label.image = on_image
            else:
                label.config(image=off_image)
                label.image = off_image
            command()

        label.bind("<Button-1>", toggle)

        frame.toggle_data = toggle_data
        frame.label = label
        return frame
    def check_current_state():
        global wifi_state, bluetooth_state

        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()

        cursor.execute("SELECT wifi, bluetooth FROM states WHERE ID = 1")
        result = cursor.fetchone()

        if result:
            wifi_state = result[0] == "on"
            bluetooth_state = result[1] == "on"

        conn.commit()
        conn.close()

        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)

        if wifi_state:
            wifi_label.config(text="Wifi: " + lang['wifi_on'], font=(gl_police, 10))
            wifi_toggle.toggle_data["is_on"] = True
            img = wifi_toggle.toggle_data["on_image"]
        else:
            wifi_label.config(text="Wifi: " + lang['wifi_off'], font=(gl_police, 10))
            wifi_toggle.toggle_data["is_on"] = False
            img = wifi_toggle.toggle_data["off_image"]
        wifi_toggle.label.config(image=img)
        wifi_toggle.label.image = img

        if bluetooth_state:
            bluetooth_label.config(text="Bluetooth: " + lang['bt_on'], font=(gl_police, 10))
            bluetooth_toggle.toggle_data["is_on"] = True
            img = bluetooth_toggle.toggle_data["on_image"]
        else:
            bluetooth_label.config(text="Bluetooth: " + lang['bt_off'], font=(gl_police, 10))
            bluetooth_toggle.toggle_data["is_on"] = False
            img = bluetooth_toggle.toggle_data["off_image"]
        bluetooth_toggle.label.config(image=img)
        bluetooth_toggle.label.image = img
    def toggle_wifi():
        global wifi_state
        wifi_state = not wifi_state

        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        global wifi_button
        if wifi_state:
            cursor.execute("UPDATE states SET wifi = ? WHERE ID = 1", ("on",))
            wifi_label.config(text="Wifi: " + lang['wifi_on'],font = (gl_police,10))
            wifi_button.config(text=lang["wifi_off"])
            log_to_file("Wi-Fi on",start_time_ = start_time_)
            wifi_button.config(image=wifi_on_icon)
        else:
            cursor.execute("UPDATE states SET wifi = ? WHERE ID = 1", ("off",))
            wifi_label.config(text="Wifi: " + lang['wifi_off'],font = (gl_police,10))
            wifi_button.config(text=lang["wifi_on"])
            log_to_file("Wi-Fi off",start_time_ = start_time_)
            wifi_button.config(image=wifi_off_icon)

        conn.commit()
        conn.close()
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
    def toggle_bluetooth():
        global bluetooth_state
        bluetooth_state = not bluetooth_state

        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()

        if bluetooth_state:
            cursor.execute("UPDATE states SET bluetooth = ? WHERE ID = 1", ("on",))
            bluetooth_label.config(text="Bluetooth: " + lang['bt_on'],font = (gl_police,10))
            log_to_file("Bluetooth on",start_time_ = start_time_)
            messagebox.showinfo("Bluetooth", lang["bt_on"],parent=wifi_win)
        else:
            cursor.execute("UPDATE states SET bluetooth = ? WHERE ID = 1", ("off",))
            bluetooth_label.config(text="Bluetooth: " + lang['bt_off'],font = (gl_police,10))
            log_to_file("Bluetooth off",start_time_ = start_time_)
            messagebox.showinfo("Bluetooth", lang["bt_off"],parent=wifi_win)

        conn.commit()
        conn.close()
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
    def initialize_db():
        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS states (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            vpn TEXT,
                            wifi TEXT,
                            bluetooth TEXT
                        )''')

        cursor.execute('''SELECT COUNT(*) FROM states''')
        row_count = cursor.fetchone()[0]
        if row_count == 0:
            cursor.execute('''INSERT INTO states (vpn, wifi, bluetooth) VALUES (?, ?, ?)''', ("off", "off", "off"))
            conn.commit()

        conn.close()
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
    initialize_db()
    def update_battery():
        import psutil
        global mes_count
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            charging = battery.power_plugged
            status = f"{percent}%"
            battery_label.config(text=status)
            if charging:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/charging.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image=icon)
                battery_bt.image = icon
            elif percent > 0 and percent < 10:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/low_bat.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image = icon)
                battery_bt.image = icon
            elif percent > 10 and percent < 20:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/low1_bat.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image=icon)
                battery_bt.image = icon
            elif percent > 40 and percent < 60:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/50bat.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image=icon)
                battery_bt.image = icon
            elif percent > 61 and percent < 90:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/80bat.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image=icon)
                battery_bt.image = icon
            else:
                icon = ImageTk.PhotoImage(
                    Image.open(f"icons/interface/full.png").resize((60, 44), Image.Resampling.LANCZOS))
                battery_bt.config(image=icon)
                battery_bt.image = icon
            if percent > 0 and percent <= 20:
                if not mes_count:
                    messagebox.showwarning(lang["wa"],lang["no_b"],parent=bat_win)
                    mes_count = True
                battery_label.config(fg="red")
            elif percent >= 30 and percent <= 50: battery_label.config(fg="yellow")
            else: battery_label.config(fg="white")
            battery_label.config(text=status)
        else: battery_label.config(text="Baterry not found")

        root.after(10, update_battery)
    def load_gradient_colors():
        if not os.path.exists("configurations.db"): return None, None
        try:
            conn = sqlite3.connect("configurations.db")
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS gradients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          start_color TEXT NOT NULL,
                                          end_color TEXT NOT NULL)''')

            conn.commit()
            cursor.execute("SELECT start_color, end_color FROM gradients ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("configurations.db", "backup_data",start_time_)

            return row if row else (None, None)
        except Exception as e:
            log_to_file(f"Error loading gradient colors: {e}",level="error",start_time_ = start_time_)
            return None, None
    def save_cursor(cursor_name):
        log_to_file('Save cursor,start_time_ = start_time_',start_time_ = start_time_)
        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cursor_table (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            cursor_name TEXT
                          )''')

        cursor.execute("DELETE FROM cursor_table")
        cursor.execute("INSERT INTO cursor_table (cursor_name) VALUES (?)", (cursor_name,))
        conn.commit()
        conn.close()
        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
        log_to_file(f"Cursor {cursor_name} saved",start_time_ = start_time_)
    def game_bar():
        import keyboard
        global setting_key
        log_to_file("Game Bar lauch", start_time_=start_time_)
        setting_key = load_settings()

        print(setting_key)

        roott = Toplevel(root)

        roott.title(lang["gamebar"])
        roott.geometry("700x100")
        c = ""
        b = ""
        if tema == "d":
            c = "#1e1e1e"
            b = "white"
            roott.configure(bg="#1e1e1e")
        else:
            c = "white"
            b = "#1e1e1e"
            roott.configure(bg="white")
        roott.overrideredirect(True)
        roott.attributes("-alpha", value)

        def start_move(event):
            roott.x = event.x
            roott.y = event.y

        def do_move(event):
            x = event.x_root - roott.x
            y = event.y_root - roott.y
            roott.geometry(f"+{x}+{y}")

        def close_bar():
            log_to_file('Exit to Game Bar', start_time_=start_time_)
            roott.destroy()

        def take_screenshot():
            log_to_file('Screenshoot', start_time_=start_time_)
            os.makedirs("screenshoots", exist_ok=True)
            filename = f"screenshoots/screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            img = ImageGrab.grab()
            img.save(filename)

        fps_var = StringVar()
        cpu_var = StringVar()
        gpu_var = StringVar()

        def settings_bar():
            def prim():
                os.makedirs('syst_comp/gamebar_settings', exist_ok=True)
                global fps_s, setting_key, tema
                fps_s = var_fps.get()
                hotkey_screenshot = entry_screenshot.get()
                hotkey_record = entry_record.get()
                save_settings(hotkey_screenshot, hotkey_record)

                keyboard.remove_all_hotkeys()
                keyboard.add_hotkey(hotkey_screenshot, take_screenshot, suppress=True, trigger_on_release=True)
                keyboard.add_hotkey(hotkey_record, lambda: toggle_recording(btn_record), suppress=True,
                                    trigger_on_release=True)
                try:
                    write_encrypted_file("syst_comp/gamebar_settings/gamebar_theme.cfg", theme.get())
                    messagebox.showinfo(lang["success"], lang["izm_p"], parent=w)
                    tema = theme.get()
                except Exception as e:
                    messagebox.showerror(lang["error"], str(e), parent=w)
                try:
                    write_encrypted_file("syst_comp/gamebar_settings/gamebar_shw_inf.cfg", str(fps_s))
                    messagebox.showinfo(lang["success"], lang["izm_p"], parent=w)
                except Exception as e:
                    messagebox.showerror(lang["error"], str(e), parent=w)
                w.destroy()

            def save_alp(val):
                global value
                value = float(val)
                try:
                    write_encrypted_file("syst_comp/gamebar_settings/gamebar_p.cfg", str(val))
                except Exception as e:
                    messagebox.showerror(lang["error"], str(e), parent=roott)
                roott.attributes("-alpha", float(val))

            global value, fps_s, tema
            w = Toplevel(root)

            w.geometry("500x400")
            w.title(lang["gamebar"])
            Label(w, text=lang["proz"]).pack()
            var_fps = IntVar(value=fps_s)
            var_p = DoubleVar()
            label_val = Label(w, text=f"{lang['current_alp']} {var_p.get():.2f}")
            label_val.pack()

            def on_slide(v):
                save_alp(v)
                label_val.config(text=f"{lang['current_alp']} {float(v):.2f}")

            scale = Scale(w, from_=0.1, to=1.0, orient="horizontal", length=250, resolution=0.01, command=on_slide)
            scale.pack()
            scale.set(float(value))
            ttk.Checkbutton(w, text=lang["pokaz_fps"], variable=var_fps, offvalue=0, onvalue=1).pack()
            Label(w, text=lang["tema"]).pack()
            theme = StringVar()
            theme.set(tema)
            d = ttk.Radiobutton(w, text=lang["da"], variable=theme, value="d")
            d.pack()
            s = ttk.Radiobutton(w, text=lang["sve"], variable=theme, value="s")
            s.pack()

            Label(w, text=lang["key_sc"], bg="#2e2e2e", fg="white").pack(pady=(10, 0))
            global setting_key

            entry_screenshot = Entry(w)
            entry_screenshot.insert(0, setting_key["hotkey_screenshot"])
            entry_screenshot.pack()

            Label(w, text=lang["key_zap"], bg="#2e2e2e", fg="white").pack(pady=(10, 0))
            entry_record = Entry(w)
            entry_record.insert(0, setting_key["hotkey_record"])
            entry_record.pack()

            ttk.Button(w, text=lang["prim"], command=prim).pack()

        def update_stats():
            import psutil
            while True:
                fps = random.randint(45, 165)
                cpu = psutil.cpu_percent(interval=None)
                gpu = random.randint(10, 99)
                fps_var.set(f"FPS: {fps}")
                cpu_var.set(f"CPU: {cpu}%")
                gpu_var.set(f"GPU: {gpu}%")
                time.sleep(2)

        threading.Thread(target=update_stats, daemon=True).start()

        roott.bind("<Button-1>", start_move)
        roott.bind("<B1-Motion>", do_move)
        Label(roott, text=lang["gamebar"], fg=b, bg=c, font=("Segoe UI", 14, "bold")).place(x=10,
                                                                                            y=10)

        btn_record = ttk.Button(roott, text=lang['zapi'], style="GameBar.TButton")
        btn_record.config(command=lambda: toggle_recording(btn_record))

        btn_screenshot = ttk.Button(roott, text=lang["screenshoot"], command=take_screenshot,
                                    style="GameBar.TButton")
        btn_settings = ttk.Button(roott, text="⚙️", style="Settings.TButton", command=settings_bar)
        btn_close = ttk.Button(roott, text="✖", command=close_bar, style="GameBar.TButton")

        btn_record.place(x=150, y=30)
        btn_screenshot.place(x=250, y=30)
        btn_settings.place(x=350, y=30)
        btn_close.place(x=550, y=30)
        if int(fps_s) == 1:
            Label(roott, textvariable=fps_var, fg="lime", bg=c, font=("Consolas", 12)).place(x=150, y=70)
            Label(roott, textvariable=cpu_var, fg="deepskyblue", bg=c, font=("Consolas", 12)).place(x=260, y=70)
            Label(roott, textvariable=gpu_var, fg="orange", bg=c, font=("Consolas", 12)).place(x=370, y=70)
        keyboard.add_hotkey(setting_key["hotkey_screenshot"], take_screenshot, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey(setting_key["hotkey_record"], lambda: toggle_recording(btn_record), suppress=True,
                            trigger_on_release=True)
    def record_screen():
        import cv2
        """
        Функция записи экрана. Выполняется в отдельном потоке.
        """
        global is_recording

        screen_size = pyautogui.size()
        os.makedirs("screen_recording", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screen_recording/recording_{timestamp}.avi"

        codec = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        out = cv2.VideoWriter(filename, codec, fps, screen_size)

        while is_recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()
        def show_message():
            messagebox.showinfo(lang["success"], f"{lang['videosave']}:\n{filename}")

        root.after(0, show_message)
    def blink_indicator():
        if recording_indicator and is_recording:
            current_color = recording_indicator.cget("fg")
            new_color = "red" if current_color == global_bg else global_bg
            recording_indicator.config(fg=new_color)
            root.after(500, blink_indicator)
    def toggle_recording(btn):
        global is_recording, recording_thread, recording_indicator, recording_window

        if not is_recording:
            is_recording = True
            record_off = ImageTk.PhotoImage(
                Image.open(f"icons/interface/record_off.png").resize((50, 50), Image.Resampling.LANCZOS))
            btn.config(image=record_off)
            btn.image = record_off
            recording_thread = threading.Thread(target=record_screen)
            recording_thread.start()

            recording_indicator = Label(root, text=lang['zapitr'], fg="red", bg=global_bg,
                                        font=("Arial", 12, "bold"))
            recording_indicator.pack(pady=5)
            blink_indicator()
        else:
            record = ImageTk.PhotoImage(
                Image.open(f"icons/interface/rec.png").resize((50, 50), Image.Resampling.LANCZOS))
            is_recording = False
            btn.config(image=record)
            btn.image = record

            if recording_indicator:
                recording_indicator.destroy()
                recording_indicator = None
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f: return json.load(f)
        return {
            "hotkey_screenshot": "F9",
            "hotkey_record": "F10"
        }
    def save_settings(hotkey_screenshot, hotkey_record):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "hotkey_screenshot": hotkey_screenshot,
                "hotkey_record": hotkey_record
            }, f)
    def open_pusk():
        def show_tooltip(event, txt):
            global tooltip
            if tooltip: return

            x = event.widget.winfo_rootx() + 20
            y = event.widget.winfo_rooty() + event.widget.winfo_height() + 10

            tooltip = Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.configure(bg="#333333")

            label = Label(tooltip,
                          text=txt,
                          background="#fcfcfa",
                          foreground="#000000",
                          font=("Segoe UI", 10),
                          relief="solid",
                          borderwidth=1,
                          padx=8, pady=4)

            label.pack()

            try:
                tooltip.attributes("-alpha", 0.97)
                tooltip.attributes("-topmost", True)
            except Exception as e:
                log_to_file(str(e), level="error", start_time_=start_time_)
        def hide_tooltip(event):
            global tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        global acc, account_img, is_recording
        run_in_thread(play_sound("sound//click.mp3",volume,state_sound,start_time_))
        def settings():
            import customtkinter as ctk
            def prim(var_log,var_sound,var_night):
                def close_progress():
                    global progress_window
                    if progress_window is not None and progress_window.winfo_exists():
                        progress_window.destroy()
                        progress_window = None
                def prog(val, idx=1):
                    global progress_window, progress_bar

                    if progress_window is None or not progress_window.winfo_exists():
                        progress_window = Toplevel(win_p)
                        progress_window.title(lang["vipo"])
                        progress_window.attributes("-alpha", float(GlobalAlpha))
                        progress_window.geometry("320x60")
                        progress_window = create_window(root, lang["vipo"], global_bg,
                                                        float(GlobalAlpha), 320, 60)
                        progress_window.attributes('-topmost', True)

                        progress_bar = ttk.Progressbar(progress_window, length=300, maximum=100)
                        progress_bar.pack(pady=10, padx=10)
                        progress_window.update()

                    progress_bar.config(value=val)
                    progress_window.update_idletasks()
                def update_language(lang_code):
                    global lang

                    with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
                        langs = json.load(file)
                    if lang_code not in langs:
                        return langs["RU"]
                    lang = langs[lang_code]
                def update_widget_text(widget):
                    if isinstance(widget, Label):
                        if widget.cget("text") in lang:
                            widget.config(text=lang[widget.cget("text")])
                    elif isinstance(widget, Button):
                        if widget.cget("text") in lang:
                            widget.config(text=lang[widget.cget("text")])
                    elif isinstance(widget, ttk.Combobox):
                        if widget.get() in lang:
                            widget.set(lang[widget.get()])

                    for child in widget.winfo_children():
                        update_widget_text(child)
                def translate_color(name):
                    mapping = {
                        lang["red"]: "red",
                        lang["yellow"]: "yellow",
                        lang["gray"]: "#808080",
                        lang["violet"]: "#800080",
                        lang["black"]: "black",
                        lang["white"]: "white",
                        lang["orange"]: "orange",
                        lang["pink"]: "#FF1493",
                        lang["olive"]: "#808000",
                        lang["green"]: "green"
                    }

                    return mapping.get(name.strip(), name)

                global win_theme,clock,gl_police,night_state,global_bg,global_fg,clock_type,auto_update_enabled,taskbar_fg,\
                    taskbar_bg,tbColor,state_sound
                prog(10,1)
                tbc = tb_color_var.get()

                if tbc == lang["red"]: tbc = 'red'
                elif tbc == lang["blue"] or tbc == "#34495e": tbc = "#34495e"
                elif tbc == lang["yellow"]:  tbc = "yellow"
                else: tbc = "green"

                write_encrypted_file("syst_comp/tb_color.cfg",str(tbc))
                taskbar_bg = tbc
                taskbar.config(bg = tbc)

                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE if not EXISTS night(state INTEGER)")
                conn.commit()
                cursor.execute("SELECT COUNT(*) FROM night")
                result = cursor.fetchone()

                if var_auto_upd.get() == 1:
                    auto_update_enabled = True
                    write_file('syst_comp/auto_upd.cfg','w',"True")
                else:
                    auto_update_enabled = False
                    write_file("syst_comp/auto_upd.cfg",'w',"False")
                if result[0] == 0: cursor.execute("INSERT INTO night (state) VALUES (?)", (int(var_night),))
                else: cursor.execute("UPDATE night SET state = ?", (int(var_night),))

                if var_type.get() == lang["hhmm"]: write_encrypted_file("syst_comp/format_clk.cfg", "hhmm")
                else: write_encrypted_file("syst_comp/format_clk.cfg", "hhmmss")

                clock_type = var_type.get()
                conn.commit()

                prog(10)
                night_state = var_night

                if var_night == 0:
                    global_bg = "white"
                    global_fg = "black"
                    taskbar_bg = "#34495e"
                    taskbar_fg = "#3e5870"
                else:
                    global_bg = "black"
                    global_fg = "white"
                    taskbar_bg = "#000000"
                    taskbar_fg = '#545353'

                thm = theme_var.get()
                write_encrypted_file("syst_comp/win_theme.cfg",thm)
                win_theme = thm
                if thm != "standart":
                    if thm in ["azure-light","azure-dark"]:
                        root.tk.call("source", "themes/azure.tcl")
                    else:
                        root.tk.call("source", f"themes/{thm}.tcl")
                    style = ttk.Style(root)
                    style.theme_use(thm)
                else:
                    style = ttk.Style(root)
                    style.theme_use('vista')
                clock = clock_var.get()

                prog(30)

                write_encrypted_file("syst_comp/plc_clk.cfg", clock_var.get())
                write_encrypted_file("syst_comp/plc_sys.cfg", police_var.get())

                gl_police = police_var.get()

                win.destroy()

                prog(40)

                if var_log == 1: log = "1"
                else:  log = "0"

                staut = var_aut.get()
                if staut == 1: add_exe_to_autostart(start_time_)
                else: remove_exe_from_autostart(start_time_)
                if var_sound == 1: st_sound = 1
                else: st_sound = 0

                prog(60)

                state_sound = int(st_sound)

                cursor_name = cursor_var.get()
                save_cursor(cursor_name)
                root.config(cursor=cursor_name)

                ll = var1.get()
                size = size_var.get()

                cursor.execute("CREATE TABLE if not EXISTS LOG_INFO(log INTEGER)")
                conn.commit()
                cursor.execute("SELECT COUNT(*) FROM LOG_INFO")
                if cursor.fetchone()[0] == 0: cursor.execute("INSERT INTO LOG_INFO (log) VALUES (?)", (log,))
                else: cursor.execute("UPDATE LOG_INFO SET log = ?", (log,))

                cursor.execute("CREATE TABLE if not EXISTS SOUND_STATE(sound INTEGER)")
                conn.commit()
                cursor.execute("SELECT COUNT(*) FROM SOUND_STATE")

                prog(70)

                if cursor.fetchone()[0] == 0: cursor.execute("INSERT INTO SOUND_STATE (sound) VALUES (?)", (state_sound,))
                else: cursor.execute("UPDATE SOUND_STATE SET sound = ?", (state_sound,))
                cursor.execute("CREATE TABLE if not EXISTS AUT_STATE(aut INTEGER)")
                conn.commit()
                cursor.execute("SELECT COUNT(*) FROM AUT_STATE")
                if cursor.fetchone()[0] == 0: cursor.execute("INSERT INTO AUT_STATE (aut) VALUES (?)", (staut,))
                else: cursor.execute("UPDATE AUT_STATE SET aut = ?", (staut,))
                conn.commit()

                write_file("syst_comp/size.cfg", 'w', size)

                clr = color_var.get()
                a = ""
                LANGS = ["English","Français","Українська","Русский","Беларускі","shqip","Српски","Deutsch","Español","Italiano",
                         "Português","Polski","Türkçe","日本語","中国人","čeština","Magyar","Български","Română"]
                LOCALES = ["EN","FR","UA","RU","BY","ALB","SRB","DE","ES","IT","PT","PL","TUR","JP","CN","CS","HU","BG","RO"]

                for i,L in enumerate(LANGS):
                    if ll == L: a = LOCALES[i]
                    elif ll in user_langs:  a = ll

                if clr == lang["blue"]: clr = "#2C3E50"
                elif clr == lang["red"]: clr = "red"
                elif clr == lang["yellow"]: clr = "yellow"
                elif clr == lang["green"]: clr = "green"
                elif clr == lang["olive"]: clr = "#808000"
                elif clr == lang["chocolate"]:  clr = "#D2691E"
                elif clr == lang["nebecn"]: clr = "#00BFFF"
                elif clr == lang["gold"]: clr = "#DAA520"
                elif clr == lang["tomat"]: clr = "#FF6347"
                elif clr == lang["pink"]: clr = "#FF1493"
                elif clr == lang["violet"]:clr = "#800080"
                elif clr == lang["orange"]: clr = "#FFA500"
                elif clr == lang["lime"]:  clr = "#00FF00"
                elif clr in user_color: clr = clr

                prog(80)

                write_encrypted_file("syst_comp/lang.cfg", a)

                if not custom_wallpeper: write_file("syst_comp/color.cfg", 'w', clr)

                log_to_file(f"Langue {a} apply",start_time_ = start_time_)

                prog(90)

                log_to_file(f"Background color {clr} apply",start_time_ = start_time_)

                update_language(a)
                if custom_wallpeper and "-" in color_var.get():
                    start_color, end_color = color_var.get().split("-")
                    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                                    highlightthickness=0)
                    canvas.place(x=0, y=0)
                    draw_gradient(canvas, start_color, end_color,root,lang)
                    canvas.update()
                    shortcut_frame = Frame(root, bg="", highlightthickness=0)
                    shortcut_frame.place(x=50, y=50)
                    root.update_idletasks()
                    set_rows(size_sh)
                    if color_var.get() == "Red-Yellow": clr = "Red"
                    elif color_var.get() == "Gray-Violet": clr = "Gray"
                    elif color_var.get() == "Black-White": clr = "Black"
                    elif color_var.get() == "Orange-Red": clr = "Orange"
                    elif color_var.get() == "Pink-White": clr = "White"
                    elif color_var.get() == "Green-Olive": clr = "Green"
                    elif color_var.get() == "Blue-White": clr = "Blue"
                    elif color_var.get() == "Violet-Blue": clr = "Blue"
                    elif color_var.get() == "Pink-Violet": clr = "Pink"
                    place_shortcuts(size,MAX_ROWS,color)
                    root.update_idletasks()

                    start_hex = translate_color(start_color)
                    end_hex = translate_color(end_color)

                    conn = sqlite3.connect("configurations.db")
                    cursor = conn.cursor()
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS gradients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            start_color TEXT,
                            end_color TEXT
                        )
                    ''')
                    cursor.execute("DELETE FROM gradients")
                    cursor.execute("INSERT INTO gradients (start_color, end_color) VALUES (?, ?)", (start_hex, end_hex))
                    conn.commit()
                    conn.close()
                if not custom_wallpeper or not image_wallpeper: root.configure(bg=str(clr))
                if not image_wallpeper:
                    for frame in special_frames:
                        if frame.winfo_exists():
                            frame.configure(bg=str(clr))
                        else:
                            log_to_file("⚠️ Frame already deleted — not possible change BG.",level="warning",start_time_= start_time_)
                        for widget in frame.winfo_children():
                            if isinstance(widget, Label):
                                widget.configure(bg=str(clr))
                if clr == "yellow" or clr == "00FF00":
                    for label in labels:
                        label.configure(foreground="black")
                        log_to_file("Label color: black",start_time_ = start_time_)
                else:
                    for label in labels:
                        try: label.configure(foreground="white")
                        except TclError: continue

                set_rows(size_sh)

                prog(100)

                close_progress()

                names = ["Thinkers Dripping Demo","cultural literature demo",
                       "Apache Tomcat Demo","caviary","kadera","ATLAS_SCRITTO","title_ren","anak_paud","auto-sharp-pencil",
                       "gnf","trickr-logo","midfriend","playgum","pqrmonday","geniehive","paulo-bittencourt","sludgeborn",
                        "Drift Wood", "Kamikaze 3D Gradient","Starbim","Mexcellent 3D","Gunplay 3D",'Minecart LCD',
                       'Soviet Program', 'Zombie Holocaust', 'Nosifer', 'Hole - Hearted', 'PWJoyeuxNoel', 'CandyTime',
                        'Kingthings Christmas 2', 'Snowtop Caps', 'Haloberry', 'Crashed Scoreboard', 'Karnivore Black',
                       'Drawliner','Minisystem','Jigsaw Trouserdrop', 'Game Bubble','SAIBA-45', 'LIBRARY 3 AM', 'Neuropol',
                       'Overload', 'Perfect Dark (BRK)', 'Squares Bold', "You're Gone",
                        'Xirod', 'Shlop', 'Budmo Jigglish' 'Living by Numbers',"Electroharmonix"]
                names1 = ["caviary","kadera",
                      "ATLAS_SCRITTO","title_ren","anak_paud","auto-sharp-pencil","gnf","trickr-logo",
                      "midfriend","playgum","pqrmonday","Kamikaze 3D Gradient","Starbim","Mexcellent 3D",
                      "Gunplay 3D",'Minecart LCD', 'Soviet Program', 'Nosifer', 'Hole - Hearted', 'PWJoyeuxNoel',
                      'CandyTime','Kingthings Christmas 2', 'Snowtop Caps', 'Haloberry' 'Crashed Scoreboard',
                      'Karnivore Black', 'Drawliner','Minisystem','Jigsaw Trouserdrop', 'Game Bubble',
                      'SAIBA-45', 'LIBRARY 3 AM', 'Neuropol', 'Overload', 'Perfect Dark (BRK)', 'Squares Bold',
                      "You're Gone",
                      'Xirod', 'Shlop', 'Budmo Jigglish' 'Living by Numbers', "Electroharmonix"
                      ]
                for n in names:
                    if police_var.get() == n and gl_police != police_var.get(): messagebox.showinfo("info", lang[n],parent=win)
                for n1 in names1:
                    if clock == n1 and clock_type != clock: messagebox.showinfo("info", lang[n1])

                messagebox.showinfo(lang["success"], lang["changes"])
                update_time()
                log_to_file(f"Message: {lang['changes']}",start_time_ = start_time_)
                place_shortcuts(int(size), MAX_ROWS, color)
                root.update_idletasks()
                return
            def invisiblepass(var):
                global invisible_pass
                if var == 0:
                    write_encrypted_file("syst_comp/invisible_pass.cfg", "False")
                    invisible_pass = False
                else:
                    write_encrypted_file("syst_comp/invisible_pass.cfg","True")
                    invisible_pass = True
            def excl():
                global svb_coins,custom_wallpeper,is_on
                is_on = True
                svb_coins = load_balance(start_time_)
                if messagebox.askyesnocancel("",lang["pay"],parent=win):
                    log_to_file(f"User accept: {lang['pay']}",start_time_ = start_time_)
                    run_in_thread(play_sound("sound//oldspice.mp3",volume,state_sound,start_time_))
                    log_to_file("Custom wallpeper on",start_time_ = start_time_)
                    svb_coins -= 1000
                    transactions("-1.000 SVb Coins"+f" {datetime.now()}",start_time_)
                    save_balance(svb_coins,start_time_)
                    log_to_file('SVB coins -= 1000',start_time_ = start_time_)

                    try:
                        write_encrypted_file("exclusive.wndrs", 'YES')
                        copy_file_to_folder("exclusive.wndrs", "backup_data",start_time_)
                    except Exception as e:
                        show_error(f"Error {errors[2]}: {str(e)}",level="error")
                        bsod.open_bsod(errors_bsod[2], f'ERROR WITH FILES: {e}', main)

                    if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                        copy_file_to_folder("exclusive.wndrs", "backup_data",start_time_)
                    messagebox.showinfo(lang["success"],lang["pay_success"],parent=win)
                    custom_wallpeper = True
                    log_to_file("custom_wallpeper = True",start_time_ = start_time_)
                else:
                    messagebox.showerror(lang["error"],lang["no_svb"],parent=win)
                    log_to_file(f"User refuse: {lang['pay']}",start_time_ = start_time_)
                    log_to_file(f'Message: {lang["no_svb"]}',level="warning",start_time_ = start_time_)
            def excl_exit():
                global custom_wallpeper,is_on
                is_on = False
                log_to_file("Custom wallpeper off",start_time_ = start_time_)
                try:
                    write_encrypted_file("exclusive.wndrs", 'NON')
                except Exception as e:
                    show_error(f"Error {errors[2]}: {str(e)}")
                    bsod.open_bsod(errors_bsod[2], f'ERROR WITH FILES: {e}', main)
                if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                    copy_file_to_folder("exclusive.wndrs", "backup_data",start_time_)
                custom_wallpeper = False
                log_to_file("Custom wallpeper = False",start_time_ = start_time_)
                global image_wallpeper
                if not image_wallpeper:
                    root.config(bg = str(color))
                messagebox.showinfo('',lang['enable_exclusive_'],parent=win)
                log_to_file(f'Message: {lang["enable_exclusive_"]}',start_time_ = start_time_)
            def changge():
                def okk(image):
                    global account_img
                    try:
                        write_file("syst_comp/icons.cfg", 'w', image)
                    except Exception as e:
                        log_to_file(str(e), level="error", start_time_=start_time_)
                    account_img = image
                    messagebox.showinfo(lang["success"],lang["icon_acc"],parent=Win)
                Win = create_window(win_p, lang["change-acc"], global_bg, float(GlobalAlpha), 400, 300,"icons/acc2.png")
                try:
                    acc_path = "icons//acc3.png"
                    acc = ImageTk.PhotoImage(Image.open(acc_path).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    acc = None
                try:
                    acc_path1 = "icons//myacc.png"
                    acc1 = ImageTk.PhotoImage(Image.open(acc_path1).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    acc1 = None
                try:
                    wifi_on_path = "icons//acc2.png"
                    wifi_on_icon = ImageTk.PhotoImage(Image.open(wifi_on_path).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon = None
                try:
                    wifi_off_path1 = "icons//acc1.png"
                    wifi_off_icon1 = ImageTk.PhotoImage(Image.open(wifi_off_path1).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_off_icon1 = None
                try:
                    wifi_on_path2 = "icons//acc4.png"
                    wifi_on_icon2 = ImageTk.PhotoImage(
                        Image.open(wifi_on_path2).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon2 = None
                try:
                    wifi_on_path3 = "icons//acc5.png"
                    wifi_on_icon3 = ImageTk.PhotoImage(
                        Image.open(wifi_on_path3).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon3 = None
                try:
                    wifi_on_path4 = "icons//acc6.png"
                    wifi_on_icon4 = ImageTk.PhotoImage(
                        Image.open(wifi_on_path4).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon4 = None
                try:
                    wifi_on_path5 = "icons//acc7.png"
                    wifi_on_icon5 = ImageTk.PhotoImage(
                        Image.open(wifi_on_path5).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon5 = None
                try:
                    wifi_on_path6 = "icons//acc8.png"
                    wifi_on_icon6 = ImageTk.PhotoImage(
                        Image.open(wifi_on_path6).resize((44, 44), Image.Resampling.LANCZOS))
                except Exception as e:
                    wifi_on_icon6 = None
                refes = [acc, acc1, wifi_off_icon1,wifi_on_icon6,wifi_on_icon,wifi_on_icon4,wifi_on_icon5,wifi_on_icon3,wifi_on_icon2]
                global user_icons
                if len(user_icons) > 0:
                    for i in user_icons:
                        refes.append(i)
                Win.image_references = refes

                frame1 = Frame(Win)
                frame1.pack(side =  LEFT)
                frame2 = Frame(Win)
                frame2.pack(side=LEFT)
                frame3 = Frame(Win)
                frame3.pack(side=LEFT)
                frame4 = Frame(Win)
                frame4.pack(side=LEFT)
                if acc:
                    Button(frame1, image=acc,command = lambda :okk(acc_path)).pack()
                if acc1:
                    Button(frame1, image=acc1,command = lambda :okk(acc_path1)).pack()
                if wifi_off_icon:
                    Button(frame1, image=wifi_on_icon,command = lambda :okk(wifi_on_path)).pack()
                if wifi_off_icon1:
                    Button(frame1, image=wifi_off_icon1,command = lambda :okk(wifi_off_path1)).pack()
                if wifi_on_icon2:
                    Button(frame2, image=wifi_on_icon2,command = lambda :okk(wifi_on_path2)).pack()
                if wifi_on_icon3:
                    Button(frame2, image=wifi_on_icon3,command = lambda :okk(wifi_on_path3)).pack()
                if wifi_on_icon4:
                    Button(frame2, image=wifi_on_icon4, command=lambda: okk(wifi_on_path4)).pack()
                if wifi_on_icon5:
                    Button(frame2, image=wifi_on_icon5, command=lambda: okk(wifi_on_path5)).pack()
                if wifi_on_icon6:
                    Button(frame3, image=wifi_on_icon6, command=lambda: okk(wifi_on_path6)).pack()
                if user_icons:
                    for path in user_icons:
                        try:
                            img = Image.open(path).resize((44, 44), Image.Resampling.LANCZOS)
                            tk_img = ImageTk.PhotoImage(img)
                            btn = Button(frame4, image=tk_img, command=lambda p=path: okk(p))
                            btn.image = tk_img
                            btn.pack()
                            refes.append(tk_img)
                        except Exception as e:
                            log_to_file(f"Error with upload image {path}: {e}",level='error',start_time_=start_time_)
            def logging_settings():
                def update_log_set(var):
                    global LoggingSett
                    write_encrypted_file("syst_comp/log_set.cfg",str(var))
                    LoggingSett = int(var)
                    if var == 0: messagebox.showinfo(lang["success"],lang["saving_error_log_tr"],parent = W)
                    else: messagebox.showinfo(lang["success"], lang["saving_error_log_fa"],parent = W)

                global LoggingSett
                W = create_window(win, lang["logging_settings"], global_bg, float(GlobalAlpha), 500, 100,"icons/interface/settings.png")

                var = IntVar()
                var.set(int(LoggingSett))

                ch = ttk.Checkbutton(W,text = lang["save_error_log"],variable=var,onvalue=1,offvalue=0,command = lambda:update_log_set(var.get()))
                ch.pack()
            def change_sys(var,lbl):
                global preview_sys
                preview_sys = str(var.get())
                lbl.config(font = (preview_sys,13))
            def change_clk(var,lbl):
                global preview_clock
                preview_clock = str(var.get())
                lbl.config(font = (preview_clock,13))
            def update_cursor(var,lbl):
                selected = var.get()
                lbl.config(cursor=selected)
            def open_preview():
                def change(lbl, key):
                    path = images.get(key)
                    if path:
                        img = Image.open(path).resize((300, 160), Image.Resampling.LANCZOS)
                        tk_img = ImageTk.PhotoImage(img)
                        lbl.config(image=tk_img)
                        lbl.image = tk_img
                def apply():
                    global img_path, image_wallpeper, canvas_icon,shortcut_frame

                    selected_name = var_img.get()
                    img_path = images.get(selected_name)

                    if not img_path or not os.path.isfile(img_path):
                        messagebox.showerror(lang["error"], f"{lang['wlp_file_not_found']}\n{img_path}", parent=w)
                        return

                    image_wallpeper = True
                    write_encrypted_file("syst_comp/img_wlp.cfg", 'TRUE')
                    write_encrypted_file("syst_comp/path_wlp.cfg", img_path)

                    def load_bg():
                        global shortcut_frame
                        def delete_frm(frm):
                            try:
                                if frm: frm.destroy()
                            except NameError:
                                pass
                        try:
                            img = Image.open(img_path).convert("RGBA")
                            img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(img)

                            canvas_icon.delete("all")
                            canvas_icon.create_image(0, 0, anchor="nw", image=photo)
                            canvas_icon.image = photo
                            delete_frm(shortcut_frame)
                            shortcut_frame = Frame(root, bg="", highlightthickness=0, bd=0)
                            shortcut_frame.place(x=50, y=50)
                            set_rows(size_sh)
                            place_shortcuts(size_sh, MAX_ROWS, "black")
                        except Exception as e:
                            log_to_file(f"Uploading error: {e}",level = "error",start_time_ = start_time_)
                    threading.Thread(target=load_bg, daemon=True).start()
                def add_wallpaper():
                    file_path = filedialog.askopenfilename(parent=w,
                                                           title=lang["select_image"],
                                                           filetypes=[(lang['izo'], "*.jpg *.jpeg *.png *.bmp *.gif")]
                                                           )

                    if not file_path:
                        return

                    file_name = os.path.basename(file_path)
                    dest_dir = "icons/wallpepers"
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, file_name)

                    try:
                        shutil.copy(file_path, dest_path)
                    except Exception as e:
                        messagebox.showerror(lang["error_with_copy"], str(e), parent=w)
                        return

                    name_without_ext = os.path.splitext(file_name)[0]
                    key = load_key()

                    try:
                        old_paths_ = read_file("syst_comp/valids/vld_path_wlp.cfg", 'rb')
                        old_names_ = read_file("syst_comp/valids/vld_wlp.cfg", 'rb')
                        old_paths = decrypt_message(old_paths_, key)
                        old_names = decrypt_message(old_names_, key)
                    except:
                        old_paths, old_names = '', ''

                    new_paths = old_paths + f'\n{dest_path}' if old_paths else dest_path
                    new_names = old_names + f'\n{name_without_ext}' if old_names else name_without_ext
                    write_file("syst_comp/valids/vld_path_wlp.cfg", 'wb', encrypt_message(new_paths, key))
                    write_file("syst_comp/valids/vld_wlp.cfg", 'wb', encrypt_message(new_names, key))

                    messagebox.showinfo(lang['added'], f"{lang['__file__']} '{file_name}' {lang['added_kak_wlp']}",
                                        parent=w)
                    valid_wlp_paths = load_paths_encrypted()
                    w.destroy()
                    open_preview()
                if var_wlp.get() == 1:
                    global ll_n
                    paths = valid_wlp_paths
                    names = valid_wlp_names
                    images = {}

                    for path in paths:
                        name = os.path.splitext(os.path.basename(path))[0]
                        images[name] = path

                    ll_n = list(images.keys())
                    w = create_window(win, lang["select_wlp"], global_bg, float(GlobalAlpha), 500, 450)

                    frm = LabelFrame(w, text=lang['prev4'])
                    frm.pack(pady=5)

                    default_name = "wallpeper1" if "wallpeper1" in images else list(images.keys())[0]
                    img_ = images[default_name]
                    img = Image.open(img_).resize((300, 160), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)

                    lbl = Label(frm, image=tk_img)
                    lbl.image = tk_img
                    lbl.pack(pady=5)

                    var_img = StringVar(value=default_name)

                    selector_frame = Frame(w)
                    selector_frame.pack(pady=5, fill="x")
                    canvas = Canvas(selector_frame, height=60)
                    scrollbar = Scrollbar(selector_frame, orient="horizontal", command=canvas.xview)
                    canvas.configure(xscrollcommand=scrollbar.set)
                    scrollbar.pack(side="bottom", fill="x")
                    canvas.pack(side="top", fill="x")

                    thumb_frame = Frame(canvas)
                    canvas.create_window((0, 0), window=thumb_frame, anchor="nw")

                    thumb_images = {}

                    def select_image(name):
                        var_img.set(name)
                        change(lbl, name)

                    for i, (name, path) in enumerate(images.items()):
                        img_thumb = Image.open(path).resize((80, 50), Image.Resampling.LANCZOS)
                        tk_thumb = ImageTk.PhotoImage(img_thumb)
                        thumb_images[name] = tk_thumb
                        btn = Button(thumb_frame, image=tk_thumb, command=lambda n=name: select_image(n))
                        btn.grid(row=0, column=i, padx=2)

                    thumb_frame.update_idletasks()
                    canvas.config(scrollregion=canvas.bbox("all"))

                    btn_frame = Frame(w)
                    btn_frame.pack(pady=10)
                    ttk.Button(btn_frame, text=lang["prim"], command=apply).pack(side=LEFT, padx=5)
                    ttk.Button(btn_frame, text=lang["add_wlp"], command=add_wallpaper).pack(side=LEFT, padx=5)

                    w.images = images
                    w.thumb_images = thumb_images
                else:
                    global img_path, image_wallpeper, color, canvas_icon
                    image_wallpeper = False
                    img_path = None

                    write_encrypted_file("syst_comp/img_wlp.cfg", 'FALSE')
                    write_encrypted_file("syst_comp/path_wlp.cfg", 'NONE')

                    if canvas_icon:
                        canvas_icon.destroy()
                        canvas_icon = None
                    shortcut_frame = Frame(root, bg=str(color), highlightthickness=0)
                    shortcut_frame.place(x=50, y=50)
                    set_rows(size_sh)
                    place_shortcuts(size_sh, MAX_ROWS, str(color))
                    root.configure(bg=str(color))
            def open_preview_pass():
                def change(lbl, key):
                    path = images.get(key)
                    if path:
                        img = Image.open(path).resize((300, 160), Image.Resampling.LANCZOS)
                        tk_img = ImageTk.PhotoImage(img)
                        lbl.config(image=tk_img)
                        lbl.image = tk_img

                def delete():
                    global image_wallpeper_pass
                    write_encrypted_file("syst_comp/img_wlp_passwordWin.cfg", 'False')
                    image_wallpeper_pass = False

                def apply():
                    global img_path_pass, image_wallpeper_pass, ll_n, paths

                    img_path_pass = ""
                    selected_name = var_img.get()

                    for i, l in enumerate(ll_n):
                        if selected_name == l:
                            img_path_pass = paths[i]
                            break

                    if not img_path_pass:
                        messagebox.showerror(lang["error"],
                                             f"{lang['neudalos1']} '{selected_name}' {lang['in_list']}\n\nll_n: {ll_n}\npaths: {paths}",
                                             parent=w)
                        return

                    if not os.path.isfile(img_path_pass):
                        messagebox.showerror(lang["error"],
                                             f"{lang['wlp_file_not_found']}\n{img_path_pass}\n\n{lang['exp1']}",
                                             parent=w)
                        return
                    try:
                        image_wallpeper_pass = True
                        write_encrypted_file("syst_comp/img_wlp_passwordWin.cfg", 'True')
                        write_encrypted_file("syst_comp/path_wlp_passwordWin.cfg", img_path_pass)
                        messagebox.showinfo(lang["succcess"], lang["success"],parent=w)
                    except Exception as e:
                        messagebox.showerror(lang['error'], str(e),parent=w)

                global ll_n
                paths = valid_wlp_paths
                names = valid_wlp_names
                images = {}

                for path in paths:
                    name = os.path.splitext(os.path.basename(path))[0]
                    images[name] = path

                ll_n = list(images.keys())
                w = create_window(win, lang["select_wlp"], global_bg, float(GlobalAlpha), 500, 450)

                frm = LabelFrame(w, text=lang['prev4'])
                frm.pack(pady=5)

                default_name = "wallpeper1" if "wallpeper1" in images else list(images.keys())[0]
                img_ = images[default_name]
                img = Image.open(img_).resize((300, 160), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)

                lbl = Label(frm, image=tk_img)
                lbl.image = tk_img
                lbl.pack(pady=5)

                var_img = StringVar(value=default_name)

                selector_frame = Frame(w)
                selector_frame.pack(pady=5, fill="x")
                canvas = Canvas(selector_frame, height=60)
                scrollbar = Scrollbar(selector_frame, orient="horizontal", command=canvas.xview)
                canvas.configure(xscrollcommand=scrollbar.set)
                scrollbar.pack(side="bottom", fill="x")
                canvas.pack(side="top", fill="x")

                thumb_frame = Frame(canvas)
                canvas.create_window((0, 0), window=thumb_frame, anchor="nw")

                thumb_images = {}

                def select_image(name):
                    var_img.set(name)
                    change(lbl, name)

                for i, (name, path) in enumerate(images.items()):
                    img_thumb = Image.open(path).resize((80, 50), Image.Resampling.LANCZOS)
                    tk_thumb = ImageTk.PhotoImage(img_thumb)
                    thumb_images[name] = tk_thumb
                    btn = Button(thumb_frame, image=tk_thumb, command=lambda n=name: select_image(n))
                    btn.grid(row=0, column=i, padx=2)

                thumb_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))

                btn_frame = Frame(w)
                btn_frame.pack(pady=10)
                ttk.Button(btn_frame, text=lang["prim"], command=apply).pack(side=LEFT, padx=5)
                ttk.Button(btn_frame, text=lang["delete_img_pass"], command=delete).pack(side=LEFT, padx=5)

                w.images = images
                w.thumb_images = thumb_images
            def vklvivkl_antvrs(var):
                global antvrs_state
                if var:
                    antvrs_state = True
                    write_encrypted_file("syst_comp/antvrs_state.cfg","True")
                    messagebox.showinfo(lang["success"],lang["antvrs_vkl"],parent=win)
                else:
                    antvrs_state = False
                    write_encrypted_file("syst_comp/antvrs_state.cfg", "False")
                    messagebox.showinfo(lang["success"], lang["antvrs_vikl"],parent=win)
                win.update_idletasks()
            def vkl_email(var):
                global email_state
                if var:
                    email_state = True
                    write_encrypted_file("syst_comp/email_state.cfg", "True")
                    messagebox.showinfo(lang["success"], lang["email_vkl"],parent=win)
                else:
                    email_state = False
                    write_encrypted_file("syst_comp/email_state.cfg", "False")
                    messagebox.showinfo(lang["success"], lang["email_vikl"],parent=win)
                win.update_idletasks()
            def vkl_block(var):
                global block_state
                if var:
                    write_encrypted_file("syst_comp/block_ecran.cfg","True")
                    block_state = True
                else:
                    block_state = False
                    write_encrypted_file("syst_comp/block_ecran.cfg", "False")
            def vkl_change(var):
                global change_state
                if var:
                    write_encrypted_file("syst_comp/change_wlp_state.cfg", "True")
                    change_state = True
                else:
                    write_encrypted_file("syst_comp/change_wlp_state.cfg", "False")
                    change_state = False
            def set_alpha():
                def draw_ui():
                    lbl = Label(Win, text=f'{lang["current_alpha="]}:{int(GlobalAlpha * 100)}', font=("Arial", 10))
                    lbl.pack(pady=10)

                    var = IntVar(value=int(GlobalAlpha * 100))
                    slider = ttk.Scale(
                        Win,
                        from_=0,
                        to=100,
                        variable=var,
                        command=lambda v: save(v),
                        value=int(GlobalAlpha * 100)
                    )
                    slider.pack()
                def save(value):
                    global GlobalAlpha
                    GlobalAlpha = int(float(value)) / 100
                    Win.attributes("-alpha", GlobalAlpha)
                    write_encrypted_file("syst_comp/alpha.cfg", str(GlobalAlpha))
                    for widget in Win.winfo_children():
                        widget.destroy()
                    draw_ui()

                global GlobalAlpha
                Win = create_window(win, lang["sept_win_alpha"], global_bg, float(GlobalAlpha), 300, 200)
                draw_ui()

            try: la = read_encrypted_file("syst_comp/lang.cfg").strip()
            except: la = "EN"

            global custom_wallpeper,gl_police,user_langs,user_color,clock_type,preview_clock,preview_sys,tbColor
            win = create_window(win_p, lang["settings"], global_bg, float(GlobalAlpha), 1050, 700,"icons/interface/settings.png")

            main_frm = Frame(win)
            main_frm.pack()

            left_frm = Frame(win,bg = global_bg,relief = "solid",highlightbackground = "gray",highlightcolor = "#0000FF",highlightthickness = 1)
            left_frm.pack(side = LEFT,anchor = N)
            central_frm = Frame(win,bg = global_bg,relief = "solid",highlightbackground = "gray",highlightcolor = "#0000FF",highlightthickness = 1)
            central_frm.pack(side = LEFT,anchor = N)
            right_frm = Frame(win,bg = global_bg,relief = "solid",highlightbackground = "gray",highlightcolor = "#0000FF",highlightthickness = 1)
            right_frm.pack(side = LEFT,anchor = N)

            pre1 = LabelFrame(win, text=lang["prev1"],bg = global_bg,fg = global_fg)
            pre1.pack(side = TOP,anchor=N)
            pr1 = Label(pre1, text="Test message", font=(preview_sys, 13),bg=global_bg,fg = global_fg)
            pr1.pack()
            pre2 = LabelFrame(win, text=lang["prev2"],bg=global_bg,fg = global_fg)
            pre2.pack(side = TOP,anchor=N)
            pr2 = Label(pre2, text="12:35", font=(preview_clock, 13),fg = global_fg,bg=global_bg)
            pr2.pack()
            pr3 = LabelFrame(win,text = lang["prev3"],bg=global_bg,fg = global_fg)
            pr3.pack(side = TOP,anchor=N)
            preview_label = Label(pr3, text=lang["navedi"],fg = global_fg,bg=global_bg)
            preview_label.pack()

            lab = Label(left_frm, text=lang["langue"],font = (gl_police,10),bg=global_bg,fg=global_fg)
            lab.pack()
            lang_display = {
                "RU": "Русский",
                "UA": "Українська",
                "FR": "Français",
                "EN": "English",
                "ALB": "shqip",
                "SRB": "Српски",
                "PT": "Português",
                "IT": "Italiano",
                "ES": "Español",
                "PL": "Polski",
                "DE": "Deutsch",
                "BY": "Беларускі",
                "TUR": "Türkçe",
                "JP": "日本語",
                "CN": "中国人",
                "CS": "čeština",
                "HU": "Magyar",
                "BG": "Български",
                "RO": "Română",
            }

            display_to_code = {v: k for k, v in lang_display.items()}

            l = list(lang_display.values())
            if len(user_langs) > 0: l.extend(user_langs)

            var1_display = lang_display.get(la, la if la in user_langs else "Русский")

            var1 = StringVar(value=var1_display)
            var_type = StringVar(value = str(clock_type))
            color_var = StringVar(value=color)
            tb_color_var = StringVar(value=tbColor)

            if os.path.exists('configurations.db'): cursor_var = StringVar(value=load_cursor(start_time_))
            else: cursor_var = StringVar(value=load_cursor(start_time_))

            language = ttk.Combobox(left_frm, textvariable=var1, values=l, state="readonly")
            language.pack()
            types = [lang["hhmm"],lang["hhmmss"]]
            Label(left_frm,text = lang["clock_frm"],font = (gl_police,10),bg=global_bg,fg=global_fg).pack()
            type = ttk.Combobox(left_frm, textvariable=var_type, values=types, state="readonly")
            type.pack()

            try: stat = read_encrypted_file("stexc.wndrs")
            except Exception: stat = "FALSE"

            if custom_wallpeper:
                is_on = ctk.BooleanVar(value=True)

                lab = Label(left_frm, text=lang["background"], font=(gl_police, 10))
                lab.pack()

                colors = (
                    "Red-Yellow", "Gray-Violet", "Black-White", "Orange-Red",
                    "Pink-White", "Green-Olive", "Blue-White",
                    "Violet-Blue", "Pink-Violet"
                )
                c = ttk.Combobox(left_frm, textvariable=color_var, values=colors, state="readonly")
                c.pack()

                def switch_callback():
                    if is_on.get(): excl()
                    else: excl_exit()

                lab = Label(win, text=lang["enable_exclusive"], font=(gl_police, 10))
                lab.pack()

                background_switch = ctk.CTkSwitch(win,text="",variable=is_on,command=switch_callback,onvalue=True,
                    offvalue=False)
                background_switch.pack(pady=10)
            else:
                is_on = ctk.BooleanVar(value=False)

                lab = Label(
                    left_frm,
                    text=lang["background"],
                    font=(gl_police, 10),
                    bg=global_bg,
                    fg=global_fg
                )
                lab.pack()

                colors = [
                    lang["red"], lang["blue"], lang["yellow"], lang["green"],
                    lang["pink"], lang["violet"], lang["orange"],
                    lang["lime"], lang["olive"]
                ]

                if len(user_color) > 0:
                    colors.extend(user_color)

                c = ttk.Combobox(left_frm, textvariable=color_var, values=colors, state="readonly")
                c.pack()

                def switch_callback():
                    if is_on.get():
                        excl()
                    else:
                        excl_exit()

                lab = Label(right_frm,text=lang["pay_exclusive"],font=(gl_police, 10),bg=global_bg,fg=global_fg)
                lab.pack()

                background_switch = ctk.CTkSwitch(right_frm,text="",variable=is_on,command=switch_callback,onvalue=True,
                    offvalue=False)
                background_switch.pack(pady=10)

            lab = Label(left_frm, text=lang["taskbar_background"], font=(gl_police, 10), bg=global_bg, fg=global_fg)
            lab.pack()
            tb_colors = [lang["red"], lang["blue"], lang["yellow"], lang["green"]]
            c = ttk.Combobox(left_frm, textvariable=tb_color_var, values=tb_colors, state="readonly")
            c.pack()

            if os.path.exists("cr.cfg"):
                cursors = [
                    "arrow", "circle", "clock", "cross", "dotbox", "exchange", "fleur", "heart",
                    "man", "mouse", "pirate", "plus", "shuttle", "sizing", "spider", "spraycan",
                    "star", "target", "tcross", "trek", "watch", "X_cursor", "hand1", "hand2",
                    "pencil", "question_arrow", "right_ptr", "sb_h_double_arrow", "sb_v_double_arrow",
                    "based_arrow_down", "based_arrow_up", "draft_large", "draft_small", "left_ptr",
                    "text", "xterm"
                ]
                Label(left_frm,text = lang["cur"],font = (gl_police,10),bg=global_bg,fg=global_fg).pack()
                curz = ttk.Combobox(left_frm, textvariable=cursor_var, values=cursors, state="readonly")
                curz.pack()
                curz.bind("<<ComboboxSelected>>",lambda event:update_cursor(cursor_var,preview_label))

            else: ttk.Button(win, text=lang["pay_cursor"], command=lambda:settings_funcs.cr(win,start_time_,lang)).pack()
            clocks = ["Arial","Courier","DS-Digital","Quartz","Pixellari","Times","caviary","kadera",
                      "ATLAS_SCRITTO","title_ren","anak_paud","auto-sharp-pencil","gnf","trickr-logo",
                      "midfriend","playgum","pqrmonday","Kamikaze 3D Gradient","Starbim","Mexcellent 3D",
                      "Gunplay 3D",'Minecart LCD', 'Soviet Program', 'Nosifer', 'Hole - Hearted', 'PWJoyeuxNoel',
                      'CandyTime','Kingthings Christmas 2', 'Snowtop Caps', 'Haloberry' 'Crashed Scoreboard',
                      'Karnivore Black', 'Drawliner','Minisystem','Jigsaw Trouserdrop', 'Game Bubble',
                      'SAIBA-45', 'LIBRARY 3 AM', 'Neuropol', 'Overload', 'Perfect Dark (BRK)', 'Squares Bold',
                      "You're Gone",
                      'Xirod', 'Shlop', 'Budmo Jigglish' 'Living by Numbers', "Electroharmonix"
                      ]

            Label(left_frm, text=lang["sh_clock"],font = (gl_police,10),bg=global_bg,fg=global_fg).pack()
            cl = ""
            try: cl = read_encrypted_file("syst_comp/plc_clk.cfg")
            except: cl = "Arial"
            clock_var = StringVar(value=cl)
            cu1 = ttk.Combobox(left_frm, textvariable=clock_var, values=clocks, state="readonly")
            cu1.pack()
            cu1.bind("<<ComboboxSelected>>", lambda event:change_clk(clock_var,pr2))
            polices = ["Arial", "Courier", "Times", "Verdana", "Pixellari","Georgia","Comic Sans MS","Consolas",
                       "Fixedsys","Verdana Pro Black","Impact","Thinkers Dripping Demo","cultural literature demo",
                       "Apache Tomcat Demo","caviary","kadera","ATLAS_SCRITTO","title_ren","anak_paud","auto-sharp-pencil",
                       "gnf","trickr-logo","midfriend","playgum","pqrmonday","geniehive","paulo-bittencourt","sludgeborn",
                        "Drift Wood", "Kamikaze 3D Gradient","Starbim","Mexcellent 3D","Gunplay 3D",'Minecart LCD',
                       'Soviet Program', 'Zombie Holocaust', 'Nosifer', 'Hole - Hearted', 'PWJoyeuxNoel', 'CandyTime',
                        'Kingthings Christmas 2', 'Snowtop Caps', 'Haloberry', 'Crashed Scoreboard', 'Karnivore Black',
                       'Drawliner','Minisystem','Jigsaw Trouserdrop', 'Game Bubble','SAIBA-45', 'LIBRARY 3 AM', 'Neuropol',
                       'Overload', 'Perfect Dark (BRK)', 'Squares Bold', "You're Gone",
                        'Xirod', 'Shlop', 'Budmo Jigglish' 'Living by Numbers',"Electroharmonix"]

            cll = ""
            try: cll = read_encrypted_file("syst_comp/plc_sys.cfg")
            except: cll = "Arial"

            Label(left_frm, text=lang["sh-"], font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
            police_var = StringVar(value=cll)
            cu = ttk.Combobox(left_frm, textvariable=police_var, values=polices, state="readonly")
            cu.pack()
            cu.bind("<<ComboboxSelected>>", lambda event:change_sys(police_var,pr1))

            if stat == "TRUE":
                if galaxy or nebo:
                    btn = ttk.Button(right_frm, text=lang["off_exc"], command=lambda:settings_funcs.off(win,lang))
                    btn.pack()
            else:
                if galaxy or nebo:
                    btn = ttk.Button(right_frm, text=lang["on_exc"], command=lambda:settings_funcs.on(win,lang))
                    btn.pack()
            try: c = read_file("syst_comp/size.cfg",'r')
            except:
                write_file('syst_comp/size.cfg','w',"52")
                c = read_file("syst_comp/size.cfg",'r')
            Label(left_frm,text = lang["razm"] + "(px)",font = (gl_police,10),bg=global_bg,fg=global_fg).pack()

            sizes = "32","42","52","64","76","84"
            size_var = StringVar(value = c)
            cc = ttk.Combobox(left_frm, textvariable=size_var, values=sizes, state="readonly")
            cc.pack()

            Label(left_frm, text=lang["select-th"], font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()

            theme_var = StringVar()
            theme_var.set(win_theme)
            themes_list = ["standart","azure-light","azure-dark","forest-light","forest-dark"]

            cc = ttk.Combobox(left_frm, textvariable=theme_var, values=themes_list, state="readonly")
            cc.pack()
            dwn = ttk.Button(right_frm,text = lang["dwn_sdk"],command = lambda:download_funcs(root,lang,"sdk",global_bg,GlobalAlpha),state = "disabled")
            dwn.pack()
            dwn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["sdk_ne_dost"]))
            dwn.bind("<Leave>", hide_tooltip)
            dwn_d = ttk.Button(right_frm, text=lang["dwn_doc"], command=lambda: download_funcs(root, lang,"docs",global_bg,GlobalAlpha),
                             state="disabled")
            dwn_d.pack()
            dwn_d.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["doc_ne_dost"]))
            dwn_d.bind("<Leave>", hide_tooltip)

            if os.path.exists("password.db"):
                btn = ttk.Button(right_frm, text=lang["Change_password"] + "🔒", command=lambda:settings_funcs.change(win_p,lang,
                                                        start_time_,global_bg,global_fg,GlobalAlpha,invisible_pass))
                btn.pack()

                btn_delete = ttk.Button(right_frm, text=lang["Delete_password"] + "🔓", command=lambda:settings_funcs.delete_password(win,
                                                                                            lang,global_bg,start_time_,GlobalAlpha))
                btn_delete.pack()
            else:
                btn1 = ttk.Button(right_frm, text=lang["set_password"] + "🔒", command=lambda:settings_funcs.set_password(win_p,root,lang,
                        start_time_,global_bg,global_fg,gl_police,GlobalAlpha))
                btn1.pack()
            bt = ttk.Button(right_frm, text=lang["change-acc"], command=changge)
            bt.pack()
            btn = ttk.Button(right_frm, text=lang["logging_settings"], command=logging_settings)
            btn.pack()

            try:
                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM LOG_INFO")
                log_inf = cursor.fetchone()
                conn.commit()
                conn.close()
                if log_inf is None: log_inf = (0,)
            except: log_inf = (0,)

            try:
                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM SOUND_STATE")
                sound_st = cursor.fetchone()
                conn.commit()
                conn.close()
                if sound_st is None: sound_st = (0,)
            except: sound_st = (0,)
            try:
                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM AUT_STATE")
                aut_st = cursor.fetchone()
                conn.commit()
                conn.close()
                if aut_st is None: aut_st = (0,)
            except: aut_st = (0,)

            global night_state,image_wallpeper
            var_log = IntVar(value=log_inf[0])
            var_sound = IntVar(value=sound_st[0])
            var_night = IntVar(value=int(night_state))
            var_aut = IntVar(value=aut_st[0])
            var_wlp = IntVar()

            if image_wallpeper: var_wlp.set(1)
            else: var_wlp.set(0)

            var_auto_upd = BooleanVar()
            var_auto_upd.set(auto_update_enabled)
            var_antvrs = BooleanVar()
            var_antvrs.set(antvrs_state)
            var_email = BooleanVar()
            var_email.set(email_state)
            var_change = BooleanVar()
            var_change.set(change_state)
            var_block = BooleanVar()
            var_block.set(block_state)
            var_inv = BooleanVar()
            var_inv.set(invisible_pass)

            checkTexts = [lang["del_log"],lang["del_sound"],lang["vkl_n"],lang["vkl_aut"],lang["vkl_wlp"],lang["vkl_auto_upd"],
                          lang["vkl_antvrs"],lang["vkl_email"],lang["vkl_change"],lang["vkl_block"],lang["invisiblepass"]]
            checkVars = [var_log,var_sound,var_night,var_aut,var_wlp,var_auto_upd,var_antvrs,var_email,var_change,var_block,var_inv]
            checkCommands = [lambda: None,lambda: None,lambda: None,lambda: None,lambda:open_preview(),lambda: None,lambda:vklvivkl_antvrs(var_antvrs.get()),
                             lambda: vkl_email(var_email.get()),lambda: vkl_change(var_change.get()),
                             lambda: vkl_block(var_block.get()),lambda:invisiblepass(var_inv.get())]

            for i,(txt,var,com) in enumerate(zip(checkTexts,checkVars,checkCommands)):
                ctk.CTkSwitch(central_frm,progress_color="#00FF00",text_color = "black",button_color="#808080",
                              button_hover_color="#A9A9A9",fg_color = "#D3D3D3",
                              text=txt, onvalue=1, offvalue=0, variable=var,command = com).pack(anchor = "w")

            if image_wallpeper:
                ttk.Button(right_frm,text = lang["_change_"],command = open_preview).pack()
            btn = ttk.Button(right_frm, text=lang['set_pass_img'],command=lambda: open_preview_pass())
            btn.pack(anchor=S, side=BOTTOM)
            btn = ttk.Button(right_frm, text=lang['set_win_alpha'],command=lambda: set_alpha())
            btn.pack(anchor=S, side=BOTTOM)
            btn = ctk.CTkButton(win, fg_color = "#32CD32",hover_color = '#008000',text=lang["Apply"] + "✅",
                command=lambda: prim(var_log.get(), var_sound.get(), var_night.get()))
            btn.pack(anchor=S,side = BOTTOM)

        actives_programs.append("Pusk")
        log_to_file('Pusk launch',start_time_ = start_time_)
        global global_bg,GlobalAlpha
        win_p = create_window(root, lang["pusk"], global_bg, float(GlobalAlpha), 1300,750,"icons/interface/wndrs1.png")

        top_frame = Frame(win_p,bg=global_bg)
        top_frame.pack(side=TOP, fill=X, pady=5, padx=10)

        center_frame = Frame(win_p, bg=global_bg)
        center_frame.pack(side=TOP,anchor=W)
        center_frame.update()

        bottom_frame = Frame(win_p, bg=global_bg)
        bottom_frame.pack(side=BOTTOM,anchor=W)
        bottom_frame.update()

        acc = ImageTk.PhotoImage(
            Image.open(account_img).resize((50, 50), Image.Resampling.LANCZOS)
        )
        bios_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/uefi.png").resize((50, 50), Image.Resampling.LANCZOS))
        diagn_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/diagn.png").resize((50, 50), Image.Resampling.LANCZOS))
        logs_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/logs.png").resize((50, 50), Image.Resampling.LANCZOS))
        settings_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/settings.png").resize((50, 50), Image.Resampling.LANCZOS))
        param_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/parametrs.png").resize((50, 50), Image.Resampling.LANCZOS))
        rec_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/rec.png").resize((50, 50), Image.Resampling.LANCZOS))
        gbar_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/gamebar.png").resize((50, 50), Image.Resampling.LANCZOS))
        clock_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/clock.png").resize((50, 50), Image.Resampling.LANCZOS))
        cloud_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/cloud.png").resize((50, 50), Image.Resampling.LANCZOS))
        tmanager_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/taskmanager.png").resize((50, 50), Image.Resampling.LANCZOS))
        faq2_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/faq2.png").resize((50, 50), Image.Resampling.LANCZOS))
        rec_off_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/record_off.png").resize((50, 50), Image.Resampling.LANCZOS))
        shutdown_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/shutdown.png").resize((50, 50), Image.Resampling.LANCZOS))
        reboot_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/reboot.png").resize((50, 50), Image.Resampling.LANCZOS))
        upd_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/update.png").resize((50, 50), Image.Resampling.LANCZOS))
        hotkeys_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/hotkey.png").resize((50, 50), Image.Resampling.LANCZOS))

        commands = [lambda: settings_funcs.open_acc(win_p, lang, global_bg, global_fg, gl_police, edition, VERSION,start_time_),
                    lambda: os.startfile("uefi.exe"),
                    lambda: os_diagnost.os_diagn_win(root,lang,global_bg,global_fg,start_time_,actives_programs,GlobalAlpha),
                    lambda: settings_funcs.open_journal(win_p, global_bg, lang, start_time_),
                    settings,
                    lambda:settings_funcs.param(VERSION,win_p,lang,start_time_,global_bg,global_fg,gl_police,edition),
                    lambda: game_bar(),
                    lambda:clocks.open_clocks(root,lang,clock_type, gl_police, global_bg, global_fg, clock_win),
                    lambda: cloud.cloud(root,lang,actives_programs,global_bg,global_fg,start_time_),
                    lambda: t_manager.open_task_manager(state_sound, volume, errors, lang, root, actives_programs, start_time_,global_bg, global_fg),
                    lambda: settings_funcs.faq(win_p, lang, global_bg, gl_police),
                    open_update_window,
                    lambda: settings_funcs.show_hotkeys(win_p,lang,global_bg,global_fg,gl_police)]
        images = [acc,bios_img,diagn_img,logs_img,settings_img,param_img,gbar_img,clock_img,cloud_img,tmanager_img,
                  faq2_img,upd_img,hotkeys_img]
        tooltips_texts = [lang["ac"],lang["bios"],lang["os_diagnost"],lang["j"],lang["settings_tooltip"],lang["param_tooltip"],
        lang["g_tooltip"],lang["clock_tooltip"],lang["cloud_tooltip"],lang["tmanager_tooltip"],lang["faq_tooltip"],lang['show_upd'],lang["show_hotkey"]]

        for txt,img,comm in zip(tooltips_texts,images,commands):
            btn = ttk.Button(top_frame,image = img,command = comm)
            btn.image = img
            btn.pack(side="left", padx=10)
            btn.bind("<Enter>", lambda event, t=txt: show_tooltip(event, txt=t))
            btn.bind("<Leave>", hide_tooltip)

        if not is_recording:
            record_btn = ttk.Button(top_frame, image = rec_img, command=lambda: toggle_recording(record_btn))
            record_btn.image = rec_img
        else:
            record_btn = ttk.Button(top_frame, image=rec_off_img, command=lambda: toggle_recording(record_btn))
            record_btn.image = rec_off_img
        record_btn.pack(side=LEFT,padx=10)
        record_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["record_tooltip"]))
        record_btn.bind("<Leave>", hide_tooltip)

        for text, command in [
            (lang["ach"], lambda: ach(root, lang, global_bg, global_fg,GlobalAlpha)),
            (lang["show_screenshoots"], lambda: OpenWindow(root,lang,global_bg,global_fg,GlobalAlpha)),
            (lang["show_screenrecords"], lambda: OpenWindowRec(root, lang, global_bg, global_fg, GlobalAlpha)),
            (lang["activity_center"], lambda: activity_center.activity_center(root,lang,global_bg,global_fg,start_time_)),
            (lang["activity_control"],lambda:activity_control.control_window(root,lang,actives_programs,global_bg,global_fg)),
            (lang["wifiinfo"],lambda:GetWifiInfo.get_wifi_info(root,lang,start_time_)),
            (lang["pror"], lambda: settings_funcs.razr(win_p, lang, global_bg, global_fg, gl_police)),
            (lang["others_dev_projects"],lambda:settings_funcs.others_dev_projects(win_p,lang,global_bg,global_fg,gl_police,GlobalAlpha)),
            (lang["pod"], lambda: techSupport.techpodd(lang, root, errors, global_bg, global_fg, start_time_,GlobalAlpha)),
            (lang['show-changelogs'],lambda:WinDow(root,lang,selected_lang,GlobalAlpha)),
            (lang["Inf-er"], lambda: settings_funcs.open_errors_codes(win_p, lang, global_bg, global_fg, errors, gl_police)),
            (lang["licn"], lambda: settings_funcs.open_lic(win_p, lang, global_bg)),
            (lang["email_sender"],lambda: user_send_email.openWin(root,lang))
        ]:
            btn = ttk.Button(center_frame, text=text, command=command, width=30)
            btn.pack(pady=2)
        n,ln,e = return_user_info()
        btn_shutdown = ttk.Button(bottom_frame, image=shutdown_img,
                                  command=lambda: shutdown_animation(root,"shutdown", volume, errors, lang, actives_programs,
                                                                     is_recording, recording_thread, start_time_,e,state_sound))
        btn_shutdown.image = shutdown_img
        btn_shutdown.pack(side=LEFT)
        btn_shutdown.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["shutdown_tooltip"]))
        btn_shutdown.bind("<Leave>", hide_tooltip)
        btn_reboot = ttk.Button(bottom_frame, image=reboot_img,
                                command=lambda: shutdown_animation(root,"reboot", volume, errors, lang, actives_programs,
                                                                   is_recording, recording_thread, start_time_,e,state_sound))
        btn_reboot.image = reboot_img
        btn_reboot.pack(side=LEFT)
        btn_reboot.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["reboot_tooltip"]))
        btn_reboot.bind("<Leave>", hide_tooltip)
        Label(bottom_frame,text = "© Developped by SVB",bg = global_bg,fg=global_fg,font = ("Arial",15,"bold")).pack()
    def save_volume(val, gr):
        global sound_but
        try:
            volume = float(val)
            if int(volume) == 0: sound_b.config(image=sound_off)
            elif 0.01 < float(volume) <= 49.0: sound_but.config(image=sound_low)
            else: sound_but.config(image=sound)
            if gr is not None: gr.config(text=f"{volume:.1f}")

            volume_str = str(volume)
            write_encrypted_file("syst_comp/volume.cfg", volume_str)
        except Exception as e:
            log_to_file(f"Error with save volume: {e}",level="error",start_time_ = start_time_)
    def sound_bar():
        global gl_police,sound_win,taskbar_height
        sound_b.config(bg=taskbar_fg)
        sound_win = Toplevel(root)

        sound_win.attributes('-alpha',0.0)
        fade_in(sound_win)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 200 - 100
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset - 250
        sound_win.overrideredirect(True)
        sound_win.geometry(f"200x200+{x}+{y}")
        sound_win.config(bg=global_bg)
        sound_win.title("Sound bar")
        img = Image.open("icons/interface/sound.png")
        icon_image = ImageTk.PhotoImage(img)
        sound_win.iconphoto(False, icon_image)
        Label(sound_win, text=lang["grom"], font=(gl_police,10),bg=global_bg,fg=global_fg).pack()

        gr = Label(sound_win, text="", font=("Arial", 13),bg=global_bg,fg=global_fg)
        gr.pack()
        try:
            content = read_encrypted_file("syst_comp/volume.cfg")
            v = float(content)
        except Exception:
            v = 50.0

        volume_slider = ttk.Scale(sound_win, from_=0, to=100, orient='horizontal', command=lambda val: save_volume(val, gr))
        volume_slider.set(v)
        volume_slider.pack(side="top", padx=10)

        gr.config(text=f"{v:.1f}")
        sound_win.protocol("WM_DELETE_WINDOW", lambda: (sound_b.config(bg=taskbar_bg), sound_win.destroy(),fade_out(calendar_win)))
    def place_shortcuts(size, rowss, color):
        global row, col, icon_refs, image_wallpeper, labels,icons

        row, col = 0, 0
        icon_refs = {}
        for widget in shortcut_frame.winfo_children():
            widget.destroy()
        user_codes_folder = "user_progs"
        if os.path.isdir(user_codes_folder):
            files = os.listdir(user_codes_folder)
            for file in files:
                if file.endswith(".py"):
                    name = os.path.splitext(file)[0]
                    icon_path = None
                    for ext in [".png", ".jpg", ".jpeg", ".gif"]:
                        candidate = os.path.join(user_codes_folder, name + ext)
                        if os.path.isfile(candidate):
                            icon_path = candidate
                            break
                    if icon_path is None:
                        icon_path = "icons/default_icon.png"

                    icons[name] = icon_path

                    def run_user_code(script_name=name):
                        script_path = os.path.join(user_codes_folder, script_name + ".py")
                        try:
                            code = read_file(script_path,'r')
                            exec(code, {"__name__": "__main__"})
                        except Exception as e:
                            messagebox.showerror(lang["error"],f"{lang['error_execute']} {script_name}:{e}",parent=root)
                            log_to_file(f"Executing error {script_name}: {e}",level="error",start_time_ = start_time_)
                    program_functions[name] = run_user_code

        def safe_run(prog_id):
            try:
                func = program_functions.get(prog_id)
                if func is None:
                    raise KeyError(f"No function for '{prog_id}' in program_functions")
                func()
            except Exception as e:
                import traceback
                err_text = f"[{datetime.now()}] {lang['error_in_launch']} '{prog_id}': {e}\n{traceback.format_exc()}"
                log_to_file(err_text, level="error", start_time_=start_time_)
                messagebox.showerror(lang['error_in_launch'], err_text)
        for prog_id, path in icons.items():
            display_name = lang.get(prog_id, prog_id)
            if prog_id not in ["file_manager", "photov", "video_player", "store", "calculator", "task_manager"]:
                try:
                    image = Image.open(path)
                    image = image.resize((int(size), int(size)), Image.Resampling.LANCZOS)
                    icon = ImageTk.PhotoImage(image)
                    icon_refs[prog_id] = icon
                except Exception as e:
                    log_to_file(f"Load Image Error {prog_id}: {e}", level="warning", start_time_=start_time_)
                    continue
                button = Button(shortcut_frame,image=icon_refs[prog_id],width=int(size),height=int(size),
                    command = program_functions.get(display_name, lambda prog_id=prog_id: safe_run(prog_id)))
                button.grid(row=row, column=col, padx=10, pady=5)

                if image_wallpeper:
                    label = Label(shortcut_frame, text=display_name,
                                  bg = "#2C3E50",fg="white", font=('Arial', 6) if prog_id == "millionaire" else None)
                elif color in ("yellow", "#00FF00"):
                    if not custom_wallpeper:
                        label = Label(shortcut_frame, text=display_name, bg=color, fg="black",
                                      font=('Arial', 6) if prog_id == "millionaire" else None)
                    else:
                        label = Label(shortcut_frame, text=display_name, fg="black",
                                      font=('Arial', 6) if prog_id == "millionaire" else None)
                else:
                    if not custom_wallpeper:
                        label = Label(shortcut_frame, text=display_name, bg=color, fg="white",
                                      font=('Arial', 6) if prog_id == "millionaire" else None)
                    else:
                        label = Label(shortcut_frame, text=display_name, bg="black", fg="white",
                                      font=('Arial', 6) if prog_id == "millionaire" else None)

                label.grid(row=row + 1, column=col, padx=10, pady=5)
                labels.append(label)

                row += 2
                if row >= rowss * 2:
                    row = 0
                    col += 1
    def volume_plus(event,n):
        def close_win(): Win.destroy()

        Win = Toplevel(root)
        Win.attributes("-alpha", float(GlobalAlpha))
        Win.title("")
        Win.configure(bg=global_bg)
        Win.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 400 - 700
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset
        Win.overrideredirect(True)
        Win.geometry(f"400x50+{x}+{y}")
        img = Image.open("icons/interface/sound.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        try:
            content = read_encrypted_file("syst_comp/volume.cfg")
            v = float(content)
        except Exception:
            v = 50.0
        v += float(n)
        if int(v) == 0:
            sound_b.config(image=sound_off)
        elif 0.01 < float(v) <= 49.0:
            sound_but.config(image=sound_low)
        else:
            sound_but.config(image=sound)
        write_encrypted_file("syst_comp/volume.cfg",str(v))
        gr = Label(Win,text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
        gr.pack()
        volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
        volume_slider.set(v)
        volume_slider.pack(side="top", padx=10)
        volume_slider.config(state="disabled")

        Win.after(3000,lambda:close_win())
    def volume_min(event, n):
        def close_win(): Win.destroy()

        Win = Toplevel(root)
        Win.attributes("-alpha", float(GlobalAlpha))
        Win.title("")
        Win.configure(bg=global_bg)
        Win.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 400 - 700
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset
        Win.overrideredirect(True)
        Win.geometry(f"400x50+{x}+{y}")
        img = Image.open("icons/interface/sound.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        try:
            content = read_encrypted_file("syst_comp/volume.cfg")
            v = float(content)
        except Exception:
            v = 50.0
        v -= float(n)
        if int(v) == 0: sound_b.config(image=sound_off)
        elif 0.01 < float(v) <= 49.0: sound_but.config(image=sound_low)
        else: sound_but.config(image=sound)

        write_encrypted_file("syst_comp/volume.cfg", str(v))
        gr = Label(Win, text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
        gr.pack()
        volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
        volume_slider.set(v)
        volume_slider.pack(side="top", padx=10)
        volume_slider.config(state="disabled")

        Win.after(3000, lambda: close_win())
    def mute(event):
        def close_win(): Win.destroy()
        global mute_state,user_volume
        Win = Toplevel(root)
        Win.attributes("-alpha", float(GlobalAlpha))
        Win.title("")
        Win.configure(bg=global_bg)
        Win.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 400 - 700
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset
        Win.overrideredirect(True)
        Win.geometry(f"400x50+{x}+{y}")
        img = Image.open("icons/interface/sound.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        if mute_state == "False":
            mute_state = "True"
            write_encrypted_file("syst_comp/mute.cfg", "True")
            try:
                content = read_encrypted_file("syst_comp/volume.cfg")
                v = float(content)
            except Exception: v = 50.0
            user_volume = v
            write_encrypted_file("syst_comp/user_v.cfg", str(user_volume))
            v = 0.0
            write_encrypted_file("syst_comp/volume.cfg", str(v))
        else:
            mute_state = "False"
            write_encrypted_file("syst_comp/mute.cfg","False")
            try:
                content = read_encrypted_file("syst_comp/user_v.cfg")
                v = float(content)
            except Exception: v = 50.0
        if int(v) == 0: sound_b.config(image=sound_off)
        elif 0.01 < float(v) <= 49.0: sound_but.config(image=sound_low)
        else: sound_but.config(image=sound)

        write_encrypted_file("syst_comp/volume.cfg",str(v))
        gr = Label(Win,text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
        gr.pack()
        volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
        volume_slider.set(v)
        volume_slider.pack(side="top", padx=10)
        volume_slider.config(state="disabled")

        Win.after(3000,lambda:close_win())
    def open_update_window():
        for widget in root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()
        w = Toplevel(root)
        w.attributes("-alpha", float(GlobalAlpha))
        w.geometry("500x500")
        w.title(lang['update-'])
        img = Image.open("icons/interface/update.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)

        date_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/date.png").resize((25, 25), Image.Resampling.LANCZOS))
        serv_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/server.png").resize((25, 25), Image.Resampling.LANCZOS))
        local_img = ImageTk.PhotoImage(
            Image.open(f"icons/interface/local.png").resize((25, 25), Image.Resampling.LANCZOS))

        serv = read_file("syst_comp/updates/update_flag.cache",'r')
        local = read_file("versions/current_version.txt",'r')
        frm1 = Frame(w)
        frm1.pack()
        frm2 = Frame(w)
        frm2.pack()
        frm3 = Frame(w)
        frm3.pack()

        lbl = Label(frm1,image = date_img)
        lbl.image = date_img
        lbl.pack(side = LEFT)
        Label(frm1, text=f"{lang['last_check']}: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", font=("Arial", 10)).pack(side = LEFT)
        lbl = Label(frm2, image=serv_img)
        lbl.image = serv_img
        lbl.pack(side=LEFT)
        Label(frm2,text = f'{lang["server_version"]}: {serv}',font = ("Arial",15,"bold"),fg = "blue").pack(side = LEFT)
        lbl = Label(frm3, image=local_img)
        lbl.image = local_img
        lbl.pack(side=LEFT)
        Label(frm3,text = f'{lang["local_version"]}: {local}',font = ("Arial",15,"bold"),fg = "blue").pack(side = LEFT)
        if serv != local:
            Label(w,text = lang["avaible_upd"],font = ("Arial",11,"bold"),fg = "red").pack()
            ttk.Button(w,text = lang['update_w'],command = run_updater).pack()
        else: Label(w, text=lang["no_avaible_upd"], font=("Arial", 10, "bold"), fg="red").pack()
    def check_update_flag():
        fl = read_file("syst_comp/updates/update_flag.cache",'r')
        c = read_file('versions/current_version.txt','r')
        if c != fl: return True
        else: return False
    def blink_button(button):
        def toggle():
            button.config(bg="#FF0000" if button.cget("bg") != "#FF0000" else "#FF8C00")
            button.after(500, toggle)
        toggle()
    def monitor_update_flag():
        global update_button_added
        if check_update_flag() and not update_button_added:
            try:
                update_icon = Image.open("icons/interface/update.png").resize((32, 32))
                update_icon = ImageTk.PhotoImage(update_icon)
                update_button = Button(taskbar, image=update_icon, command=open_update_window, bg="red")
                update_button.image = update_icon
                update_button.pack(side="right", padx=5)
                blink_button(update_button)
                taskbar_buttons.append(("Update", update_button))
                update_button_added = True
            except Exception as e:
                log_to_file(f"[UI] Failed to load update icon: {e}", level="error",start_time_ = start_time_)

        root.after(10000, monitor_update_flag)
    def show_taskbar_context_menu(event):
        menu = Menu(taskbar, tearoff=0)

        for prog_id in icons:
            if not any(btn[0] == prog_id for btn in taskbar_buttons):
                display_name = lang.get(prog_id, prog_id)
                menu.add_command(
                    label=f"{lang['addtotask']} {display_name}",
                    command=lambda n=prog_id: add_taskbar_button(taskbar, n, program_functions[n], icons)
                )

        menu.add_separator()
        for prog_id, btn in taskbar_buttons:
            if prog_id not in ["task_manager", "calculator", "file_manager", "video_player", "photov", "store"]:
                display_name = lang.get(prog_id, prog_id)
                menu.add_command(
                    label=f"❌ {lang['delete']} {display_name}",
                    command=lambda n=prog_id: remove_from_taskbar(n)
                )

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    def save_taskbar_buttons(buttons):
        """Сохраняем список кнопок (только ID программ, а не переводы)"""
        with open(TASKBAR_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump([{"id": prog_id} for prog_id, _ in buttons],
                      f, ensure_ascii=False, indent=4)
    def load_taskbar_buttons():
        """Загружаем список кнопок из JSON"""
        if os.path.exists(TASKBAR_CONFIG_FILE):
            with open(TASKBAR_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    def add_taskbar_button(frame, prog_id, command, icons):
        if prog_id not in icons:
            log_to_file(f"Taskbar: icon not found for {prog_id}", level="warning", start_time_=start_time_)
            return

        img = ImageTk.PhotoImage(Image.open(icons[prog_id]).resize((45, 45)))
        btn = Button(frame, image=img, command=command, bg=taskbar_bg, bd=0)
        btn.image = img
        btn.pack(side=LEFT, padx=2)

        taskbar_buttons.append((prog_id, btn))
        save_taskbar_buttons(taskbar_buttons)
    def remove_from_taskbar(prog_id):
        global taskbar_buttons
        for i, (pid, button) in enumerate(taskbar_buttons):
            if pid == prog_id:
                button.destroy()
                taskbar_buttons.pop(i)
                break
        save_taskbar_buttons(taskbar_buttons)
    def restore_taskbar_buttons(frame, command_map, icons):
        """Восстанавливаем кнопки из JSON"""
        loaded = load_taskbar_buttons()
        id_to_lang = {
            "store": lang["store"],
            "calculator": lang["calculator"],
            "task_manager": lang["task_manager"],
            "video_player": lang["video_player"],
            "photov": lang["photov"],
            "file_manager": lang["file_manager"]
        }

        for b in loaded:
            prog_id = b["id"]
            if prog_id in icons:
                try:
                    img = ImageTk.PhotoImage(Image.open(icons[prog_id]).resize((32, 32)))
                    command_map = {
                        prog_id: program_functions[id_to_lang[prog_id]]
                        for prog_id in id_to_lang
                        if id_to_lang[prog_id] in program_functions
                    }

                    btn = Button(frame, image=img, command=command_map[prog_id], bg=taskbar_bg, bd=0)
                    btn.image = img
                    btn.pack(side=LEFT, padx=2)
                    btn.bind("<Enter>", lambda event,bt = btn: bt.config(bg=taskbar_fg))
                    btn.bind("<Leave>", lambda event,bt = btn: bt.config(bg=taskbar_bg))
                    taskbar_buttons.append((prog_id, btn))
                except Exception as e:
                    log_to_file(f"Taskbar restore error {prog_id}: {e}", level="error", start_time_=start_time_)
    def show_battery_info(event=None):
        import psutil
        global bat_win,battery_bt,battery_label,taskbar_height
        battery_bt.config(bg = taskbar_fg)
        battery_label.config(bg = taskbar_fg)
        if hasattr(root, 'battery_info_window') and root.battery_info_window.winfo_exists():
            root.battery_info_window.lift()
            return

        battery = psutil.sensors_battery()

        bat_win = Toplevel(root)
        bat_win.title(lang["bat_info"])
        bat_win.configure(bg=global_bg)
        bat_win.attributes("-topmost", True)
        bat_win.attributes('-alpha', 0.0)
        fade_in(bat_win)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 400 - 100
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset - 250
        bat_win.overrideredirect(True)
        bat_win.geometry(f"400x250+{x}+{y}")
        img = Image.open("icons/interface/full.png")
        icon_image = ImageTk.PhotoImage(img)
        bat_win.iconphoto(False, icon_image)
        root.battery_info_window = bat_win

        if battery:
            percent = battery.percent
            charging = battery.power_plugged
            secsleft = battery.secsleft

            if secsleft == psutil.POWER_TIME_UNLIMITED:
                time_left = lang["bezk"]
            elif secsleft == psutil.POWER_TIME_UNKNOWN:
                time_left = lang["unknow"]
            else:
                mins, secs = divmod(secsleft, 60)
                hours, mins = divmod(mins, 60)
                time_left = f"{hours:02}:{mins:02}"

            Label(bat_win, text=f"{lang['zarad']} {percent}%", font=("Arial", 12), bg=global_bg, fg=global_fg).pack(pady=5)
            Label(bat_win, text=f"{lang['stat_bat']} {lang['zarad_up'] if charging else lang['razrad']}", font=("Arial", 12), bg=global_bg, fg=global_fg).pack(pady=5)
            Label(bat_win, text=f"{lang['ostalos']} {time_left}", font=("Arial", 12), bg=global_bg, fg=global_fg).pack(pady=5)

            Button(bat_win, text=lang['zakrit'], command=bat_win.destroy, bg="#3498db", fg=global_fg, relief="flat").pack(
                pady=10)
        else:
            Label(bat_win, text=lang['bat_neob'], font=("Arial", 12), bg=global_bg, fg=global_fg).pack(pady=20)
    def date_c():
        global calendar_win,date_label,taskbar_height
        date_label.config(bg = taskbar_fg)
        calendar_win = Toplevel(root)
        calendar_win.title(lang['calendar'])
        calendar_win.config(bg=global_bg)
        calendar_win.attributes('-alpha',0.0)
        fade_in(calendar_win,0.0)
        screen_width = root.winfo_screenwidth()
        x = screen_width - 300 - 100
        offset = 50
        taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
        y = taskbar_screen_y - offset - 250
        calendar_win.overrideredirect(True)
        calendar_win.geometry(f"300x250+{x}+{y}")
        img = Image.open("icons/interface/kalen.png")
        icon_image = ImageTk.PhotoImage(img)
        calendar_win.iconphoto(False, icon_image)
        with open("syst_comp/locales.json","r") as f:
            lcls = json.load(f)
        date_entry = Calendar(calendar_win, width=30, background=global_bg, foreground=global_fg,
                                  bordercolor=global_fg,
                                  headersbackground=global_bg, headersforeground=global_fg, selectbackground='blue',
                                  selectforeground=global_bg, weekendbackground=global_bg, weekendforeground='red',
                                  date_pattern='dd.mm.yyyy',
                                  locale=lcls[selected_lang])
        date_entry.pack(pady=10)
    def run_updater():
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        updater_path = os.path.join(exe_dir, "updater.exe")
        log_to_file(f"Updater Path: {updater_path}",start_time_=start_time_)
        log_to_file(f"Exists: {os.path.exists(updater_path)}", start_time_=start_time_)
        if os.path.exists(updater_path):
            threading.Thread(target = ctypes.windll.shell32.ShellExecuteW(None, "runas", updater_path, None, None, 1))
        else:
            log_to_file(f"Updater not found", start_time_=start_time_,level="error")
    def trigger_bsod():
        root.destroy()
        bsod.open_bsod("TY0001x001", "Test BSOD", on_finish=main)

    root = Tk()
    root.title(f"WinDoors 52 - {VERSION}")
    check_activity_limit()
    root.bind("<Control-Key-1>", lambda event:volume_plus(event,2))
    root.bind("<Control-Key-2>", lambda event:volume_min(event,2))
    root.bind("<Control-Key-3>", lambda event:mute(event))
    root.bind("<Control-Shift-A>",lambda event:ecran_block.ecran_b(root,lang,errors,state_sound,actives_programs,volume,
    recording_thread,is_recording,start_time_,email,selected_lang))
    root.bind_all("<Motion>", lambda event:on_activity)
    root.bind_all("<KeyPress>", lambda event:on_activity)
    root.bind_all("<Button>", lambda event:on_activity)
    start_timer()
    root.focus_set()

    if win_theme != 'standart':
        if win_theme in ["azure-light","azure-dark"]:
            root.tk.call("source", "themes/azure.tcl")
            style = ttk.Style(root)
            style.theme_use(win_theme)
        else:
            root.tk.call("source", f"themes/{win_theme}.tcl")
            style = ttk.Style(root)
            style.theme_use(win_theme)
    else:
        style = ttk.Style(root)
        style.theme_use('vista')
    _,_,email = return_user_info()

    program_functions = {
        lang['email_sender']:lambda:user_send_email.openWin(root,lang),
        'Photo Generator':lambda:soft.gener_photo(root,lang,global_bg,global_fg,GlobalAlpha),
        'SVB Hotels':lambda:hotels.open_hotel_window(root,lang,global_bg,global_fg,start_time_,edition,GlobalAlpha),
        'SVB PhotoEditor':lambda:photo_editor.open_editor_win(root,lang,global_bg,global_fg,actives_programs),
        lang["cleaning"]:lambda:cleaning.cleanup_window(root,lang,global_bg,global_fg,actives_programs,GlobalAlpha),
        "SVB History's":lambda:historys.open_hst_window(root,lang,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha),
        'SVBTube':lambda:svbtube.svbtube(root,lang,actives_programs,global_bg,global_fg,GlobalAlpha),
        lang["video_player"]:lambda:video_player(root,lang,actives_programs,global_bg,global_fg,GlobalAlpha),
        'SVB Bookmaker':lambda:BookMaker.open_win(root,lang,actives_programs,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        "Internet Store":lambda:SVBStore.main_w(root,lang,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        "SVB Archiver":lambda:archivator.open_archivator(actives_programs,root,lang,start_time_,global_bg,global_fg,GlobalAlpha),
        "SVB TxT Redactor":lambda:svbred.redactor(root,lang,start_time_,global_bg,global_fg,GlobalAlpha),
        'Book reader':lambda:book.bbb(actives_programs,root,lang,start_time_,global_bg,global_fg,GlobalAlpha),
        'Password Manager':lambda:manager(lang,actives_programs,root,errors,start_time_,global_bg,global_fg,GlobalAlpha),
        "Trade":lambda:trade.trade(actives_programs,lang,root,start_time_,global_bg,global_fg,GlobalAlpha),
        'Lottery': lambda:soft.lotereya(actives_programs,lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        "Promocodes": lambda:soft.promocodes(lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        "SVB SpeedTest":lambda:speedtest(root,lang,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha),
        "State Services": lambda:gos.gosuslugi(root,lang,actives_programs,errors,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        lang["file_manager"]: lambda:file_manager.open_file_manager(state_sound, root, lang, global_bg,actives_programs,gl_police,global_fg,volume,errors,start_time_,GlobalAlpha),
        "CMD": lambda: commandConsole.open_terminal(VERSION,time.time() - start_time_,vpn, lang, volume, errors, actives_programs, is_recording, recording_thread, root, trigger_bsod,GlobalAlpha),
        lang["calculator"]: lambda:soft.open_calc(state_sound,volume,errors,lang,root,actives_programs,color,special_frames,start_time_,GlobalAlpha),
        lang["browser"]: lambda:browser.open_browser(root,lang,state_sound,volume,start_time_,actives_programs,global_bg,global_fg,wifi_state,GlobalAlpha),
        lang["store"]: open_store,
        lang["globalchat"]:lambda:globalchat.chat_win(root,lang,email,start_time_,GlobalAlpha),
        lang["os_diagnost"]:lambda:os_diagnost.os_diagn_win(root,lang,global_bg,global_fg,start_time_,actives_programs,GlobalAlpha),
        lang["case"]: lambda:cases.cases(actives_programs,state_sound,volume,root,errors,edition,lang,start_time_,global_bg,global_fg,GlobalAlpha),
        lang["pod1"]: lambda:techSupport.techpodd(lang,root,errors,global_bg,global_fg,start_time_,GlobalAlpha),
        lang["task_manager"]: lambda:t_manager.open_task_manager(state_sound,volume,errors,lang,root,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha),
        lang["mus_pl1"]: lambda:soft.open_mus(lang,root,actives_programs,volume,state_sound,errors,start_time_,global_bg,global_fg,GlobalAlpha),
        lang["photov"]:lambda:photo_viewer(root,lang,global_bg,start_time_,actives_programs,GlobalAlpha),
        "Telegrom": lambda:messanger.open_mes(lang,root,actives_programs,volume,state_sound,errors,start_time_,global_bg,global_fg,GlobalAlpha),
        "VPN": lambda:VPN.open_vpn(root,lang,actives_programs,start_time_,volume,state_sound,edition,global_bg,global_fg,reg,GlobalAlpha),
        "Paint": lambda:soft.open_paint(state_sound,volume,actives_programs,errors,lang,root,start_time_,GlobalAlpha),
        lang["bank"]: lambda:bank.svbcoins(state_sound,volume,lang,root,errors,gl_police,actives_programs,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        lang['standart_games']:lambda:standart_games.standart_games(root,lang,actives_programs,state_sound,start_time_,volume,errors,global_bg,global_fg,GlobalAlpha),
        "Auto plate": lambda:buy_num.buy_num(lang,root,edition,errors,start_time_,global_bg,global_fg,GlobalAlpha),
        "Telephone": lambda:soft.pokup_nomer(lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        lang["antivirus"]: lambda:antvrs.open_antv(actives_programs,root,lang,color,special_frames,start_time_,GlobalAlpha),
        lang["notepad"]: lambda:soft.open_notepad(state_sound,lang,root,volume,errors,actives_programs,global_fg,global_bg,start_time_,GlobalAlpha),
        "Casino": lambda:casino.open_casino(state_sound,volume,root,actives_programs,errors,lang,edition,start_time_,global_bg,global_fg,GlobalAlpha),
        "IDE Py": lambda:ides.create_ide("Python",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE C++": lambda:ides.create_ide("C++",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE C": lambda:ides.create_ide("C",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE C#": lambda:ides.create_ide("C#",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE HTML CSS": lambda:ides.create_ide("HTML",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE JavaScript": lambda:ides.create_ide("JavaScript",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE TS": lambda:ides.create_ide("TypeScript",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Kotlin": lambda:ides.create_ide("Kotlin",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Dart": lambda:ides.create_ide("Dart",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Ruby": lambda:ides.create_ide("Ruby",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Rust": lambda:ides.create_ide("Rust",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE SQL": lambda:ides.create_ide("SQL",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE PHP": lambda:ides.create_ide("PHP",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Universal": lambda:ides.open_main_ide_menu(actives_programs,root,lang,state_sound,errors,volume,start_time_,GlobalAlpha),
        "IDE Swift": lambda:ides.create_ide("Swift",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE GO": lambda:ides.create_ide("GO",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "IDE Java": lambda:ides.create_ide("Java",actives_programs,root,lang,state_sound,volume,start_time_,GlobalAlpha),
        "SVB Antivirus": lambda:SVBantvrs.svb_ant(root,lang,start_time_,svb_coins,GlobalAlpha,global_bg),
        "Translator": lambda:soft.translate(root,actives_programs,state_sound,volume,errors,lang,global_fg,global_bg,start_time_,GlobalAlpha),
        "Delivery": lambda:deliv.delivery(root,lang,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha)
    }

    try:
        image = Image.open("icons/interface/wndrs1.png")
        icon_image = ImageTk.PhotoImage(image)
        root.icon_img_ref = icon_image
        root.iconphoto(False, root.icon_img_ref)
    except Exception as e: log_to_file(f"Error to load icon: {e}", level="error", start_time_=start_time_)

    cursor_name = load_cursor(start_time_)
    root.config(cursor=cursor_name)
    root.attributes('-fullscreen', True)

    global change_state,taskbar_height

    if not image_wallpeper: root.configure(bg=str(color))
    try: st = read_encrypted_file("stexc.wndrs")
    except Exception: st = "FALSE"

    if st == "TRUE":
        if nebo and galaxy:
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            canvas = Canvas(root, width=width, height=height, highlightthickness=0)
            canvas.place(x=0, y=0)
            draw_galaxy(canvas,width, height,4000)
        elif nebo:
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            canvas = Canvas(root, width=width, height=height, highlightthickness=0)
            canvas.place(x=0, y=0)
            draw_night_sky(canvas, width, height, 700)
        else:
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            canvas = Canvas(root, width=width, height=height, highlightthickness=0)
            canvas.place(x=0, y=0)
            draw_galaxy(canvas, width, height, 800)
        if galaxy_:
            canvas = Canvas(root, width=width, height=height, highlightthickness=0)
            canvas.place(x=0, y=0)
            anim_galaxy(canvas,root)
    elif custom_wallpeper:
        start_color, end_color = load_gradient_colors()
        canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
        canvas.place(x=0, y=0)
        draw_gradient(canvas, start_color, end_color,root,lang)
        canvas.update()

        shortcut_frame = Frame(root, bg="", highlightthickness=0)
        shortcut_frame.place(x=50, y=50)
    elif change_state:
        global canvas_icon
        paths = []
        for name in os.listdir("icons/wallpepers"):
            full = os.path.join("icons/wallpepers", name)
            if os.path.isfile(full):
                paths.append(f'icons/wallpepers/{name}')
        img_path_ = random.choice(paths)
        canvas_icon = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                             highlightthickness=0)
        canvas_icon.place(x=0, y=0)
        image = Image.open(img_path_)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)
        canvas_icon.create_image(0, 0, anchor="nw", image=photo)
        canvas_icon.image = photo
        canvas_icon.update()
        shortcut_frame = Frame(root, bg="", highlightthickness=0)
        shortcut_frame.place(x=50, y=50)
    elif image_wallpeper:
        canvas_icon = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
        canvas_icon.place(x=0, y=0)
        image = Image.open(img_path)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)
        canvas_icon.create_image(0, 0, anchor="nw", image=photo)
        canvas_icon.image = photo
        canvas_icon.update()
        shortcut_frame = Frame(root, bg="", highlightthickness=0)
        shortcut_frame.place(x=50, y=50)
    else:
        shortcut_frame = Frame(root, bg=str(color))
        shortcut_frame.place(x=50, y=50)
        root.config(bg = str(color))

    taskbar = Frame(root, bg=taskbar_bg, height=40)
    taskbar.pack(side="bottom", fill="x")

    root.update()
    taskbar_height = taskbar.winfo_height()

    taskbar.bind("<Button-3>", show_taskbar_context_menu)

    clock_frame = Frame(taskbar, bg=taskbar_bg)
    clock_frame.pack(side="right", padx=10, pady=5)
    global clock_label
    digital_font = (clock, 18, "bold")
    clock_label = Label(clock_frame, text="", fg="white", bg=taskbar_bg, font=digital_font)
    clock_label.pack(anchor="n")
    clock_label.bind("<Button-1>", lambda event: toggle_clock())

    today = date.today().strftime("%d.%m.%Y")
    global date_label
    date_label = Label(clock_frame, text=today, fg="white", bg=taskbar_bg)
    date_label.pack(anchor="s")
    date_label.bind("<Button-1>", lambda event: toggle_calendar())
    clock_frame.bind("<Enter>", lambda event: [clock_frame.config(bg=taskbar_fg), clock_label.config(bg=taskbar_fg),
                                               date_label.config(bg=taskbar_fg)])
    clock_frame.bind("<Leave>", lambda event: [clock_frame.config(bg=taskbar_bg), date_label.config(bg=taskbar_bg),
                                               clock_label.config(bg=taskbar_bg)])

    bat_frm = Frame(taskbar, bg=taskbar_bg)
    bat_frm.pack(side="right")
    global battery_bt, battery_label
    sound = ImageTk.PhotoImage(Image.open("icons//interface//sound.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_off = ImageTk.PhotoImage(Image.open("icons//interface//soundoff.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_low = ImageTk.PhotoImage(Image.open("icons//interface//soundlow.png").resize((32, 32), Image.Resampling.LANCZOS))
    battery_bt = Label(bat_frm, text="", font=("Arial", 14), bg=taskbar_bg, fg="white")
    battery_bt.pack(side="top", padx=10)
    battery_label = Label(bat_frm, text="", font=("Arial", 10), bg=taskbar_bg, fg="white")
    battery_label.pack(side="bottom", padx=10)
    battery_bt.bind("<Button-1>", lambda event: toggle_bat())
    update_battery()
    bat_frm.bind("<Enter>", lambda event: [bat_frm.config(bg=taskbar_fg), battery_label.config(bg=taskbar_fg),
                                           battery_bt.config(bg=taskbar_fg)])
    bat_frm.bind("<Leave>", lambda event: [battery_bt.config(bg=taskbar_bg), battery_label.config(bg=taskbar_bg),
                                           bat_frm.config(bg=taskbar_bg)])

    global sound_but
    volume_percent = float(volume) * 100
    imgS = ""
    if volume_percent == 0: imgS = sound_off
    elif 0 < volume_percent <= 49:imgS = sound_low
    else: imgS = sound

    sound_b = Label(taskbar, image=imgS, bg=taskbar_bg)
    sound_b.pack(side="right", padx=10)
    sound_but = sound_b
    sound_b.bind("<Button-1>", lambda event: toggle_sound_window())
    sound_b.bind("<Enter>", lambda event: sound_b.config(bg=taskbar_fg))
    sound_b.bind("<Leave>", lambda event: sound_b.config(bg=taskbar_bg))

    wifi_on_icon = ImageTk.PhotoImage(Image.open("icons/interface/wifi_on.png").resize((32, 32), Image.Resampling.LANCZOS))
    wifi_off_icon = ImageTk.PhotoImage(Image.open("icons/interface/wifi_off.png").resize((32, 32), Image.Resampling.LANCZOS))

    global wifi_button
    if wifi_state:
        wifi_button = Label(taskbar, image=wifi_on_icon, bg=active_bg)
        wifi_button.bind('<Button-1>', lambda event: toggle_wifi_window())
    else:
        wifi_button = Label(taskbar, image=wifi_off_icon, bg=active_bg)
        wifi_button.bind('<Button-1>', lambda event: toggle_wifi_window())
    wifi_button.image_on = wifi_on_icon
    wifi_button.image_off = wifi_off_icon
    wifi_button.pack(side="right", padx=10)
    wifi_button.bind("<Enter>", lambda event: wifi_button.config(bg=taskbar_fg))
    wifi_button.bind("<Leave>", lambda event: wifi_button.config(bg=taskbar_bg))

    global vpn_label
    if vpn == "on":
        vpn_label = Label(taskbar, text="VPN", fg="white", bg=taskbar_bg, font=("Arial", 12))
        vpn_label.pack(side="right", padx=10)
        vpn_label.bind('<Button-1>', lambda event: toggle_vpn())
        vpn_label.bind("<Enter>", lambda event: vpn_label.config(bg=taskbar_fg))
        vpn_label.bind("<Leave>", lambda event: vpn_label.config(bg=taskbar_bg))
    update_time()
    global LANGUAGES

    def get_keyboard_layout():
        hwnd = win32gui.GetForegroundWindow()
        thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
        layout_id = win32api.GetKeyboardLayout(thread_id)
        lang_id = layout_id & 0xffff
        return LANGUAGES.get(lang_id, f'Unkn:{hex(lang_id)}')
    def update_layout_label():
        global last_layout
        layout = get_keyboard_layout()
        if layout != last_layout:
            layout_label.config(text=layout)
            last_layout = layout
        root.after(300, update_layout_label)

    global layout_label
    layout_label = Label(taskbar, text="", fg="white", bg=taskbar_bg, font=("Arial", 14))
    update_layout_label()
    layout_label.pack(side="right", padx=10)
    layout_label.bind("<Button-1>", lambda event: toggle_lang())
    layout_label.bind("<Enter>", lambda event: layout_label.config(bg=taskbar_fg))
    layout_label.bind("<Leave>", lambda event: layout_label.config(bg=taskbar_bg))

    image = Image.open("icons/interface/wndrs1.png")
    image = image.resize((32, 32), Image.Resampling.LANCZOS)
    icon = ImageTk.PhotoImage(image)
    p = Button(taskbar, text=lang["pusk"],image = icon,command=open_pusk)
    p.pack(side = LEFT,padx = 20,pady = 5)
    restore_taskbar_buttons(taskbar, program_functions, icons)
    load_taskbar_buttons()
    special_frames.append(shortcut_frame)
    set_rows(size_sh)
    row, col = 0, 0

    installed_programs_file = "syst_comp/programs.cfg"

    try:
        installed_programs = read_file(installed_programs_file,'r').splitlines()
        for prog in installed_programs: icons[prog] = f"icons/{prog.lower()}.png"
    except FileNotFoundError:  installed_programs = []

    load_cursor(start_time_)
    place_shortcuts(size_sh,MAX_ROWS,color)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    if os.path.exists("state/dat.cfg"):
        date_str = read_file("state/dat.cfg",'r').strip()

        try: date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError: date_obj = datetime.today().date()

        today = datetime.today().date()
        if date_obj <= today:
            with open("state/job.cfg", "r", encoding='utf-8') as f:
                for line in f:
                    key2, value1 = line.strip().split("=")
                    config[key2] = value1

            a = config.get("SALARY", "0")
            a = int(a)
            year = a * 12

            tax = (a / 100) * (13 if year < 5000000 else 15)
            net_salary = int(a - tax)
            global svb_coins
            svb_coins = load_balance(start_time_)
            svb_coins += net_salary
            transactions(f'+{net_salary} SVB Coins',start_time_)
            update_file("count_svbcoins.txt", int(net_salary))
            save_balance(svb_coins,start_time_)
            check_ach()

            next_month_date = datetime.today() + relativedelta(months=1)
            write_file('state/dat.cfg','w',next_month_date.strftime("%d.%m.%Y"))
            transactions(f"+{net_salary} SVB Coins {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",start_time_)
            messagebox.showinfo("", f"{lang['nach']} {net_salary} SVB Coins")

    import ctypes

    update_button_added = False

    if not showed: win_changelogs(root,selected_lang,lang)

    monitor_update_flag()
    log_system(f"START: {time.perf_counter() - t0} sec",start_time_)
    threading.Thread(target = run_updater)

    root.mainloop()
def downl():
    from country_list import countries_for_language
    import customtkinter as ctk
    def select_to_install():
        def valid_pre_install():
            programs.clear()
            for var, name in vars_list:
                if var.get(): programs.append(name)
            for name in programs: write_file("syst_comp/programs.cfg", "a", f'{name}\n')

            messagebox.showinfo("Success", "Programs added to pre-install")
        win = create_window(Win,"Pre-install",global_bg,1.0,750,300)

        programs = []
        vars_list = []

        mainFrame = ttk.Frame(win)
        mainFrame.pack()
        frame1 = ttk.Frame(mainFrame)
        frame1.pack(side = LEFT)
        frame2 = ttk.Frame(mainFrame)
        frame2.pack(side = LEFT)
        frame3 = ttk.Frame(mainFrame)
        frame3.pack(side = LEFT)
        frame4 = ttk.Frame(mainFrame)
        frame4.pack(side = LEFT)
        frame5 = ttk.Frame(mainFrame)
        frame5.pack(side = LEFT)

        ttk.Label(mainFrame,text = 'Select a program to pre-install').pack()

        for i,name in enumerate(all_programs_list):
            frm = frame1 if i < 10 else frame2 if i < 20 else frame3 if i < 30 else frame4 if i < 40 else frame5
            var = BooleanVar()
            check = ttk.Checkbutton(frm, text=name, variable=var)
            check.pack()
            vars_list.append((var, name))

        btnOk = ttk.Button(mainFrame,text = "Apply",command = valid_pre_install)
        btnOk.pack()

    def further(name, lastname, email, edition):
        import requests
        def create_act_file(email):
            try:
                token = os.getenv("TOKEN_FOR_USERS")
                g = Github(token)

                repo = g.get_user().get_repo("statistick")

                file_path = f"time_{email}.txt"
                content = "0"

                try:
                    file = repo.get_contents(file_path)
                    repo.update_file(
                        path=file_path,
                        message="Обновлен file",
                        content=content,
                        sha=file.sha,
                        branch="main"
                    )
                except:
                    repo.create_file(
                        path=file_path,
                        message="Добавлен file",
                        content=content,
                        branch="main"
                    )
            except Exception as e:
                messagebox.showerror("ERROR",str(e))
        def further1(vvod, edition):
            import psutil
            def load_language(lang_code=""):
                with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
                    langs = json.load(file)
                if lang_code not in langs:
                    return langs["RU"]
                return langs[lang_code]

            try:
                selected_lang = read_encrypted_file("syst_comp/lang.cfg")
            except Exception:
                selected_lang = "EN"
                log_to_file('File lang.cfg not exist or error decoding: Langue = EN',start_time_ = start_time_)

            total_memory = psutil.virtual_memory().total
            total_memory_gb = total_memory / (1024 ** 3)

            total_disk = psutil.disk_usage('/').total
            total_disk_gb = total_disk / (1024 ** 3)
            lang = load_language(selected_lang)
            a = ""
            if "x64" in edition: a = "x64"
            else:
                a = "x32"
            config_data = f"RAM={total_memory_gb}GB\nROM={total_disk_gb}GB\nEDITION={edition}\nARCH={a}"

            write_encrypted_file("syst_comp/parametrs.bin", config_data)
            if vvod == pas:
                for widget in content_frame.winfo_children():
                    widget.destroy()

                write_file("syst_comp/license.bin","w",pas)
                create_act_file(email)
                style = ttk.Style()
                style.configure("Custom.TFrame", background="#2C3E50", padding=10)
                contentt_frame = ttk.Frame(Win,style = 'Custom.TFrame')
                contentt_frame.pack(padx=10, pady=10, fill="both", expand=True,anchor="n")

                ttk.Label(contentt_frame, text=lang["launch"], font=("Arial", 16, "bold"),
                          background="#2C3E50", foreground="white").pack(pady=10)

                status_label = ttk.Label(contentt_frame, text=lang['init-conf'], font=("Arial", 12),
                                         background="#2C3E50", foreground="white")
                status_label.pack(pady=5)

                progress = ctk.CTkProgressBar(contentt_frame, width=300)
                progress.pack(pady=10)
                progress.set(0)

                percent_label = ttk.Label(contentt_frame, text="0%", font=("Arial", 12), background="#2C3E50",
                                          foreground="white")
                percent_label.pack(pady=5)

                def finish(): pass
                def animate_loading():
                    init_steps = [
                        (lang["init-conf"], init_database),
                        (lang["init-data"], load_config_files),
                        (lang["init-sys"], validate_log_size),
                        (lang["init-file"], set_device_states),
                        (lang["init_sec"], load_secure_configs),
                        (lang["init-cfg"], validate_cfg_files),
                        (lang["load_activity"],load_activity_control),
                        (lang["check_hashes"],lambda:check(start_time_)),
                        (lang["f_conf"],finish)
                    ]
                    step_count = len(init_steps)
                    for i, (text, func) in enumerate(init_steps):
                        progress.set(i + 1 / step_count)
                        percent_label.config(text=f"{int(progress.get())}%")
                        status_label.config(text="              " + text + "              ")
                        Win.update_idletasks()
                        try:
                            func()
                            log_system(f"<--{text}-->",start_time_)
                        except Exception as e:
                            log_system(f"Error in step {text}: {e}",start_time_)
                        time.sleep(0.3)
                        Win.update_idletasks()

                    Win.destroy()
                    main()

                Win.after(100, animate_loading)
            else:
                messagebox.showerror(lang["error"], lang["incorrect_input"])
                log_to_file(f"Messge: {lang['incorrect_input']}", level="error",start_time_ = start_time_)
        ll = var1.get()
        lang_code = {
            "RU": "Русский",
            "UA": "Українська",
            "FR": "Français",
            "EN": "English",
            "ALB": "Shqip",
            "SRB": "Српски",
            "PT": "Português",
            "IT": "Italiano",
            "ES": "Español",
            "PL": "Polski",
            "DE": "Deutsch",
            "BY": "Беларускі",
            "TUR":"Türkçe",
            "JP":"日本語",
            "CN": "中国人",
            "CS": "čeština",
            "HU": "Magyar",
            "BG": "Български",
            "RO":"Română"
        }

        reverse_lang_dict = {v: k for k, v in lang_code.items()}
        lang_code = reverse_lang_dict.get(ll)

        write_encrypted_file("syst_comp/lang.cfg", lang_code)
        log_system(f"Language.SET(={lang_code}=)",start_time_)
        copy_file_to_folder("syst_comp/lang.cfg", "backup_data",start_time_)
        log_system('Copy file lang.cfg',start_time_)
        log_system('Copy file lang.cfg',start_time_)

        global pas
        pas = "-".join("".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=4)) for _ in range(6))
        log_to_file('License key created',start_time_ = start_time_)
        try:
            run_in_thread(send_email(
               to =  str(email),
                subject = "🔐 Your Activation Code",
            html =  f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
              <h2 style="color: #333;">🚀 Activation Code</h2>
              <p style="font-size: 16px; color: #555;">
                Your license key has been generated successfully. Use the code below to activate your product:
              </p>
              <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; font-size: 24px; letter-spacing: 2px; font-weight: bold; color: #007BFF;">
                {pas}
              </div>
              <p style="font-size: 14px; color: #888; margin-top: 20px;">
                If you did not request this code, please ignore this email.
              </p>
            </div>
          </body>
        </html>
        """)

        )
        except Exception as ex:
            messagebox.showerror('Error', f"{errors[4]}\n\n{ex}")

        global GITHUB_TOKEN,GITHUB_GIST_ID,GITHUB_GIST_FILENAME
        try:
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }
            gist_url = f"https://api.github.com/gists/{GITHUB_GIST_ID}"

            response = requests.get(gist_url, headers=headers)
            response.raise_for_status()

            gist_json = response.json()
            files = gist_json.get("files", {})

            content = files.get(GITHUB_GIST_FILENAME, {}).get("content", "{}")
            try:
                users_data = json.loads(content)
                if not isinstance(users_data, dict):
                    users_data = {}
            except json.JSONDecodeError:
                users_data = {}

            uid = "".join("".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=4)) for _ in range(2))
            write_encrypted_file("uid.key",uid)

            users_data[email] = {
                "first_name": name,
                "last_name": lastname,
                "email": email,
                "edition": edition.get() if callable(getattr(edition, "get", None)) else edition,
                "license_key": pas,
                "UID":uid
            }

            update_data = {
                "files": {
                    GITHUB_GIST_FILENAME: {
                        "content": json.dumps(users_data, indent=4, ensure_ascii=False)
                    }
                }
            }

            update_resp = requests.patch(gist_url, headers=headers, json=update_data)
            update_resp.raise_for_status()
            update_file("count_users.txt",1)
            log_to_file("User data saved to server successfully.",start_time_ = start_time_)
            if update_resp.status_code not in (200, 201):
                log_to_file(f"Failed to update gist: status code {update_resp.status_code} - {update_resp.text}",start_time_ = start_time_)
                raise Exception(f"Failed to update gist: status code {update_resp.status_code} - {update_resp.text}")

        except Exception as ex:
            log_to_file(f"Failed to upload user data to server: {ex}",start_time_ = start_time_)
        def save_country_to_db(selected_country):
            conn = sqlite3.connect("configurations.db")
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country TEXT
                )
            """)
            cur.execute("INSERT INTO user_settings (country) VALUES (?)", (selected_country,))
            conn.commit()
            conn.close()
            log_to_file("Country saved",start_time_ = start_time_)
            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("configurations.db", "backup_data",start_time_)
        selected = country_box.get()
        if selected in countries_list:
            save_country_to_db(selected)
        if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data",start_time_)
            log_system("Copy file",start_time_)

        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )""")
        conn.commit()

        def save_user(first, last, email_val):
            cursor.execute("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)",
                           (first, last, email_val))
            conn.commit()
            log_to_file("File users.db created",start_time_ = start_time_)
        def update_user(user_id, new_first, new_last, new_email):
            cursor.execute("""
            UPDATE users
            SET first_name = ?, last_name = ?, email = ?
            WHERE id = ?
            """, (new_first, new_last, new_email, user_id))
            conn.commit()
        save_user(name, lastname, email)

        for widget in content_frame.winfo_children():
            widget.destroy()

        ttk.Label(content_frame, text="Enter the license key that came to your email", font=("Arial", 16, "bold"),
                  background="#2C3E50", foreground="white").pack(pady=10)
        ttk.Label(content_frame, text="The code will look like this \n XXXX-XXXX-XXXX-XXXX-XXXX-XXXX\n(If there is no code, check your 'Spam' folder.)", font=("Arial", 16, "bold"),
                  background="#2C3E50", foreground="white").pack(pady=10)
        en2 = ctk.CTkEntry(content_frame, font=("Arial", 14),placeholder_text='Enter the code')
        en2.pack(pady=5)
        ttk.Button(content_frame, text="Continue", style="Accent.TButton",
                   command=lambda: further1(en2.get(), edition)).pack(pady=10)
    def login_screen():
        import customtkinter as ctk
        import requests
        def try_login():
            import psutil
            email = email_entry.get()
            key = key_entry.get()
            try:
                headers = {
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github+json"
                }
                gist_url = f"https://api.github.com/gists/{GITHUB_GIST_ID}"

                response = requests.get(gist_url, headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch gist: {response.status_code}\n{response.text}")

                gist_json = response.json()
                files = gist_json.get("files", {})
                if not isinstance(files, dict) or GITHUB_GIST_FILENAME not in files:
                    raise Exception(f"File {GITHUB_GIST_FILENAME} not found in gist")

                users_content = files[GITHUB_GIST_FILENAME]["content"]
                users_data = json.loads(users_content)

                if email in users_data and users_data[email].get("license_key") == key:
                    login_pass = random.randint(100000,999999)
                    run_in_thread(send_email(
                        to=str(email),
                        subject="🔐 Your Activation Code",
                        html=f"""
                            <html>
                     <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                             <h2 style="color: #333;">🔑 Login Verification</h2>
                             <p style="font-size: 16px; color: #555;">
                             We received a request to sign in to your account. Enter the verification code below to complete your login:
                                 </p>
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; font-size: 24px; letter-spacing: 2px; font-weight: bold; color: #007BFF;">
                                 {login_pass}
                                </div>
                        <p style="font-size: 14px; color: #888; margin-top: 20px;">
                          This code will expire in 10 minutes. If you did not request this code, please ignore this email.
                         </p>
                         <p style="font-size: 14px; color: #888;">
                           🔒 Keep your account secure.
                              </p>
                         </div>
                         </body>
                        </html>
                        """)

                                 )
                    user_input = simpledialog.askinteger("Verification","Enter verification code from email")
                    if user_input == login_pass:
                        user_info = users_data[email]

                        write_file("syst_comp/license.bin","w",key)

                        edition_str = user_info.get("edition", "Standart x64")
                        a = "x64" if "x64" in edition_str else "x32"
                        total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
                        total_disk_gb = psutil.disk_usage('/').total / (1024 ** 3)
                        config_data = f"RAM={total_memory_gb}GB\nROM={total_disk_gb}GB\nEDITION={edition_str}\nARCH={a}"
                        write_encrypted_file("syst_comp/parametrs.bin", config_data)

                        lang_code = "EN"
                        try:
                            selected_lang = read_encrypted_file("syst_comp/lang.cfg")
                            lang_code = selected_lang if selected_lang else "EN"
                        except:
                            write_encrypted_file("syst_comp/lang.cfg", lang_code)

                        conn = sqlite3.connect("configurations.db")
                        cursor = conn.cursor()
                        cursor.execute("""
                                                CREATE TABLE IF NOT EXISTS users (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    first_name TEXT,
                                                    last_name TEXT,
                                                    email TEXT
                                                )""")
                        conn.commit()

                        cursor.execute("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)",
                                       (user_info.get("first_name"), user_info.get("last_name"), email))
                        conn.commit()
                        conn.close()

                        copy_file_to_folder("configurations.db", "backup_data",start_time_)
                        copy_file_to_folder("syst_comp/lang.cfg", "backup_data",start_time_)

                        log_to_file("Login successful. Data saved.", start_time_=start_time_)
                        messagebox.showinfo("Success", "Login successful")
                        Win.destroy()
                        main()
                    else:
                        messagebox.showerror("Error","Invalid code!")
                else:
                    messagebox.showerror("Error", "Invalid login")
            except Exception as e:
                messagebox.showerror("Error", f"Login failed:\n{e}")
                log_to_file(f"Error with logging: {e}",start_time_ = start_time_)
        for widget in content_frame.winfo_children():
            widget.destroy()

        ttk.Label(content_frame, text="Login with your license", background="#2C3E50", foreground="white").pack()
        ttk.Label(content_frame, text="Enter your email", background="#2C3E50", foreground="white").pack()
        email_entry = ctk.CTkEntry(content_frame, font=("Arial", 12),placeholder_text="Email",fg_color = fg_widget,placeholder_text_color="white")
        email_entry.pack(pady=5)
        ttk.Label(content_frame, text="Enter your license key", background="#2C3E50", foreground="white").pack()
        key_entry = ctk.CTkEntry(content_frame, font=("Arial", 12),placeholder_text='License',fg_color = fg_widget,placeholder_text_color="white")
        key_entry.pack(pady=5)
        ctk.CTkButton(master=content_frame, text="Login", width=200, height=40, corner_radius=15,command=try_login).pack()
    log_to_file("----DOWNLOADER LAUNCH----",start_time_ = start_time_)

    fg_widget = "#2980B9"

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    Win = ctk.CTk()
    Win.geometry("900x700")
    Win.title("Windoors 52 Installer")
    Win.resizable(False, False)

    img = Image.open("icons/installer.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    bg_img = Image.open("icons/blured.png").resize((1200, 1000))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = ctk.CTkLabel(master=Win, image=bg_photo, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    content_frame = ctk.CTkFrame(master=Win, corner_radius=15, fg_color="#2C3E50",bg_color = "#2C3E50", width=600, height=650)
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(master=content_frame, text="Welcome to the Windoors 52 Installer",
                               font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 30))

    en = ctk.CTkEntry(content_frame, placeholder_text="Name", width=400, height=35, corner_radius=10,fg_color=fg_widget)
    en.pack(pady=10)

    en1 = ctk.CTkEntry(content_frame, placeholder_text="Last name", width=400, height=35, corner_radius=10,fg_color=fg_widget)
    en1.pack(pady=10)
    email1 = ctk.CTkEntry(content_frame, placeholder_text="Email", width=400, height=35, corner_radius=10,fg_color=fg_widget)
    email1.pack(pady=10)

    languages = ["Български", "Беларускі", "Deutsch", "English", "Español", "Français", "Italiano",
                 "Magyar", "Polski", "Português", "Română", "Русский", "Shqip", "Српски", "Türkçe",
                 "Українська", "čeština", "中国人", "日本語"]
    var1 = StringVar(value="English")
    language_box = ctk.CTkComboBox(master=content_frame, values=languages, width=400, height=35, fg_color=fg_widget)
    language_box.set(var1.get())
    language_box.pack(pady=10)

    editions = ["Standart x64", "Professional x64", "Gaming x64","Standart x32", "Professional x32", "Gaming x32"]
    var2 = StringVar(value="Standart x64")
    edition_box = ctk.CTkComboBox(master=content_frame, values=editions, width=400, height=35, fg_color=fg_widget)
    edition_box.set(var2.get())
    edition_box.pack(pady=10)

    countries = dict(countries_for_language('en'))
    countries_list = sorted(list(countries.values()))
    country_box = ctk.CTkComboBox(master=content_frame, values=countries_list, width=400, height=35, fg_color=fg_widget)
    country_box.set("Russia")
    country_box.pack(pady=10)

    preinstall_btn = ctk.CTkButton(master=content_frame, text="Add pre-install soft", width=200, height=40, corner_radius=15,
                                 command=select_to_install)
    preinstall_btn.pack(pady=10)
    continue_btn = ctk.CTkButton(master=content_frame, text="Continue",width=200, height=40, corner_radius=15,
                                 command=lambda: further(en.get(), en1.get(), email1.get(), edition_box.get()))
    continue_btn.pack(pady=(30, 10))

    login_btn = ctk.CTkButton(master=content_frame, text="Already have a license?",width=200, height=35, corner_radius=15,
                              fg_color="#1ABC9C", hover_color="#16A085",command=login_screen)
    login_btn.pack(pady=(0, 20))

    footer_label = ctk.CTkLabel(master=content_frame, text="Developed by SVB.",font=ctk.CTkFont(size=14, weight="bold"))
    footer_label.pack(side="bottom", pady=10)

    Win.mainloop()
def enter_password():
    import customtkinter as ctk
    global invisible_pass,totalAttemps,currentAttemp

    def start_ban(Win):
        global ban_time,ban_timer

        def update():
            global ban_time, ban_timer,currentAttemp,totalAttemps
            if ban_time.total_seconds() > 0:
                ban_time -= timedelta(seconds=1)
                lbl_ban.config(text=f'{ban_time}')
                Win.after(1000, update)
            else:
                ban_timer = False
                currentAttemp = 0
                lbl_attemps.config(text = f"Attemps: {currentAttemp}/{totalAttemps}")
                lbl_ban.config(text="Time's up!")

        ban_timer = True
        ban_time = timedelta(minutes=10)

        lbl_ban = ttk.Label(Win, text=f'{ban_time}',font = ("Arial",20,"bold"),foreground="red",background = "#018feb")
        lbl_ban.pack()

        canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2, window=lbl_ban)

        update()

    def reset_password():
        def set_new_p(new_p):
            conn = sqlite3.connect("password.db")
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM password")
            rows = cursor.fetchall()

            cursor.execute(
                        "UPDATE password SET password = ?",
                        (new_p,)
            )
            conn.commit()
            conn.close()
        def check_code2(pas,code):
            if pas != code:
                messagebox.showerror(lang["error"],lang["invalid_code"])
                return
            else:
                r.destroy()
                Win.destroy()
                main()
        def check_code(user_code):
            if user_code != code:
                messagebox.showerror(lang["error"],lang["invalid_code"])
                return
            else:
                lbl.destroy()
                r_p.destroy()
                btn_ok.destroy()

                password = "".join("".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=3)) for _ in range(2))
                set_new_p(password)

                run_in_thread(send_email(
                    to=str(email),
                    subject=lang['your_new_password'],
                    html=f"""
                        <html>
                          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                            <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                                        box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                              <h2 style="color: #333;">{lang['password_has_been_reset']}</h2>
                              <p style="font-size: 16px; color: #555;">
                                {lang['password_reset_mes']}:
                              </p>
                              <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; 
                                          text-align: center; font-size: 20px; letter-spacing: 1px; 
                                          font-weight: bold; color: #2e7d32;">
                                {password}
                              </div>
                              <p style="font-size: 14px; color: #888; margin-top: 20px;">
                                {lang["reset_sovet"]}
                              </p>
                            </div>
                          </body>
                        </html>
                        """
                ))

                labl = Label(r, text=lang["ent_ps"])
                labl.pack()

                re_p = ctk.CTkEntry(r, placeholder_text=lang["ent_ps"], width=80)
                re_p.pack()

                btnok = ttk.Button(r, text=lang['dalee'], command=lambda: check_code2(re_p.get(),password))
                btnok.pack()
        r = Toplevel(Win)
        r.attributes("-alpha", float(GlobalAlpha))
        r.geometry("400x400")
        r.title(lang["reset_p2"])
        r.resizable(False,False)
        img = Image.open("icons/interface/reset.png")
        icon_image = ImageTk.PhotoImage(img)
        r.iconphoto(False, icon_image)

        lbl = Label(r,text = lang["enter_code_podt"])
        lbl.pack()

        n, ln, email = return_user_info()
        code = "-".join("".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=3)) for _ in range(5))

        run_in_thread(send_email(
            to=str(email),
            subject=lang['reset_code'],
            html=f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                                box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                      <h2 style="color: #333;">{lang['mes_for_reset']}</h2>
                      <p style="font-size: 16px; color: #555;">
                        {lang['next_mes_reset']}:
                      </p>
                      <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; 
                                  text-align: center; font-size: 24px; letter-spacing: 2px; 
                                  font-weight: bold; color: #007BFF;">
                        {code}
                      </div>
                      <p style="font-size: 14px; color: #888; margin-top: 20px;">
                        {lang["ignore_if_none"]}
                      </p>
                    </div>
                  </body>
                </html>
                """
        ))

        r_p = ctk.CTkEntry(r,placeholder_text=lang["enter_code_podt"],width=80)
        r_p.pack()

        btn_ok = ttk.Button(r,text = lang['dalee'],command = lambda:check_code(r_p.get()))
        btn_ok.pack()
    def load_language(lang_code=""):
        try:
            with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
                langs = json.load(file)
            if lang_code not in langs:
                log_to_file(f"Error: language {lang_code} not found, use RU", start_time_=start_time_)
                return langs["RU"]
        except Exception as e:
            messagebox.showerror(f"Error {errors[0]}", f"Error with lang.json!{e}")
            log_to_file(f"Error with lang.json!{e}", level="error", start_time_=start_time_)
        return langs[lang_code]
    def ok():
        global totalAttemps, currentAttemp,ban_timer
        if ban_timer: messagebox.showerror('Error',"You have a ban for 10 min! ")
        elif currentAttemp < totalAttemps:
            log_to_file('connected to password.db', start_time_=start_time_)
            conn = sqlite3.connect("password.db")
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT password FROM password
                    ''')
            stored_password = cursor.fetchone()
            conn.close()

            if stored_password and stored_password[0] == en.get():
                log_to_file("Password correct", start_time_=start_time_)
                Win.destroy()
                main()
            else:
                currentAttemp += 1
                lbl_attemps.config(text = f'Attemps: {currentAttemp}/{totalAttemps}')
                messagebox.showerror("Error", "Incorrect password")
                log_to_file("Password incorrect", level="error", start_time_=start_time_)
        else:
            messagebox.showerror("Error","3 incorrect attempt! Ban for 10 min")
            start_ban(Win)
    try: selected_lang = read_encrypted_file("syst_comp/lang.cfg").strip()
    except Exception:
        messagebox.showerror(f'Error {errors[0]}',
                             "No file lang.cfg in directory! We created this file, or you can copy this file from folder 'backup_data'")
        log_to_file("No file lang.cfg in directory", level="error", start_time_=start_time_)
        selected_lang = "EN"
        write_encrypted_file("syst_comp/lang.cfg", selected_lang)
    lang = load_language(selected_lang)

    log_to_file("Enter password function is running", start_time_=start_time_)
    Win = Tk()
    Win.configure(bg="#2C3E50")
    Win.geometry("500x400")
    Win.attributes('-fullscreen', True)
    Win.title("Windoors 52")
    Win.resizable(False, False)

    if read_encrypted_file("syst_comp/img_wlp_passwordWin.cfg") == "True":
        pth = str(read_encrypted_file("syst_comp/path_wlp_passwordWin.cfg"))
        image = Image.open(pth)
        image = image.resize((Win.winfo_screenwidth(), Win.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)
    else:
        image = Image.open(r"icons\wallpepers\wallpeper12.jpg")
        image = image.resize((Win.winfo_screenwidth(), Win.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)

    Win.photo = photo

    canvas_icon = Canvas(Win,width=Win.winfo_screenwidth(),height=Win.winfo_screenheight(),highlightthickness=0, bd=0)
    canvas_icon.pack(fill="both", expand=True)
    canvas_icon.create_image(0, 0, anchor="nw", image=photo)

    img = Image.open('icons/accicon.png')
    img = img.resize((96, 96), Image.Resampling.LANCZOS)
    icon = ImageTk.PhotoImage(img)

    lbl_icon = Label(Win, image=icon,background = "#0e1531")
    lbl_icon.image = icon
    lbl_icon.pack()

    lbl_attemps = Label(Win, text = f"Attemps: {currentAttemp}/{totalAttemps}",background = "#018feb")
    lbl_attemps.pack()

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 10, "bold"), padding=8, background="#1E90FF")

    lbl = Label(Win, text=lang["ent_ps"], background='#0f1632', fg="white", font=("Arial", 25, "bold"))
    lbl.pack()

    en = ttk.Entry(Win)
    if invisible_pass: en.config(show = "*")
    en.pack(expand=True, fill=BOTH, padx=10, ipadx=50)

    btn = ttk.Button(Win, text="Ok", command=ok, style="Accent.TButton")
    btn.pack()

    reset_p = Label(Win,text = lang['reset_p'],background="#018feb")
    reset_p.pack()
    reset_p.bind("<Button-1>",lambda event:reset_password())

    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 100, window=lbl_attemps)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 200, window=reset_p)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 250, window=btn)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 300, window=en)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 400, window=lbl)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2, Win.winfo_screenheight() // 2 - 480, window=lbl_icon)


    Win.mainloop()
def anim(arg="s"):
    def load_language(lang_code=""):
        try:
            with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
                langs = json.load(file)
            if lang_code not in langs:
                log_to_file(f"Error: language {lang_code} not found, use RU",start_time_ = start_time_)
                return langs["RU"]
        except Exception as e:
            messagebox.showerror(f"Error {errors[0]}", f"Error with lang.json! {e}")
            log_to_file(f"Error with lang.json!: {e}",level="error",start_time_ = start_time_)
        return langs[lang_code]

    import customtkinter as ctk
    log_system("----OS LAUNCH----",start_time_)
    log_system(f'VERSION OS --> {VERSION}',start_time_)
    try:
        key = load_key()
    except FileNotFoundError:
        generate_key()
        key = load_key()

    try:
        selected_lang = read_encrypted_file("syst_comp/lang.cfg").strip()
    except Exception:
        messagebox.showerror(f'Error {errors[0]}',
                             "No file lang.cfg in directory! We created this file, or you can copy this file from folder 'backup_data'")
        log_to_file("No file lang.cfg in directory",level="error",start_time_ = start_time_)
        selected_lang = "EN"
        encrypted_lang = encrypt_message(selected_lang, key)
        write_file("syst_comp/lang.cfg",'wb',encrypted_lang)
    lang = load_language(selected_lang)
    def animate_loading(arg):
        def welc(arg):
            def animate_w(arg):
                for i in range(0, 101, 2):
                    time.sleep(0.005)
                    progress.set(i / 100)
                    percent_label.config(text=f"{i}%")
                    Win.update_idletasks()
                Win.destroy()
                if arg == "p":
                    enter_password()
                else:
                    main()
            for widget in Win.winfo_children():
                widget.destroy()

            n, ln, e = return_user_info()

            img = Image.open('icons/accicon.png')
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(img)

            style = ttk.Style()
            style.configure("TFrame", background="#4682B4", padding=10)
            content_frame = ttk.Frame(Win, style="TFrame")
            content_frame.pack(fill="both", expand=True)
            icon_label = Label(content_frame, image=icon, bg="#4682B4")
            icon_label.image = icon
            icon_label.pack()
            ttk.Label(content_frame, text=lang["welc"] + str(n), font=("Arial", 35, "bold"),
                      background="#4682B4", foreground="white").pack(pady=10)
            progress = ctk.CTkProgressBar(content_frame, width=300)
            progress.pack(pady=10)
            progress.set(0)
            percent_label = ttk.Label(content_frame, text="0%", font=("Arial", 30), background="#4682B4",
                                      foreground="white")
            percent_label.pack(pady=5)
            Win.after(40, lambda:animate_w(arg))
        def finish():
            pass
        init_steps = [
            (lang["init-conf"], init_database),
            (lang["init-data"], load_config_files),
            (lang["init-sys"], validate_log_size),
            (lang["init-file"], set_device_states),
            (lang["init_sec"], load_secure_configs),
            (lang["init-cfg"], validate_cfg_files),
            (lang["load_activity"], load_activity_control),
            (lang["check_hashes"], lambda:check(start_time_)),
            (lang["f_conf"], finish)
        ]
        step_count = len(init_steps)
        for i, (text, func) in enumerate(init_steps):
            progress.set((i + 1) / step_count)
            percent_label.config(text=f"{int(progress.get()*100)}%")
            status_label.config(text="              " + text + "              ")
            Win.update_idletasks()
            try:
                func()
                log_system(f"<--{text}-->",start_time_)
            except Exception as e:
                log_system(f"Error in step {text}: {e}",start_time_)
            time.sleep(0.3)

            Win.update_idletasks()

        welc(arg)
    run_in_thread(("sound//brr.mp3",None,state_sound,start_time_))
    Win = Tk()
    Win.config(bg = "#2C3E50")
    Win.title(lang["launch"])
    Win.geometry("400x250")
    Win.attributes('-fullscreen', True)
    Win.configure(background="#2C3E50")
    Win.focus_set()

    log_system('----START LOADING----',start_time_)
    style = ttk.Style()
    style.configure("TFrame", background="#2C3E50", padding=10)
    content_frame = ttk.Frame(Win, style="TFrame")
    content_frame.pack(fill="both", expand=True)
    ttk.Label(content_frame, text=lang["launch"], font=("Arial", 35, "bold"),
              background="#2C3E50", foreground="white").pack(pady=10)
    status_label = ttk.Label(content_frame, text=lang['init-conf'], font=("Arial", 30),
                             background="#2C3E50", foreground="white")
    status_label.pack(pady=5)
    progress = ctk.CTkProgressBar(content_frame, width=300)
    progress.pack(pady=10)
    progress.set(0)
    percent_label = ttk.Label(content_frame, text="0%", font=("Arial", 30), background="#2C3E50",
                              foreground="white")
    percent_label.pack(pady=5)
    Label(content_frame,text="Developped by SVB", font=("Arial", 20), background="#2C3E50",
          foreground="white").pack(side = "bottom",anchor = "w")

    Win.after(100, lambda:animate_loading(arg))

    Win.mainloop()

if check_did(start_time_):
    if os.path.exists("syst_comp/license.bin"):
        if is_blocked(): os.startfile("LimitWin.exe")
        else:
            if os.path.exists("password.db"): anim("p")
            else: anim()
    else:  downl()