import random
from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

def calculate_average(data):
    n = len(data)
    return sum(data) / n

def calculate_mode(data):
    counts = Counter(data)
    max_frequency = max(counts.values())
    mode = [k for k, v in counts.items() if v == max_frequency]
    return mode if len(mode) < len(data) else "Мода не знайдена"
#мода для неперервного
def calculate_mode_continuous(data):
    kde = gaussian_kde(data)
    x_values = np.linspace(min(data), max(data), 1000)
    pdf_values = kde(x_values)
    
    modes = x_values[pdf_values == max(pdf_values)]
    
    return modes.tolist() if modes else "Мода не знайдена"

def calculate_median(data):
    sorted_data = sorted(data)
    n = len(data)
    if n % 2 == 0:
        median1 = sorted_data[n // 2]
        median2 = sorted_data[n // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = sorted_data[n // 2]
    return median
#медіана для неперервного
def calculate_median_continuous(data):
    sorted_data = np.sort(data)
    n = len(sorted_data)
    
    if n % 2 == 0:
        median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        median = sorted_data[n//2]
    
    return median

def calculate_deviation(data, avg_data):
    deviations = [(x - avg_data) ** 2 for x in data]
    return sum(deviations)

def calculate_variance(data, n):
    return calculate_deviation(data, calculate_average(data)) / (n - 1)

def calculate_dyspersiia(data, n):
    return calculate_deviation(data, calculate_average(data)) / n

def calculate_standard(data):
    return math.sqrt(calculate_variance(data, len(data)))

def calculate_range(data):
    return max(data) - min(data)

def calculate_variation(data, avg_data):
    return calculate_standard(data) / avg_data

def calculate_standard_deviation(data):
    return math.sqrt(calculate_dyspersiia(data, len(data)))

def calculate_moment(data, order):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** order for x in data) / n

def calculate_quantile(data, percentile):
    sorted_data = sorted(data)
    n = len(data)
    index = int(n * percentile / 100)
    return sorted_data[index]

def calculate_skewness(data):
    n = len(data)
    mean = sum(data) / n
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in data) / n)
    skewness = sum((x - mean) ** 3 for x in data) / (n * std_dev**3)
    return skewness

def calculate_kurtosis(data):
    n = len(data)
    mean = sum(data) / n
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in data) / n)
    kurtosis = sum((x - mean) ** 4 for x in data) / (n * std_dev**4) - 3
    return kurtosis

def build_frequency_table(data):
    frequency_table = {}
    for value in data:
        frequency_table[value] = frequency_table.get(value, 0) + 1
    return sorted(frequency_table.items(), key=lambda x: x[0])

def build_variation_series(data):
    variation_series = sorted(data)
    return variation_series

def empirical_distribution(data):
    unique_values, counts = np.unique(data, return_counts=True)
    cumulative_prob = np.cumsum(counts) / len(data)
    return unique_values, cumulative_prob

def print_empirical_distribution(unique_values, cumulative_prob):
    print("\n-----Емпірична функція розподілу-----")
    print("  x  \tПроміжок")
    for x, p in zip(unique_values, cumulative_prob):
        print(f"{round(p, 2)}\t{x} <= x < {x+1}")
    print("\n")

print(f"--------------------------------------------------------------------------")
n = int(input("Введіть об'єм вибірки: "))
data = [random.randint(0, 10) for _ in range(n)]
print(f"Згенерована вибірка:\n", data)
frequency_table = build_frequency_table(data)
variation_series = build_variation_series(data)

print("\nВаріаційний ряд:\n", variation_series)
print("\nЧастотна таблиця:")
print("Значення\tЧастота")
for value, frequency in frequency_table:
    print(f"{value}:\t\t{frequency}")

avg_data = calculate_average(data)
mode_data = calculate_mode(data)
median_data = calculate_median(data)
deviation_data = calculate_deviation(data, avg_data)
variance_data = calculate_variance(data, n)
dyspersiia_data = calculate_dyspersiia(data, n)
standard_data = calculate_standard(data)
range_data = calculate_range(data)
variation_data = calculate_variation(data, avg_data)
standard_deviation_data = calculate_standard_deviation(data)
###
#order = int(input("Введіть порядок моменту: "))
#moment_result = calculate_moment(data, order)
#percentile = float(input("Введіть відсоток для квантиля: "))
#quantile_result = calculate_quantile(data, percentile)
###
skewness_result = calculate_skewness(data)
kurtosis_result = calculate_kurtosis(data)
unique_values, cumulative_prob = empirical_distribution(data)

print("\n------Числові характеристики-----")
print("Середнє вибіркове =", avg_data)
print("Мода =", mode_data)
print("Медіана =", median_data)
print("Розмах =", range_data)
print("Девіація =", deviation_data)
print("Варіанса =", variance_data)
print("Стандарт =", standard_data)
print("Варіація =", variation_data)
print("Вибіркова дисперсія =", dyspersiia_data)
print("Середньоквадратичне відхилення =", standard_deviation_data)
# 
#print("Момент:", moment_result)
#print("Квантиль:", quantile_result)
#
print("Асиметрія:", skewness_result)
print("Ексцес:", kurtosis_result)

print_empirical_distribution(unique_values, cumulative_prob)

#plt.figure(figsize=(8, 6))
plt.hist(data, bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Значення')
plt.ylabel('Частота')
plt.title('Гістограма')
plt.show()

unique_values, counts = np.unique(data, return_counts=True)
plt.plot(unique_values, counts, marker='o', linestyle='-', color='skyblue')
plt.xlabel('Значення')
plt.ylabel('Частота')
plt.title('Полігон частот')
plt.show()

plt.bar(unique_values, counts, color='skyblue', width=0.1)
plt.xlabel('Значення')
plt.ylabel('Частота')
plt.title('Діаграма частот')
plt.show()

plt.step(unique_values, cumulative_prob, where='post')
plt.title('Емпірична функція розподілу')
plt.xlabel('Значення')
plt.ylabel('Кумулятивна ймовірність')
plt.show()

n_continuous = int(input("Введіть об'єм неперервної вибірки: "))
data_continuous = [random.uniform(0, 10) for _ in range(n_continuous)]

def create_continuous_intervals(data, num_bins=10):
    # Визначення границь інтервалів
    min_value = min(data)
    max_value = max(data)
    bin_width = (max_value - min_value) / num_bins
    bin_edges = [min_value + i * bin_width for i in range(num_bins + 1)]

    # Побудова інтервалів
    intervals = [(bin_edges[i], bin_edges[i+1]) for i in range(num_bins)]

    # Підрахунок частоти (щільності) у кожному інтервалі
    hist, _ = np.histogram(data, bins=bin_edges)

    return intervals, hist

def print_continuous_intervals(intervals, frequencies):
    print("\n-----Інтервальний статистичний розподіл-----")
    print("Інтервал\t\t\t\t\tЧастота")
    for interval, frequency in zip(intervals, frequencies):
        print(f"{interval}\t\t{frequency}")
    print("\n")
intervals, frequencies = create_continuous_intervals(data_continuous)
print_continuous_intervals(intervals, frequencies)

# Розрахунок статистичних характеристик для неперервної вибірки
avg_data_continuous = calculate_average(data_continuous)
mode_data_continuous = calculate_mode_continuous(data_continuous)
median_data_continuous = calculate_median_continuous(data_continuous)
deviation_data_continuous = calculate_deviation(data_continuous, avg_data_continuous)
variance_data_continuous = calculate_variance(data_continuous, n_continuous)
dyspersiia_data_continuous = calculate_dyspersiia(data_continuous, n_continuous)
standard_data_continuous = calculate_standard(data_continuous)
range_data_continuous = calculate_range(data_continuous)
variation_data_continuous = calculate_variation(data_continuous, avg_data_continuous)
standard_deviation_data_continuous = calculate_standard_deviation(data_continuous)
range_data_continuous = calculate_range(data_continuous)
variation_data_continuous = calculate_variation(data_continuous, avg_data_continuous)
#
#order = int(input("Введіть порядок моменту: "))
#moment_result = calculate_moment(data_continuous, order)
#percentile = float(input("Введіть відсоток для квантиля: "))
#quantile_result = calculate_quantile(data_continuous, percentile)
##
skewness_result_continuous = calculate_skewness(data_continuous)
kurtosis_result_continuous = calculate_kurtosis(data_continuous)

# Побудова і графічне відображення емпіричної функції розподілу для неперервної вибірки
unique_values_continuous, cumulative_prob_continuous = empirical_distribution(data_continuous)

# Виведення числових характеристик для неперервної вибірки
print("\n------Числові характеристики для неперервної вибірки-----")
print("Середнє вибіркове =", avg_data_continuous)
print("Мода =", mode_data_continuous)
print("Медіана =", median_data_continuous)
print("Девіація =", deviation_data_continuous)
print("Варіанса =", variance_data_continuous)
print("Дисперсія =", dyspersiia_data_continuous)
print("Стандарт =", standard_data_continuous)
print("Розмах =", range_data_continuous)
print("Варіація =", variation_data_continuous)
print("Середньоквадратичне відхилення =", standard_deviation_data_continuous)
#
#print("Момент:", moment_result)
#print("Квантиль:", quantile_result)
#
print("Асиметрія:", skewness_result_continuous)
print("Ексцес:", kurtosis_result_continuous)

# Гістограма для неперервної вибірки
plt.hist(data_continuous, bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Значення')
plt.ylabel('Частота')
plt.title('Гістограма')
plt.show()

# Графічне відображення емпіричної функції розподілу для неперервної вибірки
plt.step(unique_values_continuous, cumulative_prob_continuous, where='post')
plt.title('Емпірична функція розподілу для неперервної вибірки')
plt.xlabel('Значення')
plt.ylabel('Кумулятивна ймовірність')
plt.show()








'''
import numpy as np
import pandas as pd
from collections import Counter
from random import randint
import matplotlib.pyplot as plt
import math 


mylist = [3,7,6,3,4,4,7,9,4,5,5,5,3,7,8,4,9,7,7,4,8,5,3,4,7,6,7,9,6,5]
n = 30
data = pd.Series(mylist)
print("\nУмова:", data.tolist())



sort_data = sorted(data)
print("\nВаріаційний ряд:", sort_data)

print("Частотна таблиця: значення-частота")
table = data.value_counts().sort_index()
print(table)

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.set_title('Діаграма частот')
ax.set_ylabel('Частота значень')
ax.set_xlabel('Значення')
i = table.index
v = table.values
ax.bar(i,v, color ='maroon', width = 0.05)
plt.show()

plt.plot(i, v, c="maroon")
plt.title('Полігон частот')
plt.xlabel('Частота значень')
plt.ylabel('Значення')
plt.show()

print("---Числові характеристики---")  

avg_data = sum(data) / n
print("Середнє арифметичне =", avg_data)

d = Counter(data)
get_mode = dict(d)
mode = [k for k, v in get_mode.items() if v == max(list(d.values()))]
if len(mode) == n:
    get_mode = "Моду не знайдено"
else:
    get_mode = "Мода = " + ', '.join(map(str, mode))
print(get_mode)  

if n%2 == 0:
    median1 = sort_data[n//2]
    median2 = sort_data[n//2 - 1]
    median = (median1 + median2)/2
else:
    median = sort_data[n//2]
print("Медіана =", median)  

def deviation(datas):
    d = [(x - avg_data) ** 2 for x in datas]
    return sum(d)
print("Девіація =", deviation(data))  

def variance(datas):
    return (deviation(data) / (n-1))
print("Варіанса =", variance(data))  

def dyspersiia(datas):
    return (deviation(data) / n)
print("Дисперсія =", dyspersiia(data))  

def standart(datas):
    return (+math.sqrt(variance(data)))
print("Стандарт =", standart(data)) 

p = max(data) - min(data) 
print("Розмах =", p)

def variation(datas):
    return (standart(datas)/avg_data)
print("Варіація =", variation(data)) 

def standard_deviation(datas):
    return (math.sqrt(dyspersiia(data)))
print("Середньоквадратичне відхилення =", standard_deviation(data))  

def empirical_function(datas):
    return np.cumsum(table)/ n
print("Емпірична функція Fn(x)\n", empirical_function(data))

#m = int(input("Введіть m: "))
m = 4
d = p/m
print("Довжина класу =", d)

intervals = []
sum = min(data)
while sum != max(data):
    interval = []
    interval.append(round(sum, 2))
    sum+=d
    interval.append(round(sum, 2))
    intervals.append(interval)
print(intervals)
'''