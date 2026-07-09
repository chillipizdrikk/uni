import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

# 1.ФУНКЦІЇ НАЛЕЖНОСТІ
def trimf(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Трикутна функція належності (a, b, c)."""
    left  = np.where(b != a, (x - a) / (b - a), 0.0)
    right = np.where(c != b, (c - x) / (c - b), 0.0)
    return np.clip(np.minimum(left, right), 0.0, 1.0)

def trapmf(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray:
    """Трапецієвидна функція належності (a, b, c, d)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        left  = np.where(b != a, (x - a) / (b - a), (x >= a).astype(float))
        right = np.where(d != c, (d - x) / (d - c), (x <= c).astype(float))
    top = np.ones_like(x)
    return np.clip(np.minimum(np.minimum(left, right), top), 0.0, 1.0)

# 2.ТЕРМИ ДЛЯ КОЖНОЇ ЗМІННОЇ

# Всесвіт для кожної змінної
U_X1 = np.linspace(0, 100, 1000)   # Рівень забруднення (%)
U_X2 = np.linspace(0, 10, 1000)    # Тип посуду (умовна шкала)
U_X3 = np.linspace(0, 100, 1000)   # Кількість завантаження (%)
U_Y  = np.linspace(0, 100, 1000)   # Інтенсивність миття (%)

# X1: Рівень забруднення
MF_X1 = {
    "Низький":    trapmf(U_X1,  0,  0, 25, 45),
    "Середній":   trimf (U_X1, 30, 50, 70),
    "Високий":    trapmf(U_X1, 55, 75, 100, 100),
}

# X2: Тип посуду
MF_X2 = {
    "Делікатний": trapmf(U_X2, 0, 0, 2, 4),
    "Звичайний":  trimf (U_X2, 3, 5, 7),
    "Важкий":     trapmf(U_X2, 6, 8, 10, 10),
}

# X3: Кількість завантаження
MF_X3 = {
    "Мала":       trapmf(U_X3,  0,  0, 30, 50),
    "Середня":    trimf (U_X3, 35, 55, 75),
    "Велика":     trapmf(U_X3, 60, 80, 100, 100),
}

# Y: Інтенсивність миття
MF_Y = {
    "Дуже_низька": trapmf(U_Y,  0,  0, 10, 25),
    "Низька":      trimf (U_Y, 15, 28, 42),
    "Середня":     trimf (U_Y, 35, 50, 65),
    "Висока":      trimf (U_Y, 58, 72, 86),
    "Дуже_висока": trapmf(U_Y, 78, 90, 100, 100),
}

# 3.ФАЗИФІКАЦІЯ
def fuzzify(value: float, universe: np.ndarray, mf_dict: dict) -> dict:
    """Повертає ступінь належності значення value до кожного терму."""
    idx = np.argmin(np.abs(universe - value))
    return {term: float(mf[idx]) for term, mf in mf_dict.items()}

# 4.БАЗА ПРАВИЛ

#  Кожне правило: (терм_X1, терм_X2, терм_X3) -> терм_Y
#  Зв'язок антецедентів: мінімум (AND = T-норма min)
RULES = [
    # Низький рівень забруднення
    ("Низький",  "Делікатний", "Мала",     "Дуже_низька"),
    ("Низький",  "Делікатний", "Середня",  "Дуже_низька"),
    ("Низький",  "Делікатний", "Велика",   "Низька"),
    ("Низький",  "Звичайний",  "Мала",     "Дуже_низька"),
    ("Низький",  "Звичайний",  "Середня",  "Низька"),
    ("Низький",  "Звичайний",  "Велика",   "Середня"),
    ("Низький",  "Важкий",     "Мала",     "Низька"),
    ("Низький",  "Важкий",     "Середня",  "Середня"),
    ("Низький",  "Важкий",     "Велика",   "Середня"),

    # Середній рівень забруднення
    ("Середній", "Делікатний", "Мала",     "Низька"),
    ("Середній", "Делікатний", "Середня",  "Середня"),
    ("Середній", "Делікатний", "Велика",   "Середня"),
    ("Середній", "Звичайний",  "Мала",     "Середня"),
    ("Середній", "Звичайний",  "Середня",  "Середня"),
    ("Середній", "Звичайний",  "Велика",   "Висока"),
    ("Середній", "Важкий",     "Мала",     "Середня"),
    ("Середній", "Важкий",     "Середня",  "Висока"),
    ("Середній", "Важкий",     "Велика",   "Висока"),

    # Високий рівень забруднення
    ("Високий",  "Делікатний", "Мала",     "Середня"),
    ("Високий",  "Делікатний", "Середня",  "Висока"),
    ("Високий",  "Делікатний", "Велика",   "Висока"),
    ("Високий",  "Звичайний",  "Мала",     "Висока"),
    ("Високий",  "Звичайний",  "Середня",  "Висока"),
    ("Високий",  "Звичайний",  "Велика",   "Дуже_висока"),
    ("Високий",  "Важкий",     "Мала",     "Висока"),
    ("Високий",  "Важкий",     "Середня",  "Дуже_висока"),
    ("Високий",  "Важкий",     "Велика",   "Дуже_висока"),
]

#  5.  НЕЧІТКЕ ВИВЕДЕННЯ ТА ДЕФАЗИФІКАЦІЯ (Mamdani + Centroid)
def infer(x1: float, x2: float, x3: float, verbose: bool = False) -> float:
    """
    Повертає чітке вихідне значення (інтенсивність миття).
    Метод: Mamdani (min-activation), агрегування max, Centroid.
    """
    fz1 = fuzzify(x1, U_X1, MF_X1)
    fz2 = fuzzify(x2, U_X2, MF_X2)
    fz3 = fuzzify(x3, U_X3, MF_X3)

    if verbose:
        _print_fuzzification(x1, x2, x3, fz1, fz2, fz3)

    # Агрегований вихідний нечіткий набір (max над усіма правилами)
    aggregated = np.zeros_like(U_Y)

    fired_rules = []
    for (t1, t2, t3, ty) in RULES:
        firing = min(fz1[t1], fz2[t2], fz3[t3])   # AND = min
        if firing > 0:
            clipped = np.minimum(MF_Y[ty], firing)  # активація (min/clip)
            aggregated = np.maximum(aggregated, clipped)  # агрегування (max)
            fired_rules.append((t1, t2, t3, ty, firing))

    if verbose:
        _print_rules(fired_rules)

    # Дефазифікація: Centroid (центр мас)
    denominator = np.sum(aggregated)
    if denominator == 0:
        result = 50.0
    else:
        result = float(np.sum(U_Y * aggregated) / denominator)

    return result

def _print_fuzzification(x1, x2, x3, fz1, fz2, fz3):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"  ФАЗИФІКАЦІЯ")
    print(sep)
    print(f"  X1 = {x1:.1f}% (рівень забруднення)")
    for t, v in fz1.items():
        if v > 0:
            print(f"       μ({t}) = {v:.4f}")
    print(f"  X2 = {x2:.1f} (тип посуду)")
    for t, v in fz2.items():
        if v > 0:
            print(f"       μ({t}) = {v:.4f}")
    print(f"  X3 = {x3:.1f}% (кількість завантаження)")
    for t, v in fz3.items():
        if v > 0:
            print(f"       μ({t}) = {v:.4f}")

def _print_rules(fired_rules):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"ПРАВИЛА")
    print(sep)
    for (t1, t2, t3, ty, f) in fired_rules:
        print(f"  ЯКЩО X1={t1:<12} ТА X2={t2:<12} ТА X3={t3:<10}"
              f" ТО Y={ty:<14} (сила = {f:.4f})")

# 6.ТЕСТУВАННЯ – 3 КОМБІНАЦІЇ
TEST_CASES = [
    {"label": "Мінімальне навантаження",
     "x1": 10, "x2": 1, "x3": 15,
     "desc": "Лише кілька склянок, слабке забруднення, делікатний посуд"},

    {"label": "Середнє навантаження",
     "x1": 50, "x2": 5, "x3": 55,
     "desc": "Звичайний посуд, помірне забруднення, половина машини"},

    {"label": "Критичне навантаження",
     "x1": 90, "x2": 9, "x3": 90,
     "desc": "Сильно забруднені каструлі, машина майже повна"},
]

def run_tests():
    results = []
    for tc in TEST_CASES:
        y = infer(tc["x1"], tc["x2"], tc["x3"], verbose=True)
        sep = "─" * 60
        print(f"\n{sep}")
        print(f"СЦЕНАРІЙ: {tc['label']}")
        print(f"{tc['desc']}")
        print(f"Вхід: X1={tc['x1']}%, X2={tc['x2']}, X3={tc['x3']}%")
        print(f"ІНТЕНСИВНІСТЬ МИТТЯ: {y:.2f}%")
        print(sep)
        tc["result"] = y
        results.append(tc)
    return results

# 7.ПОБУДОВА ГРАФІКІВ
COLORS = ["#2196F3", "#4CAF50", "#FF5722", "#9C27B0", "#FF9800"]

def plot_membership_functions(save_path: str = None):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Функції належності нечіткої системи",
                 fontsize=14, fontweight="bold", y=1.01)

    datasets = [
        (axes[0, 0], U_X1, MF_X1, "X₁ - Рівень забруднення (%)", [10, 50, 90]),
        (axes[0, 1], U_X2, MF_X2, "X₂ - Тип посуду (0=делікатний, 10=важкий)", [1, 5, 9]),
        (axes[1, 0], U_X3, MF_X3, "X₃ - Кількість завантаження (%)", [15, 55, 90]),
        (axes[1, 1], U_Y,  MF_Y,  "Y  - Інтенсивність миття (%)",     []),
    ]

    for ax, universe, mf_dict, title, test_vals in datasets:
        for i, (term, mf) in enumerate(mf_dict.items()):
            ax.plot(universe, mf, color=COLORS[i % len(COLORS)],
                    linewidth=2.2, label=term.replace("_", " "))
            ax.fill_between(universe, mf, alpha=0.08, color=COLORS[i % len(COLORS)])

        for xv in test_vals:
            ax.axvline(xv, color="gray", linewidth=1.0, linestyle="--", alpha=0.7)

        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Значення", fontsize=9)
        ax.set_ylabel("Ступінь належності μ", fontsize=9)
        ax.set_ylim(-0.05, 1.1)
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  [збережено] {save_path}")
    plt.show()

def plot_control_surfaces(save_path: str = None):
    """3D-поверхні відгуку для кожної пари входів (X3 фіксований)."""
    fig = plt.figure(figsize=(16, 5))
    fig.suptitle("3D-поверхні відгуку",
                 fontsize=13, fontweight="bold")

    pairs = [
        ("X₁ – Забруднення (%)", "X₂ – Тип посуду", 55, "X₃=55%",
         np.linspace(0, 100, 40), np.linspace(0, 10, 40),
         lambda x1, x2: infer(x1, x2, 55)),
        ("X₁ – Забруднення (%)", "X₃ – Завантаження (%)", 5, "X₂=5",
         np.linspace(0, 100, 40), np.linspace(0, 100, 40),
         lambda x1, x3: infer(x1, 5, x3)),
        ("X₂ – Тип посуду", "X₃ – Завантаження (%)", 50, "X₁=50%",
         np.linspace(0, 10, 40), np.linspace(0, 100, 40),
         lambda x2, x3: infer(50, x2, x3)),
    ]

    for k, (xlabel, ylabel, fixed_val, fixed_label, ua, ub, func) in enumerate(pairs):
        A, B = np.meshgrid(ua, ub)
        Z = np.vectorize(func)(A, B)

        ax = fig.add_subplot(1, 3, k + 1, projection="3d")
        surf = ax.plot_surface(A, B, Z, cmap="viridis", alpha=0.85, linewidth=0)
        ax.set_xlabel(xlabel, fontsize=8, labelpad=6)
        ax.set_ylabel(ylabel, fontsize=8, labelpad=6)
        ax.set_zlabel("Інтенсивність (%)", fontsize=8, labelpad=6)
        ax.set_title(f"Фіксовано {fixed_label}", fontsize=10, fontweight="bold")
        ax.tick_params(labelsize=7)
        fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  [збережено] {save_path}")
    plt.show()

def plot_test_results(results: list, save_path: str = None):
    """Візуалізація результатів тестових сценаріїв."""
    labels  = [r["label"] for r in results]
    outputs = [r["result"] for r in results]
    colors  = ["#2196F3", "#FF9800", "#F44336"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(labels, outputs, color=colors, height=0.45, edgecolor="white")

    for bar, val in zip(bars, outputs):
        ax.text(val + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=11, fontweight="bold")

    ax.set_xlim(0, 110)
    ax.set_xlabel("Інтенсивність миття (%)", fontsize=11)
    ax.set_title("Результати тестових сценаріїв",
                 fontsize=12, fontweight="bold")
    ax.axvline(50, color="gray", linewidth=1.2, linestyle="--", alpha=0.5, label="Середина шкали")
    ax.legend(fontsize=9)
    ax.grid(True, axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Підписи сценаріїв
    for r in results:
        ax.text(1, [l for l in labels].index(r["label"]) - 0.28,
                f"X1={r['x1']}%, X2={r['x2']}, X3={r['x3']}%",
                fontsize=8, color="gray")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  [збережено] {save_path}")
    plt.show()

def plot_aggregation_example(x1=50, x2=5, x3=55, save_path=None):
    """Показує агрегований нечіткий набір для середнього сценарію."""
    fz1 = fuzzify(x1, U_X1, MF_X1)
    fz2 = fuzzify(x2, U_X2, MF_X2)
    fz3 = fuzzify(x3, U_X3, MF_X3)

    aggregated = np.zeros_like(U_Y)
    for (t1, t2, t3, ty) in RULES:
        firing = min(fz1[t1], fz2[t2], fz3[t3])
        if firing > 0:
            clipped = np.minimum(MF_Y[ty], firing)
            aggregated = np.maximum(aggregated, clipped)

    centroid = float(np.sum(U_Y * aggregated) / (np.sum(aggregated) + 1e-9))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.suptitle(f"Фазифікація і агрегування (X1={x1}%, X2={x2}, X3={x3}%)",
                 fontsize=12, fontweight="bold")

    # Ліворуч: вхідні терми зі стрілками активованих
    ax = axes[0]
    ax.set_title("Вхідні змінні з позначенням чітких значень", fontsize=10)
    offsets = [0, 1.3, 2.6]
    var_labels = [f"X1={x1}% Забруднення", f"X2={x2} Тип посуду", f"X3={x3}% Завантаження"]
    universes  = [U_X1/100, U_X2/10, U_X3/100]
    mf_sets    = [MF_X1,    MF_X2,    MF_X3]
    vals       = [x1/100,   x2/10,    x3/100]

    for i, (uni, mfs, val, lbl) in enumerate(zip(universes, mf_sets, vals, var_labels)):
        off = offsets[i]
        for j, (term, mf) in enumerate(mfs.items()):
            ax.plot(uni + off, mf * 0.9 + 0.05, color=COLORS[j], linewidth=1.8)
        ax.axvline(val + off, color="red", linewidth=1.5, linestyle="--")
        ax.text(off + 0.5, 1.05, lbl, ha="center", fontsize=7.5, fontweight="bold")

    ax.set_xlim(-0.05, 3.65)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_ylabel("μ", fontsize=10)
    ax.grid(False)

    # Праворуч: агрегований вихід + centroid
    ax2 = axes[1]
    for i, (term, mf) in enumerate(MF_Y.items()):
        ax2.plot(U_Y, mf, "--", color=COLORS[i], alpha=0.4, linewidth=1.2,
                 label=term.replace("_", " "))
    ax2.fill_between(U_Y, aggregated, alpha=0.5, color="#2196F3", label="Агрегований набір")
    ax2.axvline(centroid, color="red", linewidth=2.0, linestyle="-",
                label=f"Centroid = {centroid:.1f}%")
    ax2.set_title("Агрегований вихідний набір та дефазифікація", fontsize=10)
    ax2.set_xlabel("Інтенсивність миття (%)", fontsize=9)
    ax2.set_ylabel("μ", fontsize=10)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.grid(True, alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  [збережено] {save_path}")
    plt.show()

# 8.ГОЛОВНА ФУНКЦІЯ
def main():
    print("\n" + "═" * 60)
    print("НЕЧІТКЕ КЕРУВАННЯ ПОСУДОМИЙНОЮ МАШИНОЮ")
    print("Лабораторна робота №3")
    print("═" * 60)
    print("\n  Вхідні змінні:")
    print("X1 - Рівень забруднення посуду  [0-100 %]")
    print("X2 - Тип посуду                 [0=делікатний … 10=важкий]")
    print("X3 - Кількість завантаження      [0-100 %]")
    print("\n  Вихідна змінна:")
    print("Y  - Інтенсивність миття         [0-100 %]")
    print("\nМетод: Mamdani (min-AND), агрегування MAX, Centroid-дефазифікація")
    print(f"\nКількість правил у базі знань: {len(RULES)}")

    # Тести
    results = run_tests()

    # Графіки
    out_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_dir = out_dir + os.sep

    print("\n" + "─" * 60)
    print("  Побудова графіків...")
    plot_membership_functions(save_path=out_dir + "mf_plots.png")
    plot_aggregation_example(x1=50, x2=5, x3=55,
                             save_path=out_dir + "aggregation.png")
    plot_test_results(results, save_path=out_dir + "test_results.png")
    plot_control_surfaces(save_path=out_dir + "control_surfaces.png")

    print("\n" + "═" * 60)
    print("  ПІДСУМОК ТЕСТУВАННЯ")
    print("═" * 60)
    print(f"  {'Сценарій':<28} {'Вхід X1':>8} {'Вхід X2':>8} {'Вхід X3':>8}  {'Вихід Y':>10}")
    print("  " + "─" * 62)
    for r in results:
        print(f"  {r['label']:<28} {r['x1']:>6}%  {r['x2']:>7}  {r['x3']:>6}%   {r['result']:>8.2f}%")
    print("═" * 60 + "\n")

if __name__ == "__main__":
    main()