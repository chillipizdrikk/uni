import copy
import math

# Введення розмірності матриці
m, n = map(int, input("Введіть кількість обмежень (m) і змінних (n), розділених пробілом: ").split())

# Введення матриці коефіцієнтів
A = []
print("Введіть коефіцієнти для кожного обмеження (по рядках, через пробіл):")
for i in range(m):
    row = list(map(float, input(f"Рядок {i + 1}: ").split()))
    A.append(row)

# Введення правих частин (b)
b = list(map(float, input("Введіть праві частини обмежень (b), через пробіл: ").split()))

# Введення коефіцієнтів цільової функції (c)
c = list(map(float, input("Введіть коефіцієнти цільової функції (c), через пробіл: ").split()))

# Штрафний коефіцієнт M
M = 10**6

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

# Основний алгоритм
print_initial_data(A, b, c)  # Виводимо початкові дані

base = find_start_base(n, m, A, c)
Cb = [c[base[i] - 1] for i in range(m)]  # Cb для базисних змінних

print_with_basis(A, c, base)  # Виводимо функцію з доданими базисними змінними

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
    print_table(base, Cb, b, A, deltaA, deltaB, m, iteration)

    # Перевірка на оптимальність
    if all(delta <= 0 for delta in deltaA):
        print("Оптимальне значення цільової функції:", deltaB)
        print("Значення вільних членів (b):", b)
        print("Базисні змінні:", base)
        # Додано друк оптимальних значень змінних
        x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
        for i in range(m):
            x_star[base[i] - 1] = b[i]
        print("Оптимальні значення змінних:", x_star)
        print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))
        break

    # Перевірка на циклічність
    if base in previous_bases:
        print("Виявлено циклічність.")
        # Друкуємо оптимальне значення, якщо всі дельти <= 0
        if all(delta <= 0 for delta in deltaA):
            print("Умова оптимальності виконується, але виявлено циклічність.")
            x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
            for i in range(m):
                x_star[base[i] - 1] = b[i]
            print("Оптимальні значення змінних:", x_star)
            print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))
        else:
            print("Рішення не знайдено.")
        break
    previous_bases.append(copy.deepcopy(base))

    column_to_fix_index = find_column_to_fix(deltaA)
    row_to_fix_index = find_row_to_fix(A, b, column_to_fix_index)

    if row_to_fix_index == -1:
        print("Рішення необмежене.")
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
    print("Досягнуто максимальної кількості ітерацій або виявлено повторення ітерації. Можливо, розв'язок не знайдено.")
    # Друкуємо оптимальне значення, якщо всі дельти <= 0
    if all(delta <= 0 for delta in deltaA):
        print("Умова оптимальності виконується.")
        x_star = [0] * (n + m)  # Збільшено розмір x_star для врахування доданих змінних
        for i in range(m):
            x_star[base[i] - 1] = b[i]
        print("Оптимальні значення змінних:", x_star)
        print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(c))))


















































# import copy
# import math

# # Введення розмірності матриці
# m, n = map(int, input("Введіть кількість обмежень (m) і змінних (n), розділених пробілом: ").split())

# # Введення матриці коефіцієнтів
# A = []
# print("Введіть коефіцієнти для кожного обмеження (по рядках, через пробіл):")
# for i in range(m):
#     row = list(map(float, input(f"Рядок {i + 1}: ").split()))
#     A.append(row)

# # Введення правих частин (b)
# b = list(map(float, input("Введіть праві частини обмежень (b), через пробіл: ").split()))

# # Введення коефіцієнтів цільової функції (c)
# c = list(map(float, input("Введіть коефіцієнти цільової функції (c), через пробіл: ").split()))

# def print_initial_data(A, b, c):
#     """Друкує цільову функцію та обмеження"""
#     print("\nПочаткові дані:")
#     print("Цільова функція:")
#     print("L =", " + ".join([f"{c[j]}*x{j+1}" for j in range(len(c))]),"-> min")
    
#     print("\nОбмеження:")
#     for i in range(len(A)):
#         print(" + ".join([f"{A[i][j]}*x{j+1}" for j in range(len(A[i]))]), f"= {b[i]}")
#     print()

# def print_with_basis(A, c, base):
#     """Друкує цільову функцію з базисними змінними"""
#     print("\nЦільова функція з базисними змінними:")
#     extended_c = c + [0] * (len(A) - len(base))
#     print("L =", " + ".join([f"{extended_c[j]}*x{j+1}" for j in range(len(extended_c))]), "-> min")
#     print()

# def find_start_base(n, m, A, c):
#     """Знаходить початковий базис або додає штучні змінні, якщо потрібно"""
#     result = []

#     for i in range(m):
#         is_row_can_be_in_base = True
#         for j in range(n):
#             is_column_can_be_in_base = True
#             if A[i][j] == 1 and is_row_can_be_in_base:
#                 for k in range(m):
#                     if A[k][j] != 0 and i != k:
#                         is_column_can_be_in_base = False
#             else:
#                 is_column_can_be_in_base = False
#             if is_column_can_be_in_base:
#                 is_row_can_be_in_base = False
#                 result.append(j + 1)

#     if len(result) != m:
#         result.clear()
#         n += m
#         for i in range(m):
#             for j in range(m):
#                 if i == j:
#                     A[i].append(1.0)
#                 else:
#                     A[i].append(0.0)
#             result.append(n + i - m + 1)
#             c.append(0)

#     return result

# def find_delta_B(base, b, c):
#     """Обчислює значення Delta B"""
#     result = 0

#     for i in range(m):
#         result += b[i] * c[base[i] - 1]

#     return result

# def find_delta_A(n, m, base, A):
#     """Обчислює значення Delta A"""
#     result = []
#     for i in range(n):
#         delta = 0
#         for j in range(m):
#             delta += A[j][i] * c[base[j] - 1]
#         result.append(delta - c[i])
#     return result

# def is_optimal(deltaA, deltaB):
#     """Перевіряє оптимальність розв'язку"""
#     if deltaB > 0:
#         return False

#     for element in deltaA:
#         if element > 0:
#             return False

#     return True

# def find_column_to_fix(deltaA):
#     """Знаходить стовпець, який потрібно виправити"""
#     return deltaA.index(max(deltaA))

# def find_row_to_fix(A, b, column_to_fix_index):
#     """Знаходить рядок, який потрібно замінити"""
#     min_ratio = math.inf
#     row_to_fix = -1
#     for i in range(m):
#         if A[i][column_to_fix_index] > 0:
#             ratio = b[i] / A[i][column_to_fix_index]
#             if ratio < min_ratio:
#                 min_ratio = ratio
#                 row_to_fix = i
#     return row_to_fix

# def print_table(base, Cb, b, A, deltaA, deltaB, m, n):
#     """Друкує таблицю симплекс-методу"""
#     print("\nСимплекс-таблиця:")
#     print(f"{'Базис':<8}{'Cb':<8}{'b':<8}" + "".join([f"x{i+1:<8}" for i in range(n)]) + "Delta")
#     print("-" * (10 * (n + 3)))

#     # Друкуємо рядки для кожного обмеження
#     for i in range(m):
#         row = f"x{base[i]:<7}{Cb[i]:<8.2f}{b[i]:<8.2f}" + "".join([f"{A[i][j]:<8.2f}" for j in range(n)])
#         print(row)

#     # Друкуємо дельта-рядок
#     delta_row = f"{'Delta':<24}" + "".join([f"{deltaA[j]:<8.2f}" for j in range(n)])
#     print(delta_row)
#     print()

# # Основний алгоритм
# print_initial_data(A, b, c)  # Виводимо початкові дані

# base = find_start_base(n, m, A, c)
# Cb = [c[base[i] - 1] for i in range(m)]  # Cb для базисних змінних

# print_with_basis(A, c, base)  # Виводимо функцію з доданими базисними змінними

# while True:
#     deltaB = find_delta_B(base, b, c)
#     deltaA = find_delta_A(n, m, base, A)

#     # Виклик функції для виводу таблиці
#     print_table(base, Cb, b, A, deltaA, deltaB, m, n)

#     if is_optimal(deltaA, deltaB):
#         print("Оптимальне значення цільової функції:", deltaB)
#         print("Значення вільних членів (b):", b)
#         print("Базисні змінні:", base)
#         break
#     else:
#         column_to_fix_index = find_column_to_fix(deltaA)
#         row_to_fix_index = find_row_to_fix(A, b, column_to_fix_index)

#         if row_to_fix_index == -1:
#             print("Рішення необмежене.")
#             break

#         base[row_to_fix_index] = column_to_fix_index + 1
#         Cb[row_to_fix_index] = c[column_to_fix_index]  # Оновлення Cb

#         # Оновлення матриці A та b
#         new_A = []
#         new_b = []

#         for i in range(m):
#             if i != row_to_fix_index:
#                 new_b.append(b[i] - (b[row_to_fix_index] * A[i][column_to_fix_index]) / A[row_to_fix_index][column_to_fix_index])
#             else:
#                 new_b.append(b[i] / A[row_to_fix_index][column_to_fix_index])

#             row = []
#             for j in range(n):
#                 if i != row_to_fix_index:
#                     row.append(A[i][j] - (A[i][column_to_fix_index] * A[row_to_fix_index][j]) / A[row_to_fix_index][column_to_fix_index])
#                 else:
#                     row.append(A[row_to_fix_index][j] / A[row_to_fix_index][column_to_fix_index])

#             new_A.append(row)

#         A = copy.deepcopy(new_A)
#         b = new_b

"------------------------------------------------------------------------------------------------------------|нижній краще"
# import copy
# import math

# # Введення розмірності матриці
# m, n = map(int, input("Введіть кількість обмежень (m) і змінних (n), розділених пробілом: ").split())

# # Введення матриці коефіцієнтів
# A = []
# print("Введіть коефіцієнти для кожного обмеження (по рядках, через пробіл):")
# for i in range(m):
#     row = list(map(float, input(f"Рядок {i + 1}: ").split()))
#     A.append(row)

# # Введення правих частин (b)
# b = list(map(float, input("Введіть праві частини обмежень (b), через пробіл: ").split()))

# # Введення коефіцієнтів цільової функції (c)
# c = list(map(float, input("Введіть коефіцієнти цільової функції (c), через пробіл: ").split()))

# # Штрафний коефіцієнт M
# M = 10**6

# def print_initial_data(A, b, c):
#     """Друкує цільову функцію та обмеження"""
#     print("\nПочаткові дані:")
#     print("Цільова функція:")
#     print("L =", " + ".join([f"{c[j]}*x{j+1}" for j in range(len(c))]),"-> min")
    
#     print("\nОбмеження:")
#     for i in range(len(A)):
#         print(" + ".join([f"{A[i][j]}*x{j+1}" for j in range(len(A[i]))]), f"= {b[i]}")
#     print()

# def print_with_basis(A, c, base):
#     """Друкує цільову функцію з базисними змінними"""
#     print("\nЦільова функція з базисними змінними:")
#     extended_c = c + [0] * (len(A) - len(base))
#     print("L =", " + ".join([f"{extended_c[j]}*x{j+1}" for j in range(len(extended_c))]), "-> min")
#     print()

# def find_start_base(n, m, A, c):
#     """Знаходить початковий базис або додає штучні змінні, якщо потрібно"""
#     result = []

#     for i in range(m):
#         is_row_can_be_in_base = True
#         for j in range(n):
#             is_column_can_be_in_base = True
#             if A[i][j] == 1 and is_row_can_be_in_base:
#                 for k in range(m):
#                     if A[k][j] != 0 and i != k:
#                         is_column_can_be_in_base = False
#             else:
#                 is_column_can_be_in_base = False
#             if is_column_can_be_in_base:
#                 is_row_can_be_in_base = False
#                 result.append(j + 1)

#     if len(result) != m:
#         result.clear()
#         n += m
#         for i in range(m):
#             for j in range(m):
#                 if i == j:
#                     A[i].append(1.0)
#                 else:
#                     A[i].append(0.0)
#             result.append(n + i - m + 1)
#             c.append(M)

#     return result

# def find_delta_B(base, b, c):
#     """Обчислює значення Delta B"""
#     result = 0

#     for i in range(m):
#         result += b[i] * c[base[i] - 1]

#     return result

# def find_delta_A(n, m, base, A):
#     """Обчислює значення Delta A"""
#     result = []
#     for i in range(n):
#         delta = 0
#         for j in range(m):
#             delta += A[j][i] * c[base[j] - 1]
#         result.append(delta - c[i])
#     return result

# def is_optimal(deltaA, deltaB):
#     """Перевіряє оптимальність розв'язку"""
#     if deltaB > 0:
#         return False

#     for element in deltaA:
#         if element > 0:
#             return False

#     return True

# def find_column_to_fix(deltaA):
#     """Знаходить стовпець, який потрібно виправити"""
#     return deltaA.index(max(deltaA))

# def find_row_to_fix(A, b, column_to_fix_index):
#     """Знаходить рядок, який потрібно замінити"""
#     min_ratio = math.inf
#     row_to_fix = -1
#     for i in range(m):
#         if A[i][column_to_fix_index] > 0:
#             ratio = b[i] / A[i][column_to_fix_index]
#             if ratio < min_ratio:
#                 min_ratio = ratio
#                 row_to_fix = i
#     return row_to_fix

# def print_table(base, Cb, b, A, deltaA, deltaB, m, n, iteration):
#     """Друкує таблицю симплекс-методу"""
#     print(f"\nСимплекс-таблиця. Ітерація {iteration}:")
#     print(f"{'Базис':<8}{'Cb':<8}{'b':<8}" + "".join([f"x{i+1:<8}" for i in range(n)]) + "Delta")
#     print("-" * (10 * (n + 3)))

#     # Друкуємо рядки для кожного обмеження
#     for i in range(m):
#         row = f"x{base[i]:<7}{Cb[i]:<8.2f}{b[i]:<8.2f}" + "".join([f"{A[i][j]:<8.2f}" for j in range(n)])
#         print(row)

#     # Друкуємо дельта-рядок
#     delta_row = f"{'Delta':<24}" + "".join([f"{deltaA[j]:<8.2f}" for j in range(n)])
#     print(delta_row)
#     print()

# # Основний алгоритм
# print_initial_data(A, b, c)  # Виводимо початкові дані

# base = find_start_base(n, m, A, c)
# Cb = [c[base[i] - 1] for i in range(m)]  # Cb для базисних змінних

# print_with_basis(A, c, base)  # Виводимо функцію з доданими базисними змінними

# iteration = 0  # Лічильник ітерацій
# max_iterations = 10  # Максимальна кількість ітерацій

# while iteration < max_iterations:
#     iteration += 1
#     deltaB = find_delta_B(base, b, c)
#     deltaA = find_delta_A(n, m, base, A)

#     # Виклик функції для виводу таблиці
#     print_table(base, Cb, b, A, deltaA, deltaB, m, n, iteration)

#     if is_optimal(deltaA, deltaB):
#         print("Оптимальне значення цільової функції:", deltaB)
#         print("Значення вільних членів (b):", b)
#         print("Базисні змінні:", base)
#         break
#     else:
#         column_to_fix_index = find_column_to_fix(deltaA)
#         row_to_fix_index = find_row_to_fix(A, b, column_to_fix_index)

#         if row_to_fix_index == -1:
#             print("Рішення необмежене.")
#             break

#         base[row_to_fix_index] = column_to_fix_index + 1
#         Cb[row_to_fix_index] = c[column_to_fix_index]  # Оновлення Cb

#         # Оновлення матриці A та b
#         new_A = []
#         new_b = []

#         for i in range(m):
#             if i != row_to_fix_index:
#                 new_b.append(b[i] - (b[row_to_fix_index] * A[i][column_to_fix_index]) / A[row_to_fix_index][column_to_fix_index])
#             else:
#                 new_b.append(b[i] / A[row_to_fix_index][column_to_fix_index])

#             row = []
#             for j in range(n):
#                 if i != row_to_fix_index:
#                     row.append(A[i][j] - (A[i][column_to_fix_index] * A[row_to_fix_index][j]) / A[row_to_fix_index][column_to_fix_index])
#                 else:
#                     row.append(A[row_to_fix_index][j] / A[row_to_fix_index][column_to_fix_index])

#             new_A.append(row)

#         A = copy.deepcopy(new_A)
#         b = new_b

# if iteration == max_iterations:
#     print("Досягнуто максимальної кількості ітерацій. Можливо, розв'язок не знайдено.")


# import copy
# import math

# # Введення розмірності матриці
# m, n = map(int, input("Введіть кількість обмежень (m) і змінних (n), розділених пробілом: ").split())

# # Введення матриці коефіцієнтів
# A = []
# print("Введіть коефіцієнти для кожного обмеження (по рядках, через пробіл):")
# for i in range(m):
#     row = list(map(float, input(f"Рядок {i + 1}: ").split()))
#     A.append(row)

# # Введення правих частин (b)
# b = list(map(float, input("Введіть праві частини обмежень (b), через пробіл: ").split()))

# # Введення коефіцієнтів цільової функції (c)
# c = list(map(float, input("Введіть коефіцієнти цільової функції (c), через пробіл: ").split()))

# # Штрафний коефіцієнт M
# M = 10**6

# def print_initial_data(A, b, c):
#     """Друкує цільову функцію та обмеження"""
#     print("\nПочаткові дані:")
#     print("Цільова функція:")
#     print("L =", " + ".join([f"{c[j]}*x{j+1}" for j in range(len(c))]), "-> min")
    
#     print("\nОбмеження:")
#     for i in range(len(A)):
#         print(" + ".join([f"{A[i][j]}*x{j+1}" for j in range(len(A[i]))]), f"= {b[i]}")
#     print()

# def print_with_basis(A, c, base):
#     """Друкує цільову функцію з базисними змінними"""
#     print("\nЦільова функція з базисними змінними:")
#     extended_c = c + [0] * (len(A) - len(base))
#     print("L =", " + ".join([f"{extended_c[j]}*x{j+1}" for j in range(len(extended_c))]), "-> min")
#     print()

# def find_start_base(n, m, A, c):
#     """Знаходить початковий базис або додає штучні змінні, якщо потрібно"""
#     result = []

#     for i in range(m):
#         is_row_can_be_in_base = True
#         for j in range(n):
#             is_column_can_be_in_base = True
#             if A[i][j] == 1 and is_row_can_be_in_base:
#                 for k in range(m):
#                     if A[k][j] != 0 and i != k:
#                         is_column_can_be_in_base = False
#             else:
#                 is_column_can_be_in_base = False
#             if is_column_can_be_in_base:
#                 is_row_can_be_in_base = False
#                 result.append(j + 1)

#     if len(result) != m:
#         result.clear()
#         n += m
#         for i in range(m):
#             for j in range(m):
#                 if i == j:
#                     A[i].append(1.0)
#                 else:
#                     A[i].append(0.0)
#             result.append(n + i - m + 1)
#             c.append(M)

#     return result

# def find_delta_B(base, b, c):
#     """Обчислює значення Delta B"""
#     result = 0

#     for i in range(m):
#         result += b[i] * c[base[i] - 1]

#     return result

# def find_delta_A(n, m, base, A):
#     """Обчислює значення Delta A"""
#     result = []
#     for i in range(n):
#         delta = 0
#         for j in range(m):
#             delta += A[j][i] * c[base[j] - 1]
#         result.append(delta - c[i])
#     return result

# def is_optimal(deltaA, deltaB):
#     """Перевіряє оптимальність розв'язку"""
#     if deltaB > 0:
#         return False

#     for element in deltaA:
#         if element > 0:
#             return False

#     return True

# def find_column_to_fix(deltaA):
#     """Знаходить стовпець, який потрібно виправити"""
#     return deltaA.index(max(deltaA))

# def find_row_to_fix(A, b, column_to_fix_index):
#     """Знаходить рядок, який потрібно замінити"""
#     min_ratio = math.inf
#     row_to_fix = -1
#     for i in range(m):
#         if A[i][column_to_fix_index] > 0:
#             ratio = b[i] / A[i][column_to_fix_index]
#             if ratio < min_ratio:
#                 min_ratio = ratio
#                 row_to_fix = i
#     return row_to_fix

# # def print_table(base, Cb, b, A, deltaA, deltaB, m, n, iteration):
# #     """Друкує таблицю симплекс-методу"""
# #     print(f"\nСимплекс-таблиця. Ітерація {iteration}:")
# #     print(f"{'Базис':<8}{'Cb':<8}{'b':<8}" + "".join([f"x{i+1:<8}" for i in range(n)]) + "Delta")
# #     print("-" * (10 * (n + 3)))

# #     # Друкуємо рядки для кожного обмеження
# #     for i in range(m):
# #         row = f"x{base[i]:<7}{Cb[i]:<8.2f}{b[i]:<8.2f}" + "".join([f"{A[i][j]:<8.2f}" for j in range(n)])
# #         print(row)

# #     # Друкуємо дельта-рядок
# #     delta_row = f"{'Delta':<24}" + "".join([f"{deltaA[j]:<8.2f}" for j in range(n)])
# #     print(delta_row)
# #     print()
# def print_table(base, Cb, b, A, deltaA, deltaB, m, n, iteration):
#     """Друкує таблицю симплекс-методу з усіма змінними"""
#     total_vars = len(A[0])  # Загальна кількість змінних, включаючи додані базисні змінні
    
#     print(f"\nСимплекс-таблиця. Ітерація {iteration}:")
#     print(f"{'Базис':<8}{'Cb':<8}{'b':<8}" + "".join([f"x{i+1:<8}" for i in range(total_vars)]))
#     print("-" * (10 * (total_vars + 3)))

#     # Друкуємо рядки для кожного обмеження
#     for i in range(m):
#         row = f"x{base[i]:<7}{Cb[i]:<8.2f}{b[i]:<8.2f}" + "".join([f"{A[i][j]:<8.2f}" for j in range(total_vars)])
#         print(row)

#     # Друкуємо базисні змінні
#     print("Базисні змінні:")
#     for i in range(m):
#         print(f"x{base[i]} = {b[i]:.2f}")
#     print()

# # Основний алгоритм
# print_initial_data(A, b, c)  # Виводимо початкові дані

# base = find_start_base(n, m, A, c)
# Cb = [c[base[i] - 1] for i in range(m)]  # Cb для базисних змінних

# print_with_basis(A, c, base)  # Виводимо функцію з доданими базисними змінними

# iteration = 0  # Лічильник ітерацій
# max_iterations = 10  # Максимальна кількість ітерацій

# # Список для збереження попередніх базисів для виявлення циклічності
# previous_bases = []

# while iteration < max_iterations:
#     iteration += 1
#     deltaB = find_delta_B(base, b, c)
#     deltaA = find_delta_A(n, m, base, A)

#     # Перевірка на повторення ітерації
#     if previous_bases and base == previous_bases[-1]:
#         break

#     # Виклик функції для виводу таблиці
#     print_table(base, Cb, b, A, deltaA, deltaB, m, n, iteration)

#     # Перевірка на оптимальність
#     if all(delta <= 0 for delta in deltaA):
#         print("Оптимальне значення цільової функції:", deltaB)
#         print("Значення вільних членів (b):", b)
#         print("Базисні змінні:", base)
#         # Додано друк оптимальних значень змінних
#         x_star = [0] * n
#         for i in range(m):
#             x_star[base[i] - 1] = b[i]
#         print("Оптимальні значення змінних:", x_star)
#         print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(x_star))))
#         break

#     # Перевірка на циклічність
#     if base in previous_bases:
#         print("Виявлено циклічність.")
#         # Друкуємо оптимальне значення, якщо всі дельти <= 0
#         if all(delta <= 0 for delta in deltaA):
#             print("Умова оптимальності виконується, але виявлено циклічність.")
#             x_star = [0] * n
#             for i in range(m):
#                 x_star[base[i] - 1] = b[i]
#             print("Оптимальні значення змінних:", x_star)
#             print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(x_star))))
#         else:
#             print("Рішення не знайдено.")
#         break
#     previous_bases.append(copy.deepcopy(base))

#     column_to_fix_index = find_column_to_fix(deltaA)
#     row_to_fix_index = find_row_to_fix(A, b, column_to_fix_index)

#     if row_to_fix_index == -1:
#         print("Рішення необмежене.")
#         break

#     base[row_to_fix_index] = column_to_fix_index + 1
#     Cb[row_to_fix_index] = c[column_to_fix_index]  # Оновлення Cb

#     # Оновлення матриці A та b
#     new_A = []
#     new_b = []

#     for i in range(m):
#         if i != row_to_fix_index:
#             new_b.append(b[i] - (b[row_to_fix_index] * A[i][column_to_fix_index]) / A[row_to_fix_index][column_to_fix_index])
#         else:
#             new_b.append(b[i] / A[row_to_fix_index][column_to_fix_index])

#         row = []
#         for j in range(n):
#             if i != row_to_fix_index:
#                 row.append(A[i][j] - (A[i][column_to_fix_index] * A[row_to_fix_index][j]) / A[row_to_fix_index][column_to_fix_index])
#             else:
#                 row.append(A[row_to_fix_index][j] / A[row_to_fix_index][column_to_fix_index])

#         new_A.append(row)

#     A = copy.deepcopy(new_A)
#     b = new_b

# # Перевірка на максимальну кількість ітерацій та виведення результатів
# if iteration == max_iterations or (previous_bases and base == previous_bases[-1]):
#     print("Досягнуто максимальної кількості ітерацій або виявлено повторення ітерації. Можливо, розв'язок не знайдено.")
#     # Друкуємо оптимальне значення, якщо всі дельти <= 0
#     if all(delta <= 0 for delta in deltaA):
#         print("Умова оптимальності виконується.")
#         x_star = [0] * n
#         for i in range(m):
#             x_star[base[i] - 1] = b[i]
#         print("Оптимальні значення змінних:", x_star)
#         print("Оптимальне значення цільової функції F*:", sum(x_star[i] * c[i] for i in range(len(x_star))))



