import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class CorrelationTable:
    def __init__(self, cells, row, col):
        self.row = row
        self.col = col
        self.table = [[None for _ in range(col)] for _ in range(row)]
        for i in range(row):
            for j in range(col):
                cell = cells[col * i + j]
                if cell == "" or cell is None:
                    self.table[i][j] = None
                else:
                    self.table[i][j] = float(cell)

    def count_hyperbola(self):
        res_hyp = [0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(1, self.col):
            n_sum = 0
            sum_yx = 0
            for j in range(1, self.row):
                if self.table[j][i] is not None:
                    n_sum += self.table[j][i]
                    sum_yx += self.table[j][i] * self.table[j][0]
            res_hyp[0] += n_sum / self.table[0][i]
            res_hyp[1] += n_sum
            res_hyp[2] += sum_yx
            res_hyp[3] += n_sum / self.table[0][i] ** 2
            res_hyp[4] += sum_yx / self.table[0][i]
        return res_hyp

    def count_sigma(self, func):
        res = 0.0
        n_total = 0
        for i in range(1, self.row):
            for j in range(1, self.col):
                if self.table[i][j] is not None:
                    res += self.table[i][j] * (self.table[i][0] - func(self.table[0][j])) ** 2
                    n_total += self.table[i][j]
        return res / n_total if n_total != 0 else None

    def count_delta(self, func):
        res = 0.0
        for i in range(1, self.col):
            yx_sum = 0.0
            n_total = 0
            for j in range(1, self.row):
                if self.table[j][i] is not None:
                    yx_sum += self.table[j][i] * self.table[j][0]
                    n_total += self.table[j][i]
            if n_total != 0:
                res += (abs(yx_sum / n_total - func(self.table[0][i]))) ** 2 * n_total
        return res

    def count_ab(self, res):
        b = (res[4] * res[0] - res[3] * res[2]) / (res[0] ** 2 - res[3] * res[1])
        a = (res[2] - b * res[1]) / res[0]
        return a, b

    def print_sigma(self, sigma):
        return f"Sigma = {sigma:.2f};"

    def print_delta(self, delta):
        return f"Delta^2 = {delta:.2f};"

    def print_table(self):
        table_str = ""
        for row in self.table:
            table_str += '\t'.join(str(cell) if cell is not None else "" for cell in row) + "\n"
        return table_str

    def count_conditional_means(self):
        conditional_means = []
        for j in range(1, self.col):
            y_sum = 0
            n_sum = 0
            for i in range(1, self.row):
                if self.table[i][j] is not None:
                    y_sum += self.table[i][0] * self.table[i][j]
                    n_sum += self.table[i][j]
            if n_sum != 0:
                mean = y_sum / n_sum
                conditional_means.append(round(mean, 1))
            else:
                conditional_means.append(None)
        return conditional_means

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Correlation and Regression Analysis")

        self.cells = [
            None, 1, 2, 4, 6, 9, 11, 12,
            3, 0, 0, 0, 0, 0, 7, 31,
            4, 0, 0, 0, 2, 21, 4, 0,
            5, 0, 0, 4, 12, 6, 0, 0,
            7, 0, 3, 22, 5, 0, 0, 0,
            10, 4, 20, 0, 0, 0, 0, 0,
            12, 23, 0, 0, 0, 0, 0, 0
        ]

        self.correlation_table = CorrelationTable(self.cells, 7, 8)
        self.a, self.b = self.correlation_table.count_ab(self.correlation_table.count_hyperbola())

        self.create_widgets()

    def create_widgets(self):
        self.conditional_means_button = ttk.Button(self, text="Calculate Conditional Means", command=self.calculate_conditional_means)
        self.conditional_means_button.pack(pady=10)

        self.show_conditional_means_table_button = ttk.Button(self, text="Show Conditional Means Table", command=self.show_conditional_means_table)
        self.show_conditional_means_table_button.pack(pady=10)

        self.correlation_field_button = ttk.Button(self, text="Plot Correlation Field", command=self.plot_correlation_field)
        self.correlation_field_button.pack(pady=10)

        self.calculate_variance_button = ttk.Button(self, text="Calculate Variance", command=self.calculate_variance)
        self.calculate_variance_button.pack(pady=10)

        self.calculate_sum_of_squares_button = ttk.Button(self, text="Calculate Sum of Squares", command=self.calculate_sum_of_squares)
        self.calculate_sum_of_squares_button.pack(pady=10)

        self.show_correlation_table_button = ttk.Button(self, text="Show Correlation Table", command=self.show_correlation_table)
        self.show_correlation_table_button.pack(pady=10)

        self.show_parameters_button = ttk.Button(self, text="Show Parameters a and b", command=self.show_parameters)
        self.show_parameters_button.pack(pady=10)

        self.show_regression_equation_button = ttk.Button(self, text="Show Regression Equation", command=self.show_regression_equation)
        self.show_regression_equation_button.pack(pady=10)

        self.output_label = tk.Label(self, text="")
        self.output_label.pack(pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(pady=20)

    def calculate_conditional_means(self):
        self.conditional_means = self.correlation_table.count_conditional_means()
        self.output_label.config(text=f"Conditional Means: {self.conditional_means}")

    def show_conditional_means_table(self):
        x_values = [self.correlation_table.table[0][j] for j in range(1, self.correlation_table.col)]
        y_values = self.conditional_means

        new_window = tk.Toplevel(self)
        new_window.title("Conditional Means Table")
        new_window.geometry("400x200")

        tree = ttk.Treeview(new_window)
        tree["columns"] = ("x", "y(x)")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("x", anchor=tk.CENTER, width=80)
        tree.column("y(x)", anchor=tk.CENTER, width=80)

        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("x", text="x", anchor=tk.CENTER)
        tree.heading("y(x)", text="y(x)", anchor=tk.CENTER)

        for i, (x, y) in enumerate(zip(x_values, y_values)):
            tree.insert("", "end", text="", values=(x, y))

        tree.pack(expand=True, fill=tk.BOTH)

    def plot_correlation_field(self):
        x_values = [self.correlation_table.table[0][j] for j in range(1, self.correlation_table.col)]
        y_values = self.conditional_means

        # Calculate regression curve values
        x_range = np.linspace(min(x_values), max(x_values), 100)
        y_regression = self.a / x_range + self.b

        self.ax.clear()
        self.ax.scatter(x_values, y_values, color='red', label='Data Points')
        self.ax.plot(x_range, y_regression, color='blue', label='Regression Curve')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Correlation Field with Regression Curve')
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def calculate_variance(self):
        self.sigma = self.correlation_table.count_sigma(lambda x: self.a / x + self.b)
        self.output_label.config(text=f"Variance: {self.sigma}")

    def calculate_sum_of_squares(self):
        self.delta = self.correlation_table.count_delta(lambda x: self.a / x + self.b)
        self.output_label.config(text=f"Sum of Squares: {self.delta}")

    def show_correlation_table(self):
        correlation_table_text = self.correlation_table.print_table()

        new_window = tk.Toplevel(self)
        new_window.title("Correlation Table")
        new_window.geometry("400x400")

        text_widget = tk.Text(new_window)
        text_widget.insert(tk.END, correlation_table_text)
        text_widget.pack(expand=True, fill=tk.BOTH)

    def show_parameters(self):
        messagebox.showinfo("Parameters", f"a = {self.a}\nb = {self.b}")

    def show_regression_equation(self):
        equation = f"y = {self.a:.2f} / x + {self.b:.2f}"
        messagebox.showinfo("Regression Equation", f"Regression Equation:\n{equation}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()

