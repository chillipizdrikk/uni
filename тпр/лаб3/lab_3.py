import itertools
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Chebyshev, Polynomial


# ==========================================================
# Лабораторна робота №3
# Відновлення цільових функцій в адитивному вигляді
# Варіант 4:
#   b_iq0 = нормовані значення Y_i[q]
#   метод розв'язання несумісної системи рівнянь — статистичний градієнт
# ==========================================================


OUTPUT_DIR = Path("results_variant4")
OUTPUT_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------------
# 1. Дискретна вибірка №4 (з рисунків завдання)
# ----------------------------------------------------------
# Стовпці:
# X11, X12, X21, X22, X31, X32, X33
DATA = np.array([
    [0.0, 1.0, 0.0, 1.0, 0.0, 0.5, 2.18],
    [0.1, 0.9, 0.19, 0.91, 0.18, 0.6, 2.22],
    [0.2, 0.8, 0.29, 0.81, 0.28, 0.7, 2.23],
    [0.3, 0.7, 0.39, 0.71, 0.38, 0.8, 2.24],
    [0.4, 0.6, 0.49, 0.61, 0.48, 0.9, 2.28],
    [0.5, 0.5, 0.59, 0.51, 0.58, 1.0, 2.32],
    [0.6, 0.4, 0.69, 0.41, 0.68, 0.4, 2.17],
    [0.7, 0.3, 0.79, 0.31, 0.78, 0.3, 2.19],
    [0.8, 0.2, 0.89, 0.21, 0.88, 0.2, 2.21],
    [0.9, 0.1, 0.99, 0.11, 0.98, 0.1, 2.25],
    [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 2.19],
    [2.0, 1.5, 1.8, 1.1, 2.0, 1.2, 6.47],
    [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 5.52],
    [0.8, 0.1, 0.7, 0.6, 0.5, 0.6, 1.95],
    [0.7, 0.2, 0.6, 0.7, 0.4, 0.7, 1.98],
    [0.6, 0.3, 0.5, 0.8, 0.3, 0.8, 2.01],
    [0.5, 0.4, 0.4, 0.9, 0.2, 0.9, 2.07],
    [0.4, 0.5, 0.3, 1.0, 0.1, 1.0, 2.13],
    [0.3, 0.6, 0.2, 1.8, 0.0, 1.1, 2.71],
    [0.2, 0.7, 0.1, 0.0, 1.1, 1.2, 2.80],
    [0.1, 0.8, 0.0, 0.1, 0.3, 0.5, 1.89],
    [0.0, 0.9, 1.1, 0.2, 0.4, 0.4, 2.20],
    [0.9, 1.0, 1.5, 0.3, 0.5, 0.3, 2.79],
    [1.8, 1.1, 1.9, 0.4, 0.6, 0.2, 3.39],
    [0.1, 1.2, 1.9, 1.3, 0.7, 0.1, 3.26],
    [0.0, 1.3, 0.2, 0.5, 0.8, 0.0, 2.67],
    [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 2.01],
    [0.6, 0.5, 0.4, 0.3, 0.4, 0.4, 1.96],
    [0.5, 0.4, 0.3, 0.2, 0.5, 0.6, 1.92],
    [0.4, 0.3, 0.2, 0.1, 0.6, 0.8, 1.90],
    [0.3, 0.2, 0.1, 0.0, 0.7, 1.0, 1.89],
    [0.2, 0.1, 0.0, 1.5, 0.8, 1.2, 2.50],
    [0.1, 0.0, 0.4, 1.3, 0.9, 1.4, 2.48],
    [0.0, 0.3, 1.3, 1.1, 1.0, 1.6, 2.94],
    [0.5, 0.4, 0.5, 0.9, 1.1, 1.8, 3.16],
    [0.4, 0.5, 0.4, 0.7, 1.2, 2.0, 3.30],
    [0.3, 0.6, 0.3, 0.5, 1.3, 0.8, 3.04],
    [0.2, 0.7, 0.25, 0.3, 1.4, 0.3, 3.04],
    [0.1, 0.8, 0.14, 0.1, 1.5, 0.4, 3.23],
    [0.0, 0.9, 0.03, 0.0, 1.6, 0.1, 3.33],
], dtype=float)

FEATURE_NAMES = ["X11", "X12", "X21", "X22", "X31", "X32", "X33"]
BLOCKS = [[0, 1], [2, 3], [4, 5, 6]]
BLOCK_NAMES = ["X1", "X2", "X3"]


# ----------------------------------------------------------
# 2. Допоміжні функції
# ----------------------------------------------------------
def minmax_to_unit(x: np.ndarray):
    x_min = x.min(axis=0)
    x_max = x.max(axis=0)
    denom = np.where(np.abs(x_max - x_min) < 1e-12, 1.0, x_max - x_min)
    x_unit = (x - x_min) / denom
    return x_unit, x_min, x_max


def unit_to_cheb_domain(x_unit: np.ndarray):
    return 2.0 * x_unit - 1.0


def cheb_values(x: np.ndarray, degree: int) -> np.ndarray:
    """Повертає матрицю [T0(x), T1(x), ..., T_degree(x)] для вектора x."""
    t = np.zeros((x.shape[0], degree + 1), dtype=float)
    t[:, 0] = 1.0
    if degree >= 1:
        t[:, 1] = x
    for p in range(2, degree + 1):
        t[:, p] = 2.0 * x * t[:, p - 1] - t[:, p - 2]
    return t


def restore_from_unit(y_unit: np.ndarray, y_min: np.ndarray, y_max: np.ndarray) -> np.ndarray:
    return y_min + y_unit * (y_max - y_min)


def max_abs_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.max(np.abs(y_true - y_pred)))


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean((y_true - y_pred) ** 2))


def poly_to_string(coeffs: np.ndarray, var: str = "x", digits: int = 6) -> str:
    parts = []
    for power, coef in enumerate(coeffs):
        if abs(coef) < 1e-12:
            continue
        c = f"{coef:.{digits}f}"
        if power == 0:
            parts.append(c)
        elif power == 1:
            parts.append(f"{c}*{var}")
        else:
            parts.append(f"{c}*{var}^{power}")
    if not parts:
        return "0"
    expr = " + ".join(parts)
    expr = expr.replace("+ -", "- ")
    return expr


# ----------------------------------------------------------
# 3. Формування цільових функцій Y1..Y4
# ----------------------------------------------------------
# У цій лабораторній за умовою потрібно самостійно сформувати цільові функції.
# Щоб модель точно відповідала адитивній структурі, цілі задаємо через
# поліноми Чебишева для окремих координат.

def build_target_functions(x_cheb: np.ndarray):
    coeff_specs = [
        {
            "c": [0.80, 0.70, 1.00],
            "alpha": [[1.00, 0.90], [1.10, 0.95], [1.00, 0.85, 1.20]],
            "lambda": {
                0: [0.12, 0.18, -0.05],
                1: [0.10, -0.08, 0.03],
                2: [0.08, 0.14, 0.02],
                3: [0.06, -0.05, 0.04],
                4: [0.05, 0.12, -0.02],
                5: [0.07, -0.06, 0.05],
                6: [0.09, 0.04, 0.03],
            },
        },
        {
            "c": [0.90, 0.75, 0.95],
            "alpha": [[1.00, 1.10], [0.90, 1.00], [1.05, 0.95, 1.10]],
            "lambda": {
                0: [0.08, -0.12, 0.07],
                1: [0.11, 0.09, -0.04],
                2: [0.07, 0.15, 0.02],
                3: [0.09, -0.07, 0.05],
                4: [0.10, 0.06, 0.03],
                5: [0.06, 0.11, -0.02],
                6: [0.04, -0.08, 0.04],
            },
        },
        {
            "c": [1.00, 0.80, 0.90],
            "alpha": [[1.05, 0.95], [1.00, 0.90], [0.90, 1.10, 1.00]],
            "lambda": {
                0: [0.05, 0.16, 0.02],
                1: [0.07, -0.10, 0.05],
                2: [0.12, 0.08, -0.03],
                3: [0.10, 0.04, 0.02],
                4: [0.06, -0.09, 0.04],
                5: [0.09, 0.07, 0.03],
                6: [0.08, 0.05, -0.01],
            },
        },
        {
            "c": [0.85, 0.90, 1.05],
            "alpha": [[0.95, 1.00], [1.10, 1.00], [1.00, 0.90, 1.15]],
            "lambda": {
                0: [0.09, -0.11, 0.04],
                1: [0.06, 0.13, -0.02],
                2: [0.05, 0.10, 0.05],
                3: [0.11, -0.06, 0.03],
                4: [0.07, 0.08, -0.01],
                5: [0.08, -0.04, 0.04],
                6: [0.10, 0.09, 0.02],
            },
        },
    ]

    y = np.zeros((x_cheb.shape[0], 4), dtype=float)
    for i, spec in enumerate(coeff_specs):
        for s, cols in enumerate(BLOCKS):
            phi_is = np.zeros(x_cheb.shape[0], dtype=float)
            for jj, col in enumerate(cols):
                degree = len(spec["lambda"][col]) - 1
                t = cheb_values(x_cheb[:, col], degree)
                psi = t @ np.array(spec["lambda"][col], dtype=float)
                phi_is += spec["alpha"][s][jj] * psi
            y[:, i] += spec["c"][s] * phi_is
    return y, coeff_specs


# ----------------------------------------------------------
# 4. Модель адитивного відновлення
# ----------------------------------------------------------
# Відновлюємо
#   ψ_i,s,j(x_sj) = Σ λ_i,s,j,p * T_p(x_sj)
#   Φ_i,s(X_s)    = Σ α_i,s,j * ψ_i,s,j(x_sj)
#   Φ_i(X1,X2,X3) = Σ c_i,s * Φ_i,s(X_s)
# Розв'язання — методом статистичного градієнта (SGD).

def init_params(output_dim: int, degrees: tuple[int, int, int], rng: np.random.Generator):
    params = []
    for _ in range(output_dim):
        p = {
            "c": rng.normal(0.5, 0.05, size=3),
            "alpha": {},
            "lambda": {},
        }
        for s, cols in enumerate(BLOCKS):
            p["alpha"][s] = rng.normal(1.0, 0.05, size=len(cols))
            for col in cols:
                vec = rng.normal(0.0, 0.1, size=degrees[s] + 1)
                vec[0] = 0.1
                p["lambda"][col] = vec
        params.append(p)
    return params


def precompute_cheb(x_cheb: np.ndarray, degrees: tuple[int, int, int]):
    t_cache = {}
    max_deg = max(degrees)
    for col in range(x_cheb.shape[1]):
        t_cache[col] = cheb_values(x_cheb[:, col], max_deg)
    return t_cache


def predict_one_output(x_cheb: np.ndarray, params_one: dict, degrees: tuple[int, int, int], t_cache: dict):
    n = x_cheb.shape[0]
    y_hat = np.zeros(n, dtype=float)
    phi_blocks = []
    psi_all = {}

    for s, cols in enumerate(BLOCKS):
        phi_s = np.zeros(n, dtype=float)
        for jj, col in enumerate(cols):
            psi = t_cache[col][:, : degrees[s] + 1] @ params_one["lambda"][col]
            psi_all[(s, jj)] = psi
            phi_s += params_one["alpha"][s][jj] * psi
        phi_blocks.append(phi_s)
        y_hat += params_one["c"][s] * phi_s

    return y_hat, phi_blocks, psi_all


def predict_all(x_cheb: np.ndarray, params: list[dict], degrees: tuple[int, int, int], t_cache: dict):
    pred = np.zeros((x_cheb.shape[0], len(params)), dtype=float)
    for i, p in enumerate(params):
        pred[:, i], _, _ = predict_one_output(x_cheb, p, degrees, t_cache)
    return pred


def fit_statistical_gradient(
    x_cheb: np.ndarray,
    y_unit: np.ndarray,
    degrees: tuple[int, int, int],
    epochs: int = 20000,
    lr: float = 0.03,
    seed: int = 42,
):
    rng = np.random.default_rng(seed)
    n, m = y_unit.shape
    params = init_params(m, degrees, rng)
    t_cache = precompute_cheb(x_cheb, degrees)
    current_lr = lr

    for epoch in range(epochs):
        q = epoch % n
        for i in range(m):
            p = params[i]
            phi_s = np.zeros(3, dtype=float)
            psi_sample = {}

            for s, cols in enumerate(BLOCKS):
                for jj, col in enumerate(cols):
                    tt = t_cache[col][q, : degrees[s] + 1]
                    psi_val = float(tt @ p["lambda"][col])
                    psi_sample[(s, jj)] = psi_val
                    phi_s[s] += p["alpha"][s][jj] * psi_val

            y_hat = float(p["c"] @ phi_s)
            err = y_hat - y_unit[q, i]
            c_old = p["c"].copy()

            # Оновлення коефіцієнтів c
            p["c"] -= current_lr * err * phi_s

            # Оновлення alpha та lambda
            for s, cols in enumerate(BLOCKS):
                for jj, col in enumerate(cols):
                    p["alpha"][s][jj] -= current_lr * err * c_old[s] * psi_sample[(s, jj)]
                    tt = t_cache[col][q, : degrees[s] + 1]
                    p["lambda"][col] -= current_lr * err * c_old[s] * p["alpha"][s][jj] * tt

        if (epoch + 1) % 5000 == 0:
            current_lr *= 0.6

    return params, t_cache


# ----------------------------------------------------------
# 5. Пошук степенів поліномів p1, p2, p3
# ----------------------------------------------------------
def search_best_degrees(x_cheb: np.ndarray, y_unit: np.ndarray, degree_values=(1, 2, 3, 4)):
    best = None
    table = []
    for degrees in itertools.product(degree_values, repeat=3):
        params, cache = fit_statistical_gradient(
            x_cheb,
            y_unit,
            degrees=degrees,
            epochs=12000,
            lr=0.025,
            seed=123,
        )
        pred = predict_all(x_cheb, params, degrees, cache)
        delta = max_abs_error(y_unit, pred)
        err_mse = mse(y_unit, pred)
        table.append((degrees, delta, err_mse))
        if best is None or delta < best[1]:
            best = (degrees, delta, err_mse, params, cache)
    return best, table


# ----------------------------------------------------------
# 6. Формування текстових представлень функцій
# ----------------------------------------------------------
def cheb_formula(coeffs: np.ndarray, var_name: str) -> str:
    terms = []
    for p, coef in enumerate(coeffs):
        if abs(coef) < 1e-12:
            continue
        if p == 0:
            terms.append(f"{coef:.6f}")
        else:
            terms.append(f"{coef:.6f}*T{p}({var_name})")
    if not terms:
        return "0"
    return " + ".join(terms).replace("+ -", "- ")


def standard_polynomial_from_cheb(coeffs: np.ndarray) -> np.ndarray:
    cheb = Chebyshev(coeffs)
    poly = cheb.convert(kind=Polynomial)
    return np.array(poly.coef, dtype=float)


def write_report(
    x_unit: np.ndarray,
    x_cheb: np.ndarray,
    y_true: np.ndarray,
    y_unit: np.ndarray,
    y_pred_unit: np.ndarray,
    y_pred: np.ndarray,
    target_specs: list[dict],
    best_degrees: tuple[int, int, int],
    params: list[dict],
    degree_table: list[tuple],
):
    lines = []
    lines.append("ЛАБОРАТОРНА РОБОТА №3")
    lines.append("Відновлення цільових функцій в адитивному вигляді")
    lines.append("Варіант 4")
    lines.append("")
    lines.append("1. Початкові умови")
    lines.append("- Вибірка: №4")
    lines.append("- Вибір b_iq0: нормовані значення Y_i[q]")
    lines.append("- Метод розв'язання несумісних систем: метод статистичного градієнта")
    lines.append("")
    lines.append("2. Розмірності")
    lines.append("- n1 = 2, n2 = 2, n3 = 3")
    lines.append("- m = 4")
    lines.append(f"- q0 = 40")
    lines.append("")
    lines.append("3. Обрані степені поліномів Чебишева")
    lines.append(f"- p1 = {best_degrees[0]}, p2 = {best_degrees[1]}, p3 = {best_degrees[2]}")
    lines.append("")
    lines.append("4. Сформовані цільові функції")
    for i, spec in enumerate(target_specs, start=1):
        lines.append(f"Y{i}(X1, X2, X3) = Σ c_{i}s * Φ_{i}s(Xs)")
        lines.append(f"  c_{i} = {np.array(spec['c'])}")
        for s, cols in enumerate(BLOCKS):
            lines.append(f"  Φ_{i}{s+1}(X{s+1}) = Σ α_{i},{s+1},j * ψ_{i},{s+1},j(x)")
            lines.append(f"    alpha = {np.array(spec['alpha'][s])}")
            for col in cols:
                lines.append(
                    f"    ψ(Y{i},{FEATURE_NAMES[col]}) = {cheb_formula(np.array(spec['lambda'][col]), FEATURE_NAMES[col])}"
                )
        lines.append("")

    lines.append("5. Таблиця пошуку степенів")
    for degrees, delta, err_mse in degree_table:
        lines.append(f"degrees={degrees}, delta={delta:.8f}, mse={err_mse:.10f}")
    lines.append("")

    lines.append("6. Отримані коефіцієнти λ, α, c")
    for i, p in enumerate(params, start=1):
        lines.append(f"--- Для Y{i} ---")
        lines.append(f"c_{i} = {p['c']}")
        for s, cols in enumerate(BLOCKS):
            lines.append(f"alpha_{i},{s+1} = {p['alpha'][s]}")
            for col in cols:
                coeffs = p['lambda'][col]
                lines.append(f"lambda(Y{i}, {FEATURE_NAMES[col]}) = {coeffs}")
        lines.append("")

    lines.append("7. Вид отриманих функцій")
    for i, p in enumerate(params, start=1):
        lines.append(f"=== Y{i} ===")
        for s, cols in enumerate(BLOCKS):
            lines.append(f"Φ_{i}{s+1}(X{s+1}):")
            for jj, col in enumerate(cols, start=1):
                coeffs = p['lambda'][col]
                lines.append(f"  ψ_{i},{s+1},{jj}({FEATURE_NAMES[col]}) = {cheb_formula(coeffs, FEATURE_NAMES[col])}")
                poly_coeffs = standard_polynomial_from_cheb(coeffs)
                lines.append(f"    Звичайний багаточлен у нормованій змінній: {poly_to_string(poly_coeffs, FEATURE_NAMES[col] + '_n')}")
        lines.append("")

    lines.append("8. Похибки відновлення")
    for i in range(y_true.shape[1]):
        delta_i = max_abs_error(y_unit[:, i], y_pred_unit[:, i])
        mse_i = mse(y_unit[:, i], y_pred_unit[:, i])
        lines.append(f"Y{i+1}: max|e| = {delta_i:.8f}, mse = {mse_i:.10f}")
    lines.append(f"Загальна максимальна похибка: {max_abs_error(y_unit, y_pred_unit):.8f}")
    lines.append(f"Загальна MSE: {mse(y_unit, y_pred_unit):.10f}")
    lines.append("")

    lines.append("9. Додатковий варіант дискретної вибірки")
    lines.append("Для другого варіанта вибірки можна згенерувати модифіковані дані:")
    lines.append("X_new = X + 0.03*sin(номер_рядка), після чого повторити всі обчислення.")
    lines.append("")

    lines.append("10. Короткий висновок")
    lines.append(
        "За вибіркою №4 побудовано адитивні наближувальні функції на основі поліномів Чебишева. "
        "Параметри λ, α, c знайдено методом статистичного градієнта. "
        "Побудовано графіки вихідних та відновлених функцій і обчислено похибки відновлення."
    )

    (OUTPUT_DIR / "report_variant4.txt").write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------
# 7. Графіки
# ----------------------------------------------------------
def save_plots(y_true_unit: np.ndarray, y_pred_unit: np.ndarray):
    q = np.arange(1, y_true_unit.shape[0] + 1)
    for i in range(y_true_unit.shape[1]):
        plt.figure(figsize=(10, 5))
        plt.plot(q, y_true_unit[:, i], label="Значення вибірки")
        plt.plot(q, y_pred_unit[:, i], label="Апроксимовані значення")
        plt.xlabel("Номер спостереження q")
        plt.ylabel(f"Y{i+1} (нормоване)")
        plt.title(f"Y{i+1}: вихідна та відновлена функції")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"Y{i+1}_plot.png", dpi=160)
        plt.close()


# ----------------------------------------------------------
# 8. Основний сценарій
# ----------------------------------------------------------
def main():
    # Нормування X
    x_unit, x_min, x_max = minmax_to_unit(DATA)
    x_cheb = unit_to_cheb_domain(x_unit)

    # Формування цільових функцій Y
    y_true, target_specs = build_target_functions(x_cheb)
    y_unit, y_min, y_max = minmax_to_unit(y_true)

    # b_iq0 = нормовані значення Y_i[q]
    b = y_unit.copy()

    # Пошук степенів p1, p2, p3
    best, degree_table = search_best_degrees(x_cheb, b, degree_values=(1, 2, 3))
    best_degrees, best_delta, best_mse, best_params, best_cache = best

    # Фінальне відновлення з найкращими степенями
    y_pred_unit = predict_all(x_cheb, best_params, best_degrees, best_cache)
    y_pred = restore_from_unit(y_pred_unit, y_min, y_max)

    # Виведення у консоль
    print("Найкращі степені поліномів:", best_degrees)
    print("Максимальна похибка delta:", best_delta)
    print("MSE:", best_mse)
    print()

    for i, p in enumerate(best_params, start=1):
        print(f"===== Y{i} =====")
        print("c =", p["c"])
        for s in range(3):
            print(f"alpha[{s+1}] =", p["alpha"][s])
        for col in range(DATA.shape[1]):
            print(f"lambda[{FEATURE_NAMES[col]}] =", p["lambda"][col])
        print()

    # Збереження результатів
    save_plots(y_unit, y_pred_unit)
    write_report(
        x_unit=x_unit,
        x_cheb=x_cheb,
        y_true=y_true,
        y_unit=y_unit,
        y_pred_unit=y_pred_unit,
        y_pred=y_pred,
        target_specs=target_specs,
        best_degrees=best_degrees,
        params=best_params,
        degree_table=degree_table,
    )

    # Збереження вихідних і відновлених значень в таблицю
    table = np.hstack([y_true, y_pred])
    header = "Y1_true Y2_true Y3_true Y4_true Y1_pred Y2_pred Y3_pred Y4_pred"
    np.savetxt(OUTPUT_DIR / "predictions.txt", table, header=header, fmt="%.10f")

    # Додатковий приклад альтернативної вибірки
    q = np.arange(1, DATA.shape[0] + 1)
    alt = DATA + 0.03 * np.sin(q[:, None])
    np.savetxt(OUTPUT_DIR / "alternative_sample.txt", alt, fmt="%.10f")

    print(f"\nУсі результати збережено в папку: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
