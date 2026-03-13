import ctypes
import winreg
from tkinter import *
from tkinter import ttk

import win32api
import win32gui
import win32process
from PIL import Image, ImageTk, ImageGrab
from logtofile  import log_to_file
from fadeinout import fade_in


def get_keyboard_layout(LANGUAGES):
    hwnd = win32gui.GetForegroundWindow()
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    layout_id = win32api.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xffff
    return LANGUAGES.get(lang_id, f'Unkn:{hex(lang_id)}')


def update_layout_label(root,layout_label,last_layout,LANGUAGES):
    layout = get_keyboard_layout(LANGUAGES)
    if layout != last_layout:
        layout_label.config(text=layout)
        last_layout = layout
    root.after(300, update_layout_label)
def show_lang(root,taskbar_fg,lang,taskbar,start_time_,lang_win, layout_label, LANGUAGES, taskbar_height):
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    layout_label.config(bg=taskbar_fg)

    lang_win = Toplevel(root)
    lang_win.attributes('-alpha', 0.0)
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
                log_to_file(f"Failed to switch layout {hkl_str}", level="error", start_time_=start_time_)
            else:
                log_to_file(f"Layout switched to {layouts[hkl_str]}", start_time_=start_time_)

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