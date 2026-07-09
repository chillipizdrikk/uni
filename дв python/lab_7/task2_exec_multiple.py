#  - Демонструє виклик os.execvp з передачею  списку файлів як аргументів до програми,
#    тобто запуск однієї програми з переліком файлів (варіант б).
# 1) Вводимо розширення (наприклад: txt).
# 2) Вводимо ім'я програми (наприклад notepad++.exe або chrome.exe або повний шлях).
# 3) Скрипт перевірить наявність exe (shutil.which або типові шляхи для Chrome), виведе аргументи і виконає os.execvp(...).

import os
import glob
import shutil
from pathlib import Path
import sys

print("task2_exec_multiple.py - початок (execvp, варіант б)")
print("Поточна робоча папка:", os.path.abspath('.'))

if os.name != 'nt':
    print("Цей скрипт орієнтований на Windows (os.execvp з GUI exe).")
    sys.exit(1)

ext = input("Введіть розширення файлів для відкриття (наприклад: txt або jpg): ").strip().lstrip('.')
if not ext:
    print("Розширення не вказано. Вихід.")
    sys.exit(0)

pattern = f"*.{ext}"
files = sorted(glob.glob(pattern))
if not files:
    print("Не знайдено файлів:", pattern)
    sys.exit(0)

files_abs = [os.path.abspath(f) for f in files]
print("Знайдені файли:")
for f in files_abs:
    print(" ", f)

viewer = input("Вкажіть exe для запуску (наприклад notepad++.exe або chrome.exe або повний шлях): ").strip()
if not viewer:
    print("Не вказано exe. Вихід.")
    sys.exit(0)

# Спроба знайти exe у PATH
exe_path = shutil.which(viewer)
if not exe_path:
    # Якщо вказали просте ім'я chrome або firefox, перевіримо типові шляхи
    low = viewer.lower()
    if 'chrome' in low:
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    elif 'code' in low or 'vscode' in low:
        candidates = [
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        ]
    else:
        candidates = []
    for c in candidates:
        c_exp = os.path.expandvars(c)
        if os.path.exists(c_exp):
            exe_path = c_exp
            break

if not exe_path:
    print("Виконувальний файл не знайдено в PATH і за типовими шляхами:", viewer)
    print("Вам потрібно вказати повний шлях до exe або додати програму в PATH.")
    sys.exit(1)

print("Знайдено виконувальний файл:", exe_path)

# Підготовка аргументів
use_file_uri = any(k in exe_path.lower() for k in ('chrome', 'firefox', 'msedge'))
args = [exe_path]
if use_file_uri:
    # перетворимо на file:// URI
    uris = [Path(p).as_uri() for p in files_abs]
    args += uris
else:
    args += files_abs

print("Аргументи, що будуть передані:")
for a in args[1:]:
    print(" ", a)

print("УВАГА: зараз викличеться os.execvp і поточний процес Python буде замінено на:", exe_path)
print("Якщо ви хочете продовжити, введіть YES, інакше - будь-який інший текст для відміни.")
confirm = input("Підтвердження (YES щоб виконати): ").strip()
if confirm != 'YES':
    print("Відмінено користувачем.")
    sys.exit(0)

# Виконати передачу керування
try:
    os.execvp(exe_path, args)
except FileNotFoundError as e:
    print("FileNotFoundError:", e)
    sys.exit(1)
except Exception as e:
    print("Помилка під час execvp:", e)
    sys.exit(1)

# Ніколи сюди не потрапимо за умови успішного execvp