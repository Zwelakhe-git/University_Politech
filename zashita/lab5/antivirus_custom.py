# antivirus.py
"""
Простейший файловый антивирус (hash-scan) на Python.

Порядок работы:
  1. Считаем SHA-256 исходных файлов  -> HashList.txt
  2. Запускаем FC (заражение/изменение файлов)
  3. Пересчитываем хеши ПОСЛЕ заражения
  4. Формируем VirusHashList.txt из ЗАРАЖЁННЫХ файлов (2.txt, 7.txt)
  5. Сравниваем: changed / infected
  6. Пишем отчёт -> report.txt
  7. Удаляем infected-файлы
"""
import hashlib
import os
import subprocess
import sys

WORK_DIR    = "test_dir"
HASH_LIST   = "HashList.txt"
VIRUS_LIST  = "VirusHashList.txt"
REPORT      = "report.txt"
BLOCK_SIZE  = 65536

VIRUS_INFECTED_NAMES = ("2.txt", "7.txt")


# ---------- Утилиты ----------
def compute_sha256(file_path: str) -> str:
    """Блочное вычисление SHA-256"""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def get_files(directory: str) -> list:
    """Список .txt-файлов в директории (отсортирован)."""
    return sorted(f for f in os.listdir(directory) if f.endswith(".txt"))


def write_hashes(files: list, directory: str, out_path: str) -> dict:
    """Считает хеши файлов и пишет их в out_path. Возвращает словарь {name: hash}."""
    hashes = {}
    with open(out_path, "w", encoding="utf-8") as out:
        for name in files:
            h = compute_sha256(os.path.join(directory, name))
            hashes[name] = h
            out.write(f"{name} - {h}\n")
    return hashes


def read_hashes(path: str) -> dict:
    """Читает файл формата 'name - hash' -> словарь {name: hash}."""
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if " - " in line:
                name, h = line.strip().split(" - ", 1)
                result[name] = h
    return result


# ---------- Основной сценарий ----------
def main() -> None:
    if not os.path.isdir(WORK_DIR):
        print(f"[!] Директория '{WORK_DIR}' не найдена. "
              f"Сначала запустите create_test_files.py")
        sys.exit(1)

    files = get_files(WORK_DIR)
    if not files:
        print(f"[!] В '{WORK_DIR}' нет .txt-файлов.")
        sys.exit(1)

    # --- Шаг 1. Исходные хеши ---
    print("[1] Вычисление исходных хешей...")
    origin = write_hashes(files, WORK_DIR, HASH_LIST)
    print(f"    -> {HASH_LIST}")

    # --- Шаг 2. Запуск «вируса» FC ---
    print("[2] Запуск FC (изменение / заражение файлов)...")
    subprocess.run([sys.executable, "FC.py"], check=True)

    # --- Шаг 3. Пересчёт хешей ПОСЛЕ заражения ---
    print("[3] Повторное вычисление хешей...")
    after = {name: compute_sha256(os.path.join(WORK_DIR, name)) for name in files}

    # --- VirusHashList.txt из ЗАРАЖЁННЫХ файлов ---
    print("[4] Формирование VirusHashList.txt из заражённых файлов...")
    with open(VIRUS_LIST, "w", encoding="utf-8") as out:
        for name in VIRUS_INFECTED_NAMES:
            if name in after:
                out.write(f"{name} - {after[name]}\n")
    print(f"    -> {VIRUS_LIST}")

    # --- Загрузка блек-листа ---
    virus_hashes = set(read_hashes(VIRUS_LIST).values())

    # --- Определяем changed / infected ---
    changed, infected = [], []
    for name in files:
        if origin.get(name) != after.get(name):       # файл изменился
            if after[name] in virus_hashes:           # и его хеш в блек-листе
                infected.append(name)
            else:
                changed.append(name)

    # --- Формируем report.txt ---
    print("[5] Формирование report.txt...")
    with open(REPORT, "w", encoding="utf-8") as rep:
        rep.write("Origin hash:\n")
        for name in files:
            rep.write(f"{name} - {origin[name]}\n")

        rep.write("\nChanged:\n")
        for name in changed:
            rep.write(f"{name} - {after[name]}\n")

        rep.write("\nInfected:\n")
        for name in infected:
            rep.write(f"{name} - {after[name]}\n")

    # --- Удаление заражённых файлов ---
    print("[6] Удаление заражённых файлов...")
    for name in infected:
        os.remove(os.path.join(WORK_DIR, name))
        print(f"    Удалён: {name}")

    # --- Итог ---
    print("\n=== ГОТОВО ===")
    print(f"Изменено (changed):  {len(changed)} -> {changed}")
    print(f"Заражено (infected): {len(infected)} -> {infected}")
    print(f"Отчёт: {REPORT}")


if __name__ == "__main__":
    main()