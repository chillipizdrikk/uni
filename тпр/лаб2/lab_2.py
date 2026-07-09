import numpy as np
import pandas as pd

# ----------------------------
# 1. Межі області та сітка
# ----------------------------
x1_vals = np.round(np.arange(0, 2.01, 0.01), 2)
x2_vals = np.round(np.arange(0, 2.01, 0.01), 2)

X1, X2 = np.meshgrid(x1_vals, x2_vals)

# ----------------------------
# 2. Цільові функції
# ----------------------------
f12 = (2 * X1**2 - 4 * X1 + 18) * (6 * X2**2 - 26 * X2 + 29)
f21 = (-6 * X2**2 + 26) * (-3 * X1**2 + 4 * X1 + 6)

# ----------------------------
# 3. Таблиці значень
# ----------------------------
df_f12 = pd.DataFrame(f12, index=x2_vals, columns=x1_vals)
df_f21 = pd.DataFrame(f21, index=x2_vals, columns=x1_vals)

print("Перші 5 рядків таблиці f12:")
print(df_f12.head())

print("\nПерші 5 рядків таблиці f21:")
print(df_f21.head())

# ----------------------------
# 4. Гарантований результат f12*
# f12* = max_x1 min_x2 f12(x1, x2)
# ----------------------------
min_by_x2_for_f12 = df_f12.min(axis=0)
f12_star = min_by_x2_for_f12.max()

x1_star_candidates = min_by_x2_for_f12[min_by_x2_for_f12 == f12_star].index.tolist()

print("\nГарантований результат для f12:")
print(f"f12* = {f12_star:.2f}")
print("Підходящі значення x1*:", x1_star_candidates)

for x1_star in x1_star_candidates:
    x2_star = df_f12[x1_star].idxmin()
    print(f"Для x1 = {x1_star:.2f} мінімум досягається при x2 = {x2_star:.2f}")

# ----------------------------
# 5. Гарантований результат f21*
# f21* = max_x2 min_x1 f21(x1, x2)
# ----------------------------
min_by_x1_for_f21 = df_f21.min(axis=1)
f21_star = min_by_x1_for_f21.max()

x2_star = min_by_x1_for_f21.idxmax()
x1_star2 = df_f21.loc[x2_star].idxmin()

print("\nГарантований результат для f21:")
print(f"f21* = {f21_star:.2f}")
print(f"Точка: x1 = {x1_star2:.2f}, x2 = {x2_star:.2f}")

# ----------------------------
# 6. Множина Парето
# ----------------------------
pareto_mask = (f12 >= f12_star) & (f21 >= f21_star)

pareto_points = pd.DataFrame({
    "x1": X1[pareto_mask],
    "x2": X2[pareto_mask],
    "f12": f12[pareto_mask],
    "f21": f21[pareto_mask]
})

print("\nКількість точок множини Парето:")
print(len(pareto_points))

print("\nПерші 10 точок множини Парето:")
print(pareto_points.head(10))

# ----------------------------
# 7. Компромісна точка
# Мінімізуємо суму відхилень
# ----------------------------
delta1 = np.abs(f12 - f12_star)
delta2 = np.abs(f21 - f21_star)
delta_sum = delta1 + delta2

delta_sum_masked = np.where(pareto_mask, delta_sum, np.inf)

best_idx = np.unravel_index(np.argmin(delta_sum_masked), delta_sum_masked.shape)

best_x2 = x2_vals[best_idx[0]]
best_x1 = x1_vals[best_idx[1]]
best_f12 = f12[best_idx]
best_f21 = f21[best_idx]
best_delta1 = delta1[best_idx]
best_delta2 = delta2[best_idx]

print("\nКомпромісна точка на сітці:")
print(f"x1 = {best_x1:.2f}, x2 = {best_x2:.2f}")
print(f"f12 = {best_f12:.4f}, f21 = {best_f21:.4f}")
print(f"Δ1 = {best_delta1:.4f}, Δ2 = {best_delta2:.4f}, Δ1+Δ2 = {best_delta1 + best_delta2:.4f}")