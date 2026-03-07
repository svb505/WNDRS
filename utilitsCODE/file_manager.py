from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import os
import threading
from PIL import Image, ImageTk
import ctypes
from logtofile import log_to_file
from play_sound import play_sound
import json
import ctypes
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
dll_path = os.path.join(PARENT_DIR, "DLLs", "LoadFiles.dll")
filelist_dll = ctypes.CDLL(dll_path)

def get_files_from_dll(path):
    buf = ctypes.create_string_buffer(65536)
    res = filelist_dll.GetFiles(path.encode("utf-8"), buf, len(buf))
    if res != 0:
        raise RuntimeError(f"DLL error {res}")
    return json.loads(buf.value.decode("utf-8"))
def open_file_manager(state_sound, root, lang, global_bg, actives_programs, gl_police, global_fg, volume, errors, start_time_,GlobalAlpha):
    def on_right_click(event, tree, base_path, allow_edit):
        item_id = tree.identify_row(event.y)
        menu = Menu(tree, tearoff=0)

        if not item_id:
            if allow_edit:
                menu.add_command(label=lang["cre"], command=lambda: create_file_in_tree(base_path, tree))
            menu.post(event.x_root, event.y_root)
            return

        values = tree.item(item_id, "values")
        if not values:
            return

        file_name = values[0]
        full_path = os.path.join(base_path, file_name)

        if os.path.exists(full_path):
            try:
                size_mb = os.path.getsize(full_path) / (1024 * 1024)
            except:
                size_mb = 0.0
            menu.add_command(label=lang["file_info"], command=lambda: messagebox.showinfo(
                lang["file_info"], f"{file_name}\n{size_mb:.2f} MB", parent=win))

        if allow_edit:
            menu.add_command(label=lang["del"], command=lambda: delete_file(full_path, tree))
            menu.add_command(label=lang["cre"], command=lambda: create_file_in_tree(base_path, tree))

        menu.post(event.x_root, event.y_root)
    def delete_file(path, tree):
        dll = ctypes.CDLL("DLLs/trashbin.dll")
        dll.AddToTrash.argtypes = [ctypes.c_char_p]
        dll.AddToTrash.restype = None
        dll.AddToTrash(path.encode("utf-8"))
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            refresh_tree(tree, os.path.dirname(path))
        except Exception as e:
            messagebox.showerror(lang["error"], str(e), parent=win)
    def create_file_in_tree(base_path, tree):
        name = simpledialog.askstring(lang["file_manager"], lang["ent-name"])
        if name:
            full_path = os.path.join(base_path, f"{name}")
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write("")
                refresh_tree(tree, base_path)
            except Exception as e:
                messagebox.showerror(lang["error"], str(e), parent=win)
    def refresh_tree(tree, base_path):
        for item in tree.get_children():
            tree.delete(item)

        threading.Thread(target=populate_tree_with_progress, args=(tree, base_path)).start()
    def populate_tree_with_progress(tree, base_path):
        try:
            items = get_files_from_dll(base_path)
        except Exception as e:
            log_to_file(f"Error load files from DLL: {e}", start_time_, "error")
            messagebox.showerror("Error", f"Error load files from DLL: {e}", parent=win)
            return
        items.sort(key=lambda x: (not x["isdir"], x["name"].lower()))
        total = len(items)

        if total == 0: return

        def insert_item(idx):

            item = items[idx]

            mod_time = datetime.fromtimestamp(
                item.get("mtime", os.path.getmtime(os.path.join(base_path, item["name"]))))
            mod_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                name = item["name"]
                ext = item["ext"].lower()
                isdir = item["isdir"]
                size = item["size"] / (1024 * 1024)

                if isdir:
                    icon = icon_images.get("folder", icon_images.get("default"))
                    values = (name, "folder", f"{size:.2f}",mod_str)
                    node = tree.insert("", "end", values=values, image=icon) if icon else tree.insert("", "end",
                                                                                                      values=values)
                    tree.insert(node, "end")  # пустышка
                else:
                    icon = icon_images.get(ext, icon_images.get("default"))
                    values = (name, "file", f"{size:.2f}",mod_str)
                    tree.insert("", "end", values=values, image=icon) if icon else tree.insert("", "end", values=values)
            except Exception:
                pass

        for i in range(total):
            win.after(i * 100, lambda idx=i: insert_item(idx))
    def add_treeview(parent, base_path, allow_edit):
        container = Frame(parent, bg=global_bg)
        container.pack(fill="both", expand=True)

        tree_frame = Frame(container)
        tree_frame.pack(fill="both", expand=True)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(tree_frame, columns=("Name", "Type", "Size (MB)","Modified"), show="tree headings",
                            yscrollcommand=scrollbar.set,selectmode="extended")
        tree.heading("Name", text=lang["name"])
        tree.heading("Type", text=lang["type"])
        tree.heading("Size (MB)", text=lang["sizefile"])
        tree.heading("Modified", text=lang["modified"])
        tree.column("Modified", width=120, anchor="center")
        tree.pack(fill="both", expand=True)

        scrollbar.config(command=tree.yview)

        # Заменяем сразу на функцию с прогрессом
        threading.Thread(target=populate_tree_with_progress, args=(tree, base_path)).start()
        tree.bind("<Button-3>", lambda e: on_right_click(e, tree, base_path, allow_edit))

        def on_item_open(event):
            item_id = tree.focus()
            if not item_id:
                return
            file_name = tree.item(item_id, "values")[0]
            path = os.path.join(base_path, file_name)
            try:
                items = get_files_from_dll(path)
            except Exception as e:
                messagebox.showerror("Error", f"Ошибка DLL: {e}", parent=win)
                return

            if any(i["isdir"] for i in items):  # если там папки
                tree.delete(*tree.get_children(item_id))
                for item in items:
                    name = item["name"]
                    ext = item["ext"].lower()
                    isdir = item["isdir"]
                    size = item["size"] / (1024 * 1024)

                    if isdir:
                        icon = icon_images.get("folder", icon_images.get("default"))
                        values = (name, "folder", f"{size:.2f}")
                        node = tree.insert(item_id, "end", values=values, image=icon) if icon else tree.insert(item_id,
                                                                                                               "end",
                                                                                                               values=values)
                        tree.insert(node, "end")
                    else:
                        icon = icon_images.get(ext, icon_images.get("default"))
                        values = (name, "file", f"{size:.2f}")
                        tree.insert(item_id, "end", values=values, image=icon) if icon else tree.insert(item_id, "end",
                                                                                                        values=values)

        tree.bind("<Double-1>", on_item_open)
    def load_icons(win):
        types = {
            "folder": "icons/file_icons/folder.png",
            "7z": "icons/file_icons/folder.png",
            ".bat": "icons/file_icons/bat.png",
            ".bin": "icons/file_icons/bin.png",
            ".c": "icons/file_icons/c.png",
            ".cfg": "icons/file_icons/cfg.png",
            ".cs": "icons/file_icons/cs.png",
            ".cpp": "icons/file_icons/cpp.png",
            ".py": "icons/file_icons/py.png",
            ".css": "icons/file_icons/css.png",
            ".csv": "icons/file_icons/csv.png",
            ".dll": "icons/file_icons/dll.png",
            ".docx": "icons/file_icons/docx.png",
            ".exe": "icons/file_icons/exe.png",
            ".gif": "icons/file_icons/gif.png",
            ".html": "icons/file_icons/html.png",
            ".jar": "icons/file_icons/jar.png",
            ".png": "icons/file_icons/image.png",
            ".jpg": "icons/file_icons/image.png",
            ".js": "icons/file_icons/js.png",
            ".json": "icons/file_icons/json.png",
            ".log": "icons/file_icons/log.png",
            ".mp3": "icons/file_icons/mp3.png",
            ".mp4": "icons/file_icons/mp4.png",
            ".msi": "icons/file_icons/msi.png",
            ".odt": "icons/file_icons/odt.png",
            ".pdf": "icons/file_icons/pdf.png",
            ".php": "icons/file_icons/php.png",
            ".ppt": "icons/file_icons/ppt.png",
            ".rar": "icons/file_icons/rar.png",
            ".zip": "icons/file_icons/zip.png",
            ".sql": "icons/file_icons/sql.png",
            ".db": "icons/file_icons/sql.png",
            ".sys": "icons/file_icons/sys.png",
            ".tga": "icons/file_icons/tga.png",
            ".ttf": "icons/file_icons/ttf.png",
            ".txt": "icons/file_icons/txt.png",
            ".wav": "icons/file_icons/wav.png",
            ".wma": "icons/file_icons/wma.png",
            ".xls": "icons/file_icons/xls.png",
            ".yaml": "icons/file_icons/yaml.png",
            "default": 'icons/file_icons/file.png'
        }
        for key, filename in types.items():
            try:
                if not os.path.exists(filename):
                    icon_images[key] = None
                    continue
                img = Image.open(filename)
                img = img.resize((16, 16), Image.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                icon_images[key] = icon
                win.icon_refs.append(icon)
            except Exception as e:
                icon_images[key] = None
    def user_file_tools():
        def open_editor(mode, file_name=""):
            editor = Toplevel(win)
            editor.attributes("-alpha",float(GlobalAlpha))
            editor.title(f"{lang['file_manager']} - {lang['change'] if mode=='edit' else lang['cre']}")
            editor.geometry("600x500")
            editor.configure(bg=global_bg)
            text_widget = Text(editor, font=("Arial", 10))
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)

            if mode == "edit":
                try:
                    with open(f"user_files/{file_name}", "r", encoding="utf-8") as f:
                        text_widget.insert(1.0, f.read())
                except Exception as e:
                    messagebox.showerror(lang["error"], str(e),parent=win)
                    return

            def save_file():
                content = text_widget.get(1.0, END)
                path = os.path.join("user_files", file_name)
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    messagebox.showinfo(lang["success"], lang["file_cr"],parent=win)
                    editor.destroy()
                except Exception as e:
                    messagebox.showerror(lang["error"], str(e),parent=win)

            ttk.Button(editor, text=lang["change"] if mode == "edit" else lang["cre"], command=save_file).pack(pady=5)
        def create_file():
            name = simpledialog.askstring(lang["file_manager"], lang["ent-name"])
            if name: open_editor("create",name)

        def edit_file():
            name = simpledialog.askstring(lang["file_manager"], lang["ent-naz"])
            if name:
                if not os.path.exists(os.path.join("user_files", name)):
                    messagebox.showerror(lang["error"], lang["nof"],parent=win)
                    return
                open_editor("edit", name)

        Button(user_tab, text=lang["cre"], command=create_file).pack(pady=10)
        Button(user_tab, text=lang["user_fs"], command=edit_file).pack(pady=5)

    play_sound("sound//click.mp3", volume, state_sound, start_time_)

    actives_programs.append("File manager")

    log_to_file("File manager launched", start_time_ = start_time_)

    win = Toplevel(root)
    win.attributes("-alpha",float(GlobalAlpha))
    win.title(lang["file_manager"])
    win.geometry("1100x600")
    win.configure(bg=global_bg)
    icon_images = {}
    win.icon_refs = []

    load_icons(win)

    try: win.iconphoto(False, ImageTk.PhotoImage(Image.open("icons/filemanager.png")))
    except Exception as e: log_to_file(f"Error: {e}",start_time_,level = 'error')

    notebook = ttk.Notebook(win)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    disk_c_tab = Frame(notebook, bg=global_bg)
    disk_d_tab = Frame(notebook, bg=global_bg)
    user_tab = Frame(notebook, bg=global_bg)

    notebook.add(disk_c_tab, text=lang["diskc"])
    notebook.add(disk_d_tab, text=lang["diskd"])
    notebook.add(user_tab, text=lang["user_f"])

    add_treeview(disk_c_tab, ".", False)
    add_treeview(disk_d_tab, "user_files", True)

    user_file_tools()
