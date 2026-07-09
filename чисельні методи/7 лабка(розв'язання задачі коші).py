# import numpy as np
# import matplotlib.pyplot as plt
# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def euler_method(f, y0, h, precision):
#     t_values = [0]
#     y_values = [y0]

#     while t_values[-1] < 5:
#         t_new = t_values[-1] + h
#         y_new = y_values[-1] + h * f(t_values[-1], y_values[-1])

#         t_values.append(t_new)
#         y_values.append(y_new)

#         h = adjust_step_size(h, f, t_values[-1], y_values[-1], precision)

#     return np.array(t_values), np.array(y_values)

# def runge_kutta_method(f, y0, h, precision):
#     t_values = [0]
#     y_values = [y0]

#     while t_values[-1] < 5:
#         k1 = h * f(t_values[-1], y_values[-1])
#         k2 = h * f(t_values[-1] + 0.5 * h, y_values[-1] + 0.5 * k1)
#         k3 = h * f(t_values[-1] + 0.5 * h, y_values[-1] + 0.5 * k2)
#         k4 = h * f(t_values[-1] + h, y_values[-1] + k3)

#         y_new = y_values[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
#         t_new = t_values[-1] + h

#         t_values.append(t_new)
#         y_values.append(y_new)

#         h = adjust_step_size(h, f, t_values[-1], y_values[-1], precision)

#     return np.array(t_values), np.array(y_values)

# def adjust_step_size(h, f, t, y, precision):
#     while True:
#         y1 = y + h * f(t, y)
#         y2 = y + h * f(t + h, y1)
#         error = abs(y2 - y1)
#         if error < precision:
#             return h
#         h /= 2

# def calculate_accuracy(t_values, y_values, exact_solution):
#     differences = np.abs(y_values - exact_solution(t_values))
#     accuracy = np.max(differences)
#     return accuracy

# def plot_euler_graph(precision):
#     f_text = function_entry.get()
#     y0 = float(y0_entry.get())
#     h = float(h_entry.get())

#     def f(t, y):
#         return eval(f_text)

#     t_euler, y_euler = euler_method(f, y0, h, precision)

#     exact_solution = lambda t: 2 * np.cos(t) + np.sin(t)

#     fig, ax = plt.subplots(figsize=(8, 4))

#     ax.plot(t_euler, y_euler, label='Метод Ейлера')
#     ax.plot(t_euler, exact_solution(t_euler), label='Точний розв\'язок', linestyle='dashed')
#     ax.set_xlabel('Час (t)')
#     ax.set_ylabel('y(t)')
#     ax.legend()

#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.grid(row=5, column=0, columnspan=2)

#     # Обчислюємо точність
#     accuracy = calculate_accuracy(t_euler, y_euler, exact_solution)
#     print("Точність методу Ейлера:", accuracy)

# def plot_runge_kutta_graph(precision):
#     f_text = function_entry.get()
#     y0 = float(y0_entry.get())
#     h = float(h_entry.get())

#     def f(t, y):
#         return eval(f_text)

#     t_rk, y_rk = runge_kutta_method(f, y0, h, precision)

#     exact_solution = lambda t: 2 * np.cos(t) + np.sin(t)

#     fig, ax = plt.subplots(figsize=(8, 4))

#     ax.plot(t_rk, y_rk, label='Метод Рунге-Кутта')
#     ax.plot(t_rk, exact_solution(t_rk), label='Точний розв\'язок', linestyle='dashed')
#     ax.set_xlabel('Час (t)')
#     ax.set_ylabel('y(t)')
#     ax.legend()

#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.grid(row=5, column=0, columnspan=2)

#     # Обчислюємо точність
#     accuracy = calculate_accuracy(t_rk, y_rk, exact_solution)
#     print("Точність методу Рунге-Кутта:", accuracy)

# # Створення вікна Tkinter
# window = tk.Tk()
# window.title("Розв'язання ЗДР методами Ейлера та Рунге-Кутта")

# # Додавання елементів у вікно
# function_label = tk.Label(window, text="Права частина ЗДР (f(t, y)):")
# function_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

# function_entry = tk.Entry(window)
# function_entry.insert(tk.END, "(1 - y * np.sin(t)) / np.cos(t)")
# function_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# y0_label = tk.Label(window, text="Початкове значення (y0):")
# y0_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# y0_entry = tk.Entry(window)
# y0_entry.insert(tk.END, "2")
# y0_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# h_label = tk.Label(window, text="Крок (h):")
# h_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

# h_entry = tk.Entry(window)
# h_entry.insert(tk.END, "0.1")
# h_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# precision_label = tk.Label(window, text="Точність:")
# precision_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

# precision_entry = tk.Entry(window)
# precision_entry.insert(tk.END, "1e-5")
# precision_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# euler_button = tk.Button(window, text="Вивести графік методом Ейлера", command=lambda: plot_euler_graph(float(precision_entry.get())))
# euler_button.grid(row=4, column=0, pady=5)

# rk_button = tk.Button(window, text="Вивести графік методом Рунге-Кутта", command=lambda: plot_runge_kutta_graph(float(precision_entry.get())))
# rk_button.grid(row=4, column=1, pady=5)

# window.mainloop()

import tkinter as tk
from tkinter import ttk
from sympy import symbols, sympify, pi
import matplotlib.pyplot as plt
import numpy as np

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.widgets = []

        self.master.title("Задача Коші")
        self.create_widgets()

    def create_widgets(self):
        labels = [
            ("Права частина: ", "(1-y*sin(x))/cos(x)"),
            ("Початкове значення х0: ", "0"),
            ("Початкове значення y0: ", "2"),
            ("Точність: ", "0.001"),
            ("Межа: ", "5"),
            ("Точний розв'язок: ", "2*cos(x)+sin(x)")
        ]

        for text, default_value in labels:
            label = ttk.Label(self.master, text=text)
            label.pack()

            entry = ttk.Entry(self.master)
            entry.insert(tk.END, default_value)
            entry.pack()

            self.widgets.append(entry)

        method_combobox = ttk.Combobox(self.master, values=["Метод Ейлера", "Метод Рунге-Кутта"])
        method_combobox.set("Метод Ейлера")
        method_combobox.pack()
        self.widgets.append(method_combobox)

        plot_button = ttk.Button(self.master, text="Накреслити", command=self.plot)
        plot_button.pack()
        self.widgets.append(plot_button)

    def euler(self, x, y, b, h):
        self.x_values = []
        self.y_values = []

        self.x_values.append(x)
        self.y_values.append(y)
        # Логіка методу Ейлера
        while x < b:
            y = y + h * self.func(x, y)
            x = x + h
            self.x_values.append(x)
            self.y_values.append(y)

    def rungeKutta(self, x, y, b, h):
        self.x_values = []
        self.y_values = []
    
        self.x_values.append(x)
        self.y_values.append(y)
    
        # Логіка методу Рунге-Кутта другого порядку
        while x < b:
            k1 = h * self.func(x, y)
            k2 = h * self.func(x + h, y + k1)
    
            y = y + 0.5 * (k1 + k2)
            x = x + h
            self.x_values.append(x)
            self.y_values.append(y)
    

    def func(self, x_value, y_value):
        x = symbols("x")
        y = symbols("y")
        result = self.function.subs([(x, x_value), (y, y_value)])
        return result

    def accurate_value_y(self):
        function_str = self.widgets[5].get()
        function = sympify(function_str)
        x = symbols("x")
        y_values = []
        for x_value in self.x_values:
            y = function.subs(x, x_value)
            y_values.append(y)
        return y_values

    def compute_accuracy(self, n, h):
        # Логіка обчислення точності
        def compute_accuracy(n, h):
            # Обчислення n коренів з кроком h
            roots_h = [i * h for i in range(1, n + 1)]
            # Обчислення 2n коренів з кроком h / 2
            roots_half_h = [i * (h / 2) for i in range(1, 2 * n + 1)]
            
            _h = 0.1

            # Обчислення значень у точках з кроком h
            roots_values_h = np.sqrt(roots_h)
            # Обчислення значень у точках з кроком h / 2
            roots_values_half_h = np.sqrt(roots_half_h)

            # Знаходження модулю від різниці для всіх пар значень
            differences = np.abs(roots_values_h - roots_values_half_h)

            # Знаходження найбільшого значення серед всіх різниць
            max_difference = np.max(differences)

            return max_difference
        pass

    def plot(self):
        function_str = self.widgets[0].get()
        self.function = sympify(function_str)

        x = self.widgets[1].get()
        y = self.widgets[2].get()
        h = float(self.widgets[3].get())
        b = float(self.widgets[4].get())

        x = sympify(x).evalf(subs={symbols('pi'): np.pi})
        y = sympify(y).evalf(subs={symbols('pi'): np.pi})
        if self.widgets[6].get() == "Метод Рунге-Кутта":
            self.rungeKutta(x, y, b, h)
            plt.plot(self.x_values, self.y_values, label='Рунге-Кутти')

        elif self.widgets[6].get() == "Метод Ейлера":
            self.euler(x, y, b, h)
            plt.plot(self.x_values, self.y_values, label="Ейлера", color='red')

        y_values = self.accurate_value_y()
        plt.plot(self.x_values, y_values, label="Точний графік", color='purple')
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()