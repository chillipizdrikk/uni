#  - Знайти в поточній папці один файл Word (.docx або .doc) і один файл зображення (.jpg, .jpeg, .bmp).
#  - Запустити кожен файл через пов'язану аплікацію (подвійний клік) за допомогою os.startfile().
#  - Надрукувати коментарі перед і після кожної важливої дії (самодокументування, як вимагалось).
#  - Далі очікує від користувача виконання 1-2 простих редагувань вручну і натискання Enter для продовження.

import os
import glob
import sys

print("task1_open_associated.py - початок сценарію")
print("Поточна робоча папка:", os.path.abspath('.'))

if os.name != 'nt':
    print("WARNING: os.startfile() працює тільки у Windows. Поточна платформа:", os.name)
    print("Сценарій завершено.")
    sys.exit(1)

# Знайти Word-файли (.docx або .doc) у поточній папці
word_patterns = ['*.docx', '*.doc']
word_files = []
for pat in word_patterns:
    word_files.extend(glob.glob(pat))

# Знайти зображення (.jpg, .jpeg, .bmp)
img_patterns = ['*.jpg', '*.jpeg', '*.bmp', '*.png']
img_files = []
for pat in img_patterns:
    img_files.extend(glob.glob(pat))

# Вибір файлів (беремо перші знайдені)
word_file = word_files[0] if word_files else None
img_file = img_files[0] if img_files else None

print("Знайдено Word файлів:", len(word_files))
print("Знайдено файлів зображень:", len(img_files))
print()

if not word_file:
    print("Не знайдено Word-файлів у поточній папці. Скопіюйте вручну один файл .docx або .doc і запустіть ще раз.")
else:
    print("Виконую запуск пов'язаного застосунку для Word-файлу:", word_file)
    print("Перед запуском: переконайтесь, що Word встановлено і відкриття файлів працює.")
    # Оператор, який відкриває файл у пов'язаній аплікації (еквівалент подвійного кліку)
    os.startfile(os.path.abspath(word_file))
    print("os.startfile() викликано для Word-файла (відкрилася програма для редагування документа).")
    print("Зробіть 1-2 прості редагування у документі та збережіть/закрийте його, потім поверніться сюди і натисніть Enter.")

if not img_file:
    print("Не знайдено файлів зображень у поточній папці. Скопіюйте вручну один файл .jpg/.jpeg/.bmp і запустіть ще раз.")
else:
    print("Виконую запуск пов'язаного застосунку для файлу зображення:", img_file)
    os.startfile(os.path.abspath(img_file))
    print("os.startfile() викликано для зображення (відкрилася програма перегляду зображень).")
    print("Зробіть 1-2 прості операції (наприклад, невелика правка або просто перегляд), закрийте програму, потім поверніться сюди і натисніть Enter.")

# Очікуємо підтвердження від користувача про виконані редагування та закриття програм
input("Після редагування і закриття програм натисніть Enter для завершення сценарію...")

print("task1_open_associated.py - кінець сценарію")