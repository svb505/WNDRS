import subprocess
import sys
import os
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

# --- Путь к JSON относительно родительской папки ---
json_path = os.path.join(BASE_DIR, "syst_comp", "lang.json")

cpp_files = ["loadfiles.cpp", "filelist.cpp"]
dll_file = "LoadFiles.dll"

result = subprocess.run(["g++", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode != 0:
    print("Ошибка: g++ не найден. Установи MinGW и добавь его в PATH.")
    sys.exit(1)

# Компилируем в DLL
cmd = [
    "g++", "-std=c++17", "-shared", "-o", dll_file, "-m64"
] + cpp_files + [
    "-Wl,--out-implib,libLoadFiles.a"
]

print("Компиляция:", " ".join(cmd))
subprocess.run(cmd, check=True)
print("Готово: DLL создана ->", dll_file)
input()
