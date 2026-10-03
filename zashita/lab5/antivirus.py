#!/usr/bin/env python3
# antivirus.py
"""
Простейший файловый антивирус (hash-scan) на Python.

Сценарий:
  1. Считаем SHA-256 файлов в Files/  ->  HashList.txt
  2. Запускаем Linux-утилиту ./FC (она изменяет часть файлов)
  3. Пересчитываем хеши
  4. Все файлы, чей хеш изменился, считаем «заражёнными»
     и записываем их новые хеши в VirusHashList.txt
  5. Формируем отчёт report.txt:
        Origin hash: <хеши до FC>
        Changed:     <изменившиеся, но не попавшие в блек-лист>
        Infected:    <изменившиеся и попавшие в блек-лист>
  6. Удаляем infected-файлы
"""
import hashlib
import os
import subprocess
import sys

# ---------- Конфигурация ----------
WORK_DIR     = "Files"          # папка с тестовыми файлами
FC_BIN       = "./FC"           # Linux-утилита, изменяющая файлы
HASH_LIST    = "HashList.txt"
VIRUS_LIST   = "VirusHashList.txt"
REPORT       = "report.txt"
BLOCK_SIZE   = 65536


# ---------- Утилиты ----------
def compute_sha256(file_path: str) -> str:
    """Блочное вычисление SHA-256 (для больших файлов)."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def get_files(directory: str) -> list:
    """Список .txt-файлов в директории (отсортирован по имени)."""
    def sort_key(name):
        base = os.path.splitext(name)[0]
        return (0, int(base)) if base.isdigit() else (1, base)

    return sorted(
        (f for f in os.listdir(directory) if f.endswith(".txt")),
        key=sort_key,
    )


def write_hashes(files: list, directory: str, out_path: str) -> dict:
    """Считает хеши и пишет их в out_path. Возвращает {name: hash}."""
    hashes = {}
    with open(out_path, "w", encoding="utf-8") as out:
        for name in files:
            h = compute_sha256(os.path.join(directory, name))
            hashes[name] = h
            out.write(f"{name} - {h}\n")
    return hashes


def read_hashes(path: str) -> dict:
    """Читает 'name - hash' -> {name: hash}."""
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if " - " in line:
                name, h = line.strip().split(" - ", 1)
                result[name] = h
    return result


def run_fc() -> None:
    """Запускает Linux-утилиту FC в текущей директории (там, где Files/)."""
    if not os.path.exists(FC_BIN):
        print(f"[!] Утилита '{FC_BIN}' не найдена.")
        sys.exit(1)

    # Делаем исполняемой (на случай, если права сбиты)
    try:
        os.chmod(FC_BIN, 0o755)
    except OSError:
        pass

    print(f"[2] Запуск утилиты {FC_BIN} ...")
    result = subprocess.run([FC_BIN], capture_output=True, text=True)

    if result.stdout.strip():
        print("    FC stdout:", result.stdout.strip())
    if result.stderr.strip():
        print("    FC stderr:", result.stderr.strip())
    if result.returncode != 0:
        print(f"[!] FC завершилась с кодом {result.returncode}")


# ---------- Основной сценарий ----------
def main() -> None:
    if not os.path.isdir(WORK_DIR):
        print(f"[!] Папка '{WORK_DIR}' не найдена. "
              f"Поместите туда файлы 1.txt ... 10.txt.")
        sys.exit(1)

    files = get_files(WORK_DIR)
    if not files:
        print(f"[!] В '{WORK_DIR}' нет .txt-файлов.")
        sys.exit(1)

    print(f"[i] Найдено файлов: {len(files)} -> {files}")

    # --- Шаг 1. Исходные хеши ---
    print("[1] Вычисление исходных хешей...")
    origin = write_hashes(files, WORK_DIR, HASH_LIST)
    print(f"    -> {HASH_LIST}")

    # --- Шаг 2. Запуск FC (Linux-утилита) ---
    run_fc()

    # --- Шаг 3. Пересчёт хешей после FC ---
    print("[3] Пересчёт хешей после FC...")
    after = {name: compute_sha256(os.path.join(WORK_DIR, name)) for name in files}

    # --- Шаг 4. Формируем VirusHashList.txt из ИЗМЕНИВШИХСЯ файлов ---
    #     Мы не знаем заранее, что меняет FC, поэтому все изменения
    #     трактуем как потенциальное заражение.
    print("[4] Формирование VirusHashList.txt из изменившихся файлов...")
    changed_names = [n for n in files if origin[n] != after[n]]

    with open(VIRUS_LIST, "w", encoding="utf-8") as out:
        for name in changed_names:
            out.write(f"{name} - {after[name]}\n")
    print(f"    Изменилось файлов: {len(changed_names)} -> {changed_names}")
    print(f"    -> {VIRUS_LIST}")

    # --- Шаг 5. Классификация ---
    #     infected = изменился И его новый хеш есть в блек-листе
    #     changed  = изменился, но в блек-лист не попал
    #
    #     В нашем сценарии все изменившиеся файлы автоматически
    #     попадают в блек-лист, поэтому все они будут «infected».
    #     Это корректно для учебной задачи: FC = «вирус», изменённые файлы = «заражённые».
    virus_hashes = set(read_hashes(VIRUS_LIST).values())

    changed, infected = [], []
    for name in files:
        if origin[name] != after[name]:
            if after[name] in virus_hashes:
                infected.append(name)
            else:
                changed.append(name)

    # --- Шаг 6. Отчёт ---
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

    # --- Шаг 7. Удаление infected ---
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