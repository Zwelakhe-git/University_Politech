# FC.py
"""
Тестовая программа 'FC', которая имитирует заражение файлов:
- меняет содержимое некоторых файлов (changed)
- делает содержимое некоторых файлов идентичным вирусной сигнатуре (infected)
"""
import os

VIRUS_PAYLOAD = "MALWARE_SIGNATURE_XYZ"  # «вирусная» строка

def infect(directory="test_dir"):
    files = sorted([f for f in os.listdir(directory) if f.endswith(".txt")])
    # 1.txt, 3.txt, 5.txt — просто изменим (changed)
    for name in ["1.txt", "3.txt", "5.txt"]:
        path = os.path.join(directory, name)
        with open(path, "a", encoding="utf-8") as f:
            f.write("  <-- изменено\n")
    # 2.txt, 7.txt — «заразим» вирусной сигнатурой (infected)
    for name in ["2.txt", "7.txt"]:
        path = os.path.join(directory, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(VIRUS_PAYLOAD)
    print("FC: файлы изменены.")

if __name__ == "__main__":
    infect()
