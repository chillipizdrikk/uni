import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Середньо квадратичне")

        self.left_label = ctk.CTkLabel(self, text="Ліва межа")
        self.right_label = ctk.CTkLabel(self, text="Права межа")

        self.func_label = ctk.CTkLabel(self, text="Функція")
        self.number_label = ctk.CTkLabel(self, text="Кількість точок")

        self.left_entry = ctk.CTkEntry(self)
        self.right_entry = ctk.CTkEntry(self)

        self.func_entry = ctk.CTkEntry(self)
        self.number_entry = ctk.CTkEntry(self)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        self.left_label.grid(row=0, column=0, padx=5, pady=5)
        self.left_entry.grid(row=0, column=1, padx=5, pady=5)

        self.right_label.grid(row=1, column=0, padx=5, pady=5)
        self.right_entry.grid(row=1, column=1 ,padx=5, pady=5)

        self.func_label.grid(row=2, column=0, padx=5, pady=5)
        self.func_entry.grid(row=2, column=1, padx=5, pady=5)

        self.number_label.grid(row=4, column=0, padx=5, pady=5)
        self.number_entry.grid(row=4, column=1, padx=5, pady=5)

        self.button = ctk.CTkButton(self, text="Показати", command=self.algo)
        self.button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.mainloop()

    # Define the function to be minimized (residuals) with different loss functions
    def fun_linear(self, x, data):
        return x[0] * data[:, 0] + x[1] - data[:, 1]

    def fun_quadratic(self, x, data):
        return x[0] * data[:, 0]**2 + x[1] * data[:, 0] + x[2] - data[:, 1]

    def fun_exponential(self, x, data):
        return x[0] * np.exp(x[1] * data[:, 0]) - data[:, 1]

    def algo(self):

        # Generate some example data
        np.random.seed(0)
        # true_params_linear = np.array([2, 1])
        # true_params_quadratic = np.array([1, -2, 1])
        # true_params_exponential = np.array([2, 0.5])
        self.x_data = np.linspace(float(self.left_entry.get()), float(self.right_entry.get()), int(self.number_entry.get()))

        self.interp_func = self.func_entry.get()

        # Parse the user-input function using SymPy
        x = sp.symbols('x')
        self.f_x = sp.sympify(self.interp_func)

        # Create lambdified function for numerical evaluation
        self.f_x_numeric = sp.lambdify(x, self.f_x, 'numpy')

        x = self.x_data.tolist()
        self.y = [self.f_x_numeric(xi) for xi in x]  # Calculate y values using the user-defined function


        # y_data_linear = true_params_linear[0] * x_data + true_params_linear[1] + 0.1 * np.random.normal(size=100)
        # y_data_quadratic = true_params_quadratic[0] * x_data**2 + true_params_quadratic[1] * x_data + true_params_quadratic[2] + 0.1 * np.random.normal(size=100)
        # y_data_exponential = true_params_exponential[0] * np.exp(true_params_exponential[1] * x_data) + 0.1 * np.random.normal(size=100)

        self.data_linear = np.column_stack((self.x_data, self.y))
        self.data_quadratic = np.column_stack((self.x_data, self.y))
        self.data_exponential = np.column_stack((self.x_data, self.y))

        # Initial guess for the parameters
        self.initial_params_linear = np.array([1, 0])
        self.initial_params_quadratic = np.array([1, 0, 0])
        self.initial_params_exponential = np.array([1, 0.1])

        # Use least squares to fit the model to the data with different loss functions
        self.result_linear = least_squares(self.fun_linear, self.initial_params_linear, args=(self.data_linear,), loss='linear')
        self.result_quadratic = least_squares(self.fun_quadratic, self.initial_params_quadratic, args=(self.data_quadratic,), loss='soft_l1')
        self.result_exponential = least_squares(self.fun_exponential, self.initial_params_exponential, args=(self.data_exponential,), loss='cauchy')

        # Extract the optimized parameters
        self.optimized_params_linear = self.result_linear.x
        self.optimized_params_quadratic = self.result_quadratic.x
        self.optimized_params_exponential = self.result_exponential.x

        # Print the results
        # print("True Parameters (Linear):", true_params_linear)
        # print("Optimized Parameters (Linear):", optimized_params_linear)
        # print("\nTrue Parameters (Quadratic):", true_params_quadratic)
        # print("Optimized Parameters (Quadratic):", optimized_params_quadratic)
        # print("\nTrue Parameters (Exponential):", true_params_exponential)
        # print("Optimized Parameters (Exponential):", optimized_params_exponential)

        #Variables
        liniar_var = ctk.StringVar(value =f'Linear Fit Coefficients: {self.optimized_params_linear}')
        quadratic_var = ctk.StringVar(value = f'Quadratic Fit Coefficients: {self.optimized_params_quadratic}')

        # Print the optimized parameters
        print("\nLinear Fit Coefficients:", self.optimized_params_linear)
        print("Quadratic Fit Coefficients:", self.optimized_params_quadratic)
        print("Exponential Fit Coefficients:", self.optimized_params_exponential)

        # Plot the results

        plt.figure(figsize=(15, 5))

        plt.subplot(131)
        plt.plot(self.x_data, self.y, label='f(x)')
        plt.plot(self.x_data, self.optimized_params_linear[0] * self.x_data + self.optimized_params_linear[1], label='Fit', color='red')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()

        plt.subplot(132)
        plt.plot(self.x_data, self.y, label='f(x)')
        plt.plot(self.x_data, self.optimized_params_quadratic[0] * self.x_data**2 + self.optimized_params_quadratic[1] * self.x_data + self.optimized_params_quadratic[2], label='Fit', color='red')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()

        plt.subplot(133)
        plt.plot(self.x_data, self.y, label='f(x)')
        plt.plot(self.x_data, self.optimized_params_exponential[0] * np.exp(self.optimized_params_exponential[1] * self.x_data), label='Fit', color='red')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = App()
