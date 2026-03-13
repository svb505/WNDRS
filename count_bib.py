import os
import ast


def get_imports_from_file(file_path):
    imports = set()

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return imports

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def scan_project(allowed_dirs):
    all_imports = set()
    base = os.getcwd()

    # 1. файлы в корне проекта
    for file in os.listdir(base):
        if file.endswith(".py"):
            path = os.path.join(base, file)
            all_imports.update(get_imports_from_file(path))

    # 2. выбранные подпапки
    for directory in allowed_dirs:

        for root, dirs, files in os.walk(directory):

            for file in files:
                if file.endswith(".py"):

                    path = os.path.join(root, file)
                    all_imports.update(get_imports_from_file(path))

    return all_imports


if __name__ == "__main__":

    folders = [
        "utilitsCODE",
    ]

    libs = scan_project(folders)

    print("Используемые библиотеки:")
    for lib in sorted(libs):
        print(lib)