from tkinter import *
from tkinter import filedialog,ttk
from PIL import Image, ImageTk
import cv2


cap = None
paused = False
current_frame = 0
fps = 0
total_frames = 0
def video_player(root,lang,actives_programs,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("Video player")
    global cap,paused,current_frame,fps,total_frames
    def select_video():
        global cap, fps, total_frames, paused, current_frame
        path = filedialog.askopenfilename(parent = Win,
            title=lang["select_video"],
            filetypes=[(lang['video_files'], "*.mp4 *.avi *.mkv *.mov"), (lang['all_files'], "*.*")]
        )
        if not path:
            return
        if cap:
            cap.release()
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0
        paused = False
        play_pause_btn.config(text="⏸️")
        show_frame()

    def play_pause():
        global paused
        paused = not paused
        play_pause_btn.config(text="▶️" if paused else "⏸️")

    def show_frame():
        global current_frame
        if cap and not paused:
            ret, frame = cap.read()
            if ret:
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(img)
                video_label.imgtk = imgtk
                video_label.config(image=imgtk)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                current_frame = 0
        Win.after(30, show_frame)

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title(lang["video_player"])
    Win.configure(bg=global_bg)
    Win.geometry("800x500")
    video_label = Label(Win)
    video_label.pack()

    controls = Frame(Win)
    controls.pack()

    select_btn = ttk.Button(controls, text=lang["select_video__"], command=select_video)
    select_btn.pack(side=LEFT, padx=5)

    play_pause_btn = ttk.Button(controls, text="⏸️", command=play_pause)
    play_pause_btn.pack(side=LEFT, padx=5)

    if cap:
        cap.release()
