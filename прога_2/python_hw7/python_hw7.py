import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import random

def generate_matrix(size):
    return [[round(random.uniform(0, 5), 2) for _ in range(size)] for _ in range(size)]

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

def square_matrix(matrix):
    size = len(matrix)
    result = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix[i][k] * matrix[k][j]
                result[i][j] = round(result[i][j], 2)
    return result

def calculate_and_display():
    size = size_var.get()
    matrix1 = generate_matrix(size)
    matrix2 = generate_matrix(size)

    trace1 = trace(matrix1)
    trace2 = trace(matrix2)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    if show_matrices_var.get():
        result_text.insert(tk.END, "Матриця 1:\n")
        for row in matrix1:
            result_text.insert(tk.END, ' '.join(str(elem) for elem in row) + "\n")
        result_text.insert(tk.END, "\n")

        result_text.insert(tk.END, "Матриця 2:\n")
        for row in matrix2:
            result_text.insert(tk.END, ' '.join(str(elem) for elem in row) + "\n")
        result_text.insert(tk.END, "\n")

    if trace1 < trace2:
        result_text.insert(tk.END, "Слід матриці 1 є меншим, отже ось її квадрат:\n")
        for row in square_matrix(matrix1):
            result_text.insert(tk.END, ' '.join(str(elem) for elem in row) + "\n")
    elif trace1 > trace2:
        result_text.insert(tk.END, "Слід матриці 2 є меншим, отже ось її квадрат:\n")
        for row in square_matrix(matrix2):
            result_text.insert(tk.END, ' '.join(str(elem) for elem in row) + "\n")
    else:
        result_text.insert(tk.END, "Сліди матриць є однаковими\n")

    result_text.config(state=tk.DISABLED)

def greet():
    name = entry.get()
    greeting = f"Приємно познайомитись, {name}. Можете продовжувати:)"
    messagebox.showinfo("Вітання", greeting)

root = tk.Tk()
root.title("Матричні операції")

# Рамка
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Група прапорців
show_matrices_var = tk.BooleanVar()
show_matrices_checkbox = ttk.Checkbutton(frame, text="Показати матриці", variable=show_matrices_var)
show_matrices_checkbox.grid(column=0, row=4, sticky=tk.W)

# Група перемикачів
size_var = tk.IntVar()
size_label = ttk.Label(frame, text="Виберіть розмір матриці:")
size_label.grid(column=0, row=2, sticky=tk.W)
size_radios = [
    ttk.Radiobutton(frame, text=f"{i}x{i}", variable=size_var, value=i)
    for i in range(2, 6)
]
for i, radio in enumerate(size_radios):
    radio.grid(column=i, row=3, sticky=tk.W)

# Entry
entry_label = ttk.Label(frame, text="Як Вас звати?:")
entry_label.grid(column=0, row=0, sticky=tk.W)
entry = ttk.Entry(frame)
entry.grid(column=0, row=1, sticky=(tk.W, tk.E))

# Greeting Button
greet_button = ttk.Button(frame, text="Відповісти", command=greet)
greet_button.grid(column=1, row=1, sticky=(tk.W, tk.E))

# Кнопка
calculate_button = ttk.Button(frame, text="Обчислити", command=calculate_and_display)
calculate_button.grid(column=0, row=5, sticky=(tk.W, tk.E))

# Текстове поле для виведення результату
result_text = scrolledtext.ScrolledText(frame, width=50, height=15, wrap=tk.WORD)
result_text.grid(column=0, row=6, columnspan=3, sticky=(tk.W, tk.E))

root.mainloop()
