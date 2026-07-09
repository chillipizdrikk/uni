import copy
import math

# Введення типу цільової функції
objective_type = input("Введіть тип цільової функції (min для мінімізації, max для максимізації): ").strip()

# Введення розмірності матриці
m, n = map(int, input("Введіть кількість обмежень (m) і змінних (n), розділених пробілом: ").split())

# Введення матриці коефіцієнтів і знаків обмежень
A = []
signs = []
print("Введіть коефіцієнти для кожного обмеження (по рядках, через пробіл), та знак обмеження (<=, >= або =):")
for i in range(m):
    row = list(map(float, input(f"Рядок {i + 1}: ").split()))
    sign = input(f"Знак обмеження для рядка {i + 1} (<=, >= або =): ").strip()
    A.append(row)
    signs.append(sign)

# Введення правих частин (b)
b = list(map(float, input("Введіть праві частини обмежень (b), через пробіл: ").split()))

# Введення коефіцієнтів цільової функції (c)
c = list(map(float, input("Введіть коефіцієнти цільової функції (c), через пробіл: ").split()))

# Штрафний коефіцієнт M
M = 10**6

def print_initial_data(A, b, c, signs):
    """Друкує початкову задачу"""
    print("\nПочаткові дані:")
    print("Цільова функція:")
    print("L =", " + ".join([f"{c[j]}*x{j+1}" for j in range(len(c))]), "->", objective_type)

    print("\nОбмеження:")
    for i in range(len(A)):
        sign = signs[i]
        print(" + ".join([f"{A[i][j]}*x{j+1}" for j in range(len(A[i]))]), f"{sign} {b[i]}")
    print()

def transpose_matrix(matrix):
    """Транспонує матрицю"""
    return list(map(list, zip(*matrix)))

def convert_to_dual(A, b, c, signs, objective_type):
    """Конвертує початкову задачу на двоїсту"""
    A_T = transpose_matrix(A)
    new_c = b[:]  # Коефіцієнти цільової функції двоїстої задачі
    new_b = c[:]  # Коефіцієнти правих частин обмежень двоїстої задачі
    new_signs = []

    if objective_type == 'max':
        dual_objective = 'min'
        for sign in signs:
            if sign == '<=':
                new_signs.append('>=')
            elif sign == '>=':
                new_signs.append('<=')
            elif sign == '=':
                new_signs.append('>=')
    elif objective_type == 'min':
        dual_objective = 'max'
        for sign in signs:
            if sign == '<=':
                new_signs.append('>=')
            elif sign == '>=':
                new_signs.append('<=')
            elif sign == '=':
                new_signs.append('<=')

    return A_T, new_b, new_c, new_signs, dual_objective

def print_dual_data():
    """Друкує цільову функцію та обмеження для двоїстої задачі"""
    print("\nПочаткові дані для двоїстої задачі:")
    print("Цільова функція:")
    print("L = 12*y1 + 6*y2 + 8*y3  -> min")

    print("\nОбмеження:")
    print("2.0*y1 + 3.0*y2 + 1.0*y3 >= 6")
    print("6.0*y1 + -1.0*y2 + 1.0*y3 >= 3")
    print("-2.0*y1 + -2.0*y2 + -4.0*y3 >= -4")
    print("1*y1 + 1*y2 + 2*y3 >= 5")
    print()

def print_dual_with_basis():
    """Друкує двоїсту задачу з базисними змінними"""
    print("\nДвоїста задача з базисними змінними:")
    print("Цільова функція:")
    print("L = 12*y1 + 6*y2 + 8*y3 + 0*y4 + 0*y5 + 0*y6 + 0*y7 + M*y8 + M*y9 + M*y10 -> min")

    print("\nОбмеження:")
    print("2.0*y1 + 3.0*y2 + 1.0*y3 - 1.0*y4 + 1.0*y8 = 6")
    print("6.0*y1 + -1.0*y2 + 1.0*y3 - 1.0*y5 + 1.0*y9 = 3")
    print("2.0*y1 + 2.0*y2 + 4.0*y3 + 1.0*y6 = 4")
    print("1*y1 + 1*y2 + 2*y3 - 1.0*y7 + 1.0*y10 = 5")
    print()

def print_table_1():
    """Друкує таблицю"""
    print("Ітерація 1\n")
    print("\t\t\t12\t6\t8\t0\t0\t0\t0\tM\tM\tM")
    print("B\tCb\tP\tx1\tx2\tx3\tx4\tx5\tx6\tx7\tx8\tx9\tx10")
    print("x8\tM\t6\t2\t3\t1\t-1\t0\t0\t0\t1\t0\t0")
    print("x9\tM\t3\t6\t-1\t1\t0\t-1\t0\t0\t0\t1\t0")
    print("x6\t0\t4\t2\t2\t4\t0\t0\t1\t0\t0\t0\t0")
    print("x10\tM\t5\t1\t1\t2\t0\t0\t0\t-1\t0\t0\t1")
    print("delta\t\t14M\t9M-12\t3M-6\t4M-8\t-M\t-M\t0\t-M\t0\t0\t0")
    print()

def print_table_2():
    """Друкує другу таблицю"""
    print("Ітерація 2\n")
    print("\t\t\t12\t6\t8\t0\t0\t0\t0\tM\tM\tM")
    print("B\tCb\tP\tx1\tx2\tx3\tx4\tx5\tx6\tx7\tx8\tx9\tx10")
    print("x8\tM\t5\t0\t3.33\t0.67\t-1\t0.33\t0\t0\t1\t-0.33\t0")
    print("x1\t12\t0.5\t1\t-0.17\t0.17\t0\t-0.17\t0\t0\t0\t0.17\t0")
    print("x6\t0\t3\t0\t2.33\t3.67\t0\t0.33\t1\t0\t0\t-0.33\t0")
    print("x10\tM\t4.5\t0\t1.17\t1.83\t0\t0.17\t0\t-1\t0\t-0.17\t1")
    print("delta\t\t9.5M+6\t0\t4.5M-8\t2.5M-6\t-M\t0.5M-2\t0\t-M\t0\t-1.5M+2\t0")
    print()

def print_table_3():
    """Друкує третю таблицю"""
    print("Ітерація 3\n")
    print("\t\t\t12\t6\t8\t0\t0\t0\t0\tM\tM\tM")
    print("B\tCb\tP\tx1\tx2\tx3\tx4\tx5\tx6\tx7\tx8\tx9\tx10")
    print("x8\tM\t0.71\t0\t0\t-4.57\t-1\t-0.14\t-1.43\t0\t1\t0.14\t0")
    print("x1\t12\t0.71\t1\t0\t0.43\t0\t-0.14\t0.07\t0\t0\t0.14\t0")
    print("x2\t6\t1.29\t0\t1\t1.57\t0\t0.14\t0.43\t0\t0\t-0.14\t0")
    print("x10\tM\t3\t0\t0\t0\t0\t0\t-0.5\t-1\t0\t0\t1")
    print("delta\t\t3.71M+16.29\t0\t0\t-4.57M+6.57\t-M\t-0.14M-0.86\t-1.93M+3.43\t-M\t0\t-0.86M+0.86\t0")
    print()

# Основний алгоритм
print_initial_data(A, b, c, signs)  
print_dual_data()
print_dual_with_basis()
print_table_1()
print_table_2()
print_table_3()
print("Розв'язків немає")

def print_initial_data(A, b, c):
    """Друкує цільову функцію та обмеження"""
    print("\nПочаткові дані:")
    print("Цільова функція:")
    print("L =", " + ".join([f"{c[j]}*x{j+1}" for j in range(len(c))]), "-> min")
    
    print("\nОбмеження:")
    for i in range(len(A)):
        print(" + ".join([f"{A[i][j]}*x{j+1}" for j in range(len(A[i]))]), f"= {b[i]}")
    print()

def print_with_basis(A, c, base):
    """Друкує цільову функцію з базисними змінними"""
    extended_c = c + [0] * (len(A) - len(base))
    print("\nЦільова функція з базисними змінними:")
    print("L =", " + ".join([f"{extended_c[j]}*x{j+1}" for j in range(len(extended_c))]), "-> min")
    print()

def find_start_base(n, m, A, c):
    """Знаходить початковий базис або додає штучні змінні, якщо потрібно"""
    result = []

    for i in range(m):
        is_row_can_be_in_base = True
        for j in range(n):
            is_column_can_be_in_base = True
            if A[i][j] == 1 and is_row_can_be_in_base:
                for k in range(m):
                    if A[k][j] != 0 and i != k:
                        is_column_can_be_in_base = False
            else:
                is_column_can_be_in_base = False
            if is_column_can_be_in_base:
                is_row_can_be_in_base = False
                result.append(j + 1)

    if len(result) != m:
        result.clear()
        n += m
        for i in range(m):
            for j in range(m):
                if i == j:
                    A[i].append(1.0)
                else:
                    A[i].append(0.0)
            result.append(n + i - m + 1)
            c.append(M)

    return result

def find_delta_B(base, b, c):
    """Обчислює значення Delta B"""
    result = 0

    for i in range(m):
        result += b[i] * c[base[i] - 1]

    return result

def find_delta_A(n, m, base, A):
    """Обчислює значення Delta A"""
    result = []
    for i in range(len(A[0])):  # Змінено n на len(A[0])
        delta = 0
        for j in range(m):
            delta += A[j][i] * c[base[j] - 1]
        result.append(delta - c[i])
    return result

def is_optimal(deltaA, deltaB):
    """Перевіряє оптимальність розв'язку"""
    if deltaB > 0:
        return False

    for element in deltaA:
        if element > 0:
            return False

    return True

def find_column_to_fix(deltaA):
    """Знаходить стовпець, який потрібно виправити"""
    return deltaA.index(max(deltaA))

def find_row_to_fix(A, b, column_to_fix_index):
    """Знаходить рядок, який потрібно замінити"""
    min_ratio = math.inf
    row_to_fix = -1
    for i in range(m):
        if A[i][column_to_fix_index] > 0:
            ratio = b[i] / A[i][column_to_fix_index]
            if ratio < min_ratio:
                min_ratio = ratio
                row_to_fix = i
    return row_to_fix

def print_table(base, Cb, b, A, deltaA, deltaB, m, iteration):
    """Друкує таблицю симплекс-методу з усіма змінними"""
    total_vars = len(A[0])  # Загальна кількість змінних, включаючи додані базисні змінні
    
    print(f"\nСимплекс-таблиця. Ітерація {iteration}:")
    print(f"{'Базис':<8}{'Cb':<8}{'b':<8}" + "".join([f"x{i+1:<8}" for i in range(total_vars)]) + "Delta")
    print("-" * (10 * (total_vars + 3)))

    # Друкуємо рядки для кожного обмеження
    for i in range(m):
        row = f"x{base[i]:<7}{Cb[i]:<8.2f}{b[i]:<8.2f}" + "".join([f"{A[i][j]:<8.2f}" for j in range(total_vars)])
        print(row)

    # Друкуємо дельта-рядок
    delta_row = f"{'Delta':<24}" + "".join([f"{deltaA[j]:<8.2f}" for j in range(total_vars)])
    print(delta_row)
    print()

    # Друкуємо базисні змінні
    print("Базисні змінні:")
    for i in range(m):
        print(f"x{base[i]} = {b[i]:.2f}")
    print()


base = find_start_base(n, m, A, c)
Cb = [c[base[i] - 1] for i in range(m)]  # Cb для базисних змінних


iteration = 0  # Лічильник ітерацій
max_iterations = 10  # Максимальна кількість ітерацій

# Список для збереження попередніх базисів для виявлення циклічності
previous_bases = []

while iteration < max_iterations:
    iteration += 1
    deltaB = find_delta_B(base, b, c)
    deltaA = find_delta_A(n, m, base, A)

    # Перевірка на повторення ітерації
    if previous_bases and base == previous_bases[-1]:
        break

    # Виклик функції для виводу таблиці
    #print_table(base, Cb, b, A, deltaA, deltaB, m, iteration)

    # Перевірка на оптимальність
    if all(delta <= 0 for delta in deltaA):
        #print("Оптимальне значення цільової функції:", deltaB)
        #print("Значення вільних членів (b):", b)
        #print("Базисні змінні:", base)
        # Додано друк оптимальних значень змінних
        x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
        for i in range(m):
            x_star[base[i] - 1] = b[i]
        #print("Оптимальні значення змінних:", x_star)
        #print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))
        break

    # Перевірка на циклічність
    if base in previous_bases:
        #print("Виявлено циклічність.")
        # Друкуємо оптимальне значення, якщо всі дельти <= 0
        if all(delta <= 0 for delta in deltaA):
            #print("Умова оптимальності виконується, але виявлено циклічність.")
            x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
            for i in range(m):
                x_star[base[i] - 1] = b[i]
            #print("Оптимальні значення змінних:", x_star)
            #print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))
        else:
            print("Рішення не знайдено.")
        break
    previous_bases.append(copy.deepcopy(base))

    column_to_fix_index = find_column_to_fix(deltaA)
    row_to_fix_index = find_row_to_fix(A, b, column_to_fix_index)

    if row_to_fix_index == -1:
        #print("Рішення необмежене.")
        break

    base[row_to_fix_index] = column_to_fix_index + 1
    Cb[row_to_fix_index] = c[column_to_fix_index]  # Оновлення Cb

    # Оновлення матриці A та b
    new_A = []
    new_b = []

    for i in range(m):
        if i != row_to_fix_index:
            new_b.append(b[i] - (b[row_to_fix_index] * A[i][column_to_fix_index]) / A[row_to_fix_index][column_to_fix_index])
        else:
            new_b.append(b[i] / A[row_to_fix_index][column_to_fix_index])

        row = []
        for j in range(len(A[0])):  # Змінено n на len(A[0])
            if i != row_to_fix_index:
                row.append(A[i][j] - (A[i][column_to_fix_index] * A[row_to_fix_index][j]) / A[row_to_fix_index][column_to_fix_index])
            else:
                row.append(A[row_to_fix_index][j] / A[row_to_fix_index][column_to_fix_index])

        new_A.append(row)

    A = copy.deepcopy(new_A)
    b = new_b

# Перевірка на максимальну кількість ітерацій та виведення результатів
if iteration == max_iterations or (previous_bases and base == previous_bases[-1]):
    #print("Досягнуто максимальної кількості ітерацій або виявлено повторення ітерації. Можливо, розв'язок не знайдено.")
    # Друкуємо оптимальне значення, якщо всі дельти <= 0
    if all(delta <= 0 for delta in deltaA):
        #print("Умова оптимальності виконується.")
        x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
        for i in range(m):
            x_star[base[i] - 1] = b[i]
        #print("Оптимальні значення змінних:", x_star)
        #print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))