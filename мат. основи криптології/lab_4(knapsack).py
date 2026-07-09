import tkinter as tk
from tkinter import messagebox
import random
import logging
logging.basicConfig(level=logging.DEBUG)

# Функції для генерування ключів та шифрування
def generate_superincreasing_sequence(length):
    """
    Генерує суперзростаючу послідовність заданої довжини.
    """
    sequence = [random.randint(1, 10)]
    for _ in range(1, length):
        sequence.append(sum(sequence) + random.randint(1, 10))
    logging.debug(f"Згенерована суперзростаюча послідовність: {sequence}")
    return sequence

def generate_public_key(private_key, multiplier, modulus):
    """
    Генерує відкритий ключ на основі приватного ключа, множника та модуля.
    """
    public_key = [(multiplier * x) % modulus for x in private_key]
    logging.debug(f"Згенерований відкритий ключ: {public_key}")
    return public_key

def encrypt_knapsack(message, public_key):
    """
    Шифрує повідомлення за допомогою відкритого ключа.
    """
    binary_message = [int(bit) for bit in message]
    logging.debug(f"Бінарне повідомлення: {binary_message}")
    encrypted_value = sum(m * pk for m, pk in zip(binary_message, public_key))
    logging.debug(f"Зашифроване значення: {encrypted_value}")
    return encrypted_value

def decrypt_knapsack(encrypted_value, private_key, modulus, multiplier, inverse_multiplier):
    """
    Розшифровує повідомлення за допомогою приватного ключа.
    """
    transformed_value = (encrypted_value * inverse_multiplier) % modulus
    logging.debug(f"Значення після трансформації (S'): {transformed_value}")

    decrypted_message = []
    for weight in reversed(private_key):
        if transformed_value >= weight:
            decrypted_message.append(1)
            transformed_value -= weight
        else:
            decrypted_message.append(0)

    decrypted_message = ''.join(map(str, reversed(decrypted_message)))
    logging.debug(f"Розшифроване бінарне повідомлення: {decrypted_message}")
    return decrypted_message

# Інтерфейс Tkinter
def generate_keys():
    """
    Генерує приватний і відкритий ключі.
    """
    try:
        length = int(key_length.get())
        modulus = int(modulus_entry.get())
        multiplier = int(multiplier_entry.get())

        if modulus <= 0 or multiplier <= 0:
            raise ValueError("Модуль та множник повинні бути більшими за нуль.")

        private = generate_superincreasing_sequence(length)
        public = generate_public_key(private, multiplier, modulus)

        private_key_text.delete("1.0", tk.END)
        private_key_text.insert(tk.END, ', '.join(map(str, private)))

        public_key_text.delete("1.0", tk.END)
        public_key_text.insert(tk.END, ', '.join(map(str, public)))

        # Обчислюємо обернене значення множника
        inverse_multiplier.set(pow(multiplier, -1, modulus))
        logging.debug(f"Обернене значення множника (t⁻¹): {inverse_multiplier.get()}")

    except ValueError as e:
        messagebox.showerror("Помилка", f"Неправильне введення: {e}")

def encrypt():
    """
    Виконує шифрування тексту.
    """
    try:
        message = binary_message.get("1.0", tk.END).strip()
        public_key = list(map(int, public_key_text.get("1.0", tk.END).strip().split(',')))

        if not all(bit in '01' for bit in message):
            raise ValueError("Повідомлення повинно містити тільки біти (0 або 1).")

        encrypted_value = encrypt_knapsack(message, public_key)
        encrypted_text.delete("1.0", tk.END)
        encrypted_text.insert(tk.END, str(encrypted_value))
    except ValueError as e:
        messagebox.showerror("Помилка", f"Неправильне введення: {e}")

def decrypt():
    """
    Виконує розшифрування тексту.
    """
    try:
        encrypted_value = int(encrypted_text.get("1.0", tk.END).strip())
        private_key = list(map(int, private_key_text.get("1.0", tk.END).strip().split(',')))
        modulus = int(modulus_entry.get())
        multiplier = int(multiplier_entry.get())

        inv_multiplier = inverse_multiplier.get()
        decrypted_message = decrypt_knapsack(encrypted_value, private_key, modulus, multiplier, inv_multiplier)
        decrypted_text.delete("1.0", tk.END)
        decrypted_text.insert(tk.END, decrypted_message)
    except ValueError as e:
        messagebox.showerror("Помилка", f"Неправильне введення: {e}")

def show_about():
    messagebox.showinfo("Про програму", "Шифрування на основі задачі рюкзака")

def exit_app():
    root.quit()

# Створення інтерфейсу
root = tk.Tk()
root.title("Шифрування на основі задачі рюкзака")
root.configure(bg="#f0f0f0")

# Змінна для оберненого значення множника
inverse_multiplier = tk.IntVar()

# Елементи інтерфейсу
tk.Label(root, text="Довжина ключа:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
key_length = tk.Entry(root)
key_length.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Модуль (q):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
modulus_entry = tk.Entry(root)
modulus_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Множник (w):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
multiplier_entry = tk.Entry(root)
multiplier_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Згенерувати ключі", command=generate_keys, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(root, text="Приватний ключ:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5)
private_key_text = tk.Text(root, height=3, width=50)
private_key_text.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Публічний ключ:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=5)
public_key_text = tk.Text(root, height=3, width=50)
public_key_text.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Обернене значення (t⁻¹):", bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=5)
tk.Label(root, textvariable=inverse_multiplier, bg="#f0f0f0").grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Бінарне повідомлення:", bg="#f0f0f0").grid(row=7, column=0, padx=10, pady=5)
binary_message = tk.Text(root, height=3, width=50)
binary_message.grid(row=7, column=1, padx=10, pady=5)

tk.Button(root, text="Зашифрувати", command=encrypt, bg="#2196F3", fg="white").grid(row=8, column=0, columnspan=2, pady=10)

tk.Label(root, text="Зашифрований текст:", bg="#f0f0f0").grid(row=9, column=0, padx=10, pady=5)
encrypted_text = tk.Text(root, height=3, width=50)
encrypted_text.grid(row=9, column=1, padx=10, pady=5)

tk.Button(root, text="Розшифрувати", command=decrypt, bg="#2196F3", fg="white").grid(row=10, column=0, columnspan=2, pady=10)

tk.Label(root, text="Розшифрований текст:", bg="#f0f0f0").grid(row=11, column=0, padx=10, pady=5)
decrypted_text = tk.Text(root, height=3, width=50)
decrypted_text.grid(row=11, column=1, padx=10, pady=5)

tk.Button(root, text="Про програму", command=show_about, bg="#FF9800", fg="white").grid(row=12, column=0, pady=10)
tk.Button(root, text="Вихід", command=exit_app, bg="#F44336", fg="white").grid(row=12, column=1, pady=10)

# Запуск програми
root.mainloop()