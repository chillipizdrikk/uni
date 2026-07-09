# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import least_squares
# from tabulate import tabulate

# # Зчитування кореляційної таблиці з CSV файлу
# df = pd.read_csv('correlation_table.csv', index_col=0)

# # Конвертуємо значення у числовий формат
# df = df.apply(pd.to_numeric)

# # Виведення кореляційної таблиці
# print("Кореляційна таблиця:")
# print(tabulate(df, headers='keys', tablefmt='grid'))

# # Обчислення умовних середніх Y за умов різних значень X
# conditional_means = {}

# for col in df.columns:
#     total_sum = 0
#     count = 0
#     for index, row in df.iterrows():
#         if not pd.isna(row[col]):
#             total_sum += row[col] * index
#             count += row[col]
#     conditional_mean = total_sum / count if count != 0 else 0
#     conditional_means[col] = conditional_mean
#     print(f"Умовна середня для X={col}: {conditional_mean}")

# # Створення таблиці умовних середніх
# conditional_means_table = pd.DataFrame.from_dict(conditional_means, orient='index', columns=['Умовні середні'])

# # Виведення таблиці умовних середніх
# print("\nТаблиця умовних середніх:")
# print(tabulate(conditional_means_table, headers='keys', tablefmt='grid'))

# # Створення списків координат для побудови точок
# x_values = list(map(float, conditional_means.keys()))  # Конвертуємо рядки у числа
# y_values = list(conditional_means.values())

# # Побудова графіка з лінією, що з'єднує точки
# plt.figure(figsize=(8, 6))
# plt.plot(x_values, y_values, color='purple', marker='o', linestyle='-')
# plt.title('Поле кореляції')
# plt.xlabel('X')
# plt.ylabel('Умовні середні Y')
# plt.grid(True)
# plt.show()

# print("\nПрипускаємо, що це гіперболічна кореляція")

# # Задання початкових значень параметрів a і b
# initial_guess = [1, 1]  # Початкове значення a і b

# # Функція, яка обчислює значення гіперболічної функції регресії
# def hyperbolic_regression(params, x):
#     a, b = params
#     x_filtered = [val for val in x if val != 0]  # Виключаємо нульові абсциси
#     return a * (np.sum(1 / np.array(x_filtered))) + b * len(x_filtered)

# # Функція, яка обчислює відхилення між значеннями функції та спостереженнями
# def objective(params):
#     return [
#         hyperbolic_regression(params, x_values) - np.sum(y_values),
#         np.sum([params[0] * (1 / np.array(x_values)[i]) + params[1] - y_values[i] for i in range(len(x_values))])
#     ]

# # Знаходження значень параметрів a і b за допомогою методу найменших квадратів
# results = least_squares(objective, initial_guess)

# # Отримання значень параметрів a і b
# a, b = results.x

# # Виведення результатів
# print("Значення параметра a:", a)
# print("Значення параметра b:", b)

# # Рівняння кривої регресії
# def regression_curve(x, a, b):
#     return a / x + b

# # Побудова графіку кривої регресії
# plt.figure(figsize=(8, 6))
# plt.scatter(x_values, y_values, color='purple', label='Точки умовних середніх')
# plt.plot(x_values, regression_curve(np.array(x_values), a, b), color='orange', linestyle='-', label='Крива регресії')
# plt.title('Крива регресії Y на X')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Обчислення дисперсії за формулою
# delta = 0
# total_count = sum([sum(row.notna()) for _, row in df.iterrows()])  # Загальна кількість спостережень

# for i, xi in enumerate(x_values):
#     yj = y_values[i]
#     if not pd.isna(yj):  # Якщо значення yj для xi не є NaN
#         delta += (yj - hyperbolic_regression([a, b], [xi])) ** 2  # Передаємо список з одним елементом

# # Обчислення дисперсії
# dispersion = delta / total_count

# # Виведення результату
# print("Дисперсія Y відносно кривої регресії Y на X:\n", dispersion)

# # Обчислення суми квадратів відхилень від функції регресії
# delta_squared_sum = 0

# for i, xi in enumerate(x_values):
#     if i < len(df):
#         yj = y_values[i]
#         if not pd.isna(yj):
#             delta_squared_sum += (yj - regression_curve(xi, a, b)) ** 2 * df.iloc[i, :].sum()


# # Виведення результату
# print("Сума квадратів відхилень δ^2 умовних середніх від значень функції регресії:\n", delta_squared_sum)




# 222222222222
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import least_squares
# from tabulate import tabulate

# # Зчитування кореляційної таблиці з CSV файлу
# df = pd.read_csv('correlation_table.csv', index_col=0)

# # Конвертуємо значення у числовий формат
# df = df.apply(pd.to_numeric)

# # Виведення кореляційної таблиці
# print("Кореляційна таблиця:")
# print(tabulate(df, headers='keys', tablefmt='grid'))

# # Обчислення умовних середніх Y за умов різних значень X
# conditional_means = {}

# for col in df.columns:
#     total_sum = 0
#     count = 0
#     for index, row in df.iterrows():
#         if not pd.isna(row[col]):
#             total_sum += row[col] * index
#             count += row[col]
#     conditional_mean = total_sum / count if count != 0 else 0
#     conditional_means[col] = conditional_mean
#     print(f"Умовна середня для X={col}: {conditional_mean}")

# # Створення таблиці умовних середніх
# conditional_means_table = pd.DataFrame.from_dict(conditional_means, orient='index', columns=['Умовні середні'])

# # Виведення таблиці умовних середніх
# print("\nТаблиця умовних середніх:")
# print(tabulate(conditional_means_table, headers='keys', tablefmt='grid'))

# # Створення списків координат для побудови точок
# x_values = np.array(list(map(float, conditional_means.keys())))  # Конвертуємо рядки у числа
# y_values = np.array(list(conditional_means.values()))

# # Побудова графіка з лінією, що з'єднує точки
# plt.figure(figsize=(8, 6))
# plt.plot(x_values, y_values, color='purple', marker='o', linestyle='-')
# plt.title('Поле кореляції')
# plt.xlabel('X')
# plt.ylabel('Умовні середні Y')
# plt.grid(True)
# plt.show()

# print("\nПрипускаємо, що це гіперболічна кореляція")

# # Задання початкових значень параметрів a і b
# initial_guess = [1, 1]  # Початкове значення a і b

# # Функція, яка обчислює значення гіперболічної функції регресії
# def hyperbolic_regression(params, x):
#     a, b = params
#     return a / x + b

# # Функція, яка обчислює відхилення між значеннями функції та спостереженнями
# def objective(params):
#     return y_values - hyperbolic_regression(params, x_values)

# # Знаходження значень параметрів a і b за допомогою методу найменших квадратів
# results = least_squares(objective, initial_guess)

# # Отримання значень параметрів a і b
# a, b = results.x

# # Виведення результатів
# print("Значення параметра a:", a)
# print("Значення параметра b:", b)

# # Рівняння кривої регресії
# def regression_curve(x, a, b):
#     return a / x + b

# # Побудова графіку кривої регресії
# plt.figure(figsize=(8, 6))
# plt.scatter(x_values, y_values, color='purple', label='Точки умовних середніх')
# plt.plot(x_values, regression_curve(x_values, a, b), color='orange', linestyle='-', label='Крива регресії')
# plt.title('Крива регресії Y на X')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Обчислення дисперсії за формулою
# delta = 0
# total_count = df.sum().sum()  # Загальна кількість спостережень

# for i in range(len(df.index)):
#     for j in range(len(df.columns)):
#         nij = df.iloc[i, j]
#         if nij > 0:
#             yj = df.index[i]
#             xi = float(df.columns[j])
#             delta += nij * (yj - regression_curve(xi, a, b)) ** 2

# # Обчислення дисперсії
# dispersion = delta / total_count

# # Виведення результату
# print("Дисперсія Y відносно кривої регресії Y на X:\n", dispersion)

# # Обчислення суми квадратів відхилень від функції регресії
# delta_squared_sum = 0

# for j, xi in enumerate(x_values):
#     yxi = y_values[j]
#     ni = df.iloc[:, j].sum()  # Кількість спостережень для xi
#     delta_squared_sum += ni * (yxi - regression_curve(xi, a, b)) ** 2

# # Виведення результату
# print("Сума квадратів відхилень δ^2 умовних середніх від значень функції регресії:\n", delta_squared_sum)




# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from tabulate import tabulate
# import sympy as sp

# # Зчитування кореляційної таблиці з CSV файлу
# df = pd.read_csv('correlation_table.csv', index_col=0)

# # Конвертуємо значення у числовий формат
# df = df.apply(pd.to_numeric)

# # Виведення кореляційної таблиці
# print("Кореляційна таблиця:")
# print(tabulate(df, headers='keys', tablefmt='grid'))

# # Обчислення умовних середніх Y за умов різних значень X
# conditional_means = {}

# for col in df.columns:
#     total_sum = 0
#     count = 0
#     for index, row in df.iterrows():
#         if not pd.isna(row[col]):
#             total_sum += row[col] * index
#             count += row[col]
#     conditional_mean = total_sum / count if count != 0 else 0
#     conditional_means[col] = conditional_mean
#     print(f"Умовна середня для X={col}: {conditional_mean}")

# # Створення таблиці умовних середніх
# conditional_means_table = pd.DataFrame.from_dict(conditional_means, orient='index', columns=['Умовні середні'])

# # Виведення таблиці умовних середніх
# print("\nТаблиця умовних середніх:")
# print(tabulate(conditional_means_table, headers='keys', tablefmt='grid'))

# # Створення списків координат для побудови точок
# x_values = np.array(list(map(float, conditional_means.keys())))  # Конвертуємо рядки у числа
# y_values = np.array(list(conditional_means.values()))

# # Побудова графіка з лінією, що з'єднує точки
# plt.figure(figsize=(8, 6))
# plt.plot(x_values, y_values, color='purple', marker='o', linestyle='-')
# plt.title('Поле кореляції')
# plt.xlabel('X')
# plt.ylabel('Умовні середні Y')
# plt.grid(True)
# plt.show()

# print("\nПрипускаємо, що це гіперболічна кореляція")

# # Задання початкових значень параметрів a і b
# initial_guess = [1, 1]  # Початкове значення a і b

# # Функція, яка обчислює значення гіперболічної функції регресії
# def hyperbolic_regression(params, x):
#     a, b = params
#     return a / x + b

# # Знаходження параметрів a і b за допомогою системи рівнянь
# total_x_inv_sum = np.sum(1 / x_values)
# total_x_inv_square_sum = np.sum(1 / x_values**2)
# total_y_x_inv_sum = np.sum(y_values / x_values)
# total_y_sum = np.sum(y_values)
# total_y_x_inv_x_sum = np.sum(y_values * x_values / x_values)
# n = len(x_values)

# a = (n * total_y_x_inv_sum - total_y_sum * total_x_inv_sum) / (n * total_x_inv_square_sum - total_x_inv_sum**2)
# b = (total_y_sum - a * total_x_inv_sum) / n

# # Виведення результатів
# print("Значення параметра a:", a)
# print("Значення параметра b:", b)

# # Рівняння кривої регресії
# def regression_curve(x, a, b):
#     return a / x + b

# # Побудова графіку кривої регресії
# plt.figure(figsize=(8, 6))
# plt.scatter(x_values, y_values, color='purple', label='Точки умовних середніх')
# plt.plot(x_values, regression_curve(x_values, a, b), color='orange', linestyle='-', label='Крива регресії')
# plt.title('Крива регресії Y на X')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Обчислення дисперсії за формулою
# delta = 0
# total_count = df.sum().sum()  # Загальна кількість спостережень

# for i in range(len(df.index)):
#     for j in range(len(df.columns)):
#         nij = df.iloc[i, j]
#         if nij > 0:
#             yj = df.index[i]
#             xi = float(df.columns[j])
#             delta += nij * (yj - regression_curve(xi, a, b)) ** 2

# # Обчислення дисперсії
# dispersion = delta / total_count

# # Виведення результату
# print("Дисперсія Y відносно кривої регресії Y на X:\n", dispersion)

# # Обчислення суми квадратів відхилень від функції регресії
# delta_squared_sum = 0

# for j, xi in enumerate(x_values):
#     yxi = y_values[j]
#     ni = df.iloc[:, j].sum()  # Кількість спостережень для xi
#     delta_squared_sum += ni * (yxi - regression_curve(xi, a, b)) ** 2

# # Виведення результату
# print("Сума квадратів відхилень δ^2 умовних середніх від значень функції регресії:\n", delta_squared_sum)

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import least_squares
# from tabulate import tabulate

# # Зчитування кореляційної таблиці з CSV файлу
# df = pd.read_csv('correlation_table.csv', index_col=0)

# # Конвертуємо значення у числовий формат
# df = df.apply(pd.to_numeric)

# # Виведення кореляційної таблиці
# print("Кореляційна таблиця:")
# print(tabulate(df, headers='keys', tablefmt='grid'))

# # Обчислення умовних середніх Y за умов різних значень X
# conditional_means = {}

# for col in df.columns:
#     total_sum = 0
#     count = 0
#     for index, row in df.iterrows():
#         if not pd.isna(row[col]):
#             total_sum += row[col] * index
#             count += row[col]
#     conditional_mean = total_sum / count if count != 0 else 0
#     conditional_means[col] = conditional_mean
#     print(f"Умовна середня для X={col}: {conditional_mean}")

# # Створення таблиці умовних середніх
# conditional_means_table = pd.DataFrame.from_dict(conditional_means, orient='index', columns=['Умовні середні'])

# # Виведення таблиці умовних середніх
# print("\nТаблиця умовних середніх:")
# print(tabulate(conditional_means_table, headers='keys', tablefmt='grid'))

# # Створення списків координат для побудови точок
# x_values = np.array(list(map(float, conditional_means.keys())))  # Конвертуємо рядки у числа
# y_values = np.array(list(conditional_means.values()))

# # Побудова графіка з лінією, що з'єднує точки
# plt.figure(figsize=(8, 6))
# plt.plot(x_values, y_values, color='purple', marker='o', linestyle='-')
# plt.title('Поле кореляції')
# plt.xlabel('X')
# plt.ylabel('Умовні середні Y')
# plt.grid(True)
# plt.show()

# print("\nПрипускаємо, що це гіперболічна кореляція")

# # Задання початкових значень параметрів a і b
# initial_guess = [1, 1]  # Початкове значення a і b

# # Функція, яка обчислює значення гіперболічної функції регресії
# def hyperbolic_regression(params, x):
#     a, b = params
#     return a / x + b

# # Функція, яка обчислює відхилення між значеннями функції та спостереженнями
# def objective(params):
#     return y_values - hyperbolic_regression(params, x_values)

# # Знаходження значень параметрів a і b за допомогою методу найменших квадратів
# results = least_squares(objective, initial_guess)

# # Отримання значень параметрів a і b
# a, b = results.x

# # Виведення результатів
# print("Значення параметра a:", a)
# print("Значення параметра b:", b)

# # Рівняння кривої регресії
# def regression_curve(x, a, b):
#     return a / x + b


# # Побудова графіку кривої регресії з точками
# plt.figure(figsize=(8, 6))
# plt.plot(x_values, y_values, color='purple', marker='o', linestyle='-', label='Регресія(Поле кореляції)')
# plt.plot(x_values, regression_curve(x_values, a, b), color='orange', marker='o', linestyle='-', label=f'Крива регресії = {a}/x + {b}')
# plt.title('Графік поля регресії та кривої регресії для гіперболічного закону кореляції')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Обчислення дисперсії за формулою
# delta = 0
# total_count = df.sum().sum()  # Загальна кількість спостережень

# for i in range(len(df.index)):
#     for j in range(len(df.columns)):
#         nij = df.iloc[i, j]
#         if nij > 0:
#             yj = df.index[i]
#             xi = float(df.columns[j])
#             delta += nij * (yj - regression_curve(xi, a, b)) ** 2

# # Обчислення дисперсії
# dispersion = delta / total_count

# # Виведення результату
# print("Дисперсія Y відносно кривої регресії Y на X:\n", dispersion)

# # Обчислення суми квадратів відхилень від функції регресії
# delta_squared_sum = 0

# for j, xi in enumerate(x_values):
#     yxi = y_values[j]
#     ni = df.iloc[:, j].sum()  # Кількість спостережень для xi
#     delta_squared_sum += ni * (yxi - regression_curve(xi, a, b)) ** 2

# # Виведення результату
# print("Сума квадратів відхилень δ^2 умовних середніх від значень функції регресії:\n", delta_squared_sum)
















import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import sympy as sp

# Зчитування кореляційної таблиці з CSV файлу
df = pd.read_csv('correlation_table.csv', index_col=0)

# Конвертуємо значення у числовий формат
df = df.apply(pd.to_numeric)

# Виведення кореляційної таблиці
print("Кореляційна таблиця:")
print(tabulate(df, headers='keys', tablefmt='grid'))

# Обчислення умовних середніх Y за умов різних значень X
conditional_means = {}

for col in df.columns:
    total_sum = 0
    count = 0
    for index, row in df.iterrows():
        if not pd.isna(row[col]):
            total_sum += row[col] * index
            count += row[col]
    conditional_mean = total_sum / count if count != 0 else 0
    conditional_means[col] = conditional_mean
    print(f"Умовна середня для X={col}: {conditional_mean}")

# Створення таблиці умовних середніх
conditional_means_table = pd.DataFrame.from_dict(conditional_means, orient='index', columns=['Умовні середні'])

# Виведення таблиці умовних середніх
print("\nТаблиця умовних середніх:")
print(tabulate(conditional_means_table, headers='keys', tablefmt='grid'))

# Створення списків координат для побудови точок
x_values = np.array(list(map(float, conditional_means.keys())))  # Конвертуємо рядки у числа
y_values = np.array(list(conditional_means.values()))

# Побудова графіка з лінією, що з'єднує точки
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, color='purple',marker='o', markerfacecolor='orange', linestyle='-')
plt.title('Поле кореляції')
plt.xlabel('X')
plt.ylabel('Умовні середні Y')
plt.grid(True)
plt.show()


# Створення списків координат для побудови точок
x_values = np.array(list(map(float, conditional_means.keys())))  # Конвертуємо рядки у числа
y_values = np.array(list(conditional_means.values()))

# Оголошення символів
a, b = sp.symbols('a b')

# Оголошення рівнянь
eq1 = a * sum(1/x_values * df.sum()) + b * sum(df.sum()) - sum(y_values * df.sum())
eq2 = a * sum(1/x_values**2 * df.sum()) + b * sum(1/x_values * df.sum()) - sum(1/x_values * y_values * df.sum())

# Розв'язання системи рівнянь
solution = sp.solve((eq1, eq2), (a, b))
print("Розв'язок системи рівнянь:")
print(solution)

# Отримання значень параметрів a і b
a_value, b_value = solution[a], solution[b]

# Рівняння кривої регресії
def regression_curve(x, a, b):
    return a / x + b

# Побудова графіку кривої регресії
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, color='purple', marker='o', markerfacecolor='orange', linestyle='-',  label='Точки умовних середніх')
plt.plot(x_values, regression_curve(x_values, a_value, b_value), color='brown', marker='o', markerfacecolor='green', linestyle='-', label=f'Крива регресії: {a_value}/x + {b_value}')
plt.title('Крива регресії Y на X')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

# Обчислення дисперсії за формулою
delta = 0
total_count = df.sum().sum()  # Загальна кількість спостережень

for i in range(len(df.index)):
    for j in range(len(df.columns)):
        nij = df.iloc[i, j]
        if nij > 0:
            yj = df.index[i]
            xi = float(df.columns[j])
            delta += nij * (yj - regression_curve(xi, a_value, b_value)) ** 2

# Обчислення дисперсії
dispersion = delta / total_count
print("Дисперсія для гіперболічного закону кореляції:\n", dispersion)

# Обчислення суми квадратів відхилень від функції регресії
delta_squared_sum = 0

for j, xi in enumerate(x_values):
    yxi = y_values[j]
    ni = df.iloc[:, j].sum()  # Кількість спостережень для xi
    delta_squared_sum += ni * (yxi - regression_curve(xi, a_value, b_value)) ** 2

# Виведення результату
print("Сума квадратів відхилень для гіперболічного закону кореляції:\n", delta_squared_sum)


# Функція для обчислення f(xi)
def f_of_xi(x, a, b):
    return a / x + b

# Обчислення f(xi) для всіх xi
f_xi_values = f_of_xi(x_values, a_value, b_value)

# Виведення результату
print("f(xi) та різниця yxi - f(xi):")
for xi, f_xi, yxi in zip(x_values, f_xi_values, y_values):
    difference = yxi - f_xi
    print(f"For x={xi}, f(xi)={f_xi}, yxi - f(xi)={difference}")



print("Система рівнянь:")
print("eq1:", eq1)
print("eq2:", eq2)
