#завдання 1
import math
def is_point_in_circle(x, y, R):
    return x**2 + y**2 <= R**2

def is_point_in_triangle(x, y, R):
    return x <= 0 and y <= 0 and x + y >= -R

x = float(input("Введіть координату x точки: "))
y = float(input("Введіть координату y точки: "))
R = float(input("Введіть радіус кола R: "))

if (x > 0 and y > 0 and is_point_in_circle(x, y, R)) or (is_point_in_triangle(x, y, R)):
    print(f"Точка ({x}, {y}) знаходиться всередині заданих секторів кола з радіусом {R}")
else:
    print(f"Точка ({x}, {y}) не знаходиться всередині заданих секторів кола з радіусом {R}")


print('\n\n\n\n\n')

#завдання №2
def find_gcd(a, b, c):
    min_gcd = min(a, b, c)
    gcd = 1
    for i in range(1, min_gcd + 1):
        if a % i == 0 and b % i == 0 and c % i == 0:
            gcd = i
    return gcd

a = int(input('Введіть 1 число: '))
b = int(input('Введіть 2 число: '))
c = int(input('Введіть 3 число: '))

result = find_gcd(a, b, c)
print(f"Найбільший спільний дільник чисел {a}, {b} і {c} дорівнює {result}")