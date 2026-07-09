import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Функція для інтерполяції методом Лагранжа
def lagrange_interpolation(x, y, x_interp):
    n = len(x)
    result = 0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j:
                term *= (x_interp - x[j]) / (x[i] - x[j])
        result += term
    return result

# Функція для відображення графіку інтерполяції
def plot_lagrange():
    start = float(entry_start.get())
    end = float(entry_end.get())
    num_nodes = int(entry_num_nodes.get())
    function_expr = entry_function.get()
    
    # Генеруємо вузли та обчислюємо значення функції на цих вузлах
    x = np.linspace(start, end, num_nodes)
    y = [sp.sympify(function_expr).subs('x', xi) for xi in x]
    
    x_interp = sp.symbols('x')
    lagrange_poly = lagrange_interpolation(x, y, x_interp)
    
    x_values = np.linspace(start, end, 400)
    y_values_interp = [lagrange_poly.subs('x', xi) for xi in x_values]
    
    function_sym = sp.sympify(function_expr)
    y_values_function = [function_sym.subs('x', xi) for xi in x_values]
    
    ax.clear()
    ax.plot(x_values, y_values_interp, label='Інтерполяція за Лагранжем')
    ax.plot(x_values, y_values_function, label='Функція')
    
    # Відображення вузлів на графіку
    ax.scatter(x, [sp.sympify(function_expr).subs('x', xi) for xi in x], color='red', label='Вузли')
    
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    
    canvas.draw()

# Створення головного вікна додатку
app = tk.Tk()
app.title("Lagrange Interpolation Calculator")

# Створення рамки для розміщення віджетів
frame = ttk.Frame(app)
frame.grid(column=0, row=0)

# Створення та розміщення елементів для введення параметрів
label_start = ttk.Label(frame, text="Початок відрізка(a):")
label_start.grid(column=0, row=0)
entry_start = ttk.Entry(frame)
entry_start.grid(column=1, row=0)
entry_start.insert(0, "-1")

label_end = ttk.Label(frame, text="Кінець відрізка(b):")
label_end.grid(column=0, row=1)
entry_end = ttk.Entry(frame)
entry_end.grid(column=1, row=1)
entry_end.insert(0, "10")

label_num_nodes = ttk.Label(frame, text="Кількість вузлів:")
label_num_nodes.grid(column=0, row=2)
entry_num_nodes = ttk.Entry(frame)
entry_num_nodes.grid(column=1, row=2)
entry_num_nodes.insert(0, "10")

label_function = ttk.Label(frame, text="Функція:")
label_function.grid(column=0, row=3)
entry_function = ttk.Entry(frame)
entry_function.grid(column=1, row=3)
entry_function.insert(0, "tan(0.58*x + 0.1) - x**2")

# Створення кнопки для побудови графіку
lagrange_button = ttk.Button(frame, text="Побудувати інтерполяцію Лагранжа", command=plot_lagrange)
lagrange_button.grid(column=0, row=4, columnspan=2)

# Створення області для розміщення графіку
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=app)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=2, row=0, rowspan=5)

# Запуск головного циклу додатку
app.mainloop()
