import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import re
import requests
from PIL import Image, ImageTk
import cv2
import shutil
import json
import sqlite3
import customtkinter as ctk
from crypto_work import load_key, decrypt_message, encrypt_message
import dropbox
from load_env import load_env

load_env()

cap = None
fps = 0
total_frames = 0
duration = 0
current_frame = 0
paused = False
current_video_index = 0
likes_dict = {}
dislikes_dict = {}
comments_dict = {}
DATA_FILE = "svbtube/video_data.json"
current_img = None
acc = False

DROPBOX_TOKEN = os.getenv("DROPBOX_SVBTUBE")
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

video_files = []

base_videos = [
    "https://www.dropbox.com/scl/fi/6zskcqhkx76qezw27rehk/video1.mp4?rlkey=05mkaszpafu0c6tdiw0e3x2rd&st=pbxmgvg9&raw=1",
    "https://www.dropbox.com/scl/fi/311f51titkqi369i101ap/video2.mp4?rlkey=nmgtoygh0abvyuosxw76rkzga&st=in68nhal&raw=1",
    "https://www.dropbox.com/scl/fi/vgl53bcf5nputnbxxugoo/video3.mp4?rlkey=otneu7lbtw1xtzbwvdzueejla&st=kqviiw2b&raw=1",
    "https://www.dropbox.com/scl/fi/srw45yq9d8lvipj3qnon6/video4.mp4?rlkey=59rtidj101c4wz6hl6znkqbes&st=8l6lxqb6&raw=1",
    "https://www.dropbox.com/scl/fi/we4gtkyu11zl8pqaxlmy0/video5.mp4?rlkey=2xsof9z5190l1v5u6pcw9mszy&st=pbyjuzhv&raw=1",
    "https://www.dropbox.com/scl/fi/kfecyws2psnhakekf8abk/video6.mp4?rlkey=khlg28kiqcn3hbkcuwpab7hsk&st=rsxnl9vd&raw=1"
]

def download_video(url, local_path="svbtube/temp_video.mp4"):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_path
    except Exception as e:
        print("Ошибка при скачивании видео:", e)
        return None

def upload_to_dropbox(local_path, dropbox_path):
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
    return link.url.replace("?dl=0", "?raw=1")

def svbtube(root, lang, actives_programs, global_bg, global_fg,GlobalAlpha):
    actives_programs.append("SVBTube")
    global acc, video_files, cap, fps, total_frames, duration, current_frame, paused, current_video_index, likes_dict, dislikes_dict, comments_dict, current_img

    if os.path.exists("svbtube/account.db"): acc = True

    def load_video_data():
        global likes_dict, dislikes_dict, comments_dict
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                likes_dict = data.get("likes", {})
                dislikes_dict = data.get("dislikes", {})
                comments_dict = data.get("comments", {})
        else:
            likes_dict = {}
            dislikes_dict = {}
            comments_dict = {}

    def save_video_data():
        data = {
            "likes": likes_dict,
            "dislikes": dislikes_dict,
            "comments": comments_dict
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02}:{s:02}"

    def update_time_label():
        time = format_time(current_frame / fps)
        total = format_time(duration)
        time_label.config(text=f"{time} / {total}")

    def draw_progress():
        progress.delete("all")
        w = progress.winfo_width()
        ratio = current_frame / total_frames if total_frames else 0
        progress.create_rectangle(0, 0, w * ratio, 20, fill='green')

    def load_video(path):
        global cap, fps, total_frames, duration, current_frame, paused
        path = normalize_dropbox_url(path) if path.startswith("http") else path
        local_file = download_video(path) if path.startswith("http") else path
        if not local_file:
            messagebox.showerror("Error", f"Не удалось открыть видео: {path}")
            return
        if cap:
            cap.release()
        cap = cv2.VideoCapture(local_file)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps else 0
        current_frame = 0
        paused = False

    def show_frame():
        global current_frame
        if not paused:
            ret, frame = cap.read()
            if ret:
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                video_label.imgtk = imgtk
                video_label.config(image=imgtk)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                current_frame = 0
        update_time_label()
        draw_progress()
        Win.after(30, show_frame)

    def play_pause():
        global paused, current_img
        paused = not paused
        current_img = img_pause if paused else img_pause1
        pause_btn.config(image=current_img)

    def seek(event):
        global current_frame
        x = event.x
        width = progress.winfo_width()
        ratio = x / width
        frame = int(total_frames * ratio)
        current_frame = frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def switch_video(delta):
        global current_video_index
        current_video_index = (current_video_index + delta) % len(video_files)
        load_video(video_files[current_video_index])
        update_ui_for_video(video_files[current_video_index])

    def update_ui_for_video(video_path):
        like_label.config(text=f"👍 {likes_dict.get(video_path, 0)}")
        dislike_label.config(text=f"👎 {dislikes_dict.get(video_path, 0)}")
        comment_listbox.delete(0, END)
        for c in comments_dict.get(video_path, []):
            comment_listbox.insert(END, c)

    def add_like(is_like):
        video_path = video_files[current_video_index]
        if is_like:
            likes_dict[video_path] = likes_dict.get(video_path, 0) + 1
        else:
            dislikes_dict[video_path] = dislikes_dict.get(video_path, 0) + 1
        update_ui_for_video(video_path)
        save_video_data()

    def add_comment(text):
        video_path = video_files[current_video_index]
        if text.strip():
            comments_dict.setdefault(video_path, []).append(text.strip())
            comment_listbox.insert(END, text.strip())
            comment_entry.delete(0, END)
            save_video_data()

    def normalize_dropbox_url(url):
        url = url.strip().replace(" ", "")
        if "dropbox.com" not in url:
            return url
        url = re.sub(r'(\?|&)raw=1(&|$)', '', url)
        return url + "?raw=1" if "?" not in url else url + "&raw=1"

    def get_direct_dropbox_url(url):
        if "dropbox.com" not in url:
            return url
        if "?raw=1" in url:
            return url
        if "?dl=0" in url:
            return url.replace("?dl=0", "?raw=1")
        if "?" in url:
            return url + "&raw=1"
        return url + "?raw=1"

    def load_videos_encrypted(filepath="svbtube/videos.cfg"):
        key = load_key()
        with open(filepath, "rb") as f:
            decrypted = decrypt_message(f.read(), key)
        return [line.strip() for line in decrypted.splitlines() if line.strip()]

    try:
        video_files = [get_direct_dropbox_url(u) for u in load_videos_encrypted()]
    except:
        video_files = [get_direct_dropbox_url(u) for u in base_videos]

    load_video_data()


    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.configure(bg=global_bg)
    Win.title("SVBTube")
    Win.geometry("1000x700")
    img = Image.open("icons/svbtube.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    like_img = ImageTk.PhotoImage(Image.open("icons/interface/like.png").resize((24, 24)))
    dislike_img = ImageTk.PhotoImage(Image.open("icons/interface/dislike.png").resize((24, 24)))
    upload_img = ImageTk.PhotoImage(Image.open("icons/interface/upload.png").resize((24, 24)))
    img_pred = ImageTk.PhotoImage(Image.open("icons/interface/pred.png").resize((35, 35)))
    img_sled = ImageTk.PhotoImage(Image.open("icons/interface/sled.png").resize((35, 35)))
    img_pause = ImageTk.PhotoImage(Image.open("icons/interface/pause1.png").resize((35, 35)))
    img_pause1 = ImageTk.PhotoImage(Image.open("icons/interface/pause2.png").resize((35, 35)))
    account_img = ImageTk.PhotoImage(Image.open("icons/interface/yt_account.png").resize((35, 35)))
    current_img = img_pause

    main_frame = Frame(Win)
    main_frame.grid(row=0, column=0, sticky="nsew")
    Win.grid_rowconfigure(0, weight=1)
    Win.grid_columnconfigure(0, weight=1)

    left_panel = Frame(main_frame)
    left_panel.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
    right_panel = Frame(main_frame)
    right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    right_panel1 = Frame(main_frame)
    right_panel1.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    video_label = Label(right_panel)
    video_label.grid(row=0, column=0, columnspan=3, sticky="ew")
    time_label = Label(right_panel, text="00:00 / 00:00", fg=global_fg, bg=global_bg)
    time_label.grid(row=1, column=0, columnspan=3)
    progress = Canvas(right_panel, height=20, bg='gray')
    progress.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)
    controls = Frame(right_panel)
    controls.grid(row=3, column=0, columnspan=3, pady=10)

    pause_btn = Button(controls, image=img_pause1, command=play_pause)
    pause_btn.image = img_pause1
    pause_btn.pack(side=LEFT, padx=5)
    prev_btn = Button(controls, image=img_pred, command=lambda: switch_video(-1))
    prev_btn.image = img_pred
    prev_btn.pack(side=LEFT, padx=5)
    next_btn = Button(controls, image=img_sled, command=lambda: switch_video(1))
    next_btn.image = img_sled
    next_btn.pack(side=LEFT, padx=5)
    progress.bind("<Button-1>", seek)

    like_dislike_frame = Frame(left_panel)
    like_dislike_frame.grid(row=0, column=0, pady=10)
    like_label = Label(like_dislike_frame, text="👍 0", fg=global_fg, bg=global_bg)
    like_label.grid(row=0, column=0, pady=5)
    like_btn = Button(like_dislike_frame, image=like_img, command=lambda: add_like(True), bd=0)
    like_btn.grid(row=1, column=0, pady=5)
    dislike_label = Label(like_dislike_frame, text="👎 0", fg=global_fg, bg=global_bg)
    dislike_label.grid(row=0, column=1, pady=5)
    dislike_btn = Button(like_dislike_frame, image=dislike_img, command=lambda: add_like(False), bd=0)

    dislike_btn.grid(row=1, column=1, pady=5)

    comment_frame = Frame(left_panel)
    comment_frame.grid(row=1, column=0, pady=20)
    comment_listbox = Listbox(comment_frame, width=30, height=10)
    comment_listbox.grid(row=0, column=0, columnspan=2, pady=5)
    comment_entry = ctk.CTkEntry(comment_frame, width=170, placeholder_text=lang['enter_comm'])
    comment_entry.grid(row=1, column=0, sticky="w", pady=5)
    add_comment_btn = Button(comment_frame, text="💬", command=lambda: add_comment(comment_entry.get()))
    add_comment_btn.grid(row=1, column=1, sticky="e", padx=5)

    load_video(video_files[current_video_index])
    update_ui_for_video(video_files[current_video_index])
    show_frame()
