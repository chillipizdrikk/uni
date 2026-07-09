import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from numpy import *
from scipy.integrate import solve_bvp

def grid_method():
    def solve_differential_equation(a, b, h, px, qx, fx, alpha0, beta0, gamma0, alpha1, beta1, gamma1):
        def fun(x, y):
            return vstack([y[1], -px(x) * y[1] - qx(x) * y[0] + fx(x)])

        def bc(ya, yb):
            return array([alpha0 * ya[0] + beta0 * ya[1] - gamma0, alpha1 * yb[0] + beta1 * yb[1] - gamma1])

        x_values = arange(a, b + h, h)
        y_guess = zeros((2, x_values.size))

        solution = solve_bvp(fun, bc, x_values, y_guess)

        return solution.sol(x_values)[0]


    def plot_results(x_values, exact_solution, approximate_solution):
        plt.plot(x_values, exact_solution, label='Exact Solution', linestyle='--', color='blue')
        plt.plot(x_values, approximate_solution, label='Approximate Solution', marker='o', linestyle='-', color='red')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.title('Differential Equation Solution')
        plt.show()


    def on_solve_button_click():
        px_func = lambda x: eval(px_entry.get())
        qx_func = lambda x: eval(qx_entry.get())
        fx_func = lambda x: eval(fx_entry.get())

        alpha0 = float(alpha0_entry.get())
        beta0 = float(beta0_entry.get())
        gamma0 = float(gamma0_entry.get())
        alpha1 = float(alpha1_entry.get())
        beta1 = float(beta1_entry.get())
        gamma1 = float(gamma1_entry.get())

        a = float(a_entry.get())
        b = float(b_entry.get())
        h = float(h_entry.get())

        x_values = arange(a, b + h, h)
        exact_solution = solve_differential_equation(a, b, h, px_func, qx_func, fx_func, alpha0, beta0, gamma0, alpha1,
                                                     beta1, gamma1)
        plot_results(x_values, exact_solution, exact_solution)  # For simplicity, both plots are the same in this example


    # GUI setup
    root = tk.Tk()
    root.title('Differential Equation Solver')

    # Widgets
    px_label = ttk.Label(root, text='Enter p(x):')
    px_label.grid(row=0, column=0)
    px_entry = ttk.Entry(root)
    px_entry.grid(row=0, column=1)

    qx_label = ttk.Label(root, text='Enter q(x):')
    qx_label.grid(row=1, column=0)
    qx_entry = ttk.Entry(root)
    qx_entry.grid(row=1, column=1)

    fx_label = ttk.Label(root, text='Enter f(x):')
    fx_label.grid(row=2, column=0)
    fx_entry = ttk.Entry(root)
    fx_entry.grid(row=2, column=1)

    # Widgets for other input fields
    alpha0_label = ttk.Label(root, text='Enter alpha0:')
    alpha0_label.grid(row=3, column=0)
    alpha0_entry = ttk.Entry(root)
    alpha0_entry.grid(row=3, column=1)

    beta0_label = ttk.Label(root, text='Enter beta0:')
    beta0_label.grid(row=4, column=0)
    beta0_entry = ttk.Entry(root)
    beta0_entry.grid(row=4, column=1)

    gamma0_label = ttk.Label(root, text='Enter gamma0:')
    gamma0_label.grid(row=5, column=0)
    gamma0_entry = ttk.Entry(root)
    gamma0_entry.grid(row=5, column=1)

    alpha1_label = ttk.Label(root, text='Enter alpha1:')
    alpha1_label.grid(row=6, column=0)
    alpha1_entry = ttk.Entry(root)
    alpha1_entry.grid(row=6, column=1)

    beta1_label = ttk.Label(root, text='Enter beta1:')
    beta1_label.grid(row=7, column=0)
    beta1_entry = ttk.Entry(root)
    beta1_entry.grid(row=7, column=1)

    gamma1_label = ttk.Label(root, text='Enter gamma1:')
    gamma1_label.grid(row=8, column=0)
    gamma1_entry = ttk.Entry(root)
    gamma1_entry.grid(row=8, column=1)

    a_label = ttk.Label(root, text='Enter interval start (a):')
    a_label.grid(row=11, column=0)
    a_entry = ttk.Entry(root)
    a_entry.grid(row=11, column=1)

    b_label = ttk.Label(root, text='Enter interval end (b):')
    b_label.grid(row=12, column=0)
    b_entry = ttk.Entry(root)
    b_entry.grid(row=12, column=1)

    h_label = ttk.Label(root, text='Enter step size (h):')
    h_label.grid(row=10, column=0)
    h_entry = ttk.Entry(root)
    h_entry.grid(row=10, column=1)

    solve_button = ttk.Button(root, text='Solve', command=on_solve_button_click)
    solve_button.grid(row=9, column=0, columnspan=2)

    # Run GUI
    root.mainloop()
    grid_method()