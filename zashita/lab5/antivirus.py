# antivirus.py
import hashlib
import os
import subprocess
import sys

WORK_DIR = "test_dir"
HASH_LIST = "HashList.txt"
VIRUS_LIST = "VirusHashList.txt"
REPORT = "report.txt"
BLOCK_SIZE = 65536


def compute_sha256(file_path: str) -> str:
    """Вычисление SHA-256 хеша файла (блочно, для больших файлов)."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def get_files(directory: str):
    """Возвращает отсортированный список файлов .txt в директории."""
    return sorted(f for f in os.listdir(directory) if f.endswith(".txt"))


def write_hashes(files, directory, out_path):
    """Записывает хеши файлов в out_path."""
    with open(out_path, "w", encoding="utf-8") as out:
        for name in files:
            h = compute_sha256(os.path.join(directory, name))
            out.write(f"{name} - {h}\n")


def read_hashes(path: str) -> dict:
    """Читает файл 'name - hash' и возвращает словарь."""
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if " - " in line:
                name, h = line.strip().split(" - ", 1)
                result[name] = h
    return result


def make_virus_hash_list(directory: str, virus_names=("2.txt", "7.txt")):
    """Создаёт словарь VirusHashList.txt на основе «заражённых» файлов."""
    with open(VIRUS_LIST, "w", encoding="utf-8") as out:
        for name in virus_names:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                out.write(f"{name} - {compute_sha256(path)}\n")


def main():
    if not os.path.isdir(WORK_DIR):
        print(f"Директория {WORK_DIR} не найдена. Запустите create_test_files.py")
        sys.exit(1)

    files = get_files(WORK_DIR)

    # --- Шаг 1. Исходные хеши ---
    print("[1] Вычисление исходных хешей...")
    origin = {}
    with open(HASH_LIST, "w", encoding="utf-8") as out:
        for name in files:
            h = compute_sha256(os.path.join(WORK_DIR, name))
            origin[name] = h
            out.write(f"{name} - {h}\n")
    print(f"    Сохранено в {HASH_LIST}")

    # --- Шаг 2. Формируем словарь вирусов (для демонстрации) ---
    # В реальности VirusHashList.txt уже существует.
    print("[2] Формирование VirusHashList.txt (демо)...")
    make_virus_hash_list(WORK_DIR)

    # --- Шаг 3. Запуск «вируса» FC ---
    print("[3] Запуск FC (изменение файлов)...")
    subprocess.run([sys.executable, "FC.py"], check=True)

    # --- Шаг 4. Пересчёт хешей после изменений ---
    print("[4] Повторное вычисление хешей...")
    after = {}
    for name in files:
        after[name] = compute_sha256(os.path.join(WORK_DIR, name))

    # --- Шаг 5. Загрузка чёрного списка ---
    virus_hashes = set(read_hashes(VIRUS_LIST).values())

    # --- Шаг 6. Определение changed / infected ---
    changed, infected = [], []
    for name in files:
        if origin.get(name) != after.get(name):
            if after[name] in virus_hashes:
                infected.append(name)
            else:
                changed.append(name)

    # --- Шаг 7. Формирование отчёта ---
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

    # --- Шаг 8. Удаление заражённых файлов ---
    print("[6] Удаление заражённых файлов...")
    for name in infected:
        os.remove(os.path.join(WORK_DIR, name))
        print(f"    Удалён: {name}")

    print("\nГотово! Смотрите report.txt")


if __name__ == "__main__":
    main()
