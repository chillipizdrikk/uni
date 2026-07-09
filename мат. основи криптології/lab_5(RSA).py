import tkinter as tk
from tkinter import messagebox, ttk
import random

def mod_exp(base, exp, mod):
    """
    Ефективне модульне піднесення до степеня.
    base: Основа
    exp: Показник степеня
    mod: Модуль
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def generate_keys():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())

        if p <= 0 or g <= 0:
            raise ValueError("Числа p і g повинні бути більшими за 0.")
        
        private_key = random.randint(1, p - 1)  # Генерація приватного ключа
        public_key = mod_exp(g, private_key, p)  # Обчислення публічного ключа

        # Виведення ключів у відповідні поля
        entry_private_key.delete(0, tk.END)
        entry_private_key.insert(0, str(private_key))

        entry_public_key.delete(0, tk.END)
        entry_public_key.insert(0, str(public_key))
    except Exception as ex:
        messagebox.showerror("Помилка", str(ex))

def calculate_shared_key():
    try:
        p = int(entry_p.get())
        private_key = int(entry_private_key.get())
        other_public_key = int(entry_other_public_key.get())

        if p <= 0:
            raise ValueError("Число p повинно бути більше за 0.")
        
        # Обчислення спільного ключа
        shared_key = mod_exp(other_public_key, private_key, p)
        entry_shared_key.delete(0, tk.END)
        entry_shared_key.insert(0, str(shared_key))
    except Exception as ex:
        messagebox.showerror("Помилка", str(ex))

# --- Вікно ---
root = tk.Tk()
root.title("Протокол обміну ключами Діффі-Геллмана")
root.geometry("600x500")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TEntry", font=("Arial", 12))

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Заголовок
ttk.Label(frame, text="Протокол обміну ключами Діффі-Геллмана", font=("Arial", 16, "bold")).pack(pady=10)

# Розділювач
ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

# Введення параметрів p і g
param_frame = ttk.Frame(frame, padding=10)
param_frame.pack()

ttk.Label(param_frame, text="p (просте число):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_p = ttk.Entry(param_frame, width=40)
entry_p.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(param_frame, text="g (примітивний корінь):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_g = ttk.Entry(param_frame, width=40)
entry_g.grid(row=1, column=1, padx=5, pady=5)

# Генерація ключів
ttk.Button(frame, text="Згенерувати ключі", command=generate_keys).pack(pady=10)

# Відображення приватного і публічного ключів
key_frame = ttk.Frame(frame, padding=10)
key_frame.pack()

ttk.Label(key_frame, text="Приватний ключ:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_private_key = ttk.Entry(key_frame, width=40)
entry_private_key.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(key_frame, text="Публічний ключ:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_public_key = ttk.Entry(key_frame, width=40)
entry_public_key.grid(row=1, column=1, padx=5, pady=5)

# Розділювач
ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

# Введення публічного ключа іншого учасника
ttk.Label(frame, text="Публічний ключ іншого учасника:").pack(anchor="center", pady=(10, 5))
entry_other_public_key = ttk.Entry(frame, width=50)
entry_other_public_key.pack(pady=(0, 10))

# Обчислення спільного ключа
ttk.Button(frame, text="Обчислити спільний ключ", command=calculate_shared_key).pack(pady=10)

# Відображення спільного ключа
ttk.Label(frame, text="Спільний ключ:").pack(anchor="center", pady=(10, 5))
entry_shared_key = ttk.Entry(frame, width=50)
entry_shared_key.pack(pady=(0, 10))

root.mainloop()