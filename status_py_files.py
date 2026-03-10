import os
import ast

KEYWORDS = ["import", "log_to_file"]


def analyze_file(filepath):
    stats = {
        "lines": 0,
        "functions": 0,
        "comments": 0,
        "keywords": {kw: 0 for kw in KEYWORDS},
    }

    try:
        with open(filepath, 'r', encoding='utf-8',errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Ошибка при чтении {filepath}: {e}")
        return stats

    stats["lines"] = content.count('\n') + 1
    stats["comments"] = sum(1 for line in content.splitlines() if line.strip().startswith('#'))

    # Разбор функций только для Python
    if filepath.endswith(".py"):
        try:
            tree = ast.parse(content)
            stats["functions"] = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
        except Exception as e:
            print(f"Ошибка при парсинге AST в {filepath}: {e}")

    for kw in KEYWORDS:
        stats["keywords"][kw] = content.count(kw)

    return stats


def analyze_directory(directory):
    total = {
        "lines": 0,
        "functions": 0,
        "comments": 0,
        "keywords": {kw: 0 for kw in KEYWORDS},
    }

    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.path.isfile(filepath) and file.endswith(".py") or file.endswith(".cpp") or file.endswith(".h"):
            file_stats = analyze_file(filepath)

            total["lines"] += file_stats["lines"]
            total["functions"] += file_stats["functions"]
            total["comments"] += file_stats["comments"]
            for kw in KEYWORDS:
                total["keywords"][kw] += file_stats["keywords"][kw]

    return total


if __name__ == "__main__":
    paths = [os.getcwd(), "utilitsCODE","D:/OpenGL_EDU/tank/tank","D:/OpenGL_EDU/fpvdrone/fpvdrone",
             "D:/OpenGL_EDU/checkers/checkers","D:\Qt_EDU\Console_ex\ValidateImgHashe\ValidateImgHashe"]
    print(f"Анализируем директории: {paths}\n")

    total_stats = {
        "lines": 0,
        "functions": 0,
        "comments": 0,
        "keywords": {kw: 0 for kw in KEYWORDS},
    }

    for p in paths:
        stats = analyze_directory(p)
        total_stats["lines"] += stats["lines"]
        total_stats["functions"] += stats["functions"]
        total_stats["comments"] += stats["comments"]
        for kw in KEYWORDS:
            total_stats["keywords"][kw] += stats["keywords"][kw]

    print("\n--- Итоговые результаты анализа ---")
    print(f"Общее количество строк: {total_stats['lines']}")
    print(f"Количество функций: {total_stats['functions']}")
    print(f"Количество комментариев: {total_stats['comments']}")
    print("Упоминания ключевых слов:")
    for kw, count in total_stats["keywords"].items():
        print(f"  {kw}: {count}")
