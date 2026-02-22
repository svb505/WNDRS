import time
from tkinter import *
from tkinter import ttk
from logtofile import log_system,log_to_file
import logging
import os
import sys
from server_statistick import update_file,update_elpsed
from play_sound import play_sound

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")


def on_closing(start_time_,email):
    log_system("----SHUT DOWN OS----",start_time_)
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0  # Если start_time_ нет, пишем 0 секунд
    update_file("time_in_windoors.txt", int(elapsed))
    update_file(f"time_{email}.txt", int(elapsed))
    update_elpsed("max_time.txt", int(elapsed))
def restart_os(actives_programs,start_time_,email):
    log_system("----RESTART OS----",start_time_ = start_time_)
    for i in actives_programs:
        log_to_file(f'Program {i} close',start_time_ = start_time_)
    on_closing(start_time_,email)
    os.execl(sys.executable, sys.executable, *sys.argv)
def exit_os(actives_programs,start_time_,email):
    log_system("----SHUT DOWN OS----",start_time_ = start_time_)
    for i in actives_programs:
        log_to_file(f'Program {i} close',start_time_ = start_time_)
    on_closing(start_time_,email)
    sys.exit()
def shutdown_animation(root,action,volume,errors,lang,actives_programs,is_recording,recording_thread,start_time_,email,state_sound):
    play_sound('sound//ressh.mp3',volume,state_sound,start_time_)
    for widget in root.winfo_children():
        widget.destroy()
    root.destroy()
    shutdown_win = Tk()
    shutdown_win.geometry("500x300")
    shutdown_win.attributes("-fullscreen", True)
    shutdown_win.title(lang["shutdown"] if action == "shutdown" else lang['restart'])
    shutdown_win.configure(bg="black")

    label = Label(shutdown_win, text=lang["shutdown_action"] if action == "shutdown" else lang["restart"] + "...",
                  font=("Arial", 20, "bold"), fg="white", bg="black")
    label.pack(pady=40)

    progress = ttk.Progressbar(shutdown_win, mode="determinate", length=300)
    progress.pack(pady=20)

    def animate(is_recording,recording_thread):
        for i in range(101):
            progress["value"] = i
            shutdown_win.update_idletasks()
            time.sleep(0.03)

        shutdown_win.destroy()
        if action == "reboot":
            if is_recording:
                is_recording = False
                recording_thread = False
            restart_os(actives_programs,start_time_,email)
        else:
            if is_recording:
                is_recording = False
                recording_thread = False
            exit_os(actives_programs,start_time_,email)

    shutdown_win.after(100, lambda:animate(is_recording,recording_thread))
