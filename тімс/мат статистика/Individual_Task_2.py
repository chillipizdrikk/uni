import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import math
from scipy.stats import chi2


print("H0-нормальний закон розподілу")
# Read data from CSV file
with open('data2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Extract rows with distribution data
ranges = data[0][1:]
frequencies = list(map(int, data[1][1:]))

# Form a list of data to display the initial table
table_data = [["T, min"] + ranges] + [["ni"] + frequencies]

# Display the initial table in the specified format
print("Початкова таблиця:")
print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# Build a histogram for the initial data
plt.bar(ranges, frequencies, color='skyblue', edgecolor='black')
plt.title('Гістограма для вихідних даних')
plt.xlabel('Діапазони')
plt.ylabel('Частота')
plt.xticks(rotation=45)
plt.show()

# Build a frequency polygon for the initial data
plt.plot(ranges, frequencies, marker='o', linestyle='-')
plt.title('Полігон частот для вихідних даних')
plt.xlabel('Діапазони')
plt.ylabel('Частота')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Check the condition ni>=5 and merge columns if necessary
i = 0
while i < len(frequencies):
    if frequencies[i] < 5:
        if i != 0:  # Merge with the previous column if it's not the first column
            frequencies[i-1] += frequencies[i]
            ranges[i-1] = ranges[i-1].split('-')[0] + '-' + ranges[i].split('-')[1]  # Merge ranges
            del frequencies[i]
            del ranges[i]
        else:  # Merge with the next column if it's the first column
            frequencies[i+1] += frequencies[i]
            ranges[i+1] = ranges[i].split('-')[0] + '-' + ranges[i+1].split('-')[1]  # Merge ranges
            del frequencies[i]
            del ranges[i]
    else:
        i += 1

# Form a list of data to display the new table
table_data = [["T, min"] + ranges] + [["ni"] + frequencies]

# Display the new table in the specified format
print("Нова таблиця:")
print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# Define the function to calculate the value of Ф(x) using Laplace's function
def laplace_function(x):
    if x < -4:
        return 0
    elif x > 4:
        return 0.5
    else:
        return (1 + math.erf(x / math.sqrt(2))) / 2


# Define whether to use calculated or manual values for a (mean_x) and sigma
use_calculated_values = input("Ви бажаєте використовувати обчислені значення для a та сигма?(yes/no): ").lower()

if use_calculated_values == 'yes':
    # Calculate the mean value of x
    sum_ni_xi = sum(int(ni) * (float(x.split('-')[0]) + float(x.split('-')[1])) / 2 for ni, x in zip(frequencies, ranges))
    sum_ni = sum(frequencies)
    mean_x = sum_ni_xi / sum_ni

    # Calculate the sum of squared differences
    sum_squared_difference = sum(int(ni) * ((float(x.split('-')[0]) + float(x.split('-')[1])) / 2 - mean_x) ** 2 for ni, x in zip(frequencies, ranges))

    # Calculate the variance and standard deviation (sigma)
    variance = sum_squared_difference / sum_ni
    sigma = variance ** 0.5

    print(f"Використання обчислених значень: x середнє = {mean_x}, дисперсія = {variance}, сигма = {sigma}")

else:
    mean_x = float(input("Введіть значення a (x середнє): "))
    sigma = float(input("Введіть значення сигми: "))

# Initialize a list to store pi values
pi_values = []

# Calculate p1 separately
argument_h1 = (-float('inf') - mean_x) / sigma
argument_h2 = (float(ranges[0].split('-')[1]) - mean_x) / sigma
p1 = laplace_function(argument_h2) - laplace_function(argument_h1)
print(f"p[1] = {p1}")

# Calculate pi values starting from p2
for i in range(1, len(ranges)):
    hi_1 = float(ranges[i].split('-')[0])
    hi = float(ranges[i].split('-')[1])
    argument_hi = (hi - mean_x) / sigma
    argument_hi_1 = (hi_1 - mean_x) / sigma
    pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
    print(f"p[{i+1}] = {pi}")

# Calculate npi values
for i in range(len(ranges)):
    hi_1 = float(ranges[i].split('-')[0])
    hi = float(ranges[i].split('-')[1])
    argument_hi = (hi - mean_x) / sigma
    argument_hi_1 = (hi_1 - mean_x) / sigma
    sum_ni = sum(frequencies)
    pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
    npi = sum_ni * pi
    print(f"npi[{i+1}] = {npi}")

# Calculate pi and npi values
pi_values = [p1]
npi_values = [sum_ni * p1]
for i in range(1, len(ranges)):
    hi_1 = float(ranges[i].split('-')[0])
    hi = float(ranges[i].split('-')[1])
    argument_hi = (hi - mean_x) / sigma
    argument_hi_1 = (hi_1 - mean_x) / sigma
    pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
    npi = sum_ni * pi
    pi_values.append(pi)
    npi_values.append(npi)

# Add pi and npi to the table data
table_data += [["pi"] + pi_values, ["npi"] + npi_values]

# Display the new table with pi and npi
print("Нова таблиця з pi та npi:")
print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# Перевірте умову npi>=10 та об'єднайте стовпці за потреби
i = 0
merged = False  # Додаткова змінна для відстеження, чи були об'єднані стовпці
while i < len(npi_values):
    if npi_values[i] < 10:
        merged = True  # Якщо стовпці об'єднані, встановіть merged в True
        if i != 0:  # Об'єднайте з попереднім стовпцем, якщо це не перший стовпець
            npi_values[i-1] += npi_values[i]
            ranges[i-1] = ranges[i-1].split('-')[0] + '-' + ranges[i].split('-')[1]  # Об'єднайте діапазони
            del npi_values[i]
            del ranges[i]
        else:  # Об'єднайте з наступним стовпцем, якщо це перший стовпець
            npi_values[i+1] += npi_values[i]
            ranges[i+1] = ranges[i].split('-')[0] + '-' + ranges[i+1].split('-')[1]  # Об'єднайте діапазони
            del npi_values[i]
            del ranges[i]
    else:
        i += 1

# Якщо стовпці були об'єднані, виведіть нову таблицю
if merged:
    # Сформуйте список даних для відображення нової таблиці
    table_data = [["T, min"] + ranges] + [["ni"] + frequencies, ["pi"] + pi_values, ["npi"] + npi_values]

    # Відобразіть нову таблицю в заданому форматі
    print("Таблиця з об'єднаними комірками по npi:")
    print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# Calculate empirical X^2
X_empirical = sum(((ni - npi) ** 2) / npi for ni, npi in zip(frequencies, npi_values))
print(f"X^2 емпіричне: {X_empirical}")

# Define the number of columns
r = len(table_data[1]) - 2  # Subtract 2 to get r

# Define the number of degrees of freedom
s = 2  # Default value
s_input = input("Введіть значення s (default 2): ")
if s_input:
    s = int(s_input)
df = r-s

# Define the significance level
alpha = 0.05  # default value
alpha_input = input("Введіть альфа (default 0.05): ")
if alpha_input:
    alpha = float(alpha_input)

# Calculate the critical value
critical_value = chi2.ppf(1 - alpha, df)
print(f"X^2 критичне: {critical_value}")

# Compare empirical X^2 and critical X^2
if X_empirical < critical_value:
    print(f"{X_empirical}<{critical_value} => H0 приймаємо(Вибірка є нормально розподіленою)")
else:
    print(f"{X_empirical}>{critical_value} => H0 відхиляємо(Вибірка НЕ є нормально розподіленою)")

sum_pi = sum(pi_values)
print(f"Сума {sum_pi}")




# import csv
# import matplotlib.pyplot as plt
# from tabulate import tabulate
# import math
# from scipy.stats import chi2


# print("H0-нормальний закон розподілу")
# # Read data from CSV file
# with open('data.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     data = list(reader)

# # Extract rows with distribution data
# ranges = data[0][1:]
# frequencies = list(map(int, data[1][1:]))

# # Form a list of data to display the initial table
# table_data = [["T, min"] + ranges] + [["ni"] + frequencies]

# # Display the initial table in the specified format
# print("Initial table:")
# print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# # Build a histogram for the initial data
# plt.bar(ranges, frequencies, color='skyblue', edgecolor='black')
# plt.title('Histogram for initial data')
# plt.xlabel('Ranges')
# plt.ylabel('Frequency')
# plt.xticks(rotation=45)
# plt.show()

# # Build a frequency polygon for the initial data
# plt.plot(ranges, frequencies, marker='o', linestyle='-')
# plt.title('Frequency polygon for initial data')
# plt.xlabel('Ranges')
# plt.ylabel('Frequency')
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# # Check the condition ni>=5 and merge columns if necessary
# i = 0
# while i < len(frequencies):
#     if frequencies[i] < 5:
#         if i != 0:  # Merge with the previous column if it's not the first column
#             frequencies[i-1] += frequencies[i]
#             ranges[i-1] = ranges[i-1].split('-')[0] + '-' + ranges[i].split('-')[1]  # Merge ranges
#             del frequencies[i]
#             del ranges[i]
#         else:  # Merge with the next column if it's the first column
#             frequencies[i+1] += frequencies[i]
#             ranges[i+1] = ranges[i].split('-')[0] + '-' + ranges[i+1].split('-')[1]  # Merge ranges
#             del frequencies[i]
#             del ranges[i]
#     else:
#         i += 1

# # Form a list of data to display the new table
# table_data = [["T, min"] + ranges] + [["ni"] + frequencies]

# # Display the new table in the specified format
# print("New table:")
# print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# # Calculate the sum of ni*xi
# sum_ni_xi = sum(int(ni) * (float(x.split('-')[0]) + float(x.split('-')[1])) / 2 for ni, x in zip(frequencies, ranges))

# # Calculate the sum of ni
# sum_ni = sum(frequencies)

# # Calculate the mean x
# mean_x = sum_ni_xi / sum_ni
# sum_squared_difference = sum(int(ni) * ((float(x.split('-')[0]) + float(x.split('-')[1])) / 2 - mean_x) ** 2 for ni, x in zip(frequencies, ranges))

# # Calculate the variance
# variance = sum_squared_difference / sum_ni

# # Calculate the standard deviation (sigma)
# sigma = variance ** 0.5
# print(f"The mean value of x is: {mean_x}")
# print(f"The variance is: {variance}")
# print(f"The standard deviation (sigma) is: {sigma}")

# # Define the function to calculate the value of Ф(x) using Laplace's function
# def laplace_function(x):
#     if x < -4:
#         return 0
#     elif x > 4:
#         return 0,5
#     else:
#         return (1 + math.erf(x / math.sqrt(2))) / 2

# # Initialize a list to store pi values
# pi_values = []

# # Calculate p1 separately
# argument_h1 = (-float('inf') - mean_x) / sigma
# argument_h2 = (float(ranges[0].split('-')[1]) - mean_x) / sigma
# p1 = laplace_function(argument_h2) - laplace_function(argument_h1)
# print(f"p[1] = {p1}")

# # Calculate pi values starting from p2
# for i in range(1, len(ranges)):
#     hi_1 = float(ranges[i].split('-')[0])
#     hi = float(ranges[i].split('-')[1])
#     argument_hi = (hi - mean_x) / sigma
#     argument_hi_1 = (hi_1 - mean_x) / sigma
#     pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
#     print(f"p[{i+1}] = {pi}")

# # Calculate npi values
# for i in range(len(ranges)):
#     hi_1 = float(ranges[i].split('-')[0])
#     hi = float(ranges[i].split('-')[1])
#     argument_hi = (hi - mean_x) / sigma
#     argument_hi_1 = (hi_1 - mean_x) / sigma
#     pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
#     npi = sum_ni * pi
#     print(f"npi[{i+1}] = {npi}")



# # Calculate pi and npi values
# pi_values = [p1]
# npi_values = [sum_ni * p1]
# for i in range(1, len(ranges)):
#     hi_1 = float(ranges[i].split('-')[0])
#     hi = float(ranges[i].split('-')[1])
#     argument_hi = (hi - mean_x) / sigma
#     argument_hi_1 = (hi_1 - mean_x) / sigma
#     pi = laplace_function(argument_hi) - laplace_function(argument_hi_1)
#     npi = sum_ni * pi
#     pi_values.append(pi)
#     npi_values.append(npi)


# # Add pi and npi to the table data
# table_data += [["pi"] + pi_values, ["npi"] + npi_values]

# # Display the new table with pi and npi
# print("New table with pi and npi:")
# print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# # Calculate empirical X^2
# X_empirical = sum(((ni - npi) ** 2) / npi for ni, npi in zip(frequencies, npi_values))
# print(f"The empirical X^2 is: {X_empirical}")

# # Define the number of columns
# r = len(table_data[1]) - 2  # Subtract 2 to get r

# # Define the number of degrees of freedom
# s = 2  # Default value
# s_input = input("Enter the value of s (default is 2): ")
# if s_input:
#     s = int(s_input)
# df = r - s

# # Define the significance level
# alpha = 0.05  # default value
# alpha_input = input("Enter the significance level (default is 0.05): ")
# if alpha_input:
#     alpha = float(alpha_input)

# # Calculate the critical value
# critical_value = chi2.ppf(1 - alpha, df)
# print(f"The critical X^2 is: {critical_value}")

# # Compare empirical X^2 and critical X^2
# if X_empirical < critical_value:
#     print(f"{X_empirical}<{critical_value} => H0 приймаємо(Вибірка є нормально розподіленою)")
# else:
#     print(f"{X_empirical}>{critical_value} => H0 відхиляємо(Вибірка НЕ є нормально розподіленою)")
