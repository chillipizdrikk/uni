# import tkinter as tk
# import numpy as np
# import scipy.integrate as spi

# # Задані функції для обчислення інтегралу різними методами
# #Поділить інтервал [a, b] на n рівних частин, для кожної частини обчислює значення функції у середині цього підінтервалу,
# #Сумує ці значення і множить на ширину кожного підінтервалу(h)
# def rectangular_rule(f, a, b, n):
#     h = (b - a) / n
#     result = 0
#     for i in range(n):
#         result += f(a + i * h)
#     result *= h
#     return result

# #Використовує аналогічний підхід до метод прямокутника, але також враховує лінійний сегмент між точками.
# #Сумує значення функції на всіх вузлах та лінійні сегменти між ними, множить на ширину кожного підрозділу та ділить на 2.
# def trapezoidal_rule(f, a, b, n):
#     h = (b - a) / n
#     x = np.linspace(a, b, n+1)
#     integral = h * (np.sum(f(x)) - 0.5 * (f(a) + f(b)))
#     return integral

# #Поділить інтервал [a, b] на парну кількість n рівних частин.
# #Обчислює значення функції у всіх вузлах та використовує формулу Сімпсона для апроксимації підінтегральної функції.
# def simpsons_rule(f, a, b, n):
#     if n % 2 != 0:
#         raise ValueError("Кількість розділень повинна бути парною")
#     h = (b - a) / n
#     x = np.linspace(a, b, n+1)
#     y = f(x)
#     integral = h / 3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
#     return integral

# def three_eighths_rule(f, a, b):
#     h = (b - a) / 3
#     x = np.linspace(a, b, 4)
#     y = f(x)
#     integral = 3 * h / 8 * (y[0] + 3*y[1] + 3*y[2] + y[3])
#     return integral

# #Використовує вузли та ваги Гауссової квадратури для наближеного обчислення інтегралу.
# #Вузли (x) та ваги (w) визначаються для конкретної кількості n.
# #Обчислює ваговану суму значень функції у вузлах.
# def gauss_rule(f, a, b, n):
#     x, w = np.polynomial.legendre.leggauss(n)
#     integral = 0.5 * (b - a) * np.sum(w * f(0.5 * (b - a) * x + 0.5 * (b + a)))
#     return integral

# def calculate_gauss_integral():
#     calculate_integral(gauss_rule, "Метод Гауса")

# def calculate_rectangle_integral():
#     calculate_integral(rectangular_rule, "Метод прямокутників")

# def calculate_trapezoidal_integral():
#     calculate_integral(trapezoidal_rule, "Метод трапецій")

# def calculate_simpsons_integral():
#     calculate_integral(simpsons_rule, "Метод Сімпсона")

# def calculate_three_eighths_integral():
#     calculate_integral(three_eighths_rule, "Метод трьох восьмих")

# def calculate_integral(method, method_name):
#     # Отримання введених користувачем значень
#     function_text = function_entry.get()
#     lower_limit = float(lower_limit_entry.get())
#     upper_limit = float(upper_limit_entry.get())
#     n = int(n_entry.get())

#     try:
#         # Задана функція
#         def f(x):
#             return eval(function_text)

#         # Обчислення точного значення інтегралу
#         exact_integral, _ = spi.quad(f, lower_limit, upper_limit)

#         # Обчислення інтегралу за вибраним методом
#         if method == three_eighths_rule:
#             integral = method(f, lower_limit, upper_limit)
#         else:
#             integral = method(f, lower_limit, upper_limit, n)

#         result_text = f"{method_name}\nРезультат: {integral}\nТочне значення: {exact_integral}"
#         result_label.config(text=result_text)

#     except Exception as e:
#         result_label.config(text=f"Помилка: {e}")

# # Створення вікна
# root = tk.Tk()
# root.title("Обчислення інтегралу")

# # Віджети для введення даних
# function_label = tk.Label(root, text="Функція f(x):")
# function_label.pack()
# function_entry = tk.Entry(root)
# function_entry.insert(tk.END, "1 / np.cos(5*x)**2")
# function_entry.pack()

# lower_limit_label = tk.Label(root, text="Нижня межа:")
# lower_limit_label.pack()
# lower_limit_entry = tk.Entry(root)
# lower_limit_entry.insert(tk.END, "0")
# lower_limit_entry.pack()

# upper_limit_label = tk.Label(root, text="Верхня межа:")
# upper_limit_label.pack()
# upper_limit_entry = tk.Entry(root)
# upper_limit_entry.insert(tk.END, "0.1")
# upper_limit_entry.pack()

# n_label = tk.Label(root, text="Кількість розділень:")
# n_label.pack()
# n_entry = tk.Entry(root)
# n_entry.insert(tk.END, "4")
# n_entry.pack()

# # Кнопки для обчислення інтегралу за різними методами
# rectangle_button = tk.Button(root, text="Метод прямокутників", command=calculate_rectangle_integral)
# rectangle_button.pack()

# trapezoidal_button = tk.Button(root, text="Метод трапецій", command=calculate_trapezoidal_integral)
# trapezoidal_button.pack()

# simpsons_button = tk.Button(root, text="Метод Сімпсона", command=calculate_simpsons_integral)
# simpsons_button.pack()

# three_eighths_button = tk.Button(root, text="Метод трьох восьмих", command=calculate_three_eighths_integral)
# three_eighths_button.pack()

# gauss_button = tk.Button(root, text="Метод Гауса", command=calculate_gauss_integral)
# gauss_button.pack()

# result_label = tk.Label(root, text="")
# result_label.pack()

# root.mainloop()





# import tkinter as tk
# import numpy as np
# import scipy.integrate as spi

# def rectangular_rule(f, a, b, n):
#     h = (b - a) / n
#     result = 0
#     for i in range(n):
#         result += f(a + i * h)
#     result *= h
#     return result

# def trapezoidal_rule(f, a, b, n):
#     h = (b - a) / n
#     x = np.linspace(a, b, n+1)
#     integral = h * (np.sum(f(x)) - 0.5 * (f(a) + f(b)))
#     return integral

# def simpsons_rule(f, a, b, n):
#     if n % 2 != 0:
#         raise ValueError("Кількість розділень повинна бути парною")
#     h = (b - a) / n
#     x = np.linspace(a, b, n+1)
#     y = f(x)
#     integral = h / 3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
#     return integral

# def three_eighths_rule(f, a, b):
#     h = (b - a) / 3
#     x = np.linspace(a, b, 4)
#     y = f(x)
#     integral = 3 * h / 8 * (y[0] + 3*y[1] + 3*y[2] + y[3])
#     return integral

# def gauss_rule(f, a, b, n):
#     x, w = np.polynomial.legendre.leggauss(n)
#     integral = 0.5 * (b - a) * np.sum(w * f(0.5 * (b - a) * x + 0.5 * (b + a)))
#     return integral

# def calculate_gauss_integral():
#     calculate_integral(gauss_rule, "Метод Гауса")

# def calculate_rectangle_integral():
#     calculate_integral(rectangular_rule, "Метод прямокутників")

# def calculate_trapezoidal_integral():
#     calculate_integral(trapezoidal_rule, "Метод трапецій")

# def calculate_simpsons_integral():
#     calculate_integral(simpsons_rule, "Метод Сімпсона")

# def calculate_three_eighths_integral():
#     calculate_integral(three_eighths_rule, "Метод трьох восьмих")

# def calculate_integral(method, method_name):
#     function_text = function_entry.get()
#     lower_limit = float(lower_limit_entry.get())
#     upper_limit = float(upper_limit_entry.get())
#     n = int(n_entry.get())

#     try:
#         def f(x):
#             return eval(function_text)

#         exact_integral, _ = spi.quad(f, lower_limit, upper_limit)

#         if method == three_eighths_rule:
#             integral = method(f, lower_limit, upper_limit)
#         else:
#             integral = method(f, lower_limit, upper_limit, n)

#         accuracy = abs(exact_integral - integral)

#         result_text = f"{method_name}\nРезультат: {integral}\nТочне значення: {exact_integral}\n Точність: {accuracy}\n"
#         result_label.config(text=result_text)

#     except Exception as e:
#         result_label.config(text=f"Помилка: {e}")

# root = tk.Tk()
# root.title("Обчислення інтегралу")

# function_label = tk.Label(root, text="Функція f(x):")
# function_label.pack()
# function_entry = tk.Entry(root)
# function_entry.insert(tk.END, "1 / np.cos(5*x)**2")
# function_entry.pack()

# lower_limit_label = tk.Label(root, text="Нижня межа:")
# lower_limit_label.pack()
# lower_limit_entry = tk.Entry(root)
# lower_limit_entry.insert(tk.END, "0")
# lower_limit_entry.pack()

# upper_limit_label = tk.Label(root, text="Верхня межа:")
# upper_limit_label.pack()
# upper_limit_entry = tk.Entry(root)
# upper_limit_entry.insert(tk.END, "0.1")
# upper_limit_entry.pack()

# n_label = tk.Label(root, text="Кількість розділень:")
# n_label.pack()
# n_entry = tk.Entry(root)
# n_entry.insert(tk.END, "4")
# n_entry.pack()

# rectangle_button = tk.Button(root, text="Метод прямокутників", command=calculate_rectangle_integral)
# rectangle_button.pack()

# trapezoidal_button = tk.Button(root, text="Метод трапецій", command=calculate_trapezoidal_integral)
# trapezoidal_button.pack()

# simpsons_button = tk.Button(root, text="Метод Сімпсона", command=calculate_simpsons_integral)
# simpsons_button.pack()

# three_eighths_button = tk.Button(root, text="Метод трьох восьмих", command=calculate_three_eighths_integral)
# three_eighths_button.pack()

# gauss_button = tk.Button(root, text="Метод Гауса", command=calculate_gauss_integral)
# gauss_button.pack()

# result_label = tk.Label(root, text="")
# result_label.pack()

# root.mainloop()



import tkinter as tk
import numpy as np
import scipy.integrate as spi

def rectangular_rule(f, a, b, n, precision):
    h = (b - a) / n
    result = 0
    for i in range(n):
        result += f(a + i * h)
    result *= h
    return result

def trapezoidal_rule(f, a, b, n, precision):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    integral = h * (np.sum(f(x)) - 0.5 * (f(a) + f(b)))
    return integral

def simpsons_rule(f, a, b, n, precision):
    if n % 2 != 0:
        raise ValueError("Кількість розділень повинна бути парною")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    integral = h / 3 * np.sum(y[0:-1:2] + 4 * y[1::2] + y[2::2])
    return integral

def three_eighths_rule(f, a, b, precision):
    h = (b - a) / 3
    x = np.linspace(a, b, 4)
    y = f(x)
    integral = 3 * h / 8 * (y[0] + 3 * y[1] + 3 * y[2] + y[3])
    return integral

def gauss_rule(f, a, b, n, precision):
    x, w = np.polynomial.legendre.leggauss(n)
    integral = 0.5 * (b - a) * np.sum(w * f(0.5 * (b - a) * x + 0.5 * (b + a)))
    return integral

def calculate_gauss_integral():
    calculate_integral(gauss_rule, "Метод Гауса")

def calculate_rectangle_integral():
    calculate_integral(rectangular_rule, "Метод прямокутників")

def calculate_trapezoidal_integral():
    calculate_integral(trapezoidal_rule, "Метод трапецій")

def calculate_simpsons_integral():
    calculate_integral(simpsons_rule, "Метод Сімпсона")



def calculate_integral(method, method_name):
    function_text = function_entry.get()
    lower_limit = float(lower_limit_entry.get())
    upper_limit = float(upper_limit_entry.get())
    n = int(n_entry.get())
    precision = float(precision_entry.get())

    try:
        def f(x):
            return eval(function_text)

        exact_integral, _ = spi.quad(f, lower_limit, upper_limit)

        if method == three_eighths_rule:
            integral = method(f, lower_limit, upper_limit, precision)
        else:
            integral = method(f, lower_limit, upper_limit, n, precision)

        iterations = [n] if method != gauss_rule else []  # для методів без n
        while True:
            n *= 2
            new_integral = method(f, lower_limit, upper_limit, n, precision)
            iterations.append(n)
            if abs(new_integral - integral) < precision:
                break
            integral = new_integral

        accuracy = abs(exact_integral - integral)

        result_text = f"{method_name}\nРезультат: {integral}\nТочне значення: {exact_integral}\nТочність: {precision}\n"
        result_label.config(text=result_text)

    except Exception as e:
        result_label.config(text=f"Помилка: {e}")

root = tk.Tk()
root.title("Обчислення інтегралу")

function_label = tk.Label(root, text="Функція f(x):")
function_label.pack()
function_entry = tk.Entry(root)
function_entry.insert(tk.END, "1 / np.cos(5*x)**2")
function_entry.pack()

lower_limit_label = tk.Label(root, text="Нижня межа:")
lower_limit_label.pack()
lower_limit_entry = tk.Entry(root)
lower_limit_entry.insert(tk.END, "0")
lower_limit_entry.pack()

upper_limit_label = tk.Label(root, text="Верхня межа:")
upper_limit_label.pack()
upper_limit_entry = tk.Entry(root)
upper_limit_entry.insert(tk.END, "0.1")
upper_limit_entry.pack()

precision_label = tk.Label(root, text="Точність:")
precision_label.pack()
precision_entry = tk.Entry(root)
precision_entry.insert(tk.END, "1e-6")  # Точність за замовчуванням
precision_entry.pack()

n_label = tk.Label(root, text="Початкова кількість розділень:")
n_label.pack()
n_entry = tk.Entry(root)
n_entry.insert(tk.END, "4")
n_entry.pack()

rectangle_button = tk.Button(root, text="Метод прямокутників", command=calculate_rectangle_integral)
rectangle_button.pack()

trapezoidal_button = tk.Button(root, text="Метод трапецій", command=calculate_trapezoidal_integral)
trapezoidal_button.pack()

simpsons_button = tk.Button(root, text="Метод Сімпсона", command=calculate_simpsons_integral)
simpsons_button.pack()

gauss_button = tk.Button(root, text="Метод Гауса", command=calculate_gauss_integral)
gauss_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

