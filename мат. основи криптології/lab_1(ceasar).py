import tkinter as tk
from collections import Counter
from tkinter import filedialog, messagebox

ukr_alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
eng_alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = '.,!?/"()'


def detect_language(text):
    has_ukr = any(char.lower() in ukr_alphabet for char in text if char.isalpha())
    has_eng = any(char.lower() in eng_alphabet for char in text if char.isalpha())

    if has_ukr and not has_eng:
        return 'ukr'
    elif has_eng and not has_ukr:
        return 'eng'
    else:
        return 'mixed'


def caesar_cipher(text, shift):
    lang = detect_language(text)
    if lang == 'mixed':
        return "Помилка. Текст містить різні мови"

    alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
    alphabet_size = len(alphabet)
    shift = shift % alphabet_size
    result = ""

    symbol_size = len(symbols)

    for char in text:
        if char.lower() in alphabet:
            base = alphabet.index(char.lower())
            new_char = alphabet[(base + shift) % alphabet_size]
            result += new_char.upper() if char.isupper() else new_char
        elif char in symbols:
            base = symbols.index(char)
            new_char = symbols[(base + shift) % symbol_size]
            result += new_char
        else:
            result += char

    return result


def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)


def brute_force_decrypt(text):
    possible_decryptions = []
    for shift in range(1, len(ukr_alphabet)):
        decrypted_text = caesar_decipher(text, shift)
        possible_decryptions.append((shift, decrypted_text))
    return possible_decryptions


def check_encrypted_length():
    original_text = original_text_area.get("1.0", tk.END).strip()
    encrypted_text = encrypted_text_area.get("1.0", tk.END).strip()

    if len(original_text) != len(encrypted_text):
        messagebox.showerror("Помилка",
                             "Кількість символів в оригінальному та зашифрованому тексті повинна бути однаковою!")
        return False
    return True


def check_all_lengths():
    original_text = original_text_area.get("1.0", tk.END).strip()
    encrypted_text = encrypted_text_area.get("1.0", tk.END).strip()
    decrypted_text = decrypted_text_area.get("1.0", tk.END).strip()

    if not (len(original_text) == len(encrypted_text) == len(decrypted_text)):
        messagebox.showerror("Помилка",
                             "Кількість символів в оригінальному, зашифрованому та розшифрованому текстах повинна бути однаковою!")
        return False
    return True


def encrypt_text():
    text = original_text_area.get("1.0", tk.END).strip()
    shift = int(shift_entry.get())
    encrypted_text = caesar_cipher(text, shift)
    encrypted_text_area.delete("1.0", tk.END)
    encrypted_text_area.insert(tk.END, encrypted_text)

    # Сповіщення після шифрування
    if len(text) == len(encrypted_text):
        messagebox.showinfo("Успішно", f"Шифрування завершено! Кількість символів зашифрованого тексту відповідає оригінальному.\nКількість символів: {len(text)}")


def decrypt_text():
    shift = int(shift_entry.get())
    text = encrypted_text_area.get("1.0", tk.END).strip()
    decrypted_text = caesar_decipher(text, shift)

    decrypted_text_area.delete("1.0", tk.END)
    decrypted_text_area.insert(tk.END, decrypted_text)

    # Перевірка кількості символів після розшифрування
    original_text = original_text_area.get("1.0", tk.END).strip()
    if len(original_text) == len(decrypted_text):
        messagebox.showinfo("Розшифрування", f"Отримано рошифрований текст! Кількість символів відповідає оригінальному.\nКількість символів: {len(text)}")
    else:
        messagebox.showerror("Помилка", "Кількість символів у розшифрованому тексті не збігається з оригіналом!")


def brute_force_decrypt_text():
    text = encrypted_text_area.get("1.0", tk.END).strip()
    decrypted_possibilities = brute_force_decrypt(text)

    result_window = tk.Toplevel(root)
    result_window.title("Груба сила - розшифрування")
    text_widget = tk.Text(result_window, wrap=tk.WORD, font=("Arial", 12), width=80, height=20)
    for shift, decrypted_text in decrypted_possibilities:
        text_widget.insert(tk.END, f"Зсув {shift}: {decrypted_text}\n\n")
    text_widget.pack(padx=10, pady=10)


def clear_text():
    original_text_area.delete("1.0", tk.END)
    encrypted_text_area.delete("1.0", tk.END)
    decrypted_text_area.delete("1.0", tk.END)


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            original_text_area.delete("1.0", tk.END)
            original_text_area.insert(tk.END, file.read())


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(encrypted_text_area.get("1.0", tk.END))


def show_about():
    messagebox.showinfo("Відомості", "Розробник: Тригуб Марта \nГрупа: ПМІ-36")


def exit_app():
    root.quit()

def build_frequency_table(text, title):
    lang = detect_language(text)
    if lang == 'mixed':
        messagebox.showerror("Помилка", "Текст містить різні мови")
        return

    alphabet = ukr_alphabet if lang == 'ukr' else eng_alphabet
    filtered_text = [char for char in text if char in alphabet]
    filtered_symbols = [char for char in text if char in symbols]

    freq_counter = Counter(filtered_text)
    symbol_counter = Counter(filtered_symbols)

    total_chars = sum(freq_counter.values())
    total_symbols = sum(symbol_counter.values())

    freq_table = {char: round(count / total_chars * 100, 2) for char, count in freq_counter.items()}
    symbol_table = {char: round(count / total_symbols * 100, 2) for char, count in symbol_counter.items()}

    results = "Частотна таблиця літер:\n" + "\n".join(
        f"{char}: {freq}%" for char, freq in sorted(freq_table.items(), key=lambda item: item[1], reverse=True))
    results += "\n\nЧастотна таблиця символів:\n" + "\n".join(
        f"{char}: {freq}%" for char, freq in sorted(symbol_table.items(), key=lambda item: item[1], reverse=True))

    result_window = tk.Toplevel(root)
    result_window.title(f"Частотний аналіз: {title}")
    text_widget = tk.Text(result_window, wrap=tk.WORD, font=("Arial", 12), width=60, height=15)
    text_widget.insert(tk.END, results)
    text_widget.pack(padx=10, pady=10)


def show_frequency_tables():
    original_text = original_text_area.get("1.0", tk.END).strip().lower()
    encrypted_text = encrypted_text_area.get("1.0", tk.END).strip().lower()
    decrypted_text = decrypted_text_area.get("1.0", tk.END).strip().lower()

    build_frequency_table(original_text, "Оригінальний текст")
    build_frequency_table(encrypted_text, "Зашифрований текст")
    build_frequency_table(decrypted_text, "Розшифрований текст")


root = tk.Tk()
root.title("Шифр Цезаря")

# Меню
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Відкрити", command=open_file)
file_menu.add_command(label="Зберегти", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Вихід", command=exit_app)
menu_bar.add_cascade(label="Файл", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Відомості", command=show_about)
menu_bar.add_cascade(label="Допомога", menu=help_menu)
root.config(menu=menu_bar)

# Поле для введення оригінального тексту
tk.Label(root, text="Оригінальний текст:").pack()
original_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
original_text_area.pack(padx=10, pady=5)

# Поле для зашифрованого тексту
tk.Label(root, text="Зашифрований текст:").pack()
encrypted_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
encrypted_text_area.pack(padx=10, pady=5)

# Поле для розшифрованого тексту
tk.Label(root, text="Розшифрований текст:").pack()
decrypted_text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=60, height=5)
decrypted_text_area.pack(padx=10, pady=5)

# Поле для введення зсуву
shift_frame = tk.Frame(root)
shift_frame.pack(pady=5)
tk.Label(shift_frame, text="Зсув:").pack(side=tk.LEFT, padx=5)
shift_entry = tk.Entry(shift_frame, width=5)
shift_entry.pack(side=tk.LEFT)
shift_entry.insert(0, "5")

# Кнопки
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

encrypt_btn = tk.Button(btn_frame, text="Зашифрувати", command=encrypt_text)
encrypt_btn.pack(side=tk.LEFT, padx=5)

decrypt_btn = tk.Button(btn_frame, text="Розшифрувати", command=decrypt_text)
decrypt_btn.pack(side=tk.LEFT, padx=5)

brute_force_btn = tk.Button(btn_frame, text="Груба сила", command=brute_force_decrypt_text)
brute_force_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(btn_frame, text="Очистити", command=clear_text)
clear_btn.pack(side=tk.LEFT, padx=5)

frequency_btn = tk.Button(btn_frame, text="Частотний аналіз", command=show_frequency_tables)
frequency_btn.pack(side=tk.LEFT, padx=5)

exit_btn = tk.Button(btn_frame, text="Вихід", command=exit_app)
exit_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
