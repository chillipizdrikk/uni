import random
import tkinter as tk
from tkinter import messagebox, filedialog

ukr_alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
eng_alphabet = 'abcdefghijklmnopqrstuvwxyz().,;:'

def create_binary_mapping(alphabet: str) -> dict:
    """
    Створює бінарне відображення символів алфавіту.
    Бінарний код має 5 біт для кожного символу, від 00001 до 11111.
    """
    return {char: format(i, '05b') for i, char in enumerate(alphabet)}

def text_to_binary(text: str, alphabet: str) -> list:
    """
    Приймає текст і перетворює кожну букву на її бінарне значення.
    Якщо символ не входить в алфавіт, його пропускаємо.
    Повертає список бінарних значень для кожного символу.
    """
    mapping = create_binary_mapping(alphabet)
    binary_text = []

    for char in text:
        if char in mapping:
            binary_text.append(mapping[char])
        else:
            # Якщо символ не знайдений в алфавіті, пропускаємо його
            print(f"Символ '{char}' не знайдений в алфавіті, пропускаємо.")

    return binary_text

def generate_random_word(length: int, alphabet: str) -> str:
    """
    Генерує випадкове слово з алфавіту тієї ж довжини, що й введений текст.
    """
    return ''.join(random.choice(alphabet) for _ in range(length))

def xor_encrypt(text: str, key: str, alphabet: str) -> str:
    """
    Шифрує текст методом гамування з використанням операції XOR.
    Пробіли залишаються без змін.
    """
    # Перетворюємо текст і ключ у бінарне представлення
    binary_text = text_to_binary(text, alphabet)
    binary_key = text_to_binary(key, alphabet)

    # Переконуємося, що ключ має таку ж довжину, як і текст
    if len(binary_key) < len(binary_text):
        binary_key = binary_key * (len(binary_text) // len(binary_key)) + binary_key[:len(binary_text) % len(binary_key)]
    elif len(binary_key) > len(binary_text):
        binary_key = binary_key[:len(binary_text)]

    # Виконуємо XOR для кожної пари бітових значень
    xor_result = []
    text_index = 0  # Індекс для відстеження символів тексту

    for char in text:
        if char == ' ':
            xor_result.append(' ')  # Пропускаємо пробіли
        else:
            b_text = binary_text[text_index]
            b_key = binary_key[text_index]
            xor_result.append(format(int(b_text, 2) ^ int(b_key, 2), '05b'))
            text_index += 1

    # Перетворюємо результат XOR назад у символи за допомогою мапи
    inverted_binary_mapping = {v: k for k, v in create_binary_mapping(alphabet).items()}
    encrypted_text = ''.join(inverted_binary_mapping[b] if b != ' ' else ' ' for b in xor_result)

    return encrypted_text

def validate_text_and_key(text: str, key: str, alphabet: str, cipher: str) -> bool:
    """
    Перевіряє, чи всі символи тексту та ключа входять в алфавіт.
    Також перевіряє, чи довжина ключа відповідає вимогам обраного шифру.
    """
    for char in text:
        if char != ' ' and char not in alphabet:
            messagebox.showerror("Помилка", f"Символ '{char}' не входить в обраний алфавіт.")
            return False
    for char in key:
        if char not in alphabet:
            messagebox.showerror("Помилка", f"Символ '{char}' у ключі не входить в обраний алфавіт.")
            return False
    if cipher == "Vernam" and len(key) < len(text):
        messagebox.showerror("Помилка", "Для шифру Вернама довжина ключа повинна бути рівною або більшою за довжину тексту.")
        return False
    return True

def vernam_encrypt(text: str, key: str, alphabet: str) -> str:
    """
    Шифрує текст методом шифру Вернама з використанням додавання індексів.
    """
    encrypted_text = []
    for t_char, k_char in zip(text, key):
        if t_char not in alphabet or k_char not in alphabet:
            encrypted_text.append(t_char)
        else:
            t_idx = alphabet.index(t_char)
            k_idx = alphabet.index(k_char)
            encrypted_idx = (t_idx + k_idx) % len(alphabet)
            encrypted_text.append(alphabet[encrypted_idx])
    return ''.join(encrypted_text)

def vernam_decrypt(encrypted_text: str, key: str, alphabet: str) -> str:
    """
    Розшифровує текст, зашифрований методом шифру Вернама з використанням віднімання індексів.
    """
    decrypted_text = []
    for e_char, k_char in zip(encrypted_text, key):
        if e_char not in alphabet or k_char not in alphabet:
            decrypted_text.append(e_char)
        else:
            e_idx = alphabet.index(e_char)
            k_idx = alphabet.index(k_char)
            decrypted_idx = (e_idx - k_idx) % len(alphabet)
            decrypted_text.append(alphabet[decrypted_idx])
    return ''.join(decrypted_text)

def encrypt():
    text = input_text.get("1.0", tk.END).strip()
    key = key_text.get("1.0", tk.END).strip()
    language = language_var.get()
    cipher = cipher_var.get()
    
    if language == "Українська":
        alphabet = ukr_alphabet
    elif language == "Англійська":
        alphabet = eng_alphabet
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть мову")
        return
    
    if not text or not key:
        messagebox.showerror("Помилка", "Текст і ключ не можуть бути порожніми")
        return
    
    if not validate_text_and_key(text, key, alphabet, cipher):
        return
    
    if cipher == "XOR":
        encrypted = xor_encrypt(text, key, alphabet)
    elif cipher == "Vernam":
        encrypted = vernam_encrypt(text, key, alphabet)
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть метод шифрування")
        return
    
    encrypted_text.delete("1.0", tk.END)
    encrypted_text.insert(tk.END, encrypted)

def decrypt():
    text = encrypted_text.get("1.0", tk.END).strip()
    key = key_text.get("1.0", tk.END).strip()
    language = language_var.get()
    cipher = cipher_var.get()
    
    if language == "Українська":
        alphabet = ukr_alphabet
    elif language == "Англійська":
        alphabet = eng_alphabet
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть мову")
        return
    
    if not text or not key:
        messagebox.showerror("Помилка", "Текст і ключ не можуть бути порожніми")
        return
    
    if not validate_text_and_key(text, key, alphabet, cipher):
        return
    
    if cipher == "XOR":
        decrypted = xor_encrypt(text, key, alphabet)
    elif cipher == "Vernam":
        decrypted = vernam_decrypt(text, key, alphabet)
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть метод шифрування")
        return
    
    decrypted_text.delete("1.0", tk.END)
    decrypted_text.insert(tk.END, decrypted)

def generate_key():
    text = input_text.get("1.0", tk.END).strip()
    language = language_var.get()
    
    if language == "Українська":
        alphabet = ukr_alphabet
    elif language == "Англійська":
        alphabet = eng_alphabet
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть мову")
        return
    
    if not text:
        messagebox.showerror("Помилка", "Вхідний текст не може бути порожнім")
        return
    
    key = generate_random_word(len(text), alphabet)
    key_text.delete("1.0", tk.END)
    key_text.insert(tk.END, key)

def generate_longer_key():
    text = input_text.get("1.0", tk.END).strip()
    language = language_var.get()
    
    if language == "Українська":
        alphabet = ukr_alphabet
    elif language == "Англійська":
        alphabet = eng_alphabet
    else:
        messagebox.showerror("Помилка", "Будь ласка, оберіть мову")
        return
    
    if not text:
        messagebox.showerror("Помилка", "Вхідний текст не може бути порожнім")
        return
    
    key = generate_random_word(len(text) * 2, alphabet)
    key_text.delete("1.0", tk.END)
    key_text.insert(tk.END, key)

def generate_key_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            text = input_text.get("1.0", tk.END).strip()
            if len(content) > len(text):
                content = content[:len(text)]
            key_text.delete("1.0", tk.END)
            key_text.insert(tk.END, content)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
    if file_path:
        # Save either input text or encrypted text based on user's choice
        if messagebox.askyesno("Зберегти текст", "Бажаєте зберегти зашифрований текст?"):
            content = encrypted_text.get("1.0", tk.END).strip()
        else:
            content = input_text.get("1.0", tk.END).strip()
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

def show_about():
    messagebox.showinfo("Про програму", "Тригуб Марта ПМІ-36")

def exit_app():
    root.quit()

# Створюємо вікно додатку
root = tk.Tk()
root.title("Гамма Шифр")
root.configure(bg="#f0f0f0")

# Створюємо елементи інтерфейсу
language_var = tk.StringVar(value="Оберіть мову")
language_label = tk.Label(root, text="Мова:", bg="#f0f0f0")
language_label.grid(row=0, column=0, padx=10, pady=10)
language_menu = tk.OptionMenu(root, language_var, "Українська", "Англійська")
language_menu.grid(row=0, column=1, padx=10, pady=10)

cipher_var = tk.StringVar(value="Оберіть шифр")
cipher_label = tk.Label(root, text="Шифр:", bg="#f0f0f0")
cipher_label.grid(row=0, column=2, padx=10, pady=10)
cipher_menu = tk.OptionMenu(root, cipher_var, "XOR", "Vernam")
cipher_menu.grid(row=0, column=3, padx=10, pady=10)

input_label = tk.Label(root, text="Вхідний текст:", bg="#f0f0f0")
input_label.grid(row=1, column=0, padx=10, pady=10)
input_text = tk.Text(root, height=5, width=50)
input_text.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

key_label = tk.Label(root, text="Ключ:", bg="#f0f0f0")
key_label.grid(row=2, column=0, padx=10, pady=10)
key_text = tk.Text(root, height=2, width=50)
key_text.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=3, column=0, columnspan=4, pady=10)

generate_key_button = tk.Button(button_frame, text="Згенерувати ключ", command=generate_key, bg="#4CAF50", fg="white")
generate_key_button.pack(side=tk.LEFT, padx=5)

generate_longer_key_button = tk.Button(button_frame, text="Згенерувати довший ключ", command=generate_longer_key, bg="#4CAF50", fg="white")
generate_longer_key_button.pack(side=tk.LEFT, padx=5)

generate_key_from_file_button = tk.Button(button_frame, text="Згенерувати ключ з файлу", command=generate_key_from_file, bg="#4CAF50", fg="white")
generate_key_from_file_button.pack(side=tk.LEFT, padx=5)

encrypt_button = tk.Button(root, text="Зашифрувати", command=encrypt, bg="#2196F3", fg="white")
encrypt_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

encrypted_label = tk.Label(root, text="Зашифрований текст:", bg="#f0f0f0")
encrypted_label.grid(row=5, column=0, padx=10, pady=10)
encrypted_text = tk.Text(root, height=5, width=50)
encrypted_text.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Розшифрувати", command=decrypt, bg="#2196F3", fg="white")
decrypt_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

decrypted_label = tk.Label(root, text="Розшифрований текст:", bg="#f0f0f0")
decrypted_label.grid(row=7, column=0, padx=10, pady=10)
decrypted_text = tk.Text(root, height=5, width=50)
decrypted_text.grid(row=7, column=1, columnspan=3, padx=10, pady=10)

additional_button_frame = tk.Frame(root, bg="#f0f0f0")
additional_button_frame.grid(row=8, column=0, columnspan=4, pady=10)

open_file_button = tk.Button(additional_button_frame, text="Відкрити файл", command=open_file, bg="#FF9800", fg="white")
open_file_button.pack(side=tk.LEFT, padx=5)

save_file_button = tk.Button(additional_button_frame, text="Зберегти текст", command=save_file, bg="#FF9800", fg="white")
save_file_button.pack(side=tk.LEFT, padx=5)

about_button = tk.Button(additional_button_frame, text="Про програму", command=show_about, bg="#FF9800", fg="white")
about_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(additional_button_frame, text="Вихід", command=exit_app, bg="#F44336", fg="white")
exit_button.pack(side=tk.LEFT, padx=5)

# Запускаємо головний цикл додатку
root.mainloop()












# import random
# import tkinter as tk
# from tkinter import messagebox, filedialog

# ukr_alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
# eng_alphabet = 'abcdefghijklmnopqrstuvwxyz().,;:'

# def create_binary_mapping(alphabet: str) -> dict:
#     """
#     Створює бінарне відображення символів алфавіту.
#     Бінарний код має 5 біт для кожного символу, від 00001 до 11111.
#     """
#     return {char: format(i, '05b') for i, char in enumerate(alphabet)}

# def text_to_binary(text: str, alphabet: str) -> list:
#     """
#     Приймає текст і перетворює кожну букву на її бінарне значення.
#     Якщо символ не входить в алфавіт, його пропускаємо.
#     Повертає список бінарних значень для кожного символу.
#     """
#     mapping = create_binary_mapping(alphabet)
#     binary_text = []

#     for char in text:
#         if char in mapping:
#             binary_text.append(mapping[char])
#         else:
#             # Якщо символ не знайдений в алфавіті, пропускаємо його
#             print(f"Символ '{char}' не знайдений в алфавіті, пропускаємо.")

#     return binary_text

# def generate_random_word(length: int, alphabet: str) -> str:
#     """
#     Генерує випадкове слово з алфавіту тієї ж довжини, що й введений текст.
#     """
#     return ''.join(random.choice(alphabet) for _ in range(length))

# def xor_encrypt(text: str, key: str, alphabet: str) -> str:
#     """
#     Шифрує текст методом гамування з використанням операції XOR.
#     Пробіли залишаються без змін.
#     """
#     # Перетворюємо текст і ключ у бінарне представлення
#     binary_text = text_to_binary(text, alphabet)
#     binary_key = text_to_binary(key, alphabet)

#     # Переконуємося, що ключ має таку ж довжину, як і текст
#     if len(binary_key) < len(binary_text):
#         binary_key = binary_key * (len(binary_text) // len(binary_key)) + binary_key[:len(binary_text) % len(binary_key)]
#     elif len(binary_key) > len(binary_text):
#         binary_key = binary_key[:len(binary_text)]

#     # Виконуємо XOR для кожної пари бітових значень
#     xor_result = []
#     text_index = 0  # Індекс для відстеження символів тексту

#     for char in text:
#         if char == ' ':
#             xor_result.append(' ')  # Пропускаємо пробіли
#         else:
#             b_text = binary_text[text_index]
#             b_key = binary_key[text_index]
#             xor_result.append(format(int(b_text, 2) ^ int(b_key, 2), '05b'))
#             text_index += 1

#     # Перетворюємо результат XOR назад у символи за допомогою мапи
#     inverted_binary_mapping = {v: k for k, v in create_binary_mapping(alphabet).items()}
#     encrypted_text = ''.join(inverted_binary_mapping[b] if b != ' ' else ' ' for b in xor_result)

#     return encrypted_text

# def validate_text_and_key(text: str, key: str, alphabet: str, cipher: str) -> bool:
#     """
#     Перевіряє, чи всі символи тексту та ключа входять в алфавіт.
#     Також перевіряє, чи довжина ключа відповідає вимогам обраного шифру.
#     """
#     for char in text:
#         if char != ' ' and char not in alphabet:
#             messagebox.showerror("Error", f"Character '{char}' is not in the selected alphabet.")
#             return False
#     for char in key:
#         if char not in alphabet:
#             messagebox.showerror("Error", f"Character '{char}' in the key is not in the selected alphabet.")
#             return False
#     if cipher == "Vernam" and len(key) < len(text):
#         messagebox.showerror("Error", "For Vernam cipher, the key length must be equal to or longer than the text length.")
#         return False
#     return True

# def vernam_encrypt(text: str, key: str, alphabet: str) -> str:
#     """
#     Шифрує текст методом шифру Вернама з використанням додавання індексів.
#     """
#     encrypted_text = []
#     for t_char, k_char in zip(text, key):
#         if t_char not in alphabet or k_char not in alphabet:
#             encrypted_text.append(t_char)
#         else:
#             t_idx = alphabet.index(t_char)
#             k_idx = alphabet.index(k_char)
#             encrypted_idx = (t_idx + k_idx) % len(alphabet)
#             encrypted_text.append(alphabet[encrypted_idx])
#     return ''.join(encrypted_text)

# def vernam_decrypt(encrypted_text: str, key: str, alphabet: str) -> str:
#     """
#     Розшифровує текст, зашифрований методом шифру Вернама з використанням віднімання індексів.
#     """
#     decrypted_text = []
#     for e_char, k_char in zip(encrypted_text, key):
#         if e_char not in alphabet or k_char not in alphabet:
#             decrypted_text.append(e_char)
#         else:
#             e_idx = alphabet.index(e_char)
#             k_idx = alphabet.index(k_char)
#             decrypted_idx = (e_idx - k_idx) % len(alphabet)
#             decrypted_text.append(alphabet[decrypted_idx])
#     return ''.join(decrypted_text)

# def encrypt():
#     text = input_text.get("1.0", tk.END).strip()
#     key = key_text.get("1.0", tk.END).strip()
#     language = language_var.get()
#     cipher = cipher_var.get()
    
#     if language == "Ukrainian":
#         alphabet = ukr_alphabet
#     elif language == "English":
#         alphabet = eng_alphabet
#     else:
#         messagebox.showerror("Error", "Please select a language")
#         return
    
#     if not text or not key:
#         messagebox.showerror("Error", "Text and key cannot be empty")
#         return
    
#     if not validate_text_and_key(text, key, alphabet, cipher):
#         return
    
#     if cipher == "XOR":
#         encrypted = xor_encrypt(text, key, alphabet)
#     elif cipher == "Vernam":
#         encrypted = vernam_encrypt(text, key, alphabet)
#     else:
#         messagebox.showerror("Error", "Please select a cipher method")
#         return
    
#     encrypted_text.delete("1.0", tk.END)
#     encrypted_text.insert(tk.END, encrypted)

# def decrypt():
#     text = encrypted_text.get("1.0", tk.END).strip()
#     key = key_text.get("1.0", tk.END).strip()
#     language = language_var.get()
#     cipher = cipher_var.get()
    
#     if language == "Ukrainian":
#         alphabet = ukr_alphabet
#     elif language == "English":
#         alphabet = eng_alphabet
#     else:
#         messagebox.showerror("Error", "Please select a language")
#         return
    
#     if not text or not key:
#         messagebox.showerror("Error", "Text and key cannot be empty")
#         return
    
#     if not validate_text_and_key(text, key, alphabet, cipher):
#         return
    
#     if cipher == "XOR":
#         decrypted = xor_encrypt(text, key, alphabet)
#     elif cipher == "Vernam":
#         decrypted = vernam_decrypt(text, key, alphabet)
#     else:
#         messagebox.showerror("Error", "Please select a cipher method")
#         return
    
#     decrypted_text.delete("1.0", tk.END)
#     decrypted_text.insert(tk.END, decrypted)

# def generate_key():
#     text = input_text.get("1.0", tk.END).strip()
#     language = language_var.get()
    
#     if language == "Ukrainian":
#         alphabet = ukr_alphabet
#     elif language == "English":
#         alphabet = eng_alphabet
#     else:
#         messagebox.showerror("Error", "Please select a language")
#         return
    
#     if not text:
#         messagebox.showerror("Error", "Input text cannot be empty")
#         return
    
#     key = generate_random_word(len(text), alphabet)
#     key_text.delete("1.0", tk.END)
#     key_text.insert(tk.END, key)

# def generate_longer_key():
#     text = input_text.get("1.0", tk.END).strip()
#     language = language_var.get()
    
#     if language == "Ukrainian":
#         alphabet = ukr_alphabet
#     elif language == "English":
#         alphabet = eng_alphabet
#     else:
#         messagebox.showerror("Error", "Please select a language")
#         return
    
#     if not text:
#         messagebox.showerror("Error", "Input text cannot be empty")
#         return
    
#     key = generate_random_word(len(text) * 2, alphabet)
#     key_text.delete("1.0", tk.END)
#     key_text.insert(tk.END, key)

# def generate_key_from_file():
#     file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
#     if file_path:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read().strip()
#             text = input_text.get("1.0", tk.END).strip()
#             if len(content) > len(text):
#                 content = content[:len(text)]
#             key_text.delete("1.0", tk.END)
#             key_text.insert(tk.END, content)

# def open_file():
#     file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
#     if file_path:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read().strip()
#             input_text.delete("1.0", tk.END)
#             input_text.insert(tk.END, content)

# def save_file():
#     file_path = filedialog.asksaveasfilename(defaultextension=".txt",
#                                              filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
#     if file_path:
#         # Save either input text or encrypted text based on user's choice
#         if messagebox.askyesno("Save Text", "Do you want to save the encrypted text?"):
#             content = encrypted_text.get("1.0", tk.END).strip()
#         else:
#             content = input_text.get("1.0", tk.END).strip()
        
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(content)

# def show_about():
#     messagebox.showinfo("About", "Тригуб Марта ПМІ-36")

# def exit_app():
#     root.quit()

# # Створюємо вікно додатку
# root = tk.Tk()
# root.title("Gamma Cipher")

# # Створюємо елементи інтерфейсу
# language_var = tk.StringVar(value="Select Language")
# language_label = tk.Label(root, text="Language:")
# language_label.grid(row=0, column=0, padx=10, pady=10)
# language_menu = tk.OptionMenu(root, language_var, "Ukrainian", "English")
# language_menu.grid(row=0, column=1, padx=10, pady=10)

# cipher_var = tk.StringVar(value="Select Cipher")
# cipher_label = tk.Label(root, text="Cipher:")
# cipher_label.grid(row=0, column=2, padx=10, pady=10)
# cipher_menu = tk.OptionMenu(root, cipher_var, "XOR", "Vernam")
# cipher_menu.grid(row=0, column=3, padx=10, pady=10)

# input_label = tk.Label(root, text="Input Text:")
# input_label.grid(row=1, column=0, padx=10, pady=10)
# input_text = tk.Text(root, height=5, width=50)
# input_text.grid(row=1, column=1, padx=10, pady=10)

# key_label = tk.Label(root, text="Key:")
# key_label.grid(row=2, column=0, padx=10, pady=10)
# key_text = tk.Text(root, height=2, width=50)
# key_text.grid(row=2, column=1, padx=10, pady=10)

# generate_key_button = tk.Button(root, text="Generate Key", command=generate_key)
# generate_key_button.grid(row=2, column=2, padx=10, pady=10)

# generate_longer_key_button = tk.Button(root, text="Generate Longer Key", command=generate_longer_key)
# generate_longer_key_button.grid(row=2, column=3, padx=10, pady=10)

# generate_key_from_file_button = tk.Button(root, text="Generate Key from File", command=generate_key_from_file)
# generate_key_from_file_button.grid(row=2, column=4, padx=10, pady=10)

# encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
# encrypt_button.grid(row=3, column=1, padx=10, pady=10)

# encrypted_label = tk.Label(root, text="Encrypted Text:")
# encrypted_label.grid(row=4, column=0, padx=10, pady=10)
# encrypted_text = tk.Text(root, height=5, width=50)
# encrypted_text.grid(row=4, column=1, padx=10, pady=10)

# decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
# decrypt_button.grid(row=5, column=1, padx=10, pady=10)

# decrypted_label = tk.Label(root, text="Decrypted Text:")
# decrypted_label.grid(row=6, column=0, padx=10, pady=10)
# decrypted_text = tk.Text(root, height=5, width=50)
# decrypted_text.grid(row=6, column=1, padx=10, pady=10)

# # Додаткові кнопки
# open_file_button = tk.Button(root, text="Open File", command=open_file)
# open_file_button.grid(row=7, column=0, padx=10, pady=10)

# save_file_button = tk.Button(root, text="Save Text", command=save_file)
# save_file_button.grid(row=7, column=1, padx=10, pady=10)

# about_button = tk.Button(root, text="About", command=show_about)
# about_button.grid(row=7, column=2, padx=10, pady=10)

# exit_button = tk.Button(root, text="Exit", command=exit_app)
# exit_button.grid(row=8, column=1, padx=10, pady=10)

# # Запускаємо головний цикл додатку
# root.mainloop()