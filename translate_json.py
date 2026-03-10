import json
import time
import shutil
from deep_translator import GoogleTranslator

LANG_FILE = "syst_comp/lang.json"
BACKUP_FILE = "syst_comp/lang.json.bak"

LANG_KEYS = [
    "RU","EN","FR","UA","BY","DE","SRB","ALB","IT","PL","ES","CS","PT","BG","HU","TUR","RO","JP","CN"
]

LANG_CODE_MAP = {
    "RU": "ru",
    "EN": "en",
    "FR": "fr",
    "UA": "uk",
    "BY": "be",
    "DE": "de",
    "SRB": "sr",
    "ALB": "sq",
    "IT": "it",
    "PL": "pl",
    "ES": "es",
    "CS": "cs",
    "PT": "pt",
    "BG": "bg",
    "HU": "hu",
    "TUR": "tr",
    "RO": "ro",
    "JP": "ja",
    "CN": "zh-CN"
}

DELAY_BETWEEN_REQUESTS = 0.10

def load_lang_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def save_lang_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def ensure_language_keys(data):
    """Создаёт пустые словари для отсутствующих языков в data."""
    for key in LANG_KEYS:
        if key not in data:
            data[key] = {}
def is_string(v):
    return isinstance(v, str)
def translate_value(text, src_code, tgt_code, translator_cache):
    cache_key = (src_code, tgt_code)
    if cache_key not in translator_cache:
        translator_cache[cache_key] = GoogleTranslator(source=src_code, target=tgt_code)
    translator = translator_cache[cache_key]
    return translator.translate(text)
def merge_translate_recursive(src_obj, tgt_obj, src_code, tgt_code, translator_cache, path_prefix=""):
    added = 0
    for key, val in src_obj.items():
        path = f"{path_prefix}.{key}" if path_prefix else key
        if isinstance(val, dict):
            if key not in tgt_obj or not isinstance(tgt_obj[key], dict):
                tgt_obj[key] = {}
            added += merge_translate_recursive(val, tgt_obj[key], src_code, tgt_code, translator_cache, path)
        elif is_string(val):
            if key not in tgt_obj or not is_string(tgt_obj[key]) or tgt_obj[key] == "":
                try:
                    translated = translate_value(val, src_code, tgt_code, translator_cache)
                    tgt_obj[key] = translated
                    added += 1
                    print(f"  + {path}  -> добавлено для {tgt_code}")
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                except Exception as e:
                    print(f"  ! Ошибка при переводе ключа '{path}' ({src_code}->{tgt_code}): {e}")
        else:
            if key not in tgt_obj:
                tgt_obj[key] = val
                added += 1
                print(f"  + {path}  -> (скопировано нетекстовое значение)")
    return added
def main():
    print("Загрузка файла...")
    data = load_lang_file(LANG_FILE)

    print(f"Создаю резервную копию: {BACKUP_FILE}")
    shutil.copyfile(LANG_FILE, BACKUP_FILE)

    if "RU" not in data:
        print("ОШИБКА: В файле нет секции 'RU' — нужен эталон для переводов.")
        return

    ensure_language_keys(data)

    src_code = LANG_CODE_MAP.get("RU", "ru")
    translator_cache = {}

    total_added = 0
    for lang_key in LANG_KEYS:
        if lang_key == "RU": continue
        tgt_code = LANG_CODE_MAP.get(lang_key)
        if not tgt_code:
            print(f"Пропущен {lang_key}: нет соответствия коду языка для переводчика.")
            continue

        print(f"\nОбработка языка {lang_key} (код {tgt_code})...")
        added = merge_translate_recursive(data["RU"], data[lang_key], src_code, tgt_code, translator_cache)
        total_added += added
        print(f"Готово для {lang_key}: добавлено {added} ключ(ов).")

    save_lang_file(LANG_FILE, data)
    print(f"\n✅ Операция завершена. Всего добавлено ключей: {total_added}")
    print(f"Резервная копия сохранена как: {BACKUP_FILE}")
if __name__ == "__main__":
    main()
