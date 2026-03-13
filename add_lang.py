import json
from deep_translator import GoogleTranslator


with open("syst_comp/lang.json", "r", encoding="utf-8") as f:
    data = json.load(f)

translator = GoogleTranslator(source="ru", target="ja")
count = 1

if "JP" not in data:
    data["JP"] = {}

for key, text in data.get("RU", {}).items():
    if key not in data["JP"]:
        try:
            print(f"{count})Перевожу: {key} -> {text}")
            translated = translator.translate(text)
            data["JP"][key] = translated
            count += 1
        except Exception as e:
            print(f"{count})Ошибка при переводе '{text}': {e}")
            count += 1

with open("syst_comp/lang.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ Перевод завершён!")
