import sys
import subprocess
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

extra_files = []

def select_script():
    file_path = filedialog.askopenfilename(title="Выберите Python скрипт", filetypes=[("Файлы Python", "*.py")])
    if file_path:
        entry_script.delete(0, tk.END)
        entry_script.insert(0, file_path)
def select_image():
    file_path = filedialog.askopenfilename(title="Выберите изображение", filetypes=[("Файлы изображений", "*.png;*.jpg;*.jpeg;*.ico")])
    if file_path:
        entry_image.delete(0, tk.END)
        entry_image.insert(0, file_path)
        try:
            load_image_preview(file_path)
        except Exception:
            image_preview_label.config(image='')
def load_image_preview(file_path):
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    img = ImageTk.PhotoImage(image)
    image_preview_label.config(image=img)
    image_preview_label.image = img
def toggle_icon_checkbox():
    state = "normal" if checkbox_icon.get() else "disabled"
    entry_image.config(state=state)
    button_browse_image.config(state=state)
    if state == "normal":
        try:
            load_image_preview(entry_image.get())
        except Exception:
            image_preview_label.config(image='')
            image_preview_label.image = None
    else:
        image_preview_label.config(image='')
        image_preview_label.image = None
def add_extra_file():
    file_path = filedialog.askopenfilename(title="Выберите файл для включения в exe")
    if file_path:
        extra_files.append(file_path)
        listbox_files.insert(tk.END, file_path)
def remove_extra_file():
    selection = listbox_files.curselection()
    if selection:
        index = selection[0]
        extra_files.pop(index)
        listbox_files.delete(index)
def append_log(message):
    text_log.config(state="normal")
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)
    text_log.config(state="disabled")
def generate_exe_thread():
    try:
        script_path = entry_script.get().strip()
        icon_path = entry_image.get().strip() if checkbox_icon.get() else None
        output_name = entry_output.get().strip()

        if not os.path.isfile(script_path):
            messagebox.showerror("Ошибка", f"Файл скрипта '{script_path}' не существует.")
            return
        if checkbox_icon.get() and not os.path.isfile(icon_path):
            messagebox.showerror("Ошибка", f"Файл изображения '{icon_path}' не существует.")
            return
        if not output_name:
            messagebox.showerror("Ошибка", "Введите имя для .exe файла.")
            return

        script_dir = os.path.dirname(os.path.abspath(script_path))
        utilits_path = os.path.join(script_dir, "utilits")

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--noconfirm",
            "--clean",
            "--distpath", os.path.join(script_dir, "dist"),
            "--workpath", os.path.join(script_dir, "build"),
            "--add-binary", "D:\\programar\\WNDRS\\DLLs;DLLs",
            "--add-data", r"D:\programar\WNDRS\.venv2\Lib\site-packages\country_list\country_data\data;country_list/country_data/data",
            "--add-data","icons;icons",
            "--add-data","games;games",
            # путь чтобы PyInstaller видел пакет
            "--paths", script_dir,
            "--hidden-import=tkhtmlview",
            "--hidden-import=send_email_template",
            "--hidden-import=pytubefix",
            "--hidden-import=pyttsx3",
            "--hidden-import=games",
            "--hidden-import=crypto_work",
            "--hidden-import=plyer",
            "--hidden-import=play_sound",
            "--hidden-import=tabulate",
            "--hidden-import=pygame",
            "--hidden-import=OpenGL",
            "--hidden-import=pygame.locals",
            "--hidden-import=OpenGL.GL",
            "--hidden-import=OpenGL.GLU",
            "--hidden-import=supabase",
            "--hidden-import=piexif",
            "--hidden-import=dropbox",
            "--hidden-import=country_list",
            # добавить саму папку utilits
            "--add-data", f"{utilits_path};utilits",

            script_path
        ]
        # Консоль
        cmd.append("--console" if checkbox_console.get() else "--noconsole")

        # Иконка
        if checkbox_icon.get():
            cmd.extend([f"--icon={icon_path}", f"--name={output_name}"])
        else:
            cmd.append(f"--name={output_name}")

        # Доп. файлы
        for f in extra_files:
            if os.path.isfile(f):
                path = f.replace("\\", "/")
                cmd.extend(["--add-data", f"{path};."])
            elif os.path.isdir(f):
                path = f.replace("\\", "/")
                cmd.extend(["--add-data", f"{path};{os.path.basename(f)}"])

        append_log("⚙ Выполняется команда:")
        append_log(" ".join(cmd))
        append_log("📤 Вывод:")

        env = os.environ.copy()

        utilits_path = os.path.join(script_dir, "utilits")

        if "PYTHONPATH" in env:
            env["PYTHONPATH"] += os.pathsep + utilits_path
        else:
            env["PYTHONPATH"] = utilits_path

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            env=env
        )

        for line in iter(process.stdout.readline, ''):
            if line:
                append_log(line.strip())

        process.stdout.close()
        process.wait()

        # Очистка
        spec_file = os.path.join(script_dir, output_name + ".spec")
        build_dir = os.path.join(script_dir, "build")
        if os.path.exists(spec_file):
            os.remove(spec_file)
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        if process.returncode != 0:
            messagebox.showerror("Ошибка", "Произошла ошибка при создании exe файла. См. лог.")
            return

        exe_name = os.path.join(script_dir, output_name + ".exe")
        messagebox.showinfo("Готово", f"Исполняемый файл создан: {exe_name}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при создании exe файла: {e}")
def generate_exe():
    threading.Thread(target=generate_exe_thread, daemon=True).start()

root = tk.Tk()
root.geometry("700x700")
root.title("Генератор EXE файлов с опциями")

style = ttk.Style()
style.theme_use('clam')

# Выбор скрипта
frame_select = ttk.Frame(root, padding=10)
frame_select.pack(fill=tk.X)
ttk.Label(frame_select, text="Выберите Python скрипт:").grid(row=0, column=0, sticky=tk.W)
entry_script = ttk.Entry(frame_select, width=50)
entry_script.insert(0,"D:/programar/WNDRS/my_os.py")
entry_script.grid(row=0, column=1, padx=5)
ttk.Button(frame_select, text="Обзор...", command=select_script).grid(row=0, column=2, padx=5)

# Опции
frame_options = ttk.Labelframe(root, text="Опции", padding=10)
frame_options.pack(fill="both", expand=True, padx=10, pady=5)
checkbox_console = tk.BooleanVar(value=False)
checkbox_icon = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_options,
                text="Консольное окно (для консольных приложений)",
                variable=checkbox_console).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ttk.Checkbutton(frame_options, text="Использовать иконку", variable=checkbox_icon,
                command=toggle_icon_checkbox).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# Иконка
frame_image = ttk.Frame(root, padding=10)
frame_image.pack(fill=tk.X)
ttk.Label(frame_image, text="Выберите иконку (PNG/ICO):").grid(row=0, column=0, sticky=tk.W)
entry_image = ttk.Entry(frame_image, width=50)
entry_image.insert(0,"D:/programar/WNDRS/icons/WinDoors52-ICON.png")
entry_image.grid(row=0, column=1, padx=5)

button_browse_image = ttk.Button(frame_image, text="Обзор...", command=select_image)
button_browse_image.grid(row=0, column=2, padx=5)
image_preview_label = ttk.Label(frame_image)
image_preview_label.grid(row=1, column=0, columnspan=3, pady=10)

# Доп. файлы
frame_files = ttk.Labelframe(root, text="Дополнительные файлы", padding=10)
frame_files.pack(fill="both", expand=True, padx=10, pady=5)
listbox_files = tk.Listbox(frame_files, height=5)
listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_files = ttk.Scrollbar(frame_files, orient="vertical", command=listbox_files.yview)
scroll_files.pack(side=tk.RIGHT, fill=tk.Y)
listbox_files.config(yscrollcommand=scroll_files.set)
frame_files_buttons = ttk.Frame(root, padding=5)
frame_files_buttons.pack(fill=tk.X)
ttk.Button(frame_files_buttons, text="Добавить файл", command=add_extra_file).pack(side=tk.LEFT, padx=5)
ttk.Button(frame_files_buttons, text="Удалить выбранный", command=remove_extra_file).pack(side=tk.LEFT, padx=5)

# Имя exe
frame_output = ttk.Frame(root, padding=10)
frame_output.pack(fill=tk.X)
ttk.Label(frame_output, text="Введите имя для .exe файла:").grid(row=0, column=0, sticky=tk.W)
entry_output = ttk.Entry(frame_output, width=50)
entry_output.grid(row=0, column=1, padx=5)

# Кнопка генерации
ttk.Button(root, text="Создать .exe файл", command=generate_exe).pack(pady=10)

# Лог сборки
frame_log = ttk.Frame(root, padding=10)
frame_log.pack(fill=tk.BOTH, expand=True)
ttk.Label(frame_log, text="Лог сборки:").pack(anchor='w')
log_container = ttk.Frame(frame_log)
log_container.pack(fill=tk.BOTH, expand=True)
text_log = tk.Text(log_container, height=15, wrap="word", state="disabled")
text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_log = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=text_log.yview)
scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
text_log.config(yscrollcommand=scroll_log.set)

root.mainloop()