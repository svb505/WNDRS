import pytz
import PIL.Image as PilImage
import PIL.ImageTk as PilImageTk
from tkinter import *
from tkinter import ttk
from datetime import datetime,timedelta

stopwatch_running = False
stopwatch_time = timedelta()
timer_running = False
timer_time = 0
clock = ""

def open_clocks(root,lang,clock_type, gl_police, global_bg, global_fg, clock_win):
    def update_clock():
        if clock_type == "hhmm":
            current_time = datetime.now().strftime("%H:%M")
        else:
            current_time = datetime.now().strftime("%H:%M:%S")
        clock_lbl.config(text=current_time)
        clock_win.after(1000, update_clock)
    def start_stopwatch():
        global stopwatch_running
        if not stopwatch_running:
            stopwatch_running = True
            run_stopwatch()
    def stop_stopwatch():
        global stopwatch_running
        stopwatch_running = False
    def reset_stopwatch():
        global stopwatch_time
        stopwatch_time = timedelta()
        stopwatch_lbl.config(text="00:00:00")
    def run_stopwatch():
        global stopwatch_time
        if stopwatch_running:
            stopwatch_time += timedelta(seconds=1)
            stopwatch_lbl.config(text=str(stopwatch_time))
            clock_win.after(1000, run_stopwatch)
    def start_timer():
        global timer_running, timer_time
        try:
            minutes = int(timer_entry.get())
            timer_time = timedelta(minutes=minutes)
            timer_running = True
            run_timer()
        except:
            timer_lbl.config(text="Invalid input")
    def stop_timer():
        global timer_running
        timer_running = False
    def reset_timer():
        global timer_time
        timer_time = timedelta()
        timer_lbl.config(text="00:00:00")
    def run_timer():
        global timer_time, timer_running
        if timer_running and timer_time.total_seconds() > 0:
            timer_time -= timedelta(seconds=1)
            timer_lbl.config(text=str(timer_time))
            clock_win.after(1000, run_timer)
        elif timer_running:
            timer_lbl.config(text="Time's up!")
            timer_running = False

    global clock
    clock_win = Toplevel(root)
    clock_win.title(lang["clocks"])
    clock_win.geometry("400x350")
    clock_win.configure(bg=global_bg)

    img = PilImage.open("icons/interface/clock.png")
    icon_image = PilImageTk.PhotoImage(img)
    clock_win.iconphoto(False, icon_image)

    notebook = ttk.Notebook(clock_win)
    notebook.pack(fill=BOTH, expand=True)

    tab_clock = Frame(notebook, bg=global_bg)
    clock_lbl = Label(tab_clock, font=(clock, 35, "bold"), fg=global_fg, bg=global_bg)
    clock_lbl.pack(pady=20)
    date__ = datetime.now().strftime("%Y-%m-%d")
    Label(tab_clock, text=date__, font=(gl_police, 16, "bold"), fg=global_fg, bg=global_bg).pack()
    offset = datetime.now().astimezone(pytz.timezone('Etc/GMT-1')).strftime("%z")
    gmt_offset = f"GMT{offset[:3]}"
    Label(tab_clock, text=gmt_offset, font=(gl_police, 16, "bold"), fg=global_fg, bg=global_bg).pack()

    update_clock()

    start_img = PilImageTk.PhotoImage(
        PilImage.open(f"icons/interface/start.png").resize((25, 25), PilImage.Resampling.LANCZOS))
    stop_img = PilImageTk.PhotoImage(
        PilImage.open(f"icons/interface/stop.png").resize((25, 25), PilImage.Resampling.LANCZOS))
    reset_img = PilImageTk.PhotoImage(
        PilImage.open(f"icons/interface/reset.png").resize((25, 25), PilImage.Resampling.LANCZOS))

    tab_stopwatch = Frame(notebook, bg=global_bg)
    stopwatch_lbl = Label(tab_stopwatch, text="00:00:00", font=(clock, 30, "bold"), fg=global_fg, bg=global_bg)
    stopwatch_lbl.pack(pady=20)
    btn = Button(tab_stopwatch, image=start_img, command=start_stopwatch)
    btn.image = start_img
    btn.pack(side=LEFT, padx=10)
    btn = Button(tab_stopwatch, image=stop_img, command=stop_stopwatch)
    btn.image = stop_img
    btn.pack(side=LEFT, padx=10)
    btn = Button(tab_stopwatch, image=reset_img, command=reset_stopwatch)
    btn.image = reset_img
    btn.pack(side=LEFT, padx=10)

    tab_timer = Frame(notebook, bg=global_bg)
    timer_lbl = Label(tab_timer, text="00:00:00", font=(clock, 30, "bold"), fg=global_fg, bg=global_bg)
    timer_lbl.pack(pady=20)
    timer_entry = Entry(tab_timer, width=5)
    timer_entry.pack()
    Label(tab_timer, text=lang["enter_minutes"], bg=global_bg, fg=global_fg).pack()
    timer_time = timedelta()
    timer_running = False
    btn = Button(tab_timer, image=start_img, command=start_timer)
    btn.image = start_img
    btn.pack(side=LEFT, padx=10)
    btn = Button(tab_timer, image=stop_img, command=stop_timer)
    btn.image = stop_img
    btn.pack(side=LEFT, padx=10)
    btn = Button(tab_timer, image=reset_img, command=reset_timer)
    btn.image = reset_img
    btn.pack(side=LEFT, padx=10)

    notebook.add(tab_clock, text=lang["clocks_lbl"])
    notebook.add(tab_stopwatch, text=lang["sec_lbl"])
    notebook.add(tab_timer, text=lang["timer_lbl"])