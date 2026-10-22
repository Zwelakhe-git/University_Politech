# create_test_files.py
import os

os.makedirs("test_dir", exist_ok=True)
for i in range(1, 11):
    with open(f"test_dir/{i}.txt", "w", encoding="utf-8") as f:
        f.write(f"Содержимое файла номер {i}\n")
print("Тестовые файлы созданы.")
