import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

matplotlib.use('TkAgg')


class FiniteElementMethod:
    def __init__(self, mu_func, beta_func, sigma_func, f_func, gamma, N, exact_func, a=0, b=1):
        self.delta_x = (b - a) / N
        self.x = np.linspace(a, b, N + 1)
        self.N = N

        self.mu_func = self.parse_function(mu_func)
        self.beta_func = self.parse_function(beta_func)
        self.sigma_func = self.parse_function(sigma_func)
        self.f_func = self.parse_function(f_func)
        self.gamma = gamma

        self.exact_func = self.parse_function(exact_func)

        self.A = self.build_matrix()
        self.F = self.build_vector_result()
        self.u = self.solve_system()
        self.u_exact = self.compute_exact_solution()

    def build_matrix(self):
        A = np.zeros((self.N + 1, self.N + 1))

        for element_index in range(self.N):
            x1 = self.x[element_index]
            x2 = self.x[element_index + 1]
            x_center = (x1 + x2) / 2

            # Основні функції та їх похідні
            phi = np.array([(x2 - x_center) / (x2 - x1), (x_center - x1) / (x2 - x1)]) #ліва та права базисні функції
            dphi = np.array([-1.0 / (x2 - x1), 1.0 / (x2 - x1)]) #

            # Обчислення коефіцієнтів у центрі
            mu = self.mu_func(x_center)
            beta = self.beta_func(x_center)
            sigma = self.sigma_func(x_center)

            # Вага для методу прямокутників
            w = (x2 - x1)

            for i in range(2):
                for j in range(2):
                    A[element_index + i, element_index + j] += (
                            mu * dphi[i] * dphi[j] * w +  # Дифузійний член
                            beta * phi[i] * dphi[j] * w +  # Конвективний член
                            sigma * phi[i] * phi[j] * w  # Реакційний член
                    )

        # Застосування граничних умов
        # Діріхле при x=0 (u(0) = 0)
        A[0, :] = 0.0
        A[0, 0] = 1.0

        # Неймана при x=1 (u'(1) = γ)
        A[self.N, :] = 0.0
        A[self.N, self.N - 1] = -1.0
        A[self.N, self.N] = 1.0

        return A

    def build_vector_result(self):
        F = np.zeros(self.N + 1)

        for i in range(self.N):
            x1 = self.x[i]
            x2 = self.x[i + 1]
            x_center = (x1 + x2) / 2

            f = self.f_func(x_center)

            # Основні функції
            phi = np.array([(x2 - x_center) / (x2 - x1), (x_center - x1) / (x2 - x1)])

            # Вага для методу прямокутників
            w = 1.0 * (x2 - x1)

            # Збір у глобальний вектор
            for j in range(2):
                F[i + j] += f * phi[j] * w

        # Застосування граничних умов
        F[0] = 0.0  # Діріхле
        F[self.N] = self.gamma * self.delta_x  # Неймана

        return F

    def calculate_l2_error_rectangle(self):
        n = len(self.x) - 1
        error_sum = 0.0

        for i in range(n):
            h = self.x[i + 1] - self.x[i]

            x_center = (self.x[i] + self.x[i + 1]) / 2

            u_numeric_center = (self.u[i] + self.u[i + 1]) / 2
            u_exact_center = self.exact_func(x_center)

            diff_center = u_exact_center - u_numeric_center
            error_sum += h * diff_center ** 2

        return np.sqrt(error_sum)

    def compute_exact_solution(self):
        return np.array([self.exact_func(x) for x in self.x])

    def solve_system(self):
        return np.linalg.solve(self.A, self.F)

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.x, self.u, 'p-', linewidth=2, marker='o', markersize=5, label='Розв\'язок МСЕ')

        if hasattr(self, 'u_exact'):
            plt.plot(self.x, self.u_exact, 'b--', linewidth=2, label='Точний розв\'язок')

        plt.title('Розв\'язок методом скінченних елементів (МСЕ) vs Точний розв\'язок')
        plt.xlabel('x')
        plt.ylabel('u(x)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def __str__(self):
        matrix_str = "Матриця A:\n" + tabulate(self.A, tablefmt="grid", floatfmt=".4f")
        vector_str = "\n\nВектор F:\n" + tabulate([self.F], headers=[f"F[{i}]" for i in range(self.N + 1)],
                                                  tablefmt="grid", floatfmt=".4f")
        solution_str = "\n\nВектор розв'язку u:\n" + tabulate([self.u], headers=[f"u[{i}]" for i in range(self.N + 1)],
                                                             tablefmt="grid", floatfmt=".4f")

        comparison_data = []
        for i in range(self.N + 1):
            comparison_data.append([self.x[i], self.u[i], self.u_exact[i], abs(self.u[i] - self.u_exact[i])])

        comparison_str = "\n\nПорівняння між МСЕ та точним розв'язком:\n" + tabulate(
            comparison_data,
            headers=["x", "Розв'язок МСЕ", "Точний розв'язок", "Абсолютна помилка"],
            tablefmt="grid",
            floatfmt=(".4f", ".6f", ".6f", ".6f")
        )

        l2_error = self.calculate_l2_error_rectangle()
        error_str = f"\n\nL² Помилка: {l2_error:.6e}"

        return matrix_str + vector_str + solution_str + comparison_str + error_str

    @staticmethod
    def parse_function(input_func):
        try:
            value = float(input_func)
            return lambda x: value
        except ValueError:
            def func(x):
                return eval(input_func, {"x": x, "np": np, "math": math, "sin": math.sin, "cos": math.cos,
                                         "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": math.pi})

            return func


if __name__ == "__main__":
    mu_func = "1"
    beta_func = "x"
    sigma_func = "1"

    f_func = "-2+3*x**2"
    gamma = 2
    N = 10

    exact_func = "x**2"

    finiteElementMethod = FiniteElementMethod(mu_func, beta_func, sigma_func, f_func, gamma, N, exact_func)
    print(finiteElementMethod)
    finiteElementMethod.plot()