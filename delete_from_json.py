import json

FILE_PATH = "syst_comp/lang.json"  # путь к файлу
KEY_TO_DELETE = "ent-name"           # ключ, который нужно удалить

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

for lang, values in data.items():
    if lang == "RU":
        continue
    if isinstance(values, dict) and KEY_TO_DELETE in values:
        del values[KEY_TO_DELETE]
        print(f"Удалён ключ '{KEY_TO_DELETE}' из {lang}")

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Готово.")
