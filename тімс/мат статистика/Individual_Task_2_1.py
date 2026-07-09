import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import math
from scipy.stats import chi2

print("H0-рівномірний закон розподілу")
# Read data from CSV file
with open('data1.csv', newline='') as csvfile:
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


#Calculate the sum of ni*xi
sum_ni_xi = sum(int(ni) * (float(x.split('-')[0]) + float(x.split('-')[1])) / 2 for ni, x in zip(frequencies, ranges))

# Calculate the sum of ni
sum_ni = sum(frequencies)

# Calculate the mean x
mean_x = sum_ni_xi / sum_ni
sum_squared_difference = sum(int(ni) * ((float(x.split('-')[0]) + float(x.split('-')[1])) / 2 - mean_x) ** 2 for ni, x in zip(frequencies, ranges))
# Calculate the variance
variance = sum_squared_difference / sum_ni

# Calculate the standard deviation (sigma)
sigma = variance ** 0.5
print(f"x середнє: {mean_x}")
print(f"Дисперсія: {variance}")
print(f"Стандартне відхилення (сигма): {sigma}")

# Calculate a* and b*
a_star = mean_x - math.sqrt(3) * sigma
b_star = mean_x + math.sqrt(3) * sigma
print(f"Значення a*: {a_star}")
print(f"Значення b*: {b_star}")

# Ask the user if they want to use the calculated values or enter their own
use_calculated_values = input("Використовувати обраховані значення? (yes/no): ")
if use_calculated_values.lower() != 'yes':
    a_star = float(input("Введіть значення a*: "))
    b_star = float(input("Введіть значення b*: "))
    

def npi_uniform(intervals, a, b, n):
    p = []
    intervals[0] = (a, intervals[0][1])
    intervals[-1] = (intervals[-1][0], b)
    hystyna = 1/(b-a)
    for i in intervals:
        p.append(hystyna*(i[1] - i[0]))
    npi = [n * i for i in p]
    return npi

# Define the intervals
intervals = [(float(x.split('-')[0]), float(x.split('-')[1])) for x in ranges]

# Call the function to calculate npi for each interval
npi_values = npi_uniform(intervals, a_star, b_star, sum_ni)

# Print each npi value separately
for i, npi in enumerate(npi_values, 1):
    print(f"npi[{i}] = {npi}")

# Додаємо значення npi до даних таблиці
table_data.append(["npi"] + npi_values)

# Calculate pi
pi_values = [npi / sum_ni for npi in npi_values]

# Add pi values to the table data
table_data.append(["pi"] + pi_values)

# Виводимо оновлену таблицю
print("Оновлена таблиця:")
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
df = r - s

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
    print(f"{X_empirical}<{critical_value} => H0 приймаємо(Вибірка є рівномірно розподіленою)")
else:
    print(f"{X_empirical}>{critical_value} => H0 відхиляємо(Вибірка НЕ є рівномірно розподіленою)")


# import csv
# import matplotlib.pyplot as plt
# from tabulate import tabulate
# import math
# from scipy.stats import chi2

# print("H0-рівномірний закон розподілу")
# # Read data from CSV file
# with open('data1.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     data = list(reader)

# # Extract rows with distribution data
# ranges = data[0][1:]
# frequencies = list(map(int, data[1][1:]))

# # Form a list of data to display the initial table
# table_data = [["T, min"] + ranges] + [["ni"] + frequencies]

# # Display the initial table in the specified format
# print("Початкова таблиця:")
# print(tabulate(table_data, headers='firstrow', tablefmt='grid'))

# # Build a frequency polygon for the initial data
# plt.plot(ranges, frequencies, marker='o', linestyle='-')
# plt.title('Полігон частот для вихідних даних')
# plt.xlabel('Діапазони')
# plt.ylabel('Частота')
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


# #Calculate the sum of ni*xi
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
# print(f"x середнє: {mean_x}")
# print(f"Дисперсія: {variance}")
# print(f"Стандартне відхилення (сигма): {sigma}")

# # Calculate a* and b*
# a_star = mean_x - math.sqrt(3) * sigma
# b_star = mean_x + math.sqrt(3) * sigma
# print(f"Значення a*: {a_star}")
# print(f"Значення b*: {b_star}")

# def npi_uniform(intervals, a, b, n):
#     p = []
#     intervals[0] = (a, intervals[0][1])
#     intervals[-1] = (intervals[-1][0], b)
#     hystyna = 1/(b-a)
#     for i in intervals:
#         p.append(hystyna*(i[1] - i[0]))
#     npi = [n * i for i in p]
#     return npi

# # Define the intervals
# intervals = [(float(x.split('-')[0]), float(x.split('-')[1])) for x in ranges]

# # Call the function to calculate npi for each interval
# npi_values = npi_uniform(intervals, a_star, b_star, sum_ni)

# # Print each npi value separately
# for i, npi in enumerate(npi_values, 1):
#     print(f"npi[{i}] = {npi}")

# # Додаємо значення npi до даних таблиці
# table_data.append(["npi"] + npi_values)

# # Calculate pi
# pi_values = [npi / sum_ni for npi in npi_values]

# # Add pi values to the table data
# table_data.append(["pi"] + pi_values)

# # Виводимо оновлену таблицю
# print("Оновлена таблиця:")
# print(tabulate(table_data, headers='firstrow', tablefmt='grid'))


# # Calculate empirical X^2
# X_empirical = sum(((ni - npi) ** 2) / npi for ni, npi in zip(frequencies, npi_values))
# print(f"X^2 емпіричне: {X_empirical}")

# # Define the number of columns
# r = len(table_data[1]) - 2  # Subtract 2 to get r

# # Define the number of degrees of freedom
# s = 2  # Default value
# s_input = input("Введіть значення s (default 2): ")
# if s_input:
#     s = int(s_input)
# df = r - s

# # Define the significance level
# alpha = 0.05  # default value
# alpha_input = input("Введіть альфа (default 0.05): ")
# if alpha_input:
#     alpha = float(alpha_input)

# # Calculate the critical value
# critical_value = chi2.ppf(1 - alpha, df)
# print(f"X^2 критичне: {critical_value}")

# # Compare empirical X^2 and critical X^2
# if X_empirical < critical_value:
#     print(f"{X_empirical}<{critical_value} => H0 приймаємо(Вибірка є рівномірно розподіленою)")
# else:
#     print(f"{X_empirical}>{critical_value} => H0 відхиляємо(Вибірка НЕ є рівномірно розподіленою)")



