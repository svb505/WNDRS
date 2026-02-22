import os
import ast

def find_unused_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code, filename=file_path)

    imports = {}
    used_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports[alias.asname or alias.name] = alias.name

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    unused = [imports[name] for name in imports if name not in used_names and imports[name] != '*']

    return unused


def main():
    py_files = [f for f in os.listdir(".") if f.endswith(".py")]
    found = False
    for file in py_files:
        unused = find_unused_imports(file)
        if unused:
            print(f"⚠️ В файле {file} не используются: {', '.join(unused)}")
            found = True

    if not found:
        print("✅ Все импорты используются")


if __name__ == "__main__":
    main()
