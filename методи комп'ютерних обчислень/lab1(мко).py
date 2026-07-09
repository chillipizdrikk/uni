# import numpy as np

# n=10
# m=5
# beta=10
# sigma=2
# f=100
# delta_x=1/n
# gama=1

from numpy.linalg import solve
import numpy as np
import matplotlib.pyplot as plt

def populate_A(n, mu, beta, sigma, delta_x):
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(0, n):
        for j in [max(i - 1, 0), i, min(i + 1, n - 1)]:
            if j == i:
                A[j][i] = mu * 2 / delta_x + sigma * 2 * delta_x / 3
            elif j < i:
                A[j][i] = -mu / delta_x + beta / 2 + sigma * delta_x / 6
            elif i < j:
                A[j][i] = -mu / delta_x - beta / 2 + sigma * delta_x / 6
    A[0][0] = 1 
    A[0][1] = 0
    A[n-1][n-2] = -1/delta_x
    A[n-1][n-1] = 1/delta_x
               
    return A

def populate_F(f, n, phi, delta_x, mu):
    F = [0 for _ in range(n)]
    for i in range(n):
        if i == n-1:
            F[i] = f*delta_x/2 + mu*phi
        else:
            F[i] = f*delta_x
    F[0] = 0
    F[-1] = phi
    return F

def compute_derivative(solution, delta_x):
    derivative = np.zeros_like(solution)
    derivative[0] = (solution[1] - solution[0]) / delta_x
    for i in range(1, len(solution) - 1):
        derivative[i] = (solution[i + 1] - solution[i - 1]) / (2 * delta_x)
    derivative[-1] = (solution[-1] - solution[-2]) / delta_x
    return derivative

def main():
    n = 10
    mu = 5
    beta = 10
    sigma = 2
    f = 100
    delta_x = 1/n
    phi = 100

    A = populate_A(n, mu, beta, sigma, delta_x)

    print("Матриця A:")
    for row in A:
        print(row)

    print("Вектор F:")
    F = populate_F(f, n, phi, delta_x, mu)
    print(F)

    A_np = np.array(A)
    F_np = np.array(F)

    solution = solve(A_np, F_np)
    np.set_printoptions(precision=6, suppress=True)
    print("\nРозв'язок:")
    print(solution)

    derivative = compute_derivative(solution, delta_x)

    # Виводимо таблицю з x, u(x) та u'(x)
    x = np.linspace(0, 1, n)
    print("\nТаблиця значень:")
    print("-" * 45)
    print("    x    |    u(x)    |    u'(x)    ")
    print("-" * 45)
    for i in range(n):
        print(f" {x[i]:.2f}    |  {solution[i]:.6f}  |  {derivative[i]:.6f}  ")
    print("-" * 45)

    # Додаємо маркери на графік
    plt.figure(figsize=(10, 6))
    plt.plot(x, solution, '-o', markersize=8, markerfacecolor='red', markeredgecolor='black', linewidth=2, label='u(x)')
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel('u(x)', fontsize=12)
    plt.title('Розв\'язок задачі', fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()