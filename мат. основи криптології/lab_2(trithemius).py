# import tkinter as tk
# from collections import Counter
# from tkinter import filedialog, messagebox

# ukr_alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
# eng_alphabet = 'abcdefghijklmnopqrstuvwxyz'
# symbols = '.,!?/"()'

# # Функція для визначення мови
# def detect_language(text):
#     has_ukr = any(char.lower() in ukr_alphabet for char in text if char.isalpha())
#     has_eng = any(char.lower() in eng_alphabet for char in text if char.isalpha())

#     if has_ukr and not has_eng:
#         return 'ukr'
#     elif has_eng and not has_ukr:
#         return 'eng'
#     else:
#         return 'mixed'

# # Лінійний шифр Тритеміуса
# def tritemius_cipher(text, A, B):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = (A * i + B) % alphabet_size
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base + k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result

# def tritemius_decipher(text, A, B):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = (A * i + B) % alphabet_size
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base - k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result

# # Нелінійний шифр Тритеміуса
# def tritemius_non_linear_cipher(text, A, B, C):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = (A * (i ** 2) + B * i + C) % alphabet_size
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base + k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result

# def tritemius_non_linear_decipher(text, A, B, C):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = (A * (i ** 2) + B * i + C) % alphabet_size
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base - k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result

# # Шифр за гаслом
# def tritemius_keyword_cipher(text, keyword):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""
#     keyword = ''.join([char for char in keyword.lower() if char in alphabet])

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = alphabet.index(keyword[i % len(keyword)])  # Зсув залежить від символу гасла
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base + k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result


# def exit_app():
#     root.quit()

# def tritemius_keyword_decipher(text, keyword):
#     lang = detect_language(text)
#     if lang == 'mixed':
#         return "Помилка. Текст містить різні мови"

#     alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
#     alphabet_size = len(alphabet)
#     result = ""
#     keyword = ''.join([char for char in keyword.lower() if char in alphabet])

#     for i, char in enumerate(text):
#         if char.lower() in alphabet:
#             k = alphabet.index(keyword[i % len(keyword)])  # Зсув залежить від символу гасла
#             base = alphabet.index(char.lower())
#             new_char = alphabet[(base - k) % alphabet_size]
#             result += new_char.upper() if char.isupper() else new_char
#         elif char in symbols:
#             result += char
#         else:
#             result += char

#     return result

# # Інтерфейс Tkinter
# root = tk.Tk()
# root.title("Шифри Тритеміуса")

# # Поля для вводу параметрів A, B, C
# param_frame = tk.Frame(root)
# param_frame.pack(pady=5)
# tk.Label(param_frame, text="A:").pack(side=tk.LEFT, padx=5)
# entry_a = tk.Entry(param_frame, width=5)
# entry_a.pack(side=tk.LEFT)
# entry_a.insert(0, "1")

# tk.Label(param_frame, text="B:").pack(side=tk.LEFT, padx=5)
# entry_b = tk.Entry(param_frame, width=5)
# entry_b.pack(side=tk.LEFT)
# entry_b.insert(0, "0")

# tk.Label(param_frame, text="C:").pack(side=tk.LEFT, padx=5)
# entry_c = tk.Entry(param_frame, width=5)
# entry_c.pack(side=tk.LEFT)
# entry_c.insert(0, "0")

# # Поле для введення гасла
# tk.Label(root, text="Гасло:").pack()
# keyword_entry = tk.Entry(root, font=("Arial", 12), width=30)
# keyword_entry.pack(padx=10, pady=5)

# # Поля для введення тексту
# tk.Label(root, text="Оригінальний текст:").pack()
# original_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
# original_text_area.pack(padx=10, pady=5)

# tk.Label(root, text="Зашифрований текст:").pack()
# encrypted_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
# encrypted_text_area.pack(padx=10, pady=5)

# tk.Label(root, text="Розшифрований текст:").pack()
# decrypted_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
# decrypted_text_area.pack(padx=10, pady=5)

# # Функції для шифрування/розшифрування
# def encrypt_tritemius():
#     text = original_text_area.get("1.0", tk.END).strip()
#     A = int(entry_a.get())
#     B = int(entry_b.get())
#     C = int(entry_c.get())
#     encrypted_text = tritemius_non_linear_cipher(text, A, B, C)
#     encrypted_text_area.delete("1.0", tk.END)
#     encrypted_text_area.insert(tk.END, encrypted_text)

# def decrypt_tritemius():
#     text = encrypted_text_area.get("1.0", tk.END).strip()
#     A = int(entry_a.get())
#     B = int(entry_b.get())
#     C = int(entry_c.get())
#     decrypted_text = tritemius_non_linear_decipher(text, A, B, C)
#     decrypted_text_area.delete("1.0", tk.END)
#     decrypted_text_area.insert(tk.END, decrypted_text)

# def encrypt_keyword():
#     text = original_text_area.get("1.0", tk.END).strip()
#     keyword = keyword_entry.get().strip()
#     encrypted_text = tritemius_keyword_cipher(text, keyword)
#     encrypted_text_area.delete("1.0", tk.END)
#     encrypted_text_area.insert(tk.END, encrypted_text)

# def decrypt_keyword():
#     text = encrypted_text_area.get("1.0", tk.END).strip()
#    # Функції для розшифрування за гаслом
#     keyword = keyword_entry.get().strip()
#     decrypted_text = tritemius_keyword_decipher(text, keyword)
#     decrypted_text_area.delete("1.0", tk.END)
#     decrypted_text_area.insert(tk.END, decrypted_text)

# # Кнопки управління
# btn_frame = tk.Frame(root)
# btn_frame.pack(pady=10)

# # Кнопки для нелінійного шифру Тритеміуса
# encrypt_tritemius_btn = tk.Button(btn_frame, text="Зашифрувати (Нелінійний)", command=encrypt_tritemius)
# encrypt_tritemius_btn.pack(side=tk.LEFT, padx=5)

# decrypt_tritemius_btn = tk.Button(btn_frame, text="Розшифрувати (Нелінійний)", command=decrypt_tritemius)
# decrypt_tritemius_btn.pack(side=tk.LEFT, padx=5)

# # Кнопки для шифру за гаслом
# encrypt_keyword_btn = tk.Button(btn_frame, text="Зашифрувати (Гасло)", command=encrypt_keyword)
# encrypt_keyword_btn.pack(side=tk.LEFT, padx=5)

# decrypt_keyword_btn = tk.Button(btn_frame, text="Розшифрувати (Гасло)", command=decrypt_keyword)
# decrypt_keyword_btn.pack(side=tk.LEFT, padx=5)

# # Додаткова кнопка для очищення всіх текстових полів
# def clear_text():
#     original_text_area.delete("1.0", tk.END)
#     encrypted_text_area.delete("1.0", tk.END)
#     decrypted_text_area.delete("1.0", tk.END)

# clear_btn = tk.Button(btn_frame, text="Очистити поля", command=clear_text)
# clear_btn.pack(side=tk.LEFT, padx=5)

# # Вихід з програми
# exit_btn = tk.Button(btn_frame, text="Вихід", command=exit_app)
# exit_btn.pack(side=tk.LEFT, padx=5)

# # Запуск графічного інтерфейсу
# root.mainloop()




import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from string import digits, punctuation
from math import gcd
from collections import Counter


UKRAINIAN_ALPHABET = {
    'upper': 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ',
    'lower': 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
}

ENGLISH_ALPHABET = {
    'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'lower': 'abcdefghijklmnopqrstuvwxyz'
}


def frequency_table():
    input_text = text_input.get("1.0", tk.END).strip()
    encrypted_text = text_output_encrypt.get("1.0", tk.END).strip()

    language = language_var.get()
    alphabet = get_alphabet(language)
    full_alphabet = alphabet['upper'] + alphabet['lower']

    def calculate_frequencies(text):
        filtered_text = [char for char in text if char in full_alphabet]
        frequency = Counter(filtered_text)
        total = sum(frequency.values())
        frequencies = {char: (count / total) * 100 for char, count in frequency.items()}
        return frequencies

    input_frequencies = calculate_frequencies(input_text)
    encrypted_frequencies = calculate_frequencies(encrypted_text)

    table_window = tk.Toplevel(root)
    table_window.title("Частотна таблиця")
    table_window.geometry("600x400+550+200")
    table_window.configure(bg="#a9a9a9")

    columns = ("Символ", "Частота (вхідний текст)", "Частота (зашифрований текст)")
    tree = ttk.Treeview(table_window, columns=columns, show="headings")
    tree.heading("Символ", text="Символ")
    tree.heading("Частота (вхідний текст)", text="Частота (вхідний текст)")
    tree.heading("Частота (зашифрований текст)", text="Частота (зашифрований текст)")
    tree.column("Символ", width=100, anchor=tk.CENTER)
    tree.column("Частота (вхідний текст)", width=200, anchor=tk.CENTER)
    tree.column("Частота (зашифрований текст)", width=200, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for char in full_alphabet:
        input_freq = input_frequencies.get(char, 0)
        encrypted_freq = encrypted_frequencies.get(char, 0)
        tree.insert("", tk.END, values=(char, f"{input_freq:.2f}%", f"{encrypted_freq:.2f}%"))

    close_button = tk.Button(table_window, text="Закрити", command=table_window.destroy, bg="lightblue", font=('Arial', 10))
    close_button.pack(pady=10)

def get_key_params():
    key_type = key_type_var.get()
    params = {}

    for widget in key_params_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            param_name = widget.winfo_name()
            params[param_name] = widget.get()

    return key_type, params

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def find_linear_key(shifts, mod):
    key_type, params = get_key_params()
    if key_type != "Лінійний":
        return None

    try:
        A = int(params.get("a", 0))
        B = int(params.get("b", 0))
    except ValueError:
        return None

    return ('Лінійний', {'a': A, 'b': B})


def find_keyword_key(shifts, mod, language):
    key_type, params = get_key_params()
    if key_type != "Гасло":
        return None

    keyword = params.get("keyword", "").strip()
    if not keyword:
        return None

    return ('Гасло', {'keyword': keyword})


def find_quadratic_key(shifts, mod):
    key_type, params = get_key_params()
    if key_type != "Квадратичний":
        return None

    try:
        A = int(params.get("a", 0))
        B = int(params.get("b", 0))
        C = int(params.get("c", 0))
    except ValueError:
        return None

    return ('Квадратичний', {'a': A, 'b': B, 'c': C})



def crack_key():
    def analyze():
        plain = text_input.get("1.0", tk.END).strip()
        cipher = text_output_encrypt.get("1.0", tk.END).strip()
        language = language_var.get()

        if not plain or not cipher:
            messagebox.showerror("Помилка", "Введіть відкритий текст у ліве поле та зашифрований текст у праве поле!")
            return

        if len(plain) != len(cipher):
            messagebox.showwarning("Увага", "Тексти мають різну довжину! Аналіз може бути неточним.")

        alphabet = get_alphabet(language)
        full_alphabet = alphabet['upper'] + alphabet['lower']
        mod = get_mod(alphabet)

        shifts = []
        for p in range(min(len(plain), len(cipher))):
            pc = plain[p]
            cc = cipher[p]
            if pc in full_alphabet and cc in full_alphabet:
                pi = full_alphabet.index(pc)
                ci = full_alphabet.index(cc)
                shift = (ci - pi) % mod
                shifts.append((p, shift))

        key = find_quadratic_key(shifts, mod)

        if not key:
            key = find_linear_key(shifts, mod)

        if not key:
            key = find_keyword_key(shifts, mod, language)

        if key:
            key_type, params = key
            result = f"Тип ключа: {key_type}\nПараметри:\n"
            for k, v in params.items():
                result += f"{k}: {v}\n"
            result_label.config(text=result)
        else:
            result_label.config(
                text="Ключ не знайдено. Можливі причини:\n- Тексти не пов'язані\n- Короткі тексти\n- Невідповідність типу ключа")

    attack_window = tk.Toplevel(root)
    attack_window.title("Атака на шифр")
    attack_window.geometry("500x300+550+200")
    attack_window.configure(bg="#a9a9a9")

    info_text = """            Щоб атака спрацювала потрібно 
           ввести текст у поле 'Вхідний текст'
    та зашифрувати його (кнопка 'Шифрувати')"""

    lang_frame = tk.Frame(attack_window, bg="#a9a9a9")
    lang_frame.pack(pady=5)
    tk.Label(lang_frame, text="Мова атаки:", bg="#a9a9a9").pack(side=tk.LEFT)

    tk.Label(attack_window, text=info_text, bg="#a9a9a9", justify=tk.LEFT).pack(pady=10)

    analyze_btn = tk.Button(attack_window, text="Запустити аналіз", command=analyze,
                            bg="#0275d8", font=('Arial', 10))
    analyze_btn.pack(pady=10)

    frequency_table_btn = tk.Button(attack_window, text="Частотна таблиця", command=frequency_table,
                            bg="#0275d8", font=('Arial', 10))
    frequency_table_btn.pack(pady=10)

    result_label = tk.Label(attack_window, text="", bg="#a9a9a9", justify=tk.LEFT)
    result_label.pack()


def get_alphabet(language):
    return UKRAINIAN_ALPHABET if language == "Українська" else ENGLISH_ALPHABET


def get_mod(language):
    alphabet = get_alphabet(language)
    return len(alphabet['upper'] + alphabet['lower'])


def shift_char(char, shift, language):
    alphabet = get_alphabet(language)
    full_alphabet = alphabet['upper'] + alphabet['lower']
    if char not in full_alphabet:
        return char
    index = full_alphabet.index(char)
    new_index = (index + shift) % len(full_alphabet)
    return full_alphabet[new_index]


def shift_char_decrypt(char, shift, language):
    alphabet = get_alphabet(language)
    full_alphabet = alphabet['upper'] + alphabet['lower']

    if char in full_alphabet:
        index = full_alphabet.index(char)
        new_index = (index - shift) % len(full_alphabet)
        return full_alphabet[new_index]
    return char


def get_shifts(key, language):
    mod = get_mod(language)
    alphabet = get_alphabet(language)['upper']
    return [alphabet.index(c.upper()) % mod for c in key if c.upper() in alphabet]


def validate_linear(key_params):
    try:
        A = int(key_params.get('a', 0))
        B = int(key_params.get('b', 0))
        return (A, B)
    except:
        return None


def validate_quadratic(key_params):
    try:
        A = int(key_params.get('a', 0))
        B = int(key_params.get('b', 0))
        C = int(key_params.get('c', 0))
        return (A, B, C)
    except:
        return None


def validate_keyword(key_params):
    keyword = key_params.get('keyword', '').strip()
    return keyword if keyword else None


def encrypt_text():
    plaintext = text_input.get("1.0", tk.END).strip()
    language = language_var.get()

    if not validate_text(plaintext, language):
        messagebox.showerror("Помилка", "Текст містить символи, які не належать до обраного алфавіту!")
        return

    key_type = key_type_var.get()
    language = language_var.get()
    mod = get_mod(language)

    key_params = {}
    for child in key_params_frame.winfo_children():
        if isinstance(child, tk.Entry):
            key_params[child.winfo_name()] = child.get()

    key = None
    if key_type == "Лінійний":
        key = validate_linear(key_params)
    elif key_type == "Квадратичний":
        key = validate_quadratic(key_params)
    elif key_type == "Гасло":
        key = validate_keyword(key_params)

    if not key:
        messagebox.showerror("Помилка", "Невірні параметри ключа")
        return

    ciphertext = []
    for p, char in enumerate(plaintext):
        if char in get_alphabet(language)['upper'] + get_alphabet(language)['lower']:
            if key_type == "Лінійний":
                A, B = key
                k = (A * p + B) % mod
            elif key_type == "Квадратичний":
                A, B, C = key
                k = (A * p ** 2 + B * p + C) % mod
            elif key_type == "Гасло":
                shifts = get_shifts(key, language)
                k = shifts[p % len(shifts)] % mod if shifts else 0
            ciphertext.append(shift_char(char, k, language))
        else:
            ciphertext.append(char)
    text_output_encrypt.delete(1.0, tk.END)
    text_output_encrypt.insert(tk.END, ''.join(ciphertext))


def decrypt_text():
    ciphertext = text_output_encrypt.get("1.0", tk.END).strip()
    language = language_var.get()

    if not validate_text(ciphertext, language):
        messagebox.showerror("Помилка", "Текст містить символи, які не належать до обраного алфавіту!")
        return

    key_type = key_type_var.get()
    language = language_var.get()
    mod = get_mod(language)

    key_params = {}
    for child in key_params_frame.winfo_children():
        if isinstance(child, tk.Entry):
            key_params[child.winfo_name()] = child.get()

    key = None
    if key_type == "Лінійний":
        key = validate_linear(key_params)
    elif key_type == "Квадратичний":
        key = validate_quadratic(key_params)
    elif key_type == "Гасло":
        key = validate_keyword(key_params)

    if not key:
        messagebox.showerror("Помилка", "Невірні параметри ключа")
        return

    plaintext = []
    for p, char in enumerate(ciphertext):
        if char in get_alphabet(language)['upper'] + get_alphabet(language)['lower']:
            if key_type == "Лінійний":
                A, B = key
                k = (A * p + B) % mod
            elif key_type == "Квадратичний":
                A, B, C = key
                k = (A * p ** 2 + B * p + C) % mod
            elif key_type == "Гасло":
                shifts = get_shifts(key, language)
                k = shifts[p % len(shifts)] % mod if shifts else 0
            plaintext.append(shift_char_decrypt(char, k, language))
        else:
            plaintext.append(char)
    text_output_decrypt.delete(1.0, tk.END)
    text_output_decrypt.insert(tk.END, ''.join(plaintext))


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося відкрити файл: {str(e)}")


def save_file():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not filepath:
        return
    try:
        content = text_output_encrypt.get("1.0", tk.END)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Успіх", "Файл успішно збережено!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {str(e)}")


def clear_input():
    text_input.delete("1.0", tk.END)
    text_output_encrypt.delete("1.0", tk.END)
    text_output_decrypt.delete("1.0", tk.END)


def paste_from_clipboard():
    try:
        clipboard_text = root.clipboard_get()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, clipboard_text)
    except tk.TclError:
        messagebox.showerror("Помилка", "Буфер обміну порожній або містить не текст")


def copy_to_clipboard():
    copy_window = tk.Toplevel(root)
    copy_window.title("Виберіть джерело")
    screen_width = copy_window.winfo_screenwidth()
    screen_height = copy_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    copy_window.geometry(f"300x100+{center_x}+{center_y}")
    copy_window.configure(bg="#a9a9a9")
    copy_window.grab_set()

    def copy_from_source(source):
        if source == "encrypted":
            text = text_output_encrypt.get("1.0", tk.END)
        else:
            text = text_output_decrypt.get("1.0", tk.END)

        root.clipboard_clear()
        root.clipboard_append(text)
        copy_window.destroy()
        messagebox.showinfo("Копіювання", "Текст успішно скопійовано в буфер обміну!")

    frame = tk.Frame(copy_window, bg="#a9a9a9")
    frame.pack(pady=15)

    tk.Button(frame, text="Шифрований текст", command=lambda: copy_from_source("encrypted"),
              width=15, bg="#0275d8").pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Дешифрований текст", command=lambda: copy_from_source("decrypted"),
              width=15, bg="#0275d8").pack(side=tk.LEFT, padx=5)


def show_info():
    messagebox.showinfo("Про розробника", "Шифр Тритеміуса\nРозробник: Тригуб Марта ПМІ-36")


def brute_force_attack():
    messagebox.showinfo("Інформація", "Функція в розробці")


def show_frequency_table():
    messagebox.showinfo("Інформація", "Функція в розробці")

def update_key_params(*args):
    for widget in key_params_frame.winfo_children():
        widget.destroy()

    key_type = key_type_var.get()
    if key_type == "Лінійний":
        tk.Label(key_params_frame, text="A:", bg="#a9a9a9").pack(side=tk.LEFT)
        a_entry = tk.Entry(key_params_frame, width=5, name="a")
        a_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(key_params_frame, text="B:", bg="#a9a9a9").pack(side=tk.LEFT)
        b_entry = tk.Entry(key_params_frame, width=5, name="b")
        b_entry.pack(side=tk.LEFT, padx=2)
    elif key_type == "Квадратичний":
        tk.Label(key_params_frame, text="A:", bg="#a9a9a9").pack(side=tk.LEFT)
        a_entry = tk.Entry(key_params_frame, width=5, name="a")
        a_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(key_params_frame, text="B:", bg="#a9a9a9").pack(side=tk.LEFT)
        b_entry = tk.Entry(key_params_frame, width=5, name="b")
        b_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(key_params_frame, text="C:", bg="#a9a9a9").pack(side=tk.LEFT)
        c_entry = tk.Entry(key_params_frame, width=5, name="c")
        c_entry.pack(side=tk.LEFT, padx=2)
    elif key_type == "Гасло":
        tk.Label(key_params_frame, text="Гасло:", bg="#a9a9a9").pack(side=tk.LEFT)
        keyword_entry = tk.Entry(key_params_frame, width=20, name="keyword")
        keyword_entry.pack(side=tk.LEFT, padx=2)


def validate_text(text, language):
    alphabet = get_alphabet(language)
    full_alphabet = alphabet['upper'] + alphabet['lower']

    for char in text:
        if char not in full_alphabet and char not in [' ', '\n', '\t']:  # Дозволяємо пробіли та інші спецсимволи
            return False
    return True

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Шифр Тритеміуса")
    root.configure(bg="#a9a9a9")

    window_width = 1000
    window_height = 500
    root.resizable(False, False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    main_frame = tk.Frame(root, bg="#a9a9a9")
    main_frame.grid(pady=15, padx=15, sticky="nsew")

    top_buttons = tk.Frame(main_frame, bg="#a9a9a9")
    top_buttons.grid(row=0, column=0, columnspan=3, pady=10)

    tk.Button(top_buttons, text="Відкрити файл", command=open_file, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Зберегти результат", command=save_file, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Копіювати", command=copy_to_clipboard, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Вставити", command=paste_from_clipboard, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Про програму", command=show_info, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Атака", command=crack_key, width=15,
              bg="#0275d8", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(top_buttons, text="Вихід", command=root.quit, width=15,
              bg="#d9534f", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    

    language_frame = tk.Frame(main_frame, bg="#a9a9a9")
    language_frame.grid(row=1, column=0, columnspan=3, pady=5)
    tk.Label(language_frame, text="Мова:", bg="#a9a9a9", font=('Arial', 10)).pack(side=tk.LEFT)
    language_var = tk.StringVar(value="Українська")
    language_menu = ttk.Combobox(language_frame, textvariable=language_var,
                                 values=["Українська", "Англійська"], state="readonly", width=15)
    language_menu.pack(side=tk.LEFT, padx=5)

    key_type_frame = tk.Frame(main_frame, bg="#a9a9a9")
    key_type_frame.grid(row=2, column=0, columnspan=3, pady=5)
    tk.Label(key_type_frame, text="Тип ключа:", bg="#a9a9a9", font=('Arial', 10)).pack(side=tk.LEFT)
    key_type_var = tk.StringVar(value="Лінійний")
    key_type_menu = ttk.Combobox(key_type_frame, textvariable=key_type_var,
                                 values=["Лінійний", "Квадратичний", "Гасло"], state="readonly", width=15)
    key_type_menu.pack(side=tk.LEFT, padx=5)
    key_type_var.trace("w", update_key_params)

    key_params_frame = tk.Frame(main_frame, bg="#a9a9a9")
    key_params_frame.grid(row=3, column=0, columnspan=3, pady=5)
    update_key_params()

    text_frame = tk.Frame(main_frame, bg="#a9a9a9")
    text_frame.grid(row=4, column=0, pady=10, sticky="nsew")

    tk.Label(text_frame, text="Вхідний текст:", bg="#a9a9a9", font=('Arial', 10)).pack()
    text_input = tk.Text(text_frame, height=10, width=60, font=('Arial', 10))
    text_input.pack()

    output_frame = tk.Frame(main_frame, bg="#a9a9a9")
    output_frame.grid(row=4, column=1, pady=10, sticky="nsew")

    tk.Label(output_frame, text="Результат шифрування:", bg="#a9a9a9", font=('Arial', 10)).pack()
    text_output_encrypt = tk.Text(output_frame, height=5, width=60, font=('Arial', 10))
    text_output_encrypt.pack()

    tk.Label(output_frame, text="Результат дешифрування:", bg="#a9a9a9", font=('Arial', 10)).pack()
    text_output_decrypt = tk.Text(output_frame, height=5, width=60, font=('Arial', 10))
    text_output_decrypt.pack()

    buttons_frame = tk.Frame(main_frame, bg="#a9a9a9")
    buttons_frame.grid(row=5, column=0, columnspan=3, pady=10)

    tk.Button(buttons_frame, text="Шифрувати", command=encrypt_text, width=15,
              bg="#5cb85c", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Дешифрувати", command=decrypt_text, width=15,
              bg="#f0ad4e", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    tk.Button(buttons_frame, text="Очистити", command=clear_input, width=15,
              bg="#d9534f", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

    root.mainloop()