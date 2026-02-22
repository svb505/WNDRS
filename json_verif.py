import json

def compare_keys(filename, base_lang="RU"):
    # Загружаем JSON
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    base_dict = data.get(base_lang, {})
    base_keys = set(base_dict.keys())
    for lang, translations in data.items():
        if lang == base_lang:
            continue

        current_keys = set(translations.keys())

        # Какие ключи отсутствуют в текущем языке
        missing_in_lang = base_keys - current_keys
        for key in missing_in_lang:
            print(f'В {lang} не хватает: {key} ["{key}": "{base_dict[key]}"]')

        # Какие ключи есть лишние (не в RU)
        extra_in_lang = current_keys - base_keys
        for key in extra_in_lang:
            print(f'В {lang} есть лишний ключ: {key} ["{key}": "{translations[key]}"]')


if __name__ == "__main__":
    compare_keys("syst_comp/lang.json", base_lang="RU")
