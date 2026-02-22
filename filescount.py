def count_lines_in_files(files):
    total = 0
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = sum(1 for _ in f)
                print(f"{file}: {lines} строк")
                total += lines
        except Exception as e:
            print(f"Ошибка при чтении {file}: {e}")

    print(f"\nВсего строк: {total}")


base = r"D:\SVBEngine\Engine"
files_to_count = [
    base + r"\main.cpp",
    base + r"\MyOpenGLWidget.cpp",
    base + r"\MyOpenGLWidget.h",
    base + r"\GUI.cpp",
    base + r"\GUI.h",
    base + r"\Objects.h",
    base + r"\ObjectsAction.cpp",
    base + r"\ObjectsAction.h",
    base + r"\HUD.h",
    base + r"\HUD.cpp",
    base + r"\ImportExport.cpp",
    base + r"\ImportExport.h",
    base + r"\Logger.h",
    base + r"\Logger.cpp",
    base + r"\Camera.h",
    base + r"\Camera.cpp",

]

count_lines_in_files(files_to_count)
