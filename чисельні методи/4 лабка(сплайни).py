import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def linear_beta_spline(x, xk):
    splines = []
    for i in range(len(xk) - 2):
        if x < xk[i] or x > xk[i + 2]:
            splines.append(0)
        elif xk[i] <= x < xk[i + 1]:
            h = xk[i + 1] - xk[i]
            splines.append(2 * (x - xk[i]) / h)
        elif xk[i + 1] <= x <= xk[i + 2]:
            h = xk[i + 2] - xk[i + 1]
            splines.append(2 * (xk[i + 2] - x) / h)
        else:
            splines.append(0)
    return splines

def cubic_spline_interpolate(a, b, h):
    number_of_starts = int((b - a) / h) + 3

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('Графік кубічного бета-сплайна')

    for i in range(number_of_starts):
        start = a + h * (i - 3)
        x_values = np.linspace(start, start + 4.0 * h, 1000)
        
        x_values = [x for x in x_values if a <= x <= b]
        y_values = []
        x_k = [start, start + h, start + 2 * h, start + 3 * h, start + 4 * h] 

        for x in x_values:
            y_value = 0
            if x_k[0] <= x <= x_k[1]:
                y_value = 1 / (6 * h**4) * ((x - x_k[0])**3)
            elif x_k[1] <= x <= x_k[2]:
                y_value = 1 / (6 * h) + 1 / (2 * h**2) * ((x - x_k[1])) + 1 / (2 * h**3) * ((x - x_k[1])**2) - 1 / (2 * h**4) * ((x - x_k[1])**3)
            elif x_k[2] <= x <= x_k[3]:
                y_value = 1 / (6 * h) + 1 / (2 * h**2) * ((x_k[3] - x)) + 1 / (2 * h**3) * ((x_k[3] - x)**2) - 1 / (2 * h**4) * ((x_k[3] - x)**3)
            elif x_k[3] <= x <= x_k[4]:
                y_value = 1 / (6 * h**4) * ((x_k[4] - x)**3)
            
            y_values.append(y_value)

        ax.plot(x_values, y_values, color='purple')
    
    ax.plot([a, b], [0, 0], color='purple')
    ax.grid()

    return fig

def plot_graph():
    a_val = float(a_entry.get())
    b_val = float(b_entry.get())
    h_val = float(h_entry.get())

    if spline_type.get() == "Лінійний":
        x_range = (a_val, b_val)
        step = h_val

        x_values = np.linspace(x_range[0], x_range[1], int((x_range[1] - x_range[0]) / step))
        xk = np.linspace(x_range[0], x_range[1], len(x_values))

        plt.figure(figsize=(8, 6))

        for i in range(len(xk) - 2):
            spline_values = [linear_beta_spline(x, xk)[i] for x in x_values]
            plt.plot(x_values, spline_values, color='purple', linestyle='-', markersize=5)

        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Графік лінійного бета-сплайна')
        plt.show()
    elif spline_type.get() == "Кубічний":
        fig = cubic_spline_interpolate(a_val, b_val, h_val)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=4, column=0, columnspan=2)

root = Tk()
root.title("Графік бета-сплайнів")

a_label = Label(root, text="Початок відрізку (a):")
a_label.grid(row=0, column=0)
a_entry = Entry(root)
a_entry.grid(row=0, column=1)

b_label = Label(root, text="Кінець відрізку (b):")
b_label.grid(row=1, column=0)
b_entry = Entry(root)
b_entry.grid(row=1, column=1)

h_label = Label(root, text="Крок (h):")
h_label.grid(row=2, column=0)
h_entry = Entry(root)
h_entry.grid(row=2, column=1)

spline_type_label = Label(root, text="Тип сплайну:")
spline_type_label.grid(row=3, column=0)
spline_type = StringVar(root)
spline_type.set("Лінійний")
spline_type_menu = OptionMenu(root, spline_type, "Лінійний", "Кубічний")
spline_type_menu.grid(row=3, column=1)

plot_button = Button(root, text="Побудувати графік", command=plot_graph)
plot_button.grid(row=4, column=0, columnspan=2)

root.mainloop()








# import numpy as np
# import matplotlib.pyplot as plt
# from tkinter import *

# def linear_beta_spline(x, xk):
#     splines = []
#     for i in range(len(xk) - 2):
#         if x < xk[i] or x > xk[i + 2]:
#             splines.append(0)
#         elif xk[i] <= x < xk[i + 1]:
#             h = xk[i + 1] - xk[i]
#             splines.append(2 * (x - xk[i]) / h)
#         elif xk[i + 1] <= x <= xk[i + 2]:
#             h = xk[i + 2] - xk[i + 1]
#             splines.append(2 * (xk[i + 2] - x) / h)
#         else:
#             splines.append(0)
#     return splines

# def plot_linear_beta_spline():
#     x_range = (float(left_limit_entry.get()), float(right_limit_entry.get()))
#     step = float(step_entry.get())

#     x_values = np.linspace(x_range[0], x_range[1], int((x_range[1] - x_range[0]) / step))
#     # Calculate knots evenly spaced across x_range using step
#     xk = np.linspace(x_range[0], x_range[1], len(x_values))

#     plt.figure(figsize=(8, 6))

#     for i in range(len(xk) - 2):
#         spline_values = [linear_beta_spline(x, xk)[i] for x in x_values]
#         plt.plot(x_values, spline_values, color='purple', linestyle='-', markersize=5)

#     plt.legend()
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Linear Beta Spline Interpolation')
#     plt.show()

# root = Tk()
# root.title("Linear Beta Spline Interpolation")

# left_limit_label = Label(root, text="Left Limit:")
# left_limit_label.grid(row=0, column=0)
# left_limit_entry = Entry(root)
# left_limit_entry.grid(row=0, column=1)

# right_limit_label = Label(root, text="Right Limit:")
# right_limit_label.grid(row=1, column=0)
# right_limit_entry = Entry(root)
# right_limit_entry.grid(row=1, column=1)

# step_label = Label(root, text="Interpolation Step:")
# step_label.grid(row=2, column=0)
# step_entry = Entry(root)
# step_entry.grid(row=2, column=1)

# interpolate_button = Button(root, text="Interpolate", command=plot_linear_beta_spline)
# interpolate_button.grid(row=3, columnspan=2)

# root.mainloop()

# import numpy as np
# import matplotlib.pyplot as plt
# from tkinter import *
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def cubic_spline_interpolate(a, b, h):
#     number_of_starts = int((b - a) / h) + 3

#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.set_title('Графік кубічного бета-сплайна')

#     for i in range(number_of_starts):
#         start = a + h * (i - 3)
#         x_values = np.linspace(start, start + 4.0 * h, 1000)
        
#         x_values = [x for x in x_values if a <= x <= b]
#         y_values = []
#         x_k = [start, start + h, start + 2 * h, start + 3 * h, start + 4 * h] 

#         for x in x_values:
#             y_value = 0
#             if x_k[0] <= x <= x_k[1]:
#                 y_value = 1 / (6 * h**4) * ((x - x_k[0])**3)
#             elif x_k[1] <= x <= x_k[2]:
#                 y_value = 1 / (6 * h) + 1 / (2 * h**2) * ((x - x_k[1])) + 1 / (2 * h**3) * ((x - x_k[1])**2) - 1 / (2 * h**4) * ((x - x_k[1])**3)
#             elif x_k[2] <= x <= x_k[3]:
#                 y_value = 1 / (6 * h) + 1 / (2 * h**2) * ((x_k[3] - x)) + 1 / (2 * h**3) * ((x_k[3] - x)**2) - 1 / (2 * h**4) * ((x_k[3] - x)**3)
#             elif x_k[3] <= x <= x_k[4]:
#                 y_value = 1 / (6 * h**4) * ((x_k[4] - x)**3)
            
#             y_values.append(y_value)

#         ax.plot(x_values, y_values, color='purple')
    
#     ax.plot([a, b], [0, 0], color='purple')
#     ax.grid()

#     return fig

# def plot_graph():
#     a_val = float(a_entry.get())
#     b_val = float(b_entry.get())
#     h_val = float(h_entry.get())

#     fig = cubic_spline_interpolate(a_val, b_val, h_val)

#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.grid(row=4, column=0, columnspan=2)

# root = Tk()
# root.title("Графік кубічного бета-сплайна")

# a_label = Label(root, text="Початок відрізку (a):")
# a_label.grid(row=0, column=0)
# a_entry = Entry(root)
# a_entry.grid(row=0, column=1)

# b_label = Label(root, text="Кінець відрізку (b):")
# b_label.grid(row=1, column=0)
# b_entry = Entry(root)
# b_entry.grid(row=1, column=1)

# h_label = Label(root, text="Крок (h):")
# h_label.grid(row=2, column=0)
# h_entry = Entry(root)
# h_entry.grid(row=2, column=1)

# plot_button = Button(root, text="Побудувати графік", command=plot_graph)
# plot_button.grid(row=3, column=0, columnspan=2)

# root.mainloop()
