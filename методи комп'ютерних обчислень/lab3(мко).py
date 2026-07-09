import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from matplotlib.animation import FuncAnimation

class TimeDepFEM:
    def __init__(self, mu_func, beta_func, sigma_func, f_func, gamma, N, T, num_time_steps, 
                 initial_func, exact_func=None, a=0, b=1, theta=0.5):
        """
        Ініціалізація методу скінченних елементів для нестаціонарної задачі КДР
        
        Параметри:
        mu_func: функція коефіцієнта дифузії μ(x)
        beta_func: функція коефіцієнта конвекції β(x)
        sigma_func: функція коефіцієнта реакції σ(x)
        f_func: функція правої частини f(x,t)
        gamma: значення γ для граничної умови Неймана
        N: кількість елементів розбиття по простору
        T: кінцевий час моделювання
        num_time_steps: кількість кроків за часом
        initial_func: початкова умова u(x,0)
        exact_func: точний розв'язок u(x,t) (якщо відомий)
        a, b: ліва та права межі відрізка
        theta: параметр θ схеми (θ=0 - явна, θ=1 - неявна, θ=0.5 - схема Кранка-Ніколсона)
        """
        self.delta_x = (b - a) / N
        self.x = np.linspace(a, b, N + 1)
        self.N = N
        
        self.T = T
        self.num_time_steps = num_time_steps
        self.delta_t = T / num_time_steps
        self.time = np.linspace(0, T, num_time_steps + 1)
        self.theta = theta  # Параметр θ схеми (0 - явна, 1 - неявна, 0.5 - Кранка-Ніколсона)
        
        self.mu_func = self.parse_function(mu_func)
        self.beta_func = self.parse_function(beta_func)
        self.sigma_func = self.parse_function(sigma_func)
        self.f_func = self.parse_time_dependent_function(f_func)
        self.gamma = gamma
        
        self.initial_func = self.parse_function(initial_func)
        
        # Точний розв'язок (якщо відомий)
        if exact_func:
            self.exact_func = self.parse_time_dependent_function(exact_func)
            self.has_exact = True
        else:
            self.has_exact = False
            
        # Матриці системи
        self.M = self.build_mass_matrix()
        self.K = self.build_stiffness_matrix()
        
        # Вектори розв'язків на всіх часових шарах
        self.u_history = np.zeros((num_time_steps + 1, N + 1))
        
        # Початкова умова
        self.u_history[0] = np.array([self.initial_func(x) for x in self.x])
        
        # Застосування граничних умов до початкової умови
        self.u_history[0, 0] = 0.0  # Діріхле при x=0
        self.u_history[0, self.N] = 0.0  # Діріхле при x=1
        
        # Розв'язання задачі на всіх часових кроках
        self.solve_time_steps()
        
        # Обчислення точного розв'язку (якщо відомий)
        if self.has_exact:
            self.u_exact_history = np.zeros((num_time_steps + 1, N + 1))
            for i, t in enumerate(self.time):
                self.u_exact_history[i] = np.array([self.exact_func(x, t) for x in self.x])
    
    def build_mass_matrix(self):
        """Побудова матриці мас M для методу скінченних елементів, для дискретизації похідної за часом"""
        M = np.zeros((self.N + 1, self.N + 1))
        
        for element_index in range(self.N):
            x1 = self.x[element_index]
            x2 = self.x[element_index + 1]
            h = x2 - x1
            
            # Побудова локальної матриці мас для елемента [x1, x2]
            # Для лінійних базисних функцій матриця мас має вигляд:
            # [h/3, h/6]
            # [h/6, h/3]
            M_local = np.array([[h/3, h/6], [h/6, h/3]])
            
            # Збірка в глобальну матрицю
            for i in range(2):
                for j in range(2):
                    M[element_index + i, element_index + j] += M_local[i, j]
        
        return M
    
    def build_stiffness_matrix(self):
        """Побудова матриці жорсткості K для методу скінченних елементів, відповідає за просторову дискретизацію рівняння КДР"""
        K = np.zeros((self.N + 1, self.N + 1))
        
        for element_index in range(self.N):
            x1 = self.x[element_index]
            x2 = self.x[element_index + 1]
            x_center = (x1 + x2) / 2
            
            # Основні функції та їх похідні
            phi = np.array([(x2 - x_center) / (x2 - x1), (x_center - x1) / (x2 - x1)])  # базисні функції зліва і справа
            dphi = np.array([-1.0 / (x2 - x1), 1.0 / (x2 - x1)])  # похідні функції зліва і справа
            
            # Обчислення коефіцієнтів у центрі
            mu = self.mu_func(x_center)
            beta = self.beta_func(x_center)
            sigma = self.sigma_func(x_center)
            
            # Вага для методу прямокутників
            w = (x2 - x1)
            
            for i in range(2):
                for j in range(2):
                    K[element_index + i, element_index + j] += (
                        mu * dphi[i] * dphi[j] * w +  # дифузійний член
                        beta * phi[i] * dphi[j] * w +  # конвективний член
                        sigma * phi[i] * phi[j] * w  # реакційний член
                    )
        
        # Застосування граничних умов
        # Діріхле при x=0 (u(0) = 0)
        K[0, :] = 0.0
        K[0, 0] = 1.0
        
        # Діріхле при x=1 (u(1) = 0)
        K[self.N, :] = 0.0
        K[self.N, self.N] = 1.0
        
        return K
    
    def build_rhs_vector(self, t):
        """Побудова вектора правої частини F(t) для заданого моменту часу t"""
        F = np.zeros(self.N + 1)
        
        for i in range(self.N):
            x1 = self.x[i]
            x2 = self.x[i + 1]
            x_center = (x1 + x2) / 2
            
            f = self.f_func(x_center, t)
            
            # Основні функції
            phi = np.array([(x2 - x_center) / (x2 - x1), (x_center - x1) / (x2 - x1)])
            
            # Вага для методу прямокутників
            w = 1.0 * (x2 - x1)
            
            # Збір у глобальний вектор
            for j in range(2):
                F[i + j] += f * phi[j] * w
        
        # Застосування граничних умов
        F[0] = 0.0  # Діріхле u(0) = 0
        F[self.N] = 0.0  # Діріхле u(1) = 0
        
        return F
    
    def solve_time_steps(self):
        """Розв'язування задачі на всіх часових кроках за допомогою θ-схеми"""
        # Підготовка матриць для лівої та правої частин схеми
        A = self.M + self.theta * self.delta_t * self.K #A використовується для неявної частини схеми (при часовому шарі n+1)
        B = self.M - (1 - self.theta) * self.delta_t * self.K #B використовується для явної частини схеми (при часовому шарі n)
        
        # Застосування граничних умов
        A[0, :] = 0.0
        A[0, 0] = 1.0
        
        # Розв'язування на кожному часовому кроці
        for n in range(self.num_time_steps):
            t_n = self.time[n]
            t_np1 = self.time[n + 1]
            
            # Права частина в момент часу t_n
            F_n = self.build_rhs_vector(t_n)
            
            # Права частина в момент часу t_{n+1}
            F_np1 = self.build_rhs_vector(t_np1)
            
            # Вектор правої частини рівняння
            rhs = B @ self.u_history[n] + self.delta_t * ((1 - self.theta) * F_n + self.theta * F_np1)
            
            # Застосування граничних умов
            rhs[0] = 0.0  # Діріхле u(0) = 0
            rhs[self.N] = 0.0  # Діріхле u(1) = 0
            
            # Розв'язування системи
            self.u_history[n + 1] = np.linalg.solve(A, rhs)
    
    def plot_results(self, time_indices=None):
        """Побудова графіків розв'язків на обраних часових шарах"""
        if time_indices is None:
            # За замовчуванням, показуємо 5 часових шарів
            time_indices = np.linspace(0, self.num_time_steps, min(5, self.num_time_steps + 1), dtype=int)
        
        plt.figure(figsize=(12, 8))
        
        for idx in time_indices:
            t = self.time[idx]
            label = f't = {t:.3f}'
            plt.plot(self.x, self.u_history[idx], '-o', markersize=4, label=label)
            
            if self.has_exact:
                plt.plot(self.x, self.u_exact_history[idx], '--', label=f'Точне t = {t:.3f}')
        
        plt.title('Розв\'язок нестаціонарної задачі КДР методом скінченних елементів')
        plt.xlabel('x')
        plt.ylabel('u(x,t)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def animate_solution(self, interval=100):
        """Анімація розв'язку задачі КДР за часом"""
        fig, ax = plt.subplots(figsize=(10, 6))
        line1, = ax.plot([], [], 'b-o', markersize=4, label='МСЕ розв\'язок')
        
        if self.has_exact:
            line2, = ax.plot([], [], 'r--', label='Точний розв\'язок')
            lines = [line1, line2]
        else:
            lines = [line1]
        
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        
        ax.set_xlim(min(self.x), max(self.x))
        ymin = np.min(self.u_history) - 0.1 * np.abs(np.min(self.u_history))
        ymax = np.max(self.u_history) + 0.1 * np.abs(np.max(self.u_history))
        ax.set_ylim(ymin, ymax)
        
        ax.set_title('Анімація розв\'язку нестаціонарної задачі КДР')
        ax.set_xlabel('x')
        ax.set_ylabel('u(x,t)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        def init():
            for line in lines:
                line.set_data([], [])
            time_text.set_text('')
            return lines + [time_text]
        
        def update(frame):
            # Оновлення даних для поточного кадру (часового кроку)
            t = self.time[frame]
            
            lines[0].set_data(self.x, self.u_history[frame])
            
            if self.has_exact:
                lines[1].set_data(self.x, self.u_exact_history[frame])
            
            time_text.set_text(f'Час: t = {t:.3f}')
            return lines + [time_text]
        
        ani = FuncAnimation(fig, update, frames=range(self.num_time_steps + 1),
                           init_func=init, blit=True, interval=interval)
        
        plt.tight_layout()
        plt.show()
        
        return ani
    
    def calculate_l2_error(self, time_index):
        """Обчислення L2 похибки для заданого часового кроку"""
        if not self.has_exact:
            return None
        
        n = len(self.x) - 1
        error_sum = 0.0
        
        for i in range(n):
            h = self.x[i + 1] - self.x[i]
            
            x_center = (self.x[i] + self.x[i + 1]) / 2
            t = self.time[time_index]
            
            u_numeric_center = (self.u_history[time_index, i] + self.u_history[time_index, i + 1]) / 2
            u_exact_center = self.exact_func(x_center, t)
            
            diff_center = u_exact_center - u_numeric_center
            error_sum += h * diff_center ** 2
        
        return np.sqrt(error_sum)
    
    def __str__(self):
        """Представлення результатів у текстовому форматі"""
        result = f"Параметри задачі:\n"
        result += f"Кількість елементів: {self.N}\n"
        result += f"Часовий інтервал: [0, {self.T}]\n"
        result += f"Кількість часових кроків: {self.num_time_steps}\n"
        result += f"Часовий крок: {self.delta_t}\n"
        result += f"Параметр θ: {self.theta}\n\n"
        
        # Вибираємо декілька часових кроків для демонстрації
        time_indices = np.linspace(0, self.num_time_steps, min(5, self.num_time_steps + 1), dtype=int)
        
        for idx in time_indices:
            t = self.time[idx]
            result += f"\nЧас t = {t:.4f}:\n"
            
            comparison_data = []
            for i in range(self.N + 1):
                row = [self.x[i], self.u_history[idx, i]]
                
                if self.has_exact:
                    u_exact = self.u_exact_history[idx, i]
                    absolute_error = abs(self.u_history[idx, i] - u_exact)
                    row.extend([u_exact, absolute_error])
                
                comparison_data.append(row)
            
            if self.has_exact:
                headers = ["x", "МСЕ розв'язок", "Точний розв'язок", "Абсолютна похибка"]
                result += tabulate(comparison_data, headers=headers, tablefmt="grid", floatfmt=".6f") + "\n"
                
                l2_error = self.calculate_l2_error(idx)
                result += f"L² Похибка при t = {t:.4f}: {l2_error:.6e}\n"
            else:
                headers = ["x", "МСЕ розв'язок"]
                result += tabulate(comparison_data, headers=headers, tablefmt="grid", floatfmt=".6f") + "\n"
        
        return result
    
    @staticmethod
    def parse_function(input_func):
        """Перетворення рядка функції у callable об'єкт для функцій однієї змінної"""
        try:
            value = float(input_func)
            return lambda x: value
        except ValueError:
            def func(x):
                return eval(input_func, {"x": x, "np": np, "math": math, "sin": math.sin, "cos": math.cos,
                                      "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": math.pi})
            return func
    
    @staticmethod
    def parse_time_dependent_function(input_func):
        """Перетворення рядка функції у callable об'єкт для функцій двох змінних (x, t)"""
        try:
            value = float(input_func)
            return lambda x, t: value
        except ValueError:
            def func(x, t):
                return eval(input_func, {"x": x, "t": t, "np": np, "math": math, "sin": math.sin, "cos": math.cos,
                                      "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": math.pi})
            return func


if __name__ == "__main__":
    # Параметри задачі КДР
    mu_func = "1"      # μ = 1
    beta_func = "0"    # β = 0
    sigma_func = "0"   # σ = 0
    
    # Права частина f(x,t) = x-x² + 2t
    f_func = "x-x**2 + 2*t"
    
    # Часові параметри
    T = 1.0            # кінцевий час
    num_time_steps = 50  # кількість часових кроків
    
    # Кількість елементів по простору
    N = 20
    
    # Початкова умова u(x,0) = 0
    initial_func = "0"
    
    # Точний розв'язок u(x,t) = t·x(1-x)
    exact_func = "t*x*(1-x)"
    
    # Створення об'єкта та розв'язування задачі
    fem = TimeDepFEM(mu_func, beta_func, sigma_func, f_func, 0, N, T, num_time_steps, 
                   initial_func, exact_func, theta=0.5)
    
    # Вивід результатів
    print(fem)
    
    # Візуалізація розв'язків на кількох часових шарах
    fem.plot_results()
    
    # Анімація розв'язку
    ani = fem.animate_solution(interval=100)