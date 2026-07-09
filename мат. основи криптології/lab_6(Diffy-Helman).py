import tkinter as tk
from tkinter import ttk, messagebox

def power_mod(base, exponent, mod):
    result = 1
    base %= mod
    while exponent > 0:
        if exponent % 2:
            result = (result * base) % mod
        exponent //= 2
        base = (base * base) % mod
    return result

def diffie_hellman(p, g, a, b):
    A = power_mod(g, a, p)
    B = power_mod(g, b, p)
    K_A = power_mod(B, a, p)
    K_B = power_mod(A, b, p)
    return A, B, K_A, K_B

def calculate():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        a = int(entry_a.get())
        b = int(entry_b.get())

        A, B, K_A, K_B = diffie_hellman(p, g, a, b)

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Відкритий ключ A: {A}\n")
        result_text.insert(tk.END, f"Відкритий ключ B: {B}\n")
        result_text.insert(tk.END, f"Спільний ключ (A): {K_A}\n")
        result_text.insert(tk.END, f"Спільний ключ (B): {K_B}\n")

        if K_A == K_B:
            result_text.insert(tk.END, "\nУспішний обмін ключами!", "success")
        else:
            result_text.insert(tk.END, "\nПомилка в обміні!", "error")
        
        result_text.tag_config("success", foreground="green")
        result_text.tag_config("error", foreground="red")
        result_text.config(state=tk.DISABLED)
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильні цілі числа!")

def autofill_example():
    entry_p.delete(0, tk.END)
    entry_g.delete(0, tk.END)
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)

    # entry_p.insert(0, "17")
    # entry_g.insert(0, "3")
    # entry_a.insert(0, "15")
    # entry_b.insert(0, "13")

root = tk.Tk()
root.title("Diffie-Hellman Key Exchange")
root.geometry("500x500")
root.resizable(False, False)

# Header
header = tk.Label(root, text="Diffie-Hellman Key Exchange", font=("Arial", 16, "bold"), pady=10)
header.pack()

# Input frame
input_frame = ttk.LabelFrame(root, text="Вхідні дані", padding=10)
input_frame.pack(padx=20, pady=10, fill="x")

ttk.Label(input_frame, text="Просте число p:").grid(row=0, column=0, sticky="w", pady=5)
entry_p = ttk.Entry(input_frame, width=20)
entry_p.grid(row=0, column=1, pady=5)

ttk.Label(input_frame, text="Первісний корінь g:").grid(row=1, column=0, sticky="w", pady=5)
entry_g = ttk.Entry(input_frame, width=20)
entry_g.grid(row=1, column=1, pady=5)

ttk.Label(input_frame, text="Секрет A:").grid(row=2, column=0, sticky="w", pady=5)
entry_a = ttk.Entry(input_frame, width=20)
entry_a.grid(row=2, column=1, pady=5)

ttk.Label(input_frame, text="Секрет B:").grid(row=3, column=0, sticky="w", pady=5)
entry_b = ttk.Entry(input_frame, width=20)
entry_b.grid(row=3, column=1, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# ttk.Button(button_frame, text="🔁 Приклад", command=autofill_example).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Обчислити", command=calculate).grid(row=0, column=1, padx=10)

# Results frame
result_frame = ttk.LabelFrame(root, text="Результати", padding=10)
result_frame.pack(padx=20, pady=10, fill="both", expand=True)

result_text = tk.Text(result_frame, height=10, state=tk.DISABLED, wrap="word", font=("Arial", 11))
result_text.pack(fill="both", expand=True)

# Autofill example values
autofill_example()

root.mainloop()
















# import tkinter as tk
# from tkinter import messagebox, ttk
# import random

# def update_log(message):
#     """
#     Додає повідомлення в текстове поле журналу.
#     """
#     text_log.config(state=tk.NORMAL)  # Дозволяємо редагування
#     text_log.insert(tk.END, message + "\n")  # Додаємо повідомлення
#     text_log.config(state=tk.DISABLED)  # Забороняємо редагування
#     text_log.see(tk.END)  # Прокручуємо до кінця

# def mod_exp(base, exp, mod):
#     """
#     Ефективне модульне піднесення до степеня.
#     base: Основа
#     exp: Показник степеня
#     mod: Модуль
#     """
#     result = 1
#     base %= mod
#     while exp > 0:
#         if exp % 2:
#             result = (result * base) % mod
#         base = (base * base) % mod
#         exp //= 2
#     return result

# def generate_keys():
#     try:
#         p = int(entry_p.get())
#         g = int(entry_g.get())

#         if p <= 0 or g <= 0:
#             raise ValueError("Числа p і g повинні бути більшими за 0.")
        
#         private_key = random.randint(1, p - 1)  # Генерація приватного ключа
#         public_key = mod_exp(g, private_key, p)  # Обчислення публічного ключа

#         # Виведення ключів у відповідні поля
#         entry_private_key.delete(0, tk.END)
#         entry_private_key.insert(0, str(private_key))

#         entry_public_key.delete(0, tk.END)
#         entry_public_key.insert(0, str(public_key))

#         update_log(f"Приватний ключ згенеровано: {private_key}")
#         update_log(f"Публічний ключ згенеровано: {public_key}")
#     except Exception as ex:
#         messagebox.showerror("Помилка", str(ex))
#         update_log(f"Помилка: {str(ex)}")

# def calculate_shared_key():
#     try:
#         update_log("Обчислення спільного ключа...")
#         p = int(entry_p.get())
#         private_key = int(entry_private_key.get())
#         other_public_key = int(entry_other_public_key.get())

#         update_log(f"p = {p}, private_key = {private_key}, other_public_key = {other_public_key}")

#         if p <= 0:
#             raise ValueError("Число p повинно бути більше за 0.")
        
#         shared_key = mod_exp(other_public_key, private_key, p)
#         update_log(f"Спільний ключ: {shared_key}")

#         # Оновлюємо поле "Спільний ключ" в інтерфейсі
#         entry_shared_key.delete(0, tk.END)
#         entry_shared_key.insert(0, str(shared_key))
#     except Exception as ex:
#         messagebox.showerror("Помилка", str(ex))
#         update_log(f"Помилка: {str(ex)}")

# # --- Вікно ---
# root = tk.Tk()
# root.title("Протокол обміну ключами Діффі-Геллмана")
# root.geometry("700x700")
# root.resizable(False, False)

# style = ttk.Style()
# style.configure("TLabel", font=("Arial", 12))
# style.configure("TButton", font=("Arial", 12), padding=6)
# style.configure("TEntry", font=("Arial", 12))

# frame = ttk.Frame(root, padding=20)
# frame.pack(fill="both", expand=True)

# # Заголовок
# ttk.Label(frame, text="Протокол обміну ключами Діффі-Геллмана", font=("Arial", 16, "bold")).pack(pady=10)

# # Розділювач
# ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

# # Введення параметрів p і g
# param_frame = ttk.Frame(frame, padding=10)
# param_frame.pack()

# ttk.Label(param_frame, text="p (просте число):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
# entry_p = ttk.Entry(param_frame, width=40)
# entry_p.grid(row=0, column=1, padx=5, pady=5)

# ttk.Label(param_frame, text="g (примітивний корінь):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
# entry_g = ttk.Entry(param_frame, width=40)
# entry_g.grid(row=1, column=1, padx=5, pady=5)

# # Генерація ключів
# ttk.Button(frame, text="Згенерувати ключі", command=generate_keys).pack(pady=10)

# # Відображення приватного і публічного ключів
# key_frame = ttk.Frame(frame, padding=10)
# key_frame.pack()

# ttk.Label(key_frame, text="Приватний ключ:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
# entry_private_key = ttk.Entry(key_frame, width=40)
# entry_private_key.grid(row=0, column=1, padx=5, pady=5)

# ttk.Label(key_frame, text="Публічний ключ:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
# entry_public_key = ttk.Entry(key_frame, width=40)
# entry_public_key.grid(row=1, column=1, padx=5, pady=5)

# # Розділювач
# ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

# # Введення публічного ключа іншого учасника
# ttk.Label(frame, text="Публічний ключ іншого учасника:").pack(anchor="center", pady=(10, 5))
# entry_other_public_key = ttk.Entry(frame, width=50)
# entry_other_public_key.pack(pady=(0, 10))

# # Обчислення спільного ключа
# ttk.Button(frame, text="Обчислити спільний ключ", command=calculate_shared_key).pack(pady=10)

# # Відображення спільного ключа
# ttk.Label(frame, text="Спільний ключ:").pack(anchor="center", pady=(10, 5))
# entry_shared_key = ttk.Entry(frame, width=50)
# entry_shared_key.pack(pady=(0, 10))

# # Розділювач
# ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

# # Журнал подій
# ttk.Label(frame, text="Журнал подій:").pack(anchor="center", pady=(10, 5))
# text_log = tk.Text(frame, width=70, height=10, state=tk.DISABLED, font=("Arial", 10))
# text_log.pack(pady=(0, 10))

# root.mainloop()