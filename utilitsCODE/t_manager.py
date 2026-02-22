from logtofile import log_to_file
from play_sound import play_sound
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import psutil

def open_task_manager(state_sound, volume, errors, lang, root, actives_programs, start_time_, global_bg, global_fg,GlobalAlpha):
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    actives_programs.append("Task Manager")
    log_to_file("Task manager launch", start_time_)
    win = Toplevel(root)
    win.attributes("-alpha", float(GlobalAlpha))
    win.title(lang["task_manager"])
    win.geometry("600x400")
    img = Image.open("icons/disp.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    cpu_label = Label(win, text=lang["cpu_load"] + str(psutil.cpu_percent()) + "%", font=("Arial", 12), fg=global_fg,
                      bg=global_bg)

    cpu_label.pack()
    log_to_file(f'Cpu load ==> {psutil.cpu_percent()}+"%"', start_time_)
    frame = Frame(win, bg=global_bg)
    frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("PID", "Name", "CPU %", "RAM MB"), show="headings")
    tree.heading("PID", text="PID")
    tree.heading("Name", text="Name")
    tree.heading("CPU %", text="CPU %")
    tree.heading("RAM MB", text="RAM MB")
    tree.pack(fill=BOTH, expand=True)

    def update_processes():
        for row in tree.get_children():
            tree.delete(row)
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                tree.insert("", "end", values=(
                    proc.info['pid'], proc.info['name'], proc.info['cpu_percent'],
                    round(proc.info['memory_info'].rss / 1024 / 1024, 1)
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        cpu_label.config(text=f'{lang["cpu_load"]} + {psutil.cpu_percent()}%')
        log_to_file(f'Cpu load ==> {psutil.cpu_percent()}+"%"', start_time_)
        win.after(2000, update_processes)

    update_processes()