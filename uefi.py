from tkinter import *
import platform
import psutil
import os

selected_index = 0

def bios():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "WinDoors52.exe":
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except psutil.NoSuchProcess:
                pass
            except psutil.TimeoutExpired:
                proc.kill()
    global selected_index
    selected_index = 0
    menu_items = ["Boot Order", "CPU Info", "Memory Info", "Power Settings", "Return","Exit"]
    label_list = []

    bs = Tk()
    bs.title("UEFI Setup Utility")
    bs.geometry("400x250")
    bs.attributes('-fullscreen', True)
    bs.configure(bg="black")
    bs.focus_set()
    def draw_menu():
        global label_list
        for widget in bs.winfo_children():
            widget.destroy()

        Label(bs, text="UEFI Setup Utility", fg="lightblue", bg="black",
                 font=("Courier", 18, "bold")).pack(pady=10)

        label_list = []
        for i, item in enumerate(menu_items):
            color = "yellow" if i == selected_index else "white"
            prefix = "> " if i == selected_index else "  "
            label = Label(bs, text=prefix + item, fg=color, bg="black", font=("Courier", 14))
            label.pack(anchor="w", padx=30)
            label_list.append(label)
    def move_up(event):
        global selected_index
        selected_index = (selected_index - 1) % len(menu_items)
        draw_menu()
    def move_down(event):
        global selected_index
        selected_index = (selected_index + 1) % len(menu_items)
        draw_menu()
    def select_option(event):
        option = menu_items[selected_index]
        if option == "Exit":
            bs.destroy()
        elif option == "Return":
            bs.destroy()
            os.startfile("WinDoors52.exe")
        else:
            show_info_screen(option)
    def show_info_screen(option):
        for widget in bs.winfo_children():
            widget.destroy()

        Label(bs, text=f"{option}", fg="lightgreen", bg="black", font=("Courier", 16)).pack(pady=10)

        info_text = ""
        if option == "Boot Order":
            info_text = "1. USB Drive\n2. Hard Disk\n3. Network Boot\n4. CD/DVD"
        elif option == "CPU Info":
            info_text = f"Processor: {platform.processor() or 'Unknown'}\nCores: {psutil.cpu_count(logical=False)}\nThreads: {psutil.cpu_count()}"
        elif option == "Memory Info":
            mem = psutil.virtual_memory()
            info_text = f"Total RAM: {round(mem.total / 1024 ** 3, 2)} GB\nUsed: {round(mem.used / 1024 ** 3, 2)} GB"
        elif option == "Power Settings":
            info_text = "Power Saving Mode: OFF\nSleep Timer: 30 min\nWake-on-LAN: ENABLED"

        Label(bs, text=info_text, fg="white", bg="black", font=("Courier", 13), justify="left").pack(pady=10)
        Label(bs, text="[Press ESC to go back]", fg="gray", bg="black", font=("Courier", 12)).pack(pady=10)

        bs.bind("<Escape>", go_back)
    def go_back(event):
        draw_menu()
        bs.bind("<Up>", move_up)
        bs.bind("<Down>", move_down)
        bs.bind("<Return>", select_option)

    bs.bind("<Up>", move_up)
    bs.bind("<Down>", move_down)
    bs.bind("<Return>", select_option)

    draw_menu()
    bs.focus_set()
    bs.mainloop()
bios()