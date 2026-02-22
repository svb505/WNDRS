import hashlib
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

base_folder = Path("icons")
hashes_list = []

for f in base_folder.rglob("*"):  # рекурсивно ищем файлы
    if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        # относительный путь
        rel_path = str(f.relative_to(base_folder))
        h = sha256(f)
        hashes_list.append(f"{rel_path}:{h}")

# превращаем в строку для DLL
hashes_str = ";".join(hashes_list)
print(hashes_str)
