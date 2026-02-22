import sqlite3
from tkinter import *
from tkinter import messagebox
import psutil
from datetime import datetime
import socket
import platform
import os
import random
from PIL import Image, ImageTk
from excos import shutdown_animation

names = []
last = ""
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
def open_terminal(version,start_time,vpn,lang,volume,errors,actives_programs,is_recording,recording_thread,root,bsod_func,GlobalAlpha):
    global n
    def func(event):
        global names,last,n
        text = event.widget
        commands = {
            "echo": "Print text in console.",
            "cls": "Clear terminal.",
            'mkdir ""': "Create new directory",
            "systeminfo": "Show system info.",
            "shutdown": "Shutdown system.",
            "hostname": "Show PC name.",
            "help": "Show all commands.",
            "dir": "Show all files in current directory",
            "dir /s": "Show all files in current directory and subdirectories",
            "ping": "Internet connection",
            "time": "Show current time",
            "ipconfig": "Show IP",
            "color": "Change CMD color",
            "title":"Change window title",
            "whoami": "Name of user",
            "ver": "Version of WinDoors52",
            "!!": "Repeat last command",
            "del": "Delete file",
            "BSOD": "Open Bsod",
            "uptime": "Time from start OS",
            "date":"Current date",
            "exit":"Close current window",
            "history":"History of the commands"

        }
        def clear():
            text.delete("1.0", "end")  # Удаляем всё, кроме приглашения
        def sys_inf():
            return {
                "Pc name": socket.gethostname(),
                "OS": "Windoors 52",
                "Processor": platform.processor(),
                "Architecture": platform.machine(),
                "Cpu count": psutil.cpu_count(logical=True),
                "VM": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            }
        def blink_cursor():
            global cursor_id
            if blinking:
                current_text = text.get("end-2c", "end-1c")
                if current_text == "_":
                    text.delete("end-2c", "end-1c")
                else:
                    text.insert("end", "_")
                cursor_id = text.after(500, blink_cursor)
        def handle_command(command,n):
            global names,last
            if command != "!!":
                last = command
            names.append(command)
            if command.startswith("echo "):
                text.insert("end", f"{command[5:]}\n")
            if command.startswith("title "):
                win.title(command[6:])
            elif command == "ver":
                text.insert("end", version)
            elif command == "whoami":
                text.insert("end", str(n))
            elif command == "color 0a":
                text.config(fg="lime")
            elif command == "color 0b":
                text.config(fg="lightblue")
            elif command == "color 0c":
                text.config(fg="red")
            elif command == "color 0d":
                text.config(fg="violet")
            elif command == "color 0e":
                text.config(fg="yellow")
            elif command == "color 0f":
                text.config(fg="white")
            elif command == "cls":
                clear()
            elif "mkdir" in command:
                try:
                    os.makedirs(command[7:-1],exist_ok = True)
                    text.insert('end',f'direcory {command[7:-1]} created\n')
                except Exception as e:
                    text.insert("end",f'{e}\n')
            elif command == "dir/s" or command == "dir /s":
                file_list = []
                try:
                    for root, dirs, files in os.walk(os.getcwd()):
                        file_list.append(f"\n> Directory: {root}")
                        for file in files:
                            file_list.append(file)
                except Exception as e:
                    text.insert("end", f"Error: {e}\n")
                    return

                def show_next_line(index=0):
                    if index < len(file_list):
                        # Убираем мигающий курсор, если есть
                        if text.get("end-2c", "end-1c") == "_":
                            text.delete("end-2c", "end-1c")
                        text.insert("end", f"{file_list[index]}\n")
                        text.see("end")
                        text.after(2, show_next_line, index + 1)
                    else:
                        # Завершаем мигание курсора
                        global blinking
                        blinking = False
                        if cursor_id:
                            text.after_cancel(cursor_id)
                        # Убедимся, что курсор удалён
                        if text.get("end-2c", "end-1c") == "_":
                            text.delete("end-2c", "end-1c")
                        text.insert("end", f"\nC:\\{n}> ")

                blinking = True
                blink_cursor()
                show_next_line()
            elif command.startswith("del "):
                try:
                    os.remove(str(command[4:]))
                except Exception as e:
                    messagebox.showinfo(lang["error"], str(e))
            elif command == "systeminfo":
                sys_info = sys_inf()
                text.insert("end", "\n> System Information:\n")
                for key, value in sys_info.items():
                    text.insert("end", f"{key}: {value}\n")
            elif command == "shutdown":
                shutdown_animation("shutdown", volume, errors, lang, actives_programs, is_recording, recording_thread)
            elif command == "BSOD":
                bsod_func()  # просто вызываем переданную функцию
            elif command == "hostname":
                text.insert("end", f"{socket.gethostname()}\n")
            elif command == "help":
                text.insert("end", "\n> List of all commands:\n")
                for cmd, description in commands.items():
                    text.insert("end", f"{cmd}: {description}\n")
            elif command == "date":
                text.insert("end", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            elif command == "ipconfig":
                if vpn:
                    ip = random.randint(10000, 99999)
                    text.insert("end", f"{ip}\n")
                else:
                    hostname = socket.gethostname()
                    ip_address = socket.gethostbyname(hostname)
                    text.insert("end", f"{ip_address}\n")
            elif command == "dir":
                try:
                    files = os.listdir(os.getcwd())
                    text.insert("end", "\n> Files in current directory:\n")
                    for file in files:
                        text.insert("end", f"{file}\n")
                except Exception as e:
                    text.insert("end", f"Error listing directory: {e}\n")
            elif command.startswith("ping "):
                address = command[5:].strip()
                response = os.system(f"ping {address}")
                if response == 0:
                    text.insert("end", f"Ping to {address} successful.\n")
                else:
                    text.insert("end", f"Ping to {address} failed.\n")
            elif command == "exit":
                win.destroy()
            elif command == "uptime":
                text.insert("end", f"{start_time:.2f}")
            elif command == 'history':
                for n in names:
                    text.insert("end", f"{n} - {start_time:.2f}\n")
            elif command == "time":
                text.insert("end", f"{datetime.now().strftime('%H:%M:%S')}\n")
            elif command == "!!":
                text.insert("end", f"Repeating last command: {last}\n")
                handle_command(last)  # повторный вызов своей же функции
            else:
                text.insert("end", "\n> Unknown command\n")
        # Получаем введенную строку, **но убираем префикс только перед обработкой**
        full_command = text.get("end-2l", "end-1c").strip()

        command = full_command.replace(f"C:\\{n}> ", "", 1)  # Убираем "C:\>" только перед обработкой
        clear()  # Очищаем старый вывод
        text.insert("end", f"> {command}\n")  # Отображаем команду в терминале

        if command != "!!":
            last = command
        names.append(command)
        if command.startswith("echo "):
            text.insert("end", f"{command[5:]}\n")
        if command.startswith("title "):
            win.title(command[6:])
        elif command == "ver":
            text.insert("end",version)
        elif command == "whoami":
            text.insert("end",str(n))
        elif command == "color 0a":
            text.config(fg="lime")
        elif command == "color 0b":
            text.config(fg="lightblue")
        elif command == "color 0c":
            text.config(fg="red")
        elif command == "color 0d":
            text.config(fg="violet")
        elif command == "color 0e":
            text.config(fg="yellow")
        elif command == "color 0f":
            text.config(fg="white")
        elif command == "cls":
            clear()
        elif "mkdir" in command:
            try:
                os.makedirs(command[7:-1], exist_ok=True)
                text.insert('end', f'direcory {command[7:-1]} created\n')
            except Exception as e:
                text.insert("end", f'{e}\n')
        elif command == "dir/s" or command == "dir /s":
            file_list = []
            try:
                for root, dirs, files in os.walk(os.getcwd()):
                    file_list.append(f"\n> Directory: {root}")
                    for file in files:
                        file_list.append(file)
            except Exception as e:
                text.insert("end", f"Error: {e}\n")
                return

            def show_next_line(index=0):
                if index < len(file_list):
                    # Убираем мигающий курсор, если есть
                    if text.get("end-2c", "end-1c") == "_":
                        text.delete("end-2c", "end-1c")
                    text.insert("end", f"{file_list[index]}\n")
                    text.see("end")
                    text.after(2, show_next_line, index + 1)
                else:
                    # Завершаем мигание курсора
                    global blinking
                    blinking = False
                    if cursor_id:
                        text.after_cancel(cursor_id)
                    # Убедимся, что курсор удалён
                    if text.get("end-2c", "end-1c") == "_":
                        text.delete("end-2c", "end-1c")
                    text.insert(f"end", "\nC:\\{n}> ")

            blinking = True
            blink_cursor()
            show_next_line()
        elif command.startswith("del "):
            try:
                os.remove(str(command[4:]))
            except Exception as e:
                messagebox.showinfo(lang["error"], str(e))
        elif command == "systeminfo":
            sys_info = sys_inf()
            text.insert("end", "\n> System Information:\n")
            for key, value in sys_info.items():
                text.insert("end", f"{key}: {value}\n")
        elif command == "shutdown":
            shutdown_animation("shutdown", volume, errors, lang, actives_programs, is_recording, recording_thread)
        elif command == "BSOD":
            bsod_func()  # просто вызываем переданную функцию
        elif command == "hostname":
            text.insert("end", f"{socket.gethostname()}\n")
        elif command == "help":
            text.insert("end", "\n> List of all commands:\n")
            for cmd, description in commands.items():
                text.insert("end", f"{cmd}: {description}\n")
        elif command == "date":
            text.insert("end", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        elif command == "ipconfig":
            if vpn:
                ip = random.randint(10000, 99999)
                text.insert("end", f"{ip}\n")
            else:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                text.insert("end", f"{ip_address}\n")
        elif command == "dir":
            try:
                files = os.listdir(os.getcwd())
                text.insert("end", "\n> Files in current directory:\n")
                for file in files:
                    text.insert("end", f"{file}\n")
            except Exception as e:
                text.insert("end", f"Error listing directory: {e}\n")
        elif command.startswith("ping "):
            address = command[5:].strip()
            response = os.system(f"ping {address}")
            if response == 0:
                text.insert("end", f"Ping to {address} successful.\n")
            else:
                text.insert("end", f"Ping to {address} failed.\n")
        elif command == "exit":
            win.destroy()
        elif command == "uptime":
            text.insert("end", f"{start_time:.2f}")
        elif command == 'history':
            for n in names:
                text.insert("end", f"{n} - {start_time:.2f}\n")
        elif command == "time":
            text.insert("end", f"{datetime.now().strftime('%H:%M:%S')}\n")
        elif command == "!!":
            text.insert("end", f"Repeating last command: {last}\n")
            handle_command(last,n)  # повторный вызов своей же функции
        else:
            text.insert("end", "\n> Unknown command\n")

        # Всегда вставляем приглашение `C:\>` для следующей команды
        text.insert("end", f"\nC:\\{n}> ")

        # Создание окна терминала

    win = Toplevel()
    win.attributes("-alpha", float(GlobalAlpha))
    win.title(lang["command"])
    img = Image.open("icons/cmd2.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.geometry("1500x800")
    win.configure(bg="black")

    text = Text(win, fg="lime", bg="black")
    text.pack(expand=True, fill="both")

    win.bind("<Return>",func)
    text.insert("end",f"WinDoors 52 [VERSION - {version}]\n(c) SVB Corporation SoftWare Dev.\n")
    text.insert("end", f"C:\\{n}> ")  # Оставляем префикс при запуске