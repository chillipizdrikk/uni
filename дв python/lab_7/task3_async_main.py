#  - Демонстрація асинхронного створення дочірнього процесу (без очікування) за допомогою subprocess.Popen.
#  - Основний процес запускає дочірній паралельно, продовжує свою роботу, перевіряє стан дочірнього процесу.

import subprocess
import os
import time

print("task3_async_main.py - початок (асинхронний запуск дочірнього процесу)")

dirname = os.path.abspath('.')
child = os.path.join(dirname, 'task3_async_child.py')

if not os.path.exists(child):
    print("НЕ знайдено task3_async_child.py у поточній папці. Створіть і запустіть знову.")
    exit(1)

print("Запускаю дочірній процес паралельно (Popen)...")
parprog = subprocess.Popen(["python", child])

print("Після запуску дочірнього процесу основний продовжує роботу.")
time.sleep(1)
print("main process - після 1 сек затримки")
time.sleep(1)
print("main process - перед перевіркою стану дочірнього")
print("subprocess finished ?", parprog.poll())  # повертає None, якщо ще виконується
print("main process - кінець основних дій")

input("Натисніть Enter щоб завершити основний процес (дочірній може ще завершуватись у фоновому режимі)...")
print("task3_async_main.py - кінець")