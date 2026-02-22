import ctypes
import sys
import time
from tkinter import *
from tkinter import ttk, messagebox,colorchooser, simpledialog, filedialog
import json
import os
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
import keyword
import builtins
from logtofile import log_to_file
from crypto_work import load_key,encrypt_message,decrypt_message

python_types = ["int", "str", "float", "list", "tuple", "dict", "set", "bool", "None"]
special_vars = ["__name__", "__file__", "__dict__", "__doc__", "__init__"]
python_keywords = keyword.kwlist
builtin_functions = dir(builtins)

start_time_ = time.time()
version = 'SD1.0.0'
errors = []

def load_language(lang_code=""):
    try:
        with open("sdk_settings/sdk_lang.json", "r", encoding="utf-8") as file:
            langs = json.load(file)
        if lang_code not in langs:
            log_to_file(f"Error: language {lang_code} not found, use RU")
            return langs["RU"]
    except:
        messagebox.showerror(f"Error {errors[0]}", "No file lang.json in dirrectory!")
        log_to_file("No file lang.json", level="error")
    return langs[lang_code]
key = load_key()
try:
    with open("syst_comp/lang.cfg", "rb") as f:
        encrypted_data = f.read()
        selected_lang = decrypt_message(encrypted_data, key).strip()
except Exception:
    messagebox.showerror(f'Error {errors[0]}',
                         "No file lang.cfg in directory! We created this file, or you can copy this file from folder 'backup_data'")
    log_to_file("No file lang.cfg in directory", level="error")
    selected_lang = "EN"
    encrypted_data = encrypt_message(selected_lang, key)
    with open("syst_comp/lang.cfg", "wb") as f:
        f.write(encrypted_data)

lang = load_language(selected_lang)


def load_valid_languages_plain(filepath="syst_comp/valids/vld_l.cfg") -> set:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return set(line.strip() for line in lines if line.strip())
def create_lang():
    def block_keys(event):
        index = text.index(INSERT)
        tags = text.tag_names(index)
        if "readonly" in tags: return "break"
    def open_search(event=None):
        search_window = Toplevel(w)
        search_window.title(lang["poisk"])
        search_window.geometry("300x80")
        search_window.resizable(False, False)

        Label(search_window, text=lang["naiti"]).pack(pady=5)
        search_entry = Entry(search_window, width=30)
        search_entry.pack()

        def do_search():
            query = search_entry.get()
            text.tag_remove("highlight", "1.0", END)
            if query:
                start = "1.0"
                first_match = None
                while True:
                    start = text.search(query, start, stopindex=END)
                    if not start:
                        break
                    end = f"{start}+{len(query)}c"
                    text.tag_add("highlight", start, end)
                    if not first_match:
                        first_match = start
                    start = end

                text.tag_config("highlight", background="yellow", foreground="black")

                if first_match:
                    text.see(first_match)
                    text.mark_set("insert", first_match)
                    text.focus()

        Button(search_window, text=lang["naiti1"], command=do_search).pack(pady=5)
        search_entry.bind("<Return>", lambda event: do_search())
    def save_lang():
        def save(code):
            if len(code) > 0:
                try:
                    key = load_key()
                    raw = text.get("1.0", END)
                    lines = raw.strip().splitlines()
                    inner_dict = {}

                    for line in lines:
                        if ':' not in line:
                            continue
                        k, v = line.split(":", 1)
                        k = k.strip().strip('"')
                        v = v.strip().strip(',').strip('"')
                        inner_dict[k] = v

                    lang_code = str(code)
                    json_path = "syst_comp/lang.json"
                    vld_path = "syst_comp/valids/vld_l.cfg"

                    if os.path.exists(json_path):
                        with open(json_path, "r", encoding="utf-8") as f:
                            existing_data = json.load(f)
                    else:
                        existing_data = {}

                    existing_data[lang_code] = inner_dict

                    if os.path.exists(vld_path):
                        with open(vld_path, "rb") as f:
                            try:
                                decrypted = decrypt_message(f.read(), key)
                                lang_set = set(decrypted.splitlines())
                            except:
                                lang_set = set()
                    else:
                        lang_set = set()

                    if lang_code not in lang_set:
                        lang_set.add(lang_code)
                        encrypted = encrypt_message("\n".join(sorted(lang_set)), key)
                        with open(vld_path, "wb") as f:
                            f.write(encrypted)

                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=2)
                    w.destroy()
                    messagebox.showinfo(lang["success"], lang["new_lang_added"])
                    status.config(text=lang['add_lang'])

                except Exception as e:
                    messagebox.showerror(lang["error"], f"{lang['error_with_save']}:\n{e}")
                    status.config(text=lang['error'],fg = "red")

            else:
                messagebox.showerror(lang["error"],lang["polepust"])
                return

        W = Toplevel(w)
        W.title(lang["redyaz"])
        W.resizable(False, False)
        W.geometry("450x300")
        Label(W,text = lang["enter_yaz"]).pack()
        code = ttk.Entry(W)
        code.pack()
        ttk.Button(W,text = lang["sdk_save"],command = lambda:save(code.get())).pack()
    def block_delete(event):
        try:
            sel_start = text.index("sel.first")
            sel_end = text.index("sel.last")
            if sel_start != sel_end:
                return "break"
        except:
            return "break"

    w = Toplevel(root)
    w.title(lang["redyaz"])
    w.resizable(False, False)
    w.geometry("800x500")
    scrollbar = Scrollbar(w)
    scrollbar.pack(side=RIGHT, fill=Y)
    text = Text(w, wrap="word", yscrollcommand=scrollbar.set, font=("Consolas", 12))
    text.pack(fill=BOTH, expand=True)
    scrollbar.config(command=text.yview)
    lang_dict = load_language("RU")
    for key, value in lang_dict.items():
        start_index = text.index(INSERT)
        text.insert(INSERT, f'"{key}": ')
        mid_index = text.index(INSERT)
        text.insert(INSERT, f'"{value}"\n')
        text.tag_add("readonly", start_index, mid_index)  # тег на ключ
        text.tag_add("key_style", start_index, mid_index)
        text.tag_configure("highlight", background="yellow", foreground="black")

    text.tag_configure("key_style", foreground="blue", font=("Consolas", 12, "bold"))
    text.bind("<Key>", block_keys)
    text.bind("<BackSpace>", block_keys)
    text.bind("<Delete>", block_keys)
    w.bind("<Control-f>", open_search)
    text.bind("<Button-3>", lambda e: "break")
    text.bind("<BackSpace>", block_delete)
    text.bind("<Delete>", block_delete)
    text.bind("<Control-BackSpace>", block_delete)
    text.bind("<Control-Delete>", block_delete)
    ttk.Button(w, text=lang["save__"], command=save_lang).pack(pady=5)
def shorten(text, max_len=400):
    return text[:max_len] + "..." if len(text) > max_len else text
def read_syst_files():
    def on_double_click(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            file, decr, encr = values
            messagebox.showinfo(f"{lang['sod']}: {file}", f"{lang['encr']}:\n{decr}\n\n{lang['shifr']}:\n{encr}")
    key = load_key()
    w = Toplevel(root)
    w.title(lang["prosfiles"])
    w.geometry("1100x600")

    tree = ttk.Treeview(w, columns=("name", "decr", "encr"), show='headings', height=7)
    tree.heading("name", text=lang["files"])
    tree.heading("decr", text=lang["decrypted"])
    tree.heading("encr", text=lang["encrypted"])
    tree.pack(fill='both', expand=True)
    tree.bind("<Double-1>", on_double_click)
    files = [
        "syst_comp/lang.cfg",
        "syst_comp/license.bin",
        "syst_comp/parametrs.bin",
        "syst_comp/plc_sys.cfg",
        "syst_comp/plc_clk.cfg",
        "syst_comp/volume.cfg",
        "syst_comp/valids/vld_l.cfg",
        "syst_comp/gamebar_settings/gamebar_p.cfg",
        "syst_comp/gamebar_settings/gamebar_shw_inf.cfg",
        "syst_comp/gamebar_settings/gamebar_theme.cfg",
        "syst_comp/valids/vld_c.cfg",
        "syst_comp/valids/vld_icons.cfg",
        "syst_comp/valids/vld_path_wlp.cfg",
        "syst_comp/valids/vld_wlp.cfg"
    ]

    for file in files:
        try:
            with open(file, "rb") as f:
                encr = f.read()
            decr = decrypt_message(encr, key)
        except Exception as e:
            decr = f"[Error]: {e}"
            encr = "[Error with read]"

        if isinstance(decr, bytes):
            decr_str = decr.decode("utf-8", errors="replace")
        else:
            decr_str = decr

        if isinstance(encr, bytes):
            encr_str = encr.decode("utf-8", errors="replace")
        else:
            encr_str = encr

        if "syst_comp/valids/" in file:
            lines = decr_str.splitlines()
            short_decr = ", ".join(line.strip() for line in lines if line.strip())
        else:
            short_decr = decr_str[:100] + ("..." if len(decr_str) > 100 else "")

        short_encr = encr_str[:100] + ("..." if len(encr_str) > 100 else "")

        if 'syst_comp/parametrs.bin' in file:
            tree.insert("", "end", values=(file, shorten(short_decr), shorten(short_encr)))
        else:
            tree.insert("", "end", values=(file, short_decr, short_encr))


def change_color():
    def save(color,vld_path = "syst_comp/valids/vld_c.cfg"):
        key = load_key()
        if os.path.exists(vld_path):
            with open(vld_path, "rb") as f:
                try:
                    decrypted = decrypt_message(f.read(), key)
                    lang_set = set(decrypted.splitlines())
                except:
                    lang_set = set()
        else:
            lang_set = set()

        if color not in lang_set:
            lang_set.add(color)
            encrypted = encrypt_message("\n".join(sorted(lang_set)), key)
            with open(vld_path, "wb") as f:
                f.write(encrypted)
        messagebox.showinfo(lang["success"],lang["new_color_added"])
        status.config(text=lang['add_clr'])
    w = Toplevel(root)
    w.title(lang["backcolor"])
    w.geometry("200x200")
    w.resizable(False,False)
    color_code = colorchooser.askcolor(parent = w,title=lang["color_chose"])[1]
    if color_code:
        ttk.Button(w,text = lang["save__"],command = lambda:save(color_code)).pack()
    else:
        Label(w,text = lang["nocolor"]).pack()
def add_icon():
    def add(path,vld_path = "syst_comp/valids/vld_icons.cfg"):
        if path == "icons//myimage.png":
            messagebox.showerror(lang["error"],lang["invalid_icon"])
        else:
            # --- Загружаем существующие языки ---
            if os.path.exists(vld_path):
                with open(vld_path, "rb") as f:
                    try:
                        decrypted = decrypt_message(f.read(), key)
                        lang_set = set(decrypted.splitlines())
                    except:
                        lang_set = set()
            else:
                lang_set = set()

            # --- Добавляем, если нового нет ---
            if path not in lang_set:
                lang_set.add(path)
                encrypted = encrypt_message("\n".join(sorted(lang_set)), key)
                with open(vld_path, "wb") as f:
                    f.write(encrypted)
            messagebox.showinfo(lang["success"],lang["icon_added"])
            status.config(text = lang['add_ic'])
    w = Toplevel(root)
    w.title(lang["addic"])
    w.geometry("500x400")
    w.resizable()
    Label(w,text = lang["add_in_folder"]).pack()
    path = ttk.Entry(w)
    path.pack()
    path.insert(1,"icons//myimage.png")
    ttk.Button(w,text = lang["save__"],command = lambda:add(path.get())).pack()
def remove_icon():
    def remove(icon):
        key = load_key()
        try:
            with open("syst_comp/valids/vld_icons.cfg","rb") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror(lang["error"], str(e))
        dec = decrypt_message(data,key)
        if icon in dec:
            stripp = dec.strip("icons//acc9.png")
            data_to = encrypt_message(stripp,key)
            try:
                with open("syst_comp/valids/vld_icons.cfg", "wb") as f:
                    f.write(data_to)
                messagebox.showinfo(lang["success"],lang["removesuc"])
            except Exception as e:
                messagebox.showerror(lang["error"],str(e))
        else:
            messagebox.showerror(lang["error"],lang['noimage'])
    w = Toplevel(root)
    w.title(lang["remove"])
    w.geometry("300x300")
    w.resizable(False,False)

    Label(w,text = lang["enter_path"]).pack()
    inp = ttk.Entry(w)
    inp.pack()
    ttk.Button(w,text = lang["remove"],command = lambda:remove(inp.get())).pack()
def remove_lang():
    def remove(ll):
        with open('syst_comp/lang.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if ll in data:
            del data[ll]
            with open('syst_comp/lang.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo(lang["success"],lang["key_deleted"])
        else:
            messagebox.showerror(lang["error"],lang["error_with_delete_key"])
    w = Toplevel(root)
    w.title(lang["remove"])
    w.geometry("300x300")
    w.resizable(False, False)

    Label(w, text=lang["enter_lang_name"]).pack()
    inp = ttk.Entry(w)
    inp.pack()
    ttk.Button(w, text=lang["remove"], command=lambda: remove(inp.get())).pack()
def create_user_prog():

    def write():
        def clear_tags():
            for tag in ["keyword", "builtin", "type", "special", "comment"]:
                text.tag_remove(tag, "1.0", END)
        def apply_tag(word_list, tag, use_regex=True):
            for word in word_list:
                start = "1.0"
                pattern = rf'\m{word}\M' if use_regex else word
                while True:
                    pos = text.search(pattern, start, stopindex=END, regexp=use_regex)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    text.tag_add(tag, pos, end)
                    start = end
        def highlight_comments():
            start = "1.0"
            while True:
                pos = text.search(r"#.*", start, stopindex=END, regexp=True)
                if not pos:
                    break
                line_end = text.search(r"\n", pos, stopindex=END)
                end = line_end if line_end else END
                text.tag_add("comment", pos, end)
                start = end
        def update_syntax_highlighting(event=None):
            clear_tags()
            apply_tag(python_keywords, "keyword")
            apply_tag(builtin_functions, "builtin", use_regex=False)
            apply_tag(python_types, "type")
            apply_tag(special_vars, "special", use_regex=False)
            highlight_comments()
        def open_file():
            file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    text.delete("1.0", END)
                    text.insert("1.0", f.read())
                update_syntax_highlighting()
        def save(data):
            name = simpledialog.askstring(lang["write_name"], lang["write_name"])
            if name and name.strip():
                with open(f"user_progs/{name}.py", "w", encoding="utf-8") as f:
                    f.write(data)
                messagebox.showinfo(lang["success"], lang["code_file_saved"])
            else:
                messagebox.showerror(lang["error"], lang["name<0"])
        W = Toplevel(root)
        W.title(lang["user_prog"])
        W.geometry('800x600')
        W.state('zoomed')

        menu = Menu(W)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label=lang["open"], command=open_file)
        file_menu.add_command(label=lang["save"], command=lambda: save(text.get("1.0", "end-1c")))
        file_menu.add_separator()
        file_menu.add_command(label=lang["exit"], command=W.destroy)
        menu.add_cascade(label=lang["file"], menu=file_menu)
        W.config(menu=menu)

        # Scrollbar + Text
        frame = Frame(W, bg="#2b2b2b")
        frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text = Text(frame, bg="#1e1e1e", fg="#ffffff", insertbackground="white",
                    font=("Courier New", 12), undo=True, wrap=NONE, yscrollcommand=scrollbar.set,
                    borderwidth=2, relief=GROOVE)
        text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=text.yview)

        # Highlighting colors
        text.tag_config("keyword", foreground="#569CD6")
        text.tag_config("builtin", foreground="#DCDCAA")
        text.tag_config("type", foreground="#4EC9B0")
        text.tag_config("special", foreground="#C586C0")
        text.tag_config("comment", foreground="#6A9955", font=("Courier New", 10, "italic"))

        text.bind("<KeyRelease>", update_syntax_highlighting)
        update_syntax_highlighting()

    write()
root = Tk()
root.resizable(False,False)
root.geometry("600x500")
root.title(f"SDK DEv Kit - {version}")

img = Image.open("sdk_icons/sdk.png")
icon_image = ImageTk.PhotoImage(img)
root.iconphoto(True, icon_image)

image1 = Image.open("sdk_icons//create.png")  # путь к картинке
image1 = image1.resize((64, 64))  # изменяем размер (необязательно)
photo1 = ImageTk.PhotoImage(image1)

image2 = Image.open("sdk_icons//view.png")  # путь к картинке
image2 = image2.resize((64, 64))  # изменяем размер (необязательно)
photo2 = ImageTk.PhotoImage(image2)

image3 = Image.open("sdk_icons//add.png")  # путь к картинке
image3 = image3.resize((64, 64))  # изменяем размер (необязательно)
photo3 = ImageTk.PhotoImage(image3)

image4 = Image.open("sdk_icons//addicon.png")  # путь к картинке
image4 = image4.resize((64, 64))  # изменяем размер (необязательно)
photo4= ImageTk.PhotoImage(image4)

image5 = Image.open("sdk_icons//remove.png")  # путь к картинке
image5 = image5.resize((64, 64))  # изменяем размер (необязательно)
photo5 = ImageTk.PhotoImage(image5)

image6 = Image.open("sdk_icons//remove_icon.png")  # путь к картинке
image6 = image6.resize((64, 64))  # изменяем размер (необязательно)
photo6 = ImageTk.PhotoImage(image6)

image7 = Image.open("sdk_icons//exe.png")  # путь к картинке
image7 = image7.resize((64, 64))  # изменяем размер (необязательно)
photo7 = ImageTk.PhotoImage(image7)

frame_tit = Frame()
frame_tit.pack()
frame1 = Frame()
frame1.pack(side = "left")
frame_status = Frame()
frame_status.pack(side=BOTTOM, fill=X,anchor="w")
title = Label(frame_tit, text="WinDoors52 SDK Tool", font=("Segoe UI", 16, "bold"))
title.pack(side = TOP,anchor=CENTER)

buttons = [
    (photo1, create_lang, lang["create_lang"],lang["create_lang"]),
    (photo2, read_syst_files, lang["view_sys_files"],lang["view_sys_files"]),
    (photo3, change_color, lang["add_new_color"],lang["add_new_color"]),
    (photo4, add_icon, lang["add_new_icon"],lang["add_new_icon"]),
    (photo6, remove_icon, lang["remove_icon"],lang["remove_icon"]),
    (photo5, remove_lang, lang["remove_lang"],lang["remove_lang"]),
    (photo7, create_user_prog, lang["create_user_prog"],lang["create_user_prog"]),
]

for i, (img, cmd, text_label,tool) in enumerate(buttons):
    row, col = divmod(i, 3)
    btn = ttk.Button(frame1, image=img, command=cmd)
    btn.image = img
    btn.grid(row=row*2, column=col, padx=20, pady=(10, 0))
    Hovertip(btn, tool)
    lbl = Label(frame1, text=text_label)
    lbl.grid(row=row*2+1, column=col)
status = Label(frame_status, text=lang["gotovo"], fg="green", bd=1, relief=RAISED, anchor="w")
status.pack(side=BOTTOM, fill=X)


def run_updater():
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    updater_path = os.path.join(exe_dir, "sdkupdater.exe")

    print("Path:", updater_path)
    print("Exists:", os.path.exists(updater_path))

    if os.path.exists(updater_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", updater_path, None, None, 1)
    else:
        print("Updater not found")
run_updater()
root.mainloop()