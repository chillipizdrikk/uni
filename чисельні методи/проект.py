import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

#№1
def gaus(A, b):
    n = len(A)

    # пх методу гауса
    for i in range(n):
        # макс елемент
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # нормалізація
        norm = A[i][i]
        for j in range(i, n):
            A[i][j] /= norm
        b[i] /= norm

        # видаляємо інші рядки
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # зх метод гауса
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]

    return x

def matrix_vector_multiply(A, x):
    n = len(A)
    m = len(x)
    if len(A[0]) != m:
        raise Exception("Несумісні розміри матриці і вектора")

    result = [0] * n
    for i in range(n):
        for j in range(m):
            result[i] += A[i][j] * x[j]

    return result

# мпі
def mpi(A, b, epsilon=1e-6, max_iterations=1000):
    n = len(A)
    x = [0] * n
    iterations = 0
    while iterations < max_iterations:
        x_new = [0] * n
        for i in range(n):
            x_new[i] = (b[i] - sum(A[i][j] * x[j] for j in range(n)) + A[i][i] * x[i]) / A[i][i]
        print(f"Ітерація {iterations+1}: {x_new}")
        if max(abs(x_new[i] - x[i]) for i in range(n)) < epsilon:
            return x_new
        x = x_new
        iterations += 1
    raise Exception("Метод МПІ не зійшовся")


A = [[1, 2, -1, 1],
     [2, 1, 1, 1],
     [1, -1, 2, 1],
     [1, 1, -1, 3]]
b = [6, 9, 3, 4]

# розв'язок методом гауса
gaus_solution = gaus(A, b)
print("Розв'язок методом Гауса:", gaus_solution)

# розв'язок мпі
mpi_solution = mpi(A, b)
print("Розв'язок МПІ:", mpi_solution)


#№2
def f(x):
    return math.tan(0.58 * x + 0.1) - x**2

def df(x):
    return (1 / math.cos(0.58 * x + 0.1)**2) * 0.58 - 2 * x

def newton_method(f, df, x0, tol=1e-6, max_iter=100):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        x -= fx / df(x)
    return x

def iterative_method(f, x0, tol=1e-6, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_next = f(x)
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x

def plot_function(f, x_range):
    x_values = np.linspace(x_range[0], x_range[1], 1000)
    y_values = [f(x) for x in x_values]
    plt.plot(x_values, y_values)
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(0, color='black', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Графік функції')
    plt.grid(True)

def solve_newton():
    equation = equation_entry.get()
    x0 = float(x0_entry.get())
    tolerance = float(tolerance_entry.get())
    
    result = newton_method(f, df, x0, tol=tolerance)
    
    result_label.config(text=f"Метод Ньютона: x = {result}")

def solve_iterative():
    equation = equation_entry.get()
    x0 = float(x0_entry.get())
    tolerance = float(tolerance_entry.get())
    
    # Визначимо функцію phi(x) для методу простих ітерацій
    def phi(x):
        return x - f(x) / df(x)
    
    # Застосовуємо метод простих ітерацій
    result = iterative_method(phi, x0, tol=tolerance)
    
    result_label.config(text=f"Метод послідовних наближень: x = {result}")



def plot():
    left_limit = float(left_limit_entry.get())
    right_limit = float(right_limit_entry.get())
    
    # Рисуємо графік функції
    plot_function(f, (left_limit, right_limit))
    canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()


# Створення головного вікна
root = tk.Tk()
root.title("Розв'язання рівняння методом Ньютона та методом послідовних наближень")

# Створення та розміщення елементів інтерфейсу
equation_label = tk.Label(root, text="Функція f(x):")
equation_label.pack()

equation_entry = tk.Entry(root)
equation_entry.insert(0, "tan(0.58*x + 0.1) - x**2")
equation_entry.pack()

x0_label = tk.Label(root, text="Початкове наближення (x0):")
x0_label.pack()

x0_entry = tk.Entry(root)
x0_entry.insert(0, "1.0")
x0_entry.pack()

tolerance_label = tk.Label(root, text="Точність (tol):")
tolerance_label.pack()

tolerance_entry = tk.Entry(root)
tolerance_entry.insert(0, "1e-6")
tolerance_entry.pack()

limits_label = tk.Label(root, text="Межі графіка (ліва і права через кому):")
limits_label.pack()

limits_frame = tk.Frame(root)
limits_frame.pack()

left_limit_entry = tk.Entry(limits_frame)
left_limit_label = tk.Label(limits_frame, text="Ліва межа:")
left_limit_label.pack(side="left")
left_limit_entry.pack(side="left")

right_limit_entry = tk.Entry(limits_frame)
right_limit_label = tk.Label(limits_frame, text="Права межа:")
right_limit_label.pack(side="left")
right_limit_entry.pack(side="left")

newton_button = tk.Button(root, text="Метод Ньютона", command=solve_newton)
newton_button.pack()

iterative_button = tk.Button(root, text="Метод послідовних наближень", command=solve_iterative)
iterative_button.pack()

plot_button = tk.Button(root, text="Створити графік", command=plot)
plot_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

plot_frame = tk.Frame(root)
plot_frame.pack()

root.mainloop()
