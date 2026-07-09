"""
Програма дозволяє:
1. Знайти всі файли з розширенням *.dat
2. Отримати повні шляхи файлів
3. Показати всі атрибути та властивості файлів
4. Вивести вміст одного з файлів
5. Порахувати суму чисел з коригуванням помилок
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re

class FileAttributesLab:
    """
    Клас для роботи з атрибутами файлів та їх властивостями
    """
    
    def __init__(self):
        """Ініціалізація програми"""
        self.found_files = []
        self.protocol_file = "protocol.txt"
        self.protocol_lines = []
    
    def log(self, message):
        """
        Логує повідомлення одночасно до консолі та протоколу
        
        Args:
            message (str): Повідомлення для логування
        """
        print(message)
        self.protocol_lines.append(message)
    
    def save_protocol(self):
        """Зберігає протокол роботи в текстовий файл"""
        try:
            with open(self.protocol_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.protocol_lines))
            self.log(f"\n✓ Протокол збережено в файл: {self.protocol_file}")
        except Exception as e:
            self.log(f"✗ Помилка при збереженні протоколу: {e}")
    
    def find_dat_files(self):
        """
        Операція 1: Встановити і показати повні імена файлів з розширенням *.dat
        
        Шукає файли з розширенням .dat у поточній папці, папці problem та всіх вкладених папках
        """
        self.log("\n" + "="*70)
        self.log("ОПЕРАЦІЯ 1: Пошук файлів з розширенням *.dat")
        self.log("="*70)
        
        self.found_files = []
        current_dir = Path.cwd()
        
        self.log(f"\nПошук у поточній папці та вкладених папках: {current_dir}")
        
        # Рекурсивний пошук у всіх папках
        for file in current_dir.rglob("*.dat"):
            self.found_files.append(file)
            # Показуємо відносний шлях від поточної папки
            relative_path = file.relative_to(current_dir)
            self.log(f"  ✓ Знайдено: {relative_path}")
        
        if not self.found_files:
            self.log("✗ Файлів з розширенням *.dat не знайдено!")
            self.log(f"  Переконайтеся, що файли .dat розташовані у:")
            self.log(f"    - {current_dir}")
            self.log(f"    - {current_dir / 'problem'}")
            return False
        
        self.log(f"\n✓ Всього знайдено файлів: {len(self.found_files)}")
        return True
    
    def show_full_paths(self):
        """
        Операція 2: Знайти і показати повний шлях від кореня логічного диску до файлу
        """
        self.log("\n" + "="*70)
        self.log("ОПЕРАЦІЯ 2: Повні шляхи файлів")
        self.log("="*70)
        
        if not self.found_files:
            self.log("✗ Спочатку виконайте операцію 1")
            return
        
        for i, file_path in enumerate(self.found_files, 1):
            absolute_path = file_path.resolve()
            self.log(f"\nФайл {i}:")
            self.log(f"  Ім'я файлу: {file_path.name}")
            self.log(f"  Абсолютний шлях: {absolute_path}")
            self.log(f"  Диск: {absolute_path.drive}")
            self.log(f"  Папка: {absolute_path.parent}")
    
    def show_file_attributes(self):
        """
        Операція 3: Отримати і показати всі параметри/властивості і атрибути файлів
        """
        self.log("\n" + "="*70)
        self.log("ОПЕРАЦІЯ 3: Атрибути та властивості файлів")
        self.log("="*70)
        
        if not self.found_files:
            self.log("✗ Спочатку виконайте операцію 1")
            return
        
        for i, file_path in enumerate(self.found_files, 1):
            self.log(f"\n{'─'*70}")
            self.log(f"ФАЙЛ {i}: {file_path.name}")
            self.log(f"{'─'*70}")
            
            try:
                stat = file_path.stat()
                
                # Основні властивості
                self.log(f"\nОСНОВНІ ВЛАСТИВОСТІ:")
                self.log(f"  Повне ім'я:        {file_path.resolve()}")
                self.log(f"  Ім'я файлу:        {file_path.name}")
                self.log(f"  Розширення:        {file_path.suffix}")
                self.log(f"  Папка:             {file_path.parent.name}")
                
                # Розмір
                self.log(f"\nРОЗМІР:")
                size_bytes = stat.st_size
                size_kb = size_bytes / 1024
                self.log(f"  Розмір (байти):    {size_bytes:,} B")
                self.log(f"  Розмір (кілобайти):{size_kb:.2f} KB")
                
                # Дати
                self.log(f"\nДАТИ:")
                created_time = datetime.fromtimestamp(stat.st_ctime)
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                accessed_time = datetime.fromtimestamp(stat.st_atime)
                
                self.log(f"  Дата створення:    {created_time.strftime('%d.%m.%Y %H:%M:%S')}")
                self.log(f"  Дата змінення:     {modified_time.strftime('%d.%m.%Y %H:%M:%S')}")
                self.log(f"  Дата доступу:      {accessed_time.strftime('%d.%m.%Y %H:%M:%S')}")
                
                # Атрибути прав доступу
                self.log(f"\nПРАВА ДОСТУПУ:")
                mode = stat.st_mode
                is_readable = bool(stat.st_mode & 0o400)
                is_writable = bool(stat.st_mode & 0o200)
                is_executable = bool(stat.st_mode & 0o100)
                
                self.log(f"  Для читання:       {'✓ Так' if is_readable else '✗ Ні'}")
                self.log(f"  Для запису:        {'✓ Так' if is_writable else '✗ Ні'}")
                self.log(f"  Для виконання:     {'✓ Так' if is_executable else '✗ Ні'}")
                self.log(f"  Режим доступу:     {oct(mode)[-3:]}")
                
                # Інші атрибути
                self.log(f"\nІНШІ АТРИБУТИ:")
                self.log(f"  UID власника:      {stat.st_uid}")
                self.log(f"  GID групи:         {stat.st_gid}")
                self.log(f"  Тип файлу:         {'Звичайний файл' if file_path.is_file() else 'Невідомо'}")
                
            except Exception as e:
                self.log(f"✗ Помилка при отриманні атрибутів: {e}")
    
    def show_file_content(self):
        """
        Операція 4: Показати текст одного з файлів у вікні без використання класу OpenFileDialog
        """
        self.log("\n" + "="*70)
        self.log("ОПЕРАЦІЯ 4: Перегляд вмісту файлу")
        self.log("="*70)
        
        if not self.found_files:
            self.log("✗ Спочатку виконайте операцію 1")
            return
        
        # Показуємо список файлів
        self.log("\nДоступні файли:")
        for i, file_path in enumerate(self.found_files, 1):
            self.log(f"  {i}. {file_path.name}")
        
        # Запитуємо вибір
        try:
            choice = input(f"\nОберіть номер файлу для перегляду (1-{len(self.found_files)}): ").strip()
            file_index = int(choice) - 1
            
            if file_index < 0 or file_index >= len(self.found_files):
                self.log("✗ Невірний вибір!")
                return
            
            selected_file = self.found_files[file_index]
            self.log(f"\n ВМІСТ ФАЙЛУ: {selected_file.name}")
            self.log("─" * 70)
            
            with open(selected_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if content:
                    self.log(content)
                else:
                    self.log("[Файл порожній]")
            
            self.log("─" * 70)
            
        except ValueError:
            self.log("✗ Будь ласка, введіть число!")
        except Exception as e:
            self.log(f"✗ Помилка при читанні файлу: {e}")
    
    def parse_number(self, value_str):
        """
        Парсить рядок як число (ціле або дійсне)
        
        Args:
            value_str (str): Рядок для парсування
            
        Returns:
            float або None: Спарсене число або None якщо помилка
        """
        value_str = value_str.strip()
        
        # Регулярний вираз для числа (ціле або дійсне, з мінусом)
        number_pattern = r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$'
        
        if re.match(number_pattern, value_str):
            try:
                return float(value_str)
            except ValueError:
                return None
        return None
    
    def calculate_sum(self):
        """
        Операція 5: Порахувати суму чисел файлу, виправивши неправильні записи
        """
        self.log("\n" + "="*70)
        self.log("ОПЕРАЦІЯ 5: Обчислення суми чисел з коригуванням помилок")
        self.log("="*70)
        
        if not self.found_files:
            self.log("✗ Спочатку виконайте операцію 1")
            return
        
        # Запитуємо значення для заміни неправильних чисел
        try:
            replacement = input(f"\nВведіть число для заміни помилкових записів (за замовчуванням 0): ").strip()
            replacement_value = float(replacement) if replacement else 0.0
        except ValueError:
            self.log("✗ Невірний формат числа! Використовується 0")
            replacement_value = 0.0
        
        # Обробляємо кожний файл
        for file_path in self.found_files:
            self.log(f"\n{'─'*70}")
            self.log(f"ОБРОБКА ФАЙЛУ: {file_path.name}")
            self.log(f"{'─'*70}")
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Шукаємо всі числові послідовності
                # Розділяємо на потенціальні числа
                tokens = re.findall(r'[^\s,;:()[\]{}]+', content)
                
                total_sum = 0.0
                valid_count = 0
                invalid_count = 0
                corrections = []
                
                self.log(f"\nАналіз записів:")
                
                for token in tokens:
                    parsed = self.parse_number(token)
                    
                    if parsed is not None:
                        total_sum += parsed
                        valid_count += 1
                    else:
                        # Спробуємо витягти число з рядка
                        # Видаляємо символи, які можуть бути в дужках
                        cleaned = re.sub(r'[^\d+.eE-]', '', token)
                        if cleaned:
                            parsed_cleaned = self.parse_number(cleaned)
                            if parsed_cleaned is not None:
                                total_sum += parsed_cleaned
                                valid_count += 1
                                continue
                        
                        # Якщо не можна зпарсити - замінюємо
                        total_sum += replacement_value
                        invalid_count += 1
                        corrections.append(f"'{token}' → {replacement_value}")
                
                self.log(f"  Коректних записів: {valid_count}")
                self.log(f"  Помилкових записів: {invalid_count}")
                
                if corrections:
                    self.log(f"\nВИПРАВЛЕНІ ЗАПИСИ:")
                    for correction in corrections[:10]:  # Показуємо першие 10
                        self.log(f"    {correction}")
                    if len(corrections) > 10:
                        self.log(f"    ... та ще {len(corrections) - 10} помилок")
                
                self.log(f"\n   РЕЗУЛЬТАТИ:")
                self.log(f"  Сума всіх чисел: {total_sum}")
                self.log(f"  Всього елементів: {valid_count + invalid_count}")
                self.log(f"  Середнє значення: {total_sum / (valid_count + invalid_count) if (valid_count + invalid_count) > 0 else 0}")
                
            except Exception as e:
                self.log(f"✗ Помилка при обробці файлу: {e}")
    
    def show_menu(self):
        """Показує головне меню"""
        self.log("\n" + "="*70)
        self.log("ГОЛОВНЕ МЕНЮ")
        self.log("="*70)
        self.log("1. Знайти файли з розширенням *.dat")
        self.log("2. Показати повні шляхи файлів")
        self.log("3. Показати атрибути та властивості файлів")
        self.log("4. Переглянути вміст файлу")
        self.log("5. Обчислити суму чисел з коригуванням")
        self.log("6. Виконати ВСІ операції")
        self.log("0. Вихід")
        self.log("="*70)
    
    def run(self):
        """Головна функція програми з діалоговим інтерфейсом"""
        self.log("\nЛАБОРАТОРНА РОБОТА 2: АТРИБУТИ ФАЙЛІВ")
        
        while True:
            self.show_menu()
            choice = input("\nОберіть операцію: ").strip()
            
            if choice == "1":
                self.find_dat_files()
            elif choice == "2":
                self.show_full_paths()
            elif choice == "3":
                self.show_file_attributes()
            elif choice == "4":
                self.show_file_content()
            elif choice == "5":
                self.calculate_sum()
            elif choice == "6":
                if self.find_dat_files():
                    self.show_full_paths()
                    self.show_file_attributes()
                    self.show_file_content()
                    self.calculate_sum()
            elif choice == "0":
                self.log("\nДо побачення!")
                break
            else:
                self.log("\n✗ Невірний вибір! Спробуйте ще раз.")
        
        self.save_protocol()


def main():
    """Точка входу програми"""
    try:
        lab = FileAttributesLab()
        lab.run()
    except KeyboardInterrupt:
        print("\n\nПрограма переривана користувачем")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Критична помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()