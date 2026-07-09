import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os
import tempfile
import unittest
import subprocess
import itertools
import string
import threading
import time

class SymmetricCipher:
    def __init__(self, key_path="secret.key", alphabet="ukrainian"):
        self.key_path = key_path
        self.key = self.load_or_generate_key()
        self.alphabet = alphabet
        
        # Створюємо алфавіт в залежності від мови
        if self.alphabet == "ukrainian":
            self.alphabet = "абвгдеєжзиїйклмнопрстуфхцчшщьюя"
        else:  # Якщо англійський алфавіт
            self.alphabet = string.ascii_lowercase
    
    def load_or_generate_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            return key
    
    def validate_key(self, key=None):
        # Якщо ключ не передано, перевіряється внутрішній ключ
        if key is None:
            key = self.key
        return isinstance(key, bytes) and len(key) == 44
    
    def encrypt(self, data):
        if not self.validate_key():
            raise ValueError("Недійсний ключ шифрування")
        cipher = Fernet(self.key)
        
        # Шифруємо, замінюючи символи на індекси у визначеному алфавіті
        encrypted_data = ''.join(
            [self.alphabet[(self.alphabet.index(c) + 1) % len(self.alphabet)] if c in self.alphabet else c for c in data.lower()])
        
        return encrypted_data
    
    def decrypt(self, encrypted_data):
        if not self.validate_key():
            raise ValueError("Недійсний ключ розшифрування")
        cipher = Fernet(self.key)
        
        # Розшифровуємо, замінюючи символи на попередні індекси
        decrypted_data = ''.join(
            [self.alphabet[(self.alphabet.index(c) - 1) % len(self.alphabet)] if c in self.alphabet else c for c in encrypted_data.lower()])
        
        return decrypted_data

    
# class BruteForceAttack:
#     def __init__(self, cipher):
#         self.cipher = cipher
#         self.found = False
    
#     def brute_force_attack(self, encrypted_text, max_time=15):
#         start_time = time.time()
#         for i in range(1000000):  # наприклад, обмежимо кількість спроб
#             if time.time() - start_time > max_time:
#                 break  # Якщо час вийшов, завершити атаку
#             key = str(i).encode()  # Просто приклад генерації ключа
#             try:
#                 decrypted_text = self.cipher.decrypt(encrypted_text)
#                 if decrypted_text:
#                     self.found = True
#                     return decrypted_text
#             except:
#                 continue
#         return None  # Повернути None, якщо не знайдений ключ за заданий час

class BruteForceAttack:
    def __init__(self, cipher):
        self.cipher = cipher
    
    def brute_force_attack(self, encrypted_data):
        # Дефолтно намагаємось перебрати всі можливі ключі довжиною 44 символи, 
        # які складаються з малих літер і цифр (наприклад, для тесту).
        possible_characters = string.ascii_letters + string.digits
        for key_tuple in itertools.product(possible_characters, repeat=44):
            key = ''.join(key_tuple).encode()  # генеруємо ключ
            if self.cipher.validate_key(key):
                self.cipher.key = key  # задаємо ключ для шифратора
                try:
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    return decrypted_data
                except:
                    continue
        return None  # Якщо жоден ключ не підійшов

class FrequencyAnalyzer:
    @staticmethod
    def analyze(text, language="ukrainian"):
        # Створення таблиці частоти для символів
        frequency_table = {}
        
        if language == "ukrainian":
            ukraine_alphabet = "абвгдеєжзиїйклмнопрстуфхцчшщьюя"
            ukraine_alphabet_upper = ukraine_alphabet.upper()
            frequency_table = {char: 0 for char in ukraine_alphabet + ukraine_alphabet_upper}
        else:
            frequency_table = {char: 0 for char in string.ascii_lowercase}
        
        text = text.lower()  # Приведення до нижнього регістру для коректного підрахунку
        
        for char in text:
            if char in frequency_table:
                frequency_table[char] += 1
        
        # Сортуємо таблицю частоти
        sorted_frequency = {k: v for k, v in sorted(frequency_table.items(), key=lambda item: item[1], reverse=True)}
        
        return sorted_frequency
    
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Криптографічна система")
        self.cipher = SymmetricCipher()
        self.brute_force = BruteForceAttack(self.cipher)  # Додаємо атаку "грубої сили"
        self.frequency_analyzer = FrequencyAnalyzer()  # Додаємо аналізатор частоти
        
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Створити", command=self.create_file)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_command(label="Друк", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        
        crypto_menu = tk.Menu(menu_bar, tearoff=0)
        crypto_menu.add_command(label="Зашифрувати", command=self.encrypt_file)
        crypto_menu.add_command(label="Розшифрувати", command=self.decrypt_file)
        crypto_menu.add_command(label="Атака грубою силою", command=self.brute_force_attack)  # Додаємо кнопку для атаки
        menu_bar.add_cascade(label="Шифрування", menu=crypto_menu)

         # Додаємо нове меню для частотних таблиць
        frequency_menu = tk.Menu(menu_bar, tearoff=0)
        frequency_menu.add_command(label="Частотна таблиця (Українська)", command=self.show_ukrainian_frequency)
        frequency_menu.add_command(label="Частотна таблиця (Англійська)", command=self.show_english_frequency)
        menu_bar.add_cascade(label="Частота", menu=frequency_menu)
        
        menu_bar.add_command(label="Про автора", command=self.show_info)
        
        root.config(menu=menu_bar)
        
        self.text_area = tk.Text(root, wrap="word")
        self.text_area.pack(expand=True, fill="both")
    

    def show_ukrainian_frequency(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Частотна таблиця", "Немає тексту для аналізу")
            return
        
        frequency = self.frequency_analyzer.analyze(text, language="ukrainian")
        self.show_frequency_table(frequency, "Українська частотна таблиця")
    
    def show_english_frequency(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Частотна таблиця", "Немає тексту для аналізу")
            return
        
        frequency = self.frequency_analyzer.analyze(text, language="english")
        self.show_frequency_table(frequency, "Англійська частотна таблиця")
    
    def show_frequency_table(self, frequency, title):
        frequency_text = "\n".join([f"{char}: {count}" for char, count in frequency.items()])
        messagebox.showinfo(title, frequency_text)

    def create_file(self):
        self.text_area.delete(1.0, tk.END)
        
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
                
    def print_file(self):
        content = self.text_area.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Друк", "Немає тексту для друку")
            return
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
        temp_file.write(content)
        temp_file.close()
        
        try:
            if os.name == "nt":
                os.startfile(temp_file.name, "print")
            else:
                subprocess.run(["lp", temp_file.name])
            messagebox.showinfo("Друк", "Документ надіслано на друк")
        except Exception as e:
            messagebox.showerror("Помилка друку", f"Не вдалося надрукувати документ: {e}")
        
    def encrypt_file(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Шифрування", "Немає тексту для шифрування")
            return
        
        try:
            encrypted_text = self.cipher.encrypt(text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, encrypted_text)
        except Exception as e:
            messagebox.showerror("Помилка шифрування", str(e))
        
    def decrypt_file(self):
        encrypted_text = self.text_area.get(1.0, tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("Розшифрування", "Немає тексту для розшифрування")
            return
        
        try:
            decrypted_text = self.cipher.decrypt(encrypted_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, decrypted_text)
        except Exception as e:
            messagebox.showerror("Помилка розшифрування", str(e))
        
    def brute_force_attack(self):
        encrypted_text = self.text_area.get(1.0, tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("Атака грубою силою", "Немає тексту для розшифрування")
            return
        
        decrypted_text = self.brute_force.brute_force_attack(encrypted_text)
        if decrypted_text:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, decrypted_text)
            messagebox.showinfo("Атака грубою силою", "Текст успішно розшифровано!")
        else:
            messagebox.showerror("Атака грубою силою", "Не вдалося розшифрувати текст")

    def show_info(self):
        messagebox.showinfo("Про автора", "Розробник: Марта")
    

        
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()


class TestSymmetricCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = SymmetricCipher()
    
    def test_key_validation(self):
        self.assertTrue(self.cipher.validate_key())
    
    def test_encryption_decryption(self):
        original_text = "Привіт, світ!"
        encrypted_text = self.cipher.encrypt(original_text)
        decrypted_text = self.cipher.decrypt(encrypted_text)
        self.assertEqual(original_text, decrypted_text)
    
    def test_invalid_decryption(self):
        with self.assertRaises(Exception):
            self.cipher.decrypt("некоректний текст")

if __name__ == "__main__":
    unittest.main()