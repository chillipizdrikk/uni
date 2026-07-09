# Лабораторна робота №8 (Python)
# Функції планування, лямбда-вирази, замикання

print("=== Лабораторна робота №8 (Python) ===")

# Приклад 1: map з лямбда
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
print("Квадрати чисел:", squares)

# Приклад 2: reduce з лямбда
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print("Сума чисел:", total)

# Приклад 3: лексичне замикання
def make_counter():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner

counter = make_counter()
print("Лічильник:", counter(), counter(), counter())
