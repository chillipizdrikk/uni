def gaus(A, b):
    n = len(A)

    # метод Гауса
    for i in range(n):
        # пошук макс елемента
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Нормалізація поточного рядка
        norm = A[i][i]
        for j in range(i, n):
            A[i][j] /= norm
        b[i] /= norm

        # Виключення інших рядків
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Зворотній хід методу Гауса
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]

    return x


def matrix_multiply(A, x):
    n = len(A)
    m = len(x)
    if len(A[0]) != m:
        raise Exception("Несумісні розміри матриці і вектора")

    result = [0] * n
    for i in range(n):
        for j in range(m):
            result[i] += A[i][j] * x[j]

    return result


def mpi(A, b, epsilon=1e-6, max_iterations=1000):
    n = len(A)
    x = [0] * n
    iterations = 0
    while iterations < max_iterations:
        x_new = [0] * n
        for i in range(n):
            x_new[i] = (b[i] - sum(A[i][j] * x[j] for j in range(n)) + A[i][i] * x[i]) / A[i][i]
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

# Розв'язок за допомогою методу Гауса
gaus_solution = gaus(A, b)
print("Розв'язок за допомогою методу Гауса:", gaus_solution)

# Розв'язок за допомогою методу МПІ
mpi_solution = mpi(A, b)
print("Розв'язок за допомогою методу МПІ:", mpi_solution)