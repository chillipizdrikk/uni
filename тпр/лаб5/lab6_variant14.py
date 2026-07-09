"""
Лабораторна робота #6 - Варіант 14
Задача протидії коаліцій з урахуванням факторів ризику

Варіант 14:
I'_12(x,y) = (3x^2 + 4y^2 + 5xy) / 10,  x∈[0;3], y∈[0;3]
I'_21(x,y) = (4x - 2y^2 + 5xy) / 5,     x∈[0;3], y∈[0;3]

Функції збитку (Таблиця 4.2, варіант 14):
J_12ns(x,y) = (2y + x + 1.2xy) / 7
J_12fm(x,y) = y + 1.5x + 3x + 3.78   (тобто y + 4.5x + 3.78)
J_12in(x,y) = (3.44y - 3.8x - 2.6xy + 4.7) / 10

J_21ns(x,y) = (0.37y + 1.36x + 2.21x + 3.6) / 2  = (0.37y + 3.57x + 3.6) / 2
J_21fm(x,y) = 1.14y + 2.5x + 3.45xy - 3
J_21in(x,y) = (0.76y - x - 0.37xy + 5.3) / 12.3

Ситуаційні матриці (Таблиця 4.3, варіант 14):
R1 (y=0,1,2,3):
        S1      S2      S3      S4
eta_ns: 0.03    0.11    0.09    0.02
eta_fm: 0.17    0.43    0.03    0.03
eta_in: 0.26    0.25    0.02    0.06

R2 (x=0,1,2,3):
        S1      S2      S3      S4
eta_ns: 0.13    0.01    0.19    0.27
eta_fm: 0.07    0.24    0.3     0.15
eta_in: 0.16    0.5     0.29    0.08
"""

import numpy as np

print("=" * 65)
print("ЛАБОРАТОРНА РОБОТА #5 - Варіант 14")

# ВИХІДНІ ДАНІ
def I12(x, y):
    return (3*x**2 + 4*y**2 + 5*x*y) / 10

def I21(x, y):
    return (4*x - 2*y**2 + 5*x*y) / 5

# Функції збитку коаліції 1
def J12ns(x, y):
    return (2*y + x + 1.2*x*y) / 7

def J12fm(x, y):
    return y + 1.5*x + 3*x + 3.78   # y + 4.5x + 3.78

def J12in(x, y):
    return (3.44*y - 3.8*x - 2.6*x*y + 4.7) / 10

# Функції збитку коаліції 2
def J21ns(x, y):
    return (0.37*y + 1.36*x + 2.21*x + 3.6) / 2   # (0.37y + 3.57x + 3.6)/2

def J21fm(x, y):
    return 1.14*y + 2.5*x + 3.45*x*y - 3

def J21in(x, y):
    return (0.76*y - x - 0.37*x*y + 5.3) / 12.3

# Ситуаційні матриці ймовірностей
# R1: рядки - eta_ns, eta_fm, eta_in; стовпці - S1(y=0), S2(y=1), S3(y=2), S4(y=3)
R1 = np.array([
    [0.03, 0.11, 0.09, 0.02],   # eta_ns
    [0.17, 0.43, 0.03, 0.03],   # eta_fm
    [0.26, 0.25, 0.02, 0.06],   # eta_in
])
# Ситуації для R1 відповідають y = 0,1,2,3

# R2: рядки - eta_ns, eta_fm, eta_in; стовпці - S1(x=0), S2(x=1), S3(x=2), S4(x=3)
R2 = np.array([
    [0.13, 0.01, 0.19, 0.27],   # eta_ns
    [0.07, 0.24, 0.30, 0.15],   # eta_fm
    [0.16, 0.50, 0.29, 0.08],   # eta_in
])
# Ситуації для R2 відповідають x = 0,1,2,3

x_vals = [0, 1, 2, 3]
y_vals = [0, 1, 2, 3]

# ЗАВДАННЯ 1: Принцип гарантованого результату
print("=" * 65)
print("ЗАВДАННЯ 1: Гарантований результат")
print("=" * 65)

# Таблиця I'12(x,y)
print("\nТаблиця значень I'_12(x,y):")
header = 'y\\x'
print(f"{header:>6}", end="")
for x in x_vals:
    print(f"  {x:>10}", end="")
print()

I12_table = np.zeros((len(y_vals), len(x_vals)))
for i, y in enumerate(y_vals):
    print(f"{y:>6}", end="")
    for j, x in enumerate(x_vals):
        val = I12(x, y)
        I12_table[i, j] = val
        print(f"  {val:>10.6f}", end="")
    print()

# Гарантований результат для коаліції 1: max_x min_y I'12(x,y)
min_by_y = np.min(I12_table, axis=0)   # мін по y для кожного x
I12_star = np.max(min_by_y)
x_star_12 = x_vals[np.argmax(min_by_y)]
y_star_12 = y_vals[np.argmin(I12_table[:, np.argmax(min_by_y)])]

print(f"\nI*_12 = max_x min_y I'_12(x,y) = {I12_star:.6f}")
print(f"Гарантований результат для коаліції 1: точка x={x_star_12}, y={y_star_12}")

# Таблиця I'21(x,y)
print("\nТаблиця значень I'_21(x,y):")
print(f"{header:>6}", end="")
for x in x_vals:
    print(f"  {x:>10}", end="")
print()

I21_table = np.zeros((len(y_vals), len(x_vals)))
for i, y in enumerate(y_vals):
    print(f"{y:>6}", end="")
    for j, x in enumerate(x_vals):
        val = I21(x, y)
        I21_table[i, j] = val
        print(f"  {val:>10.6f}", end="")
    print()

# Гарантований результат для коаліції 2: max_y min_x I'21(x,y)
min_by_x = np.min(I21_table, axis=1)   # мін по x для кожного y
I21_star = np.max(min_by_x)
y_star_21 = y_vals[np.argmax(min_by_x)]
x_star_21 = x_vals[np.argmin(I21_table[np.argmax(min_by_x), :])]

print(f"\nI*_21 = max_y min_x I'_21(x,y) = {I21_star:.6f}")
print(f"Гарантований результат для коаліції 2: точка x={x_star_21}, y={y_star_21}")

# ЗАВДАННЯ 2: Цільові функції з урахуванням факторів ризику
print("\n" + "=" * 65)
print("ЗАВДАННЯ 2: Цільові функції з урахуванням факторів ризику")
print("=" * 65)

# Формула (4.17):
# F_Sigma12(x,y,eta) = (1-eta_ns)(1-eta_fm)(1-eta_in)*I'_12(x,y)
#                    - (eta_ns*J12ns + eta_fm*J12fm + eta_in*J12in)

def F_sigma12(x, y, eta_ns, eta_fm, eta_in):
    return ((1 - eta_ns) * (1 - eta_fm) * (1 - eta_in) * I12(x, y)
            - (eta_ns * J12ns(x, y) + eta_fm * J12fm(x, y) + eta_in * J12in(x, y)))

def F_sigma21(x, y, eta_ns, eta_fm, eta_in):
    return ((1 - eta_ns) * (1 - eta_fm) * (1 - eta_in) * I21(x, y)
            - (eta_ns * J21ns(x, y) + eta_fm * J21fm(x, y) + eta_in * J21in(x, y)))

# Для коаліції 1: гарантований результат у точці x=x_star_12, y=y_star_12
# За значенням y визначаємо ситуацію (y=0->S1, y=1->S2, y=2->S3, y=3->S4)
sit_idx_12 = y_star_12   # індекс ситуації для R1

eta_ns_12 = R1[0, sit_idx_12]
eta_fm_12 = R1[1, sit_idx_12]
eta_in_12 = R1[2, sit_idx_12]

print(f"\nКоаліція 1: гарантований результат у точці x={x_star_12}, y={y_star_12}")
print(f"Ситуація S{sit_idx_12+1}: eta_ns={eta_ns_12}, eta_fm={eta_fm_12}, eta_in={eta_in_12}")

F_12_guar = F_sigma12(x_star_12, y_star_12, eta_ns_12, eta_fm_12, eta_in_12)
print(f"F_Σ12({x_star_12},{y_star_12}) = {F_12_guar:.6f}")

# Для коаліції 2: гарантований результат у точці x=x_star_21, y=y_star_21
# За значенням x визначаємо ситуацію (x=0->S1, x=1->S2, x=2->S3, x=3->S4)
sit_idx_21 = x_star_21   # індекс ситуації для R2

eta_ns_21 = R2[0, sit_idx_21]
eta_fm_21 = R2[1, sit_idx_21]
eta_in_21 = R2[2, sit_idx_21]

print(f"\nКоаліція 2: гарантований результат у точці x={x_star_21}, y={y_star_21}")
print(f"Ситуація S{sit_idx_21+1}: eta_ns={eta_ns_21}, eta_fm={eta_fm_21}, eta_in={eta_in_21}")

F_21_guar = F_sigma21(x_star_21, y_star_21, eta_ns_21, eta_fm_21, eta_in_21)
print(f"F_Σ21({x_star_21},{y_star_21}) = {F_21_guar:.6f}")

# ЗАВДАННЯ 3: Найнесприятливіша ситуація
print("\n" + "=" * 65)
print("ЗАВДАННЯ 3: Найнесприятливіша ситуація")
print("=" * 65)

# Ймовірність ситуації = добуток відповідних ймовірностей з матриці
# P(Sk) = eta_ns[k] * eta_fm[k] * eta_in[k]
print("\nЙмовірності ситуацій для коаліції 1 (R1):")
P1 = []
for k in range(R1.shape[1]):
    p = R1[0, k] * R1[1, k] * R1[2, k]
    P1.append(p)
    print(f"  P(S{k+1}) = {R1[0,k]} * {R1[1,k]} * {R1[2,k]} = {p:.6f}")

worst_sit_12 = np.argmax(P1)
print(f"\nНайнесприятливіша ситуація для коаліції 1: S{worst_sit_12+1} (y={worst_sit_12})")

# Максимальне значення I'12 для ситуації worst_sit_12 (y = worst_sit_12)
y_worst_12 = worst_sit_12
I12_vals_worst = [I12(x, y_worst_12) for x in x_vals]
I12_max_worst = max(I12_vals_worst)
x_max_worst_12 = x_vals[np.argmax(I12_vals_worst)]
print(f"Максимальне значення I'_12 для S{worst_sit_12+1}: I'_12({x_max_worst_12},{y_worst_12}) = {I12_max_worst:.6f}")

# Значення з урахуванням факторів ризику у найнесприятливішій ситуації
eta_ns_w12 = R1[0, worst_sit_12]
eta_fm_w12 = R1[1, worst_sit_12]
eta_in_w12 = R1[2, worst_sit_12]

# Шукаємо максимум F_sigma12 по y при x=x_max_worst_12
F12_worst_vals = [F_sigma12(x_max_worst_12, y, eta_ns_w12, eta_fm_w12, eta_in_w12) for y in y_vals]
F12_worst_max = max(F12_worst_vals)
y_F12_worst = y_vals[np.argmax(F12_worst_vals)]
print(f"F_Σ12 з урахуванням ризику (найнесприятливіша S{worst_sit_12+1}): {F12_worst_max:.6f}")

print("\nЙмовірності ситуацій для коаліції 2 (R2):")
P2 = []
for k in range(R2.shape[1]):
    p = R2[0, k] * R2[1, k] * R2[2, k]
    P2.append(p)
    print(f"  P(S{k+1}) = {R2[0,k]} * {R2[1,k]} * {R2[2,k]} = {p:.6f}")

worst_sit_21 = np.argmax(P2)
print(f"\nНайнесприятливіша ситуація для коаліції 2: S{worst_sit_21+1} (x={worst_sit_21})")

# Максимальне значення I'21 для ситуації worst_sit_21 (x = worst_sit_21)
x_worst_21 = worst_sit_21
I21_vals_worst = [I21(x_worst_21, y) for y in y_vals]
I21_max_worst = max(I21_vals_worst)
y_max_worst_21 = y_vals[np.argmax(I21_vals_worst)]
print(f"Максимальне значення I'_21 для S{worst_sit_21+1}: I'_21({x_worst_21},{y_max_worst_21}) = {I21_max_worst:.6f}")

# Значення з урахуванням факторів ризику
eta_ns_w21 = R2[0, worst_sit_21]
eta_fm_w21 = R2[1, worst_sit_21]
eta_in_w21 = R2[2, worst_sit_21]

F21_worst_vals = [F_sigma21(x_worst_21, y, eta_ns_w21, eta_fm_w21, eta_in_w21) for y in y_vals]
F21_worst_max = max(F21_worst_vals)
y_F21_worst = y_vals[np.argmax(F21_worst_vals)]
print(f"F_Σ21 з урахуванням ризику (найнесприятливіша S{worst_sit_21+1}): {F21_worst_max:.6f}")

# АНАЛІЗ РЕЗУЛЬТАТІВ
print("\n" + "=" * 65)
print("АНАЛІЗ РЕЗУЛЬТАТІВ")
print("=" * 65)

print(f"\n1. Гарантований результат (без урахування ризику):")
print(f"   Коаліція 1: I*_12 = {I12_star:.6f}  (точка x={x_star_12}, y={y_star_12})")
print(f"   Коаліція 2: I*_21 = {I21_star:.6f}  (точка x={x_star_21}, y={y_star_21})")

print(f"\n2. Цільові функції з урахуванням факторів ризику (у точці гарантованого результату):")
print(f"   Коаліція 1: F_Σ12 = {F_12_guar:.6f}")
print(f"   Коаліція 2: F_Σ21 = {F_21_guar:.6f}")

change12 = (F_12_guar - I12_star) / I12_star * 100 if I12_star != 0 else 0
change21 = (F_21_guar - I21_star) / I21_star * 100 if I21_star != 0 else 0
print(f"\n   Зміна для коаліції 1: {change12:.1f}%")
print(f"   Зміна для коаліції 2: {change21:.1f}%")

print(f"\n3. Найнесприятливіша ситуація:")
print(f"   Коаліція 1: S{worst_sit_12+1} (y={worst_sit_12})")
print(f"   Коаліція 2: S{worst_sit_21+1} (x={worst_sit_21})")

print(f"\n   Без урахування ризику (найнесприятливіша ситуація):")
print(f"   I'_12 = {I12_max_worst:.6f}")
print(f"   I'_21 = {I21_max_worst:.6f}")

print(f"\n   З урахуванням ризику (найнесприятливіша ситуація):")
print(f"   F_Σ12 = {F12_worst_max:.6f}")
print(f"   F_Σ21 = {F21_worst_max:.6f}")

print("\n" + "=" * 65)
print("Виконання завершено.")
print("=" * 65)
