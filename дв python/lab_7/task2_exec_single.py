#  - Демонструє "Передачу керування іншій програмі" через os.exec* (тут - os.execvp).
#  - Виконує повну заміну поточного процесу Python на програму перегляду/редагування (наприклад, notepad.exe).
#  - Скрипт очікує, що ви вручну скопіювали у поточну папку кілька файлів однакового типу.
#  - Для демонстрації цей скрипт бере перший файл з відповідного розширення і виконує execvp, передавши його як параметр.

import os
import glob
import sys

print("task2_exec_single.py - початок сценарію")
print("Поточна робоча папка:", os.path.abspath('.'))

if os.name != 'nt':
    print("WARNING: приклад орієнтовано на Windows (notepad.exe та os.execvp). Поточна платформа:", os.name)
    print("Виконайте аналогічні дії на Windows або змініть програму для вашої ОС.")
    sys.exit(1)

# Позначте тип файлів, з яким працюємо (наприклад .txt)
pattern = '*.txt'
files = glob.glob(pattern)

if not files:
    print(f"Не знайдено файлів з шаблоном {pattern}. Скопіюйте декілька .txt файлів у теку і запустіть ще раз.")
    sys.exit(1)

filename = os.path.abspath(files[0])
print("Обрано файл для передачі керування іншій програмі:", filename)
print("Готуємось до os.execvp('notepad.exe', ['notepad.exe', filename])")
print("УВАГА: цей виклик замінить поточний процес Python на notepad.exe. Ніякий Python-код після виклику не виконається.")

# Виконуємо передачу керування: заміна процесу Python на notepad, який відкриє файл
os.execvp("notepad.exe", ["notepad.exe", filename])

# Код сюди не потрапить (os.execvp не повертає при успішному виклику).
print("Якщо ви бачите цей рядок, os.execvp завершився з помилкою.")