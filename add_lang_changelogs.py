import json
import os
import time
from deep_translator import GoogleTranslator
from http.client import RemoteDisconnected
from requests.exceptions import RequestException

# Папка с JSON-файлами
folder_path = "changelogs"

# Языки для перевода
lang_map = {
    "EN": "en",
    "FR": "fr",
    "UA": "uk",
    "IT": "it",
    "ES": "es",
    "DE": "de",
    "PT": "pt",
    "PL": "pl",
    "ALB": "sq",
    "SRB": "sr",
    "BY": "be",
    "TUR": "tr",
    "BG": "bg",
    "HU": "hu",
    "RO": "ro",
    "CN": "zh-CN",
    "CS": "cs",
    "JP": "ja"
}

source_lang = "RU"  # язык, с которого переводим
MAX_CHUNK = 5000  # максимальная длина текста для перевода
DELAY = 0.3  # задержка между переводами


def translate_text_safe(translator, text, max_len=MAX_CHUNK, delay=DELAY):
    """Разбиваем текст на куски <= max_len и добавляем задержку после каждого."""
    if len(text) <= max_len:
        time.sleep(delay)
        return translator.translate(text)

    translated_parts = []
    start = 0
    while start < len(text):
        chunk = text[start:start + max_len]
        translated_parts.append(translator.translate(chunk))
        start += max_len
        time.sleep(delay)
    return "".join(translated_parts)


def translate_with_retry(translator, text, retries=3, delay=DELAY):
    """Безопасный перевод с повторными попытками и задержкой."""
    for attempt in range(retries):
        try:
            return translate_text_safe(translator, text, delay=delay)
        except (RemoteDisconnected, RequestException) as e:
            print(f"⚠ Попытка {attempt + 1} не удалась: {e}")
            time.sleep(1)
    print("❌ Не удалось перевести текст после нескольких попыток, верну оригинал")
    return text


def translate_entry(entry, translator, delay=DELAY):
    """Рекурсивный перевод всех текстовых полей внутри словаря или списка."""
    if isinstance(entry, str):
        return translate_with_retry(translator, entry, delay=delay)
    elif isinstance(entry, list):
        return [translate_entry(e, translator, delay=delay) for e in entry]
    elif isinstance(entry, dict):
        new_dict = {}
        for k, v in entry.items():
            if k == "text":  # переводим только текстовые поля
                new_dict[k] = translate_with_retry(translator, v, delay=delay)
            else:
                new_dict[k] = translate_entry(v, translator, delay=delay)
        return new_dict
    else:
        return entry


# Проходим по всем JSON-файлам в папке
for filename in os.listdir(folder_path):
    if filename.endswith(".json") and filename != "changelog_KW1.6.500.json":
        file_path = os.path.join(folder_path, filename)
        print(f"\n🔹 Обрабатываем файл: {filename}")

        # Загружаем данные
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 1
        # Переводим с RU на все остальные языки
        for target_lang_key, target_lang_code in lang_map.items():
            if target_lang_key == source_lang:
                continue

            if target_lang_key not in data:
                data[target_lang_key] = {}

            translator = GoogleTranslator(source="ru", target=target_lang_code)

            for key, value in data.get(source_lang, {}).items():
                if key not in data[target_lang_key]:
                    try:
                        print(f"{count}) {source_lang}->{target_lang_key}: {key}")
                        data[target_lang_key][key] = translate_entry(value, translator)
                        count += 1
                    except Exception as e:
                        print(f"{count}) Ошибка при переводе '{key}': {e}")
                        count += 1

        # Сохраняем результат
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

print("\n✅ Все переводы завершены!")
