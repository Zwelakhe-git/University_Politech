#!/usr/bin/env python3
# antivirus.py
"""
Простейший файловый антивирус (hash-scan) на Python.

Сценарий:
  1. Считаем SHA-256 файлов в Files/  ->  HashList.txt
  2. Запускаем Linux-утилиту ./FC ВНУТРИ Files/ (она интерактивно
     запрашивает номер варианта и изменяет часть файлов)
  3. Пересчитываем хеши
  4. Все файлы, чей хеш изменился, считаем «заражёнными»
     и записываем их новые хеши в VirusHashList.txt
  5. Формируем отчёт report.txt:
        Origin hash: <хеши до FC>
        Changed:     <изменившиеся, но не попавшие в блек-лист>
        Infected:    <изменившиеся и попавшие в блек-лист>
  6. Удаляем infected-файлы
"""
import argparse
import hashlib
import os
import subprocess
import sys

# ---------- Конфигурация ----------
WORK_DIR     = "Files"           # папка с тестовыми файлами
FC_BIN       = "./FC"            # Linux-утилита (относительно корня проекта)
HASH_LIST    = "HashList.txt"
VIRUS_LIST   = "VirusHashList.txt"
REPORT       = "report.txt"
BLOCK_SIZE   = 65536

DEFAULT_VARIANT = 13             # номер варианта в списке группы


# ---------- Утилиты ----------
def compute_sha256(file_path: str) -> str:
    """Блочное вычисление SHA-256 (подходит для больших файлов)."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def get_files(directory: str) -> list:
    """Список .txt-файлов в директории (натуральная сортировка)."""
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


def run_fc(variant: int, work_dir: str) -> None:
    """
    Запускает Linux-утилиту FC ВНУТРИ рабочей директории (work_dir),
    чтобы она изменяла файлы именно в Files/.

    Ключевые моменты:
      * используем АБСОЛЮТНЫЙ путь к бинарнику — иначе './FC'
        не найдётся, так как cwd мы меняем на Files/;
      * передаём номер варианта через stdin;
      * cwd=work_dir — FC ищет файлы в текущей директории.
    """
    fc_path = os.path.abspath(FC_BIN)

    if not os.path.exists(fc_path):
        print(f"[!] Утилита '{fc_path}' не найдена.")
        sys.exit(1)

    # Делаем исполняемой (на случай, если права сбиты)
    try:
        os.chmod(fc_path, 0o755)
    except OSError:
        pass

    print(f"[2] Запуск {FC_BIN} (вариант {variant}) в '{work_dir}' ...")

    result = subprocess.run(
        [fc_path],                       # абсолютный путь
        input=f"{variant}\n",            # ответ на «Выберите вариант...»
        capture_output=True,
        text=True,
        timeout=120,
        cwd=work_dir,                    # <-- FC работает внутри Files/
    )

    # Показываем вывод FC
    if result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            print(f"    [FC] {line}")
    if result.stderr.strip():
        for line in result.stderr.strip().splitlines():
            print(f"    [FC:err] {line}")

    if result.returncode != 0:
        print(f"[!] FC завершилась с кодом {result.returncode}")
        sys.exit(1)


# ---------- Основной сценарий ----------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Простейший файловый антивирус (hash-scan)."
    )
    parser.add_argument(
        "-v", "--variant", type=int, default=DEFAULT_VARIANT,
        help=f"Номер варианта в списке группы (1..25). По умолчанию {DEFAULT_VARIANT}."
    )
    parser.add_argument(
        "-d", "--dir", default=WORK_DIR,
        help=f"Папка с тестовыми файлами. По умолчанию '{WORK_DIR}'."
    )
    args = parser.parse_args()

    if not (1 <= args.variant <= 25):
        print(f"[!] Номер варианта должен быть в диапазоне 1..25, получено {args.variant}")
        sys.exit(1)

    work_dir = args.dir
    if not os.path.isdir(work_dir):
        print(f"[!] Папка '{work_dir}' не найдена.")
        sys.exit(1)

    files = get_files(work_dir)
    if not files:
        print(f"[!] В '{work_dir}' нет .txt-файлов.")
        sys.exit(1)

    print(f"[i] Рабочая папка: {work_dir}")
    print(f"[i] Вариант: {args.variant}")
    print(f"[i] Найдено файлов: {len(files)} -> {files}")

    # --- Шаг 1. Исходные хеши ---
    print("[1] Вычисление исходных хешей...")
    origin = write_hashes(files, work_dir, HASH_LIST)
    print(f"    -> {HASH_LIST}")

    # --- Шаг 2. Запуск FC (внутри work_dir) ---
    run_fc(args.variant, work_dir)

    # --- Шаг 3. Пересчёт хешей после FC ---
    print("[3] Пересчёт хешей после FC...")
    after = {name: compute_sha256(os.path.join(work_dir, name)) for name in files}

    # --- Шаг 4. Формируем VirusHashList.txt из ИЗМЕНИВШИХСЯ файлов ---
    print("[4] Формирование VirusHashList.txt из изменившихся файлов...")
    changed_names = [n for n in files if origin[n] != after[n]]

    with open(VIRUS_LIST, "w", encoding="utf-8") as out:
        for name in changed_names:
            out.write(f"{name} - {after[name]}\n")
    print(f"    Изменилось файлов: {len(changed_names)} -> {changed_names}")
    print(f"    -> {VIRUS_LIST}")

    # --- Шаг 5. Классификация ---
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
        os.remove(os.path.join(work_dir, name))
        print(f"    Удалён: {name}")

    # --- Итог ---
    print("\n=== ГОТОВО ===")
    print(f"Изменено (changed):  {len(changed)} -> {changed}")
    print(f"Заражено (infected): {len(infected)} -> {infected}")
    print(f"Отчёт: {REPORT}")


if __name__ == "__main__":
    main()