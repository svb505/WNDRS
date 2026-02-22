import json

with open("changelogs/changelog_KW3.1.700.json","r", encoding="utf-8") as f:
    data = json.load(f)

# Извлекаем только тексты
ru_changes = data.get("RU", {}).get("changes", [])
texts = [item["text"] for item in ru_changes if "text" in item]

# Выводим построчно
for t in texts:
    print(f'<li>"{t}"</li>')
