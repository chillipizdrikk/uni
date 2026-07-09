# lab7_python.py
# Лабораторна робота 7 — використання DLL мовою Python
# Бібліотека: Lab5_DLL1.dll
# Метод: модуль ctypes (явне зв'язування)
# Документація: https://docs.python.org/uk/3/library/ctypes.html

import ctypes
import os
import sys

# ============================================================
#  Завантаження бібліотеки DLL
# ============================================================

DLL_PATH = os.path.join(os.path.dirname(__file__), "Lab5_DLL1.dll")

try:
    lib = ctypes.CDLL(DLL_PATH)
    print(f"[OK] Бібліотеку {DLL_PATH} успішно завантажено.\n")
except OSError as e:
    print(f"[Помилка] Не вдалося завантажити Lab5_DLL1.dll:\n  {e}")
    print("Переконайтесь, що Lab5_DLL1.dll знаходиться у тій самій папці, що й скрипт.")
    sys.exit(1)

# ============================================================
#  Оголошення сигнатур функцій (argtypes + restype)
# ============================================================

# INT CountAboveThresholdWin(INT* arr, INT size, INT threshold)
lib.CountAboveThresholdWin.argtypes = [
    ctypes.POINTER(ctypes.c_int),  # INT* arr
    ctypes.c_int,                  # INT size
    ctypes.c_int                   # INT threshold
]
lib.CountAboveThresholdWin.restype = ctypes.c_int

# double AverageOfPositiveWin(double* arr, INT size)
lib.AverageOfPositiveWin.argtypes = [
    ctypes.POINTER(ctypes.c_double),  # double* arr
    ctypes.c_int                      # INT size
]
lib.AverageOfPositiveWin.restype = ctypes.c_double

# BOOL IsArithmeticProgressionWin(double a, double b, double c)
lib.IsArithmeticProgressionWin.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double
]
lib.IsArithmeticProgressionWin.restype = ctypes.c_bool

# CHAR ToUpperCharWin(CHAR ch)
lib.ToUpperCharWin.argtypes = [ctypes.c_char]
lib.ToUpperCharWin.restype  = ctypes.c_char

# INT CountWordsStartingWithLetterWin(LPSTR text, CHAR letter)
lib.CountWordsStartingWithLetterWin.argtypes = [
    ctypes.c_char_p,  # LPSTR text
    ctypes.c_char     # CHAR letter
]
lib.CountWordsStartingWithLetterWin.restype = ctypes.c_int

# ============================================================
#  Допоміжні функції для конвертації масивів Python → ctypes
# ============================================================

def make_int_array(lst):
    """Перетворює список Python int у масив ctypes c_int."""
    arr_type = ctypes.c_int * len(lst)
    return arr_type(*lst)

def make_dbl_array(lst):
    """Перетворює список Python float у масив ctypes c_double."""
    arr_type = ctypes.c_double * len(lst)
    return arr_type(*lst)

# ============================================================
#  Тестування функцій DLL
# ============================================================

print("====================================================")
print("  Тест DLL — мова Python (ctypes, явне зв'язування)")
print("====================================================\n")

# --- 1. CountAboveThresholdWin ---
print("--- 1. CountAboveThresholdWin ---")

data1a = [3, 7, 1, 9, 4, 12, 2, 8]
arr1a  = make_int_array(data1a)
print(f"Масив: {data1a}")
print("Поріг: 5")
r1a = lib.CountAboveThresholdWin(arr1a, len(data1a), 5)
print(f"Кількість елементів > 5: {r1a}  (очікується: 4)\n")

data1b = [1, 2, 3]
arr1b  = make_int_array(data1b)
print(f"Масив: {data1b}")
print("Поріг: 10")
r1b = lib.CountAboveThresholdWin(arr1b, len(data1b), 10)
print(f"Кількість елементів > 10: {r1b}  (очікується: 0)\n")

data1c = [-1, -2, -3]
arr1c  = make_int_array(data1c)
print(f"Масив: {data1c}")
print("Поріг: -5")
r1c = lib.CountAboveThresholdWin(arr1c, len(data1c), -5)
print(f"Кількість елементів > -5: {r1c}  (очікується: 3)\n")

# --- 2. AverageOfPositiveWin ---
print("--- 2. AverageOfPositiveWin ---")

data2a = [-3.0, 5.0, -1.5, 4.0, 0.0, 2.5]
arr2a  = make_dbl_array(data2a)
print(f"Масив: {data2a}")
r2a = lib.AverageOfPositiveWin(arr2a, len(data2a))
print(f"Середнє додатних: {r2a:.4f}  (очікується: {(5.0+4.0+2.5)/3.0:.4f})\n")

data2b = [-1.0, -2.0, 0.0]
arr2b  = make_dbl_array(data2b)
print(f"Масив: {data2b}")
r2b = lib.AverageOfPositiveWin(arr2b, len(data2b))
print(f"Середнє додатних: {r2b:.4f}  (очікується: 0.0000)\n")

data2c = [1.0, 3.0, 5.0, 7.0]
arr2c  = make_dbl_array(data2c)
print(f"Масив: {data2c}")
r2c = lib.AverageOfPositiveWin(arr2c, len(data2c))
print(f"Середнє додатних: {r2c:.4f}  (очікується: 4.0000)\n")

# --- 3. IsArithmeticProgressionWin ---
print("--- 3. IsArithmeticProgressionWin ---")

cases_ap = [
    (2.0, 4.0, 6.0, "TRUE"),
    (9.0, 6.0, 3.0, "TRUE"),
    (1.0, 2.0, 4.0, "FALSE"),
    (5.0, 5.0, 5.0, "TRUE"),
]
for a, b, c, exp in cases_ap:
    res = lib.IsArithmeticProgressionWin(a, b, c)
    result_str = "TRUE" if res else "FALSE"
    print(f"({a:.0f}, {b:.0f}, {c:.0f}): {result_str}  (очікується: {exp})")
print()

# --- 4. ToUpperCharWin ---
print("--- 4. ToUpperCharWin ---")

test_chars = [('a','A'), ('z','Z'), ('m','M'), ('A','A'), ('Z','Z'), ('5','5'), (' ',' ')]
for ch, exp in test_chars:
    res = lib.ToUpperCharWin(ch.encode('ascii'))
    res_char = res.decode('ascii')
    print(f"ToUpperCharWin('{ch}') = '{res_char}'  (очікується: '{exp}')")
print()

# --- 5. CountWordsStartingWithLetterWin ---
print("--- 5. CountWordsStartingWithLetterWin ---")

text1 = b"bear Big ball run Boy best"
print(f"Рядок: \"{text1.decode()}\"")
r5a = lib.CountWordsStartingWithLetterWin(text1, b'b')
print(f"Слів на 'b'/'B': {r5a}  (очікується: 5)\n")

text2 = b"Sun sets slowly Sometimes sky shines"
print(f"Рядок: \"{text2.decode()}\"")
r5b = lib.CountWordsStartingWithLetterWin(text2, b'S')
print(f"Слів на 's'/'S': {r5b}  (очікується: 6)\n")

text3 = b"hello world"
print(f"Рядок: \"{text3.decode()}\"")
r5c = lib.CountWordsStartingWithLetterWin(text3, b'z')
print(f"Слів на 'z': {r5c}  (очікується: 0)\n")

print("====================================================")
print("  Всі функції DLL викликано успішно!")
print("====================================================")