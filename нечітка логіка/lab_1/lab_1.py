import numpy as np
import matplotlib.pyplot as plt

X = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)

muA = np.array([0.0, 0.3, 0.6, 1.0, 1.0, 0.6, 0.3, 0.0], dtype=float)
muB = np.array([1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0, 0.0], dtype=float)


def complement(mu):
    return 1.0 - mu

def zadeh_union(mu1, mu2):
    return np.maximum(mu1, mu2)

def zadeh_intersection(mu1, mu2):
    return np.minimum(mu1, mu2)

def algebraic_intersection(mu1, mu2):
    return mu1 * mu2

def algebraic_union(mu1, mu2):
    return mu1 + mu2 - mu1 * mu2

def difference(muA, muB):
    # A \ B = A ∩ (not B) за Заде: min(muA, 1-muB)
    return np.minimum(muA, 1.0 - muB)

def symmetric_difference(muA, muB):
    # (A\B) ∪ (B\A) за Заде: max(...)
    return np.maximum(difference(muA, muB), difference(muB, muA))

def concentration(mu):
    return mu ** 2

def dilation(mu):
    return np.sqrt(mu)

def bounded_intersection(mu1, mu2):
    # max(mu1 + mu2 - 1, 0)
    return np.maximum(mu1 + mu2 - 1.0, 0.0)

def bounded_union(mu1, mu2):
    # min(mu1 + mu2, 1)
    return np.minimum(mu1 + mu2, 1.0)

def support(X, mu):
    return X[mu > 0]

def core(X, mu, eps=1e-12):
    return X[np.abs(mu - 1.0) <= eps]

def height(mu):
    return float(np.max(mu))

def alpha_cut(X, mu, alpha):
    return X[mu >= alpha]

def print_set(name, arr):
    if arr.size == 0:
        print(f"{name} = ∅")
    else:
        nice = [int(v) if abs(v - int(v)) < 1e-12 else float(v) for v in arr]
        print(f"{name} = {nice}")

def print_table(rows, headers):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))
    fmt = " | ".join("{:<" + str(w) + "}" for w in widths)
    sep = "-+-".join("-" * w for w in widths)
    print(fmt.format(*headers))
    print(sep)
    for r in rows:
        print(fmt.format(*r))

# ----------------------------
# Основні множини/операції
muA_bar = complement(muA)
muB_bar = complement(muB)

mu_union = zadeh_union(muA, muB)
mu_inter = zadeh_intersection(muA, muB)

mu_alg_inter = algebraic_intersection(muA, muB)
mu_alg_union = algebraic_union(muA, muB)

mu_A_diff_B = difference(muA, muB)
mu_B_diff_A = difference(muB, muA)
mu_sym_diff = symmetric_difference(muA, muB)

mu_conA = concentration(muA)
mu_dilA = dilation(muA)

mu_bounded_inter = bounded_intersection(muA, muB)
mu_bounded_union = bounded_union(muA, muB)

# ----------------------------
# Характеристики A та B
print("=== Характеристики A ===")
print_set("supp(A)", support(X, muA))
print_set("core(A)", core(X, muA))
print("height(A) =", height(muA))

print("\n=== Характеристики B ===")
print_set("supp(B)", support(X, muB))
print_set("core(B)", core(X, muB))
print("height(B) =", height(muB))

# alpha-рівень 
while True:
    try:
        alpha = float(input("\nВведіть alpha (0..1), наприклад 0.5: ").strip().replace(",", "."))
        if 0.0 <= alpha <= 1.0:
            break
        print("alpha має бути в межах [0, 1].")
    except ValueError:
        print("Введіть число, наприклад 0.5")

print_set(f"A_alpha (alpha={alpha})", alpha_cut(X, muA, alpha))
print_set(f"B_alpha (alpha={alpha})", alpha_cut(X, muB, alpha))

rows = []
for i, x in enumerate(X):
    rows.append([
        str(int(x)),
        f"{muA[i]:.2f}",
        f"{muB[i]:.2f}",
        f"{muA_bar[i]:.2f}",
        f"{muB_bar[i]:.2f}",
        f"{mu_union[i]:.2f}",
        f"{mu_inter[i]:.2f}",
        f"{mu_alg_inter[i]:.2f}",
        f"{mu_alg_union[i]:.2f}",
        f"{mu_A_diff_B[i]:.2f}",
        f"{mu_sym_diff[i]:.2f}",
        f"{mu_conA[i]:.2f}",
        f"{mu_dilA[i]:.3f}",
        f"{mu_bounded_inter[i]:.2f}",
        f"{mu_bounded_union[i]:.2f}",
    ])

headers = [
    "x", "muA", "muB", "muA_bar", "muB_bar",
    "A∪B", "A∩B", "alg∩", "alg∪", "A\\B",
    "AΔB", "CON(A)", "DIL(A)", "bnd∩", "bnd∪"
]

print("\n=== Таблиця значень ===")
print_table(rows, headers)

# Для апроксимації беремо кусково-лінійну
x_dense = np.linspace(X.min(), X.max(), 400)
muA_lin = np.interp(x_dense, X, muA)
muB_lin = np.interp(x_dense, X, muB)

plt.figure()
plt.title("Нечіткі множини A та B (дискретно + апроксимація)")
plt.plot(x_dense, muA_lin, label="A (апрокс. лінійна)")
plt.plot(x_dense, muB_lin, label="B (апрокс. лінійна)")
plt.scatter(X, muA, marker="o", label="A (точки)")
plt.scatter(X, muB, marker="x", label="B (точки)")
plt.xlabel("x")
plt.ylabel("μ(x)")
plt.ylim(-0.05, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()

# Графіки для A̅, B̅, A∪B, A∩B (дискретно)
plt.figure()
plt.title("A̅, B̅, A∪B, A∩B (дискретно)")
plt.plot(X, muA_bar, marker="o", label="A̅")
plt.plot(X, muB_bar, marker="o", label="B̅")
plt.plot(X, mu_union, marker="o", label="A∪B")
plt.plot(X, mu_inter, marker="o", label="A∩B")
plt.xlabel("x")
plt.ylabel("μ(x)")
plt.ylim(-0.05, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()

# Графіки для “операцій з пункту 3”
plt.figure()
plt.title("Операції: alg∩, alg∪, A\\B, AΔB, bnd∩, bnd∪ (дискретно)")
plt.plot(X, mu_alg_inter, marker="o", label="alg∩ (A·B)")
plt.plot(X, mu_alg_union, marker="o", label="alg∪ (a+b−ab)")
plt.plot(X, mu_A_diff_B, marker="o", label="A\\B")
plt.plot(X, mu_sym_diff, marker="o", label="AΔB")
plt.plot(X, mu_bounded_inter, marker="o", label="bnd∩")
plt.plot(X, mu_bounded_union, marker="o", label="bnd∪")
plt.xlabel("x")
plt.ylabel("μ(x)")
plt.ylim(-0.05, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()

# CON(A), DIL(A)
plt.figure()
plt.title("CON(A) та DIL(A) (дискретно)")
plt.plot(X, mu_conA, marker="o", label="CON(A)=μA^2")
plt.plot(X, mu_dilA, marker="o", label="DIL(A)=sqrt(μA)")
plt.xlabel("x")
plt.ylabel("μ(x)")
plt.ylim(-0.05, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()

plt.show()