import numpy as np
import math

#Матриця переходів P(Y|X)
matrix_transitions = np.array([[0.52, 0.48],
                               [0.47, 0.53]])

#Середня тривалість кожного символу на виході джерела(тау)
avg_duration = 10**(-3)

#Список p(x1) від 0 до 1 з кроком 0.1
p_x1_val1 = np.linspace(0, 1, num=11)
result = []

#Пропускна здатність для кожного значення p(x1)
for p_x1 in p_x1_val1:
    p_x2 = 1 - p_x1
    p_y1 = p_x1 * matrix_transitions[0][0] + p_x2 * matrix_transitions[1][0]
    p_y2 = p_x1 * matrix_transitions[0][1] + p_x2 * matrix_transitions[1][1]
    #H(Y|x1) та H(Y|x2)
    entropy_Y_x1 = - (matrix_transitions[0][0] * math.log2(matrix_transitions[0][0]) +
                            matrix_transitions[0][1] * math.log2(matrix_transitions[0][1]))
    entropy_Y_x2 = - (matrix_transitions[1][0] * math.log2(matrix_transitions[1][0]) +
                            matrix_transitions[1][1] * math.log2(matrix_transitions[1][1]))
    #H(Y|X)
    entropy_Y_X = p_x1 * entropy_Y_x1 + p_x2 * entropy_Y_x2
    #H(Y)
    entropy_Y = - (p_y1 * math.log2(p_y1) + p_y2 * math.log2(p_y2))
    #Пропускна здатність каналу
    capacity = (entropy_Y - entropy_Y_X) / avg_duration
    result.append((p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity))

#Максимальна пропускна здатність 
max_capacity = max(result, key=lambda x: x[5])

print("Таблиця пропускної здатності каналу від 0 до 1:")
print("p(x1)\tp(y1)\tp(y2)\tH(Y)\tH(Y|X)\tПропускна здатність(біт/с)")
for p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity in result:
    print("{:.1f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity))

#Результати для максимальної пропускної здатності
print("\nМаксимальна пропускна здатність(перша частина):")
print("p(x1)\tp(y1)\tp(y2)\tH(Y)\tH(Y|X)\tПропускна здатність(біт/с)")
print("{:.1f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(*max_capacity))

#Друга частина
low_bound = max(0, max_capacity[0] - 0.1)
upp_bound = min(1, max_capacity[0] + 0.1)
step = 0.01

#Список p(x1) від max до 1 з кроком 0.01
p_x1_val2 = np.arange(low_bound + step, upp_bound + step, step)
result1 = []

#Пропускна здатність для кожного значення p(x1) 
for p_x1 in p_x1_val2:
    p_x2 = 1 - p_x1
    p_y1 = p_x1 * matrix_transitions[0][0] + p_x2 * matrix_transitions[1][0]
    p_y2 = p_x1 * matrix_transitions[0][1] + p_x2 * matrix_transitions[1][1]
    #H(Y|x1) та H(Y|x2)
    entropy_Y_x1 = - (matrix_transitions[0][0] * math.log2(matrix_transitions[0][0]) +
                            matrix_transitions[0][1] * math.log2(matrix_transitions[0][1]))
    entropy_Y_x2 = - (matrix_transitions[1][0] * math.log2(matrix_transitions[1][0]) +
                            matrix_transitions[1][1] * math.log2(matrix_transitions[1][1]))
    #H(Y|X)
    entropy_Y_X = p_x1 * entropy_Y_x1 + p_x2 * entropy_Y_x2
    #H(Y)
    entropy_Y = - (p_y1 * math.log2(p_y1) + p_y2 * math.log2(p_y2))
    #Пропускна здатність каналу
    capacity = (entropy_Y - entropy_Y_X) / avg_duration
    result1.append((p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity))

#Максимальна пропускна здатність
max_capacity2 = max(result1, key=lambda x: x[5])
print("\nТаблиця пропускної здатності каналу:")
print("p(x1)\tp(y1)\tp(y2)\tH(Y)\tH(Y|X)\tПропускна здатність (біт/с)")
for p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity in result1:
    print("{:.2f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(p_x1, p_y1, p_y2, entropy_Y, entropy_Y_X, capacity))

#Результати для максимальної пропускної здатності
print("\nМаксимальна пропускна здатність:")
print("p(x1)\tp(y1)\tp(y2)\tH(Y)\tH(Y|X)\tПропускна здатність (біт/с)")
print("{:.3f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(*max_capacity2))