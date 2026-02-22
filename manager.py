from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # Для загрузки иконок
import os
import subprocess
import platform
import pyperclip  # pip install pyperclip

def disk_d():
    def get_folder_size(folder):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def populate_tree(parent, path):
        try:
            items = os.listdir(path)
            full_items = [(item, os.path.join(path, item)) for item in items]

            full_items.sort(key=lambda x: (
                0 if os.path.isdir(x[1]) else 1,
                os.path.splitext(x[0])[1].lower() if not os.path.isdir(x[1]) else '',  # Расширение
                x[0].lower()  # Имя
            ))

            for item, item_path in full_items:
                is_dir = os.path.isdir(item_path)
                ext = os.path.splitext(item)[1].lower()

                if is_dir:
                    node = tree.insert(parent, "end", text=item, image=icons["folder"],
                                       values=("folder", ""), open=False)
                    tree.insert(node, "end")
                else:
                    size_bytes = os.path.getsize(item_path)
                    size_mb = size_bytes / (1024 * 1024)

                    ext_icon_map = {
                        ".txt": "txt",
                        ".png": "image", ".jpg": "image", ".jpeg": "image",
                        ".py": "py",
                        ".cfg": "cfg",
                        ".db": "db",
                        ".cpp": "cpp",
                        ".exe": "exe",
                        ".bin": "bin",
                        ".json": "json",
                        ".log": "log",
                        ".html": "html",
                        ".zip": "zip",
                        ".bat": "bat",
                        ".mp3": "mp3",
                        ".mp4": "mp4",
                        ".xml": "xml",
                        ".docx": "docx",
                        ".csv": "csv",
                        ".xls": "xls",
                        ".dll": "dll",
                        ".odt": "odt",
                        ".css": "css",
                        ".c": "c",
                        ".cs": "cs",
                        ".js": "js",
                        ".rar": "rar",
                        ".wav": "wav",
                        ".pdb": "pdb",
                        ".pdf": "pdf",
                        ".tga": "tga",
                        ".gif": "gif",
                        ".php": "php",
                        ".yaml": "yaml",
                        ".ppt": "ppt",
                        ".ttf": "ttf",
                        ".sys": "sys",
                        ".jar": "jar",
                        ".msi": "msi"
                    }
                    size_bytes = os.path.getsize(item_path)
                    size_mb = size_bytes / (1024 * 1024)

                    icon_name = ext_icon_map.get(ext, "default")
                    icon = icons.get(icon_name, icons["default"])

                    tree.insert(parent, "end", text=item, image=icon,
                                values=(ext or "—", f"{size_mb:.2f} MB"))

        except PermissionError:
            pass
    def on_open_node(event):
        node = tree.focus()
        path = get_full_path(node)

        if tree.get_children(node):
            first_child = tree.get_children(node)[0]
            if tree.item(first_child, "text") == "":
                tree.delete(first_child)
                populate_tree(node, path)
    def get_full_path(node):
        path_parts = []
        while node != "":
            path_parts.insert(0, tree.item(node, "text"))
            node = tree.parent(node)
        return os.path.join(*path_parts) if path_parts else "."

    viewer = Tk()
    viewer.title("SVB Storage Viewer 1.3.440")
    viewer.geometry("1900x900")
    viewer.attributes('-alpha', True)
    viewer.state('zoomed')
    viewer.resizable(True, True)
    image = Image.open("icons/svbfilemanager.png")
    icon_image = ImageTk.PhotoImage(image)
    viewer.icon_img_ref = icon_image
    viewer.iconphoto(True,viewer.icon_img_ref)
    style = ttk.Style()
    style.configure("Treeview", rowheight=40)

    # Загрузка иконок
    def load_icon(filename, size=(34, 34)):
        img = Image.open(filename).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    icons = {
        "folder": load_icon("icons/file_icons/folder.png"),
        "txt": load_icon("icons/file_icons/txt.png"),
        "image": load_icon("icons/file_icons/image.png"),
        "py": load_icon("icons/file_icons/py.png"),
        "cpp": load_icon("icons/file_icons/cpp.png"),
        "db":load_icon("icons/file_icons/sql.png"),
        "cfg": load_icon("icons/file_icons/cfg.png"),
        "json": load_icon("icons/file_icons/json.png"),
        "exe": load_icon("icons/file_icons/exe.png"),
        "bin": load_icon("icons/file_icons/bin.png"),
        "log": load_icon("icons/file_icons/log.png"),
        "html": load_icon("icons/file_icons/html.png"),
        "zip": load_icon("icons/file_icons/zip.png"),
        "bat": load_icon("icons/file_icons/bat.png"),
        "mp3": load_icon("icons/file_icons/mp3.png"),
        "mp4": load_icon("icons/file_icons/mp4.png"),
        "xml": load_icon("icons/file_icons/xml.png"),
        "docx": load_icon("icons/file_icons/docx.png"),
        "default": load_icon("icons/file_icons/file.png"),
        "c": load_icon("icons/file_icons/c.png"),
        "cs": load_icon("icons/file_icons/cs.png"),
        "js": load_icon("icons/file_icons/js.png"),
        "rar": load_icon("icons/file_icons/rar.png"),
        "wav": load_icon("icons/file_icons/wav.png"),
        "xls": load_icon("icons/file_icons/xls.png"),
        "csv": load_icon("icons/file_icons/csv.png"),
        "odt": load_icon("icons/file_icons/odt.png"),
        "css": load_icon("icons/file_icons/css.png"),
        "dll": load_icon("icons/file_icons/dll.png"),
        "yaml": load_icon("icons/file_icons/yaml.png"),
        "ppt": load_icon("icons/file_icons/ppt.png"),
        "sys": load_icon("icons/file_icons/sys.png"),
        "php": load_icon("icons/file_icons/php.png"),
        "ttf": load_icon("icons/file_icons/ttf.png"),
        "msi": load_icon("icons/file_icons/msi.png"),
        "jar": load_icon("icons/file_icons/jar.png"),
        "pdf": load_icon("icons/file_icons/pdf.png"),
        "tga": load_icon("icons/file_icons/tga.png"),
        "gif": load_icon("icons/file_icons/gif.png"),
        "pdb": load_icon("icons/file_icons/pdb.png"),

    }

    container = Frame(viewer)
    container.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(container)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(container, columns=("Type", "Size"), yscrollcommand=scrollbar.set)
    tree.heading("#0", text="Name", anchor="w")
    tree.heading("Type", text="Type")
    tree.heading("Size", text="Size")

    tree.column("#0", width=300)
    tree.column("Type", width=50, anchor="center")
    tree.column("Size", width=50, anchor="center")
    tree.pack(fill=BOTH, expand=True, side=LEFT)

    scrollbar.config(command=tree.yview)

    tree.bind("<<TreeviewOpen>>", on_open_node)

    def show_context_menu(event):
        node = tree.identify_row(event.y)
        if node:
            tree.selection_set(node)
            tree.focus(node)
            context_menu.tk_popup(event.x_root, event.y_root)
        else:
            tree.selection_remove(tree.focus())

    def open_selected_path():
        node = tree.focus()
        if node:
            path = get_full_path(node)
            try:
                if os.path.isdir(path):
                    os.startfile(path) if platform.system() == "Windows" else subprocess.call(["xdg-open", path])
                else:
                    os.startfile(path) if platform.system() == "Windows" else subprocess.call(["xdg-open", path])
            except Exception as e:
                pass
    def copy_selected_path():
        node = tree.focus()
        if node:
            path = get_full_path(node)
            pyperclip.copy(path)

    # Контекстное меню
    context_menu = Menu(viewer, tearoff=0)
    context_menu.add_command(label="Открыть", command=open_selected_path)
    context_menu.add_command(label="Копировать путь", command=copy_selected_path)

    tree.bind("<Button-3>", show_context_menu)

    populate_tree("", ".")

    viewer.mainloop()

disk_d()
