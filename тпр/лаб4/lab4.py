import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("results_lab4_v7")
OUT.mkdir(exist_ok=True)
EPS = 1e-9

with open("D:\тпр\лаб4\data.json") as f:
    raw = np.array(json.load(f), dtype=float)

X_raw = raw[:, :6]          # x₁₁ x₁₂ x₂₁ x₂₂ x₃₁ x₃₂
Y_raw = raw[:, 6:7]         # Y   (one output)
Q = len(raw)                 # 40 спостережень
N1, N2, N3 = 2, 2, 2        # розмірності блоків
M = 1                        # кількість цільових функцій

# ──────────────────────────────────────────────────────────────────────────────
# 2. Нормування [0, 1]
# ──────────────────────────────────────────────────────────────────────────────
def normalize(arr):
    lo  = arr.min(axis=0)
    hi  = arr.max(axis=0)
    rng = np.where(hi - lo < 1e-12, 1.0, hi - lo)
    return (arr - lo) / rng, lo, hi

X_norm, X_lo, X_hi = normalize(X_raw)
Y_norm, Y_lo, Y_hi = normalize(Y_raw)

x1 = X_norm[:, 0:2]
x2 = X_norm[:, 2:4]
x3 = X_norm[:, 4:6]
y  = Y_norm[:, 0]           # нормована ціль, shape (Q,)

BLOCKS   = [x1, x2, x3]
N_SIZES  = [N1, N2, N3]
BLOCK_NAMES = ["X₁", "X₂", "X₃"]
VAR_NAMES   = ["x₁₁", "x₁₂", "x₂₁", "x₂₂", "x₃₁", "x₃₂"]

# ──────────────────────────────────────────────────────────────────────────────
# 3. Поліноми Чебишева (зсунуті на [0,1])
# ──────────────────────────────────────────────────────────────────────────────
def chebT(x: np.ndarray, n: int) -> np.ndarray:
    """T*ₙ(x) = Tₙ(2x−1)"""
    t = 2.0 * x - 1.0
    if n == 0: return np.ones_like(x)
    if n == 1: return t.copy()
    p, c = np.ones_like(x), t.copy()
    for _ in range(2, n + 1):
        p, c = c, 2.0 * t * c - p
    return c

def chebU(x: np.ndarray, n: int) -> np.ndarray:
    """U*ₙ(x) = Uₙ(2x−1)"""
    t = 2.0 * x - 1.0
    if n == 0: return np.ones_like(x)
    if n == 1: return (2.0 * t).copy()
    p, c = np.ones_like(x), (2.0 * t).copy()
    for _ in range(2, n + 1):
        p, c = c, 2.0 * t * c - p
    return c

def phi_v7(x: np.ndarray, p: int) -> np.ndarray:
    """
    Варіант 7:
      φ₀(x) = 0.5
      φₚ(x) = (1 + 2·T*ₚ(x)) / (U*₂ₚ(x) + 2(2p+1)·U*ₚ(x)),  p ≥ 1
    """
    if p == 0:
        return 0.5 * np.ones_like(x)
    alpha = 2 * p + 1
    T_p  = chebT(x, p)
    U_2p = chebU(x, 2 * p)
    U_p  = chebU(x, p)
    denom = U_2p + 2.0 * alpha * U_p
    # Числова стабілізація
    denom = np.where(np.abs(denom) < EPS,
                     np.sign(denom + EPS) * EPS, denom)
    return (1.0 + 2.0 * T_p) / denom

# ──────────────────────────────────────────────────────────────────────────────
# 4. Алгоритм відновлення (Structure II, МНК)
# ──────────────────────────────────────────────────────────────────────────────

def _safe_log(v):
    return np.log(np.abs(v) + EPS)

def compute_lambdas(x_blocks, y_vec, degrees):
    """
    Крок 1: знаходимо λ через систему МНК.
    Матриця: [ln(1+φ₀), ln(1+φ₁(x)), ..., ln(1+φₚ(x))]
    Права частина: ln(1+y)
    """
    P = list(degrees)
    n_cols = 1 + sum(ni * pi for ni, pi in zip(N_SIZES, P))
    A = np.zeros((Q, n_cols))
    A[:, 0] = np.log(1.0 + 0.5 + EPS)          # φ₀ = 0.5 для всіх

    col = 1
    for xi, pi, ni in zip(x_blocks, P, N_SIZES):
        for j in range(ni):
            for p in range(1, pi + 1):
                pv = phi_v7(xi[:, j], p)
                A[:, col] = np.log(1.0 + np.clip(pv, -1.0 + EPS, None) + EPS)
                col += 1

    b = np.log(1.0 + y_vec + EPS)
    lam, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    # Розбивка по блоках: кожній змінній j відповідає вектор λ₀..λₚ
    lam_blocks = []
    col = 1
    for ni, pi in zip(N_SIZES, P):
        lk = np.zeros((ni, pi + 1))
        for j in range(ni):
            lk[j, 0] = lam[0]       # спільний λ₀
            for p in range(1, pi + 1):
                lk[j, p] = lam[col]; col += 1
        lam_blocks.append(lk)
    return lam_blocks


def compute_psi(xi, lam_k, pk):
    """
    Ψₖⱼ(xₖⱼ) = exp{ λ₀·ln(1+φ₀) + Σₚ λₚ·ln(1+φₚ(x)) } − 1
    shape: (Q, nk)
    """
    ni = lam_k.shape[0]
    out = np.zeros((Q, ni))
    for j in range(ni):
        s = lam_k[j, 0] * np.log(1.0 + 0.5 + EPS)
        for p in range(1, pk + 1):
            pv = phi_v7(xi[:, j], p)
            s = s + lam_k[j, p] * np.log(1.0 + np.clip(pv, -1.0 + EPS, None) + EPS)
        out[:, j] = np.exp(s) - 1.0
    return out


def compute_A_coefs(psi_list, y_vec):
    """
    Крок 3: знаходимо A-коефіцієнти для Φₖ.
    Матриця: [ln(1+|Ψ₁|), ln(1+|Ψ₂|), ..., ln(1+|Ψₙ|)]
    Права частина: ln(1+|y|)
    """
    n_cols = sum(p.shape[1] for p in psi_list)
    Mm = np.zeros((Q, n_cols))
    col = 0
    for psi in psi_list:
        for j in range(psi.shape[1]):
            Mm[:, col] = np.log(1.0 + np.abs(psi[:, j]) + EPS); col += 1
    b = np.log(1.0 + np.abs(y_vec) + EPS)
    a, _, _, _ = np.linalg.lstsq(Mm, b, rcond=None)
    parts, col = [], 0
    for psi in psi_list:
        ni = psi.shape[1]
        parts.append(a[col:col + ni]); col += ni
    return parts


def compute_phi_k(psi, a_vec):
    """
    Φₖ(xₖ) = exp{ Σⱼ aⱼ·ln(1+|Ψₖⱼ|) } − 1
    """
    res = np.zeros(Q)
    for j in range(psi.shape[1]):
        res += a_vec[j] * np.log(1.0 + np.abs(psi[:, j]) + EPS)
    return np.exp(res) - 1.0


def compute_C(phi_list, y_vec):
    """
    Крок 5: знаходимо C-коефіцієнти.
    [ln(1+|Φ₁|), ln(1+|Φ₂|), ln(1+|Φ₃|)] · c = ln(1+|y|)
    """
    K = len(phi_list)
    Mm = np.zeros((Q, K))
    for k, fk in enumerate(phi_list):
        Mm[:, k] = np.log(1.0 + np.abs(fk) + EPS)
    b = np.log(1.0 + np.abs(y_vec) + EPS)
    c, _, _, _ = np.linalg.lstsq(Mm, b, rcond=None)
    return c


def reconstruct_Y(phi_list, c):
    """Φᵢ(x) = exp{ Σₖ cₖ·ln(1+|Φₖ|) } − 1"""
    res = np.zeros(Q)
    for k, fk in enumerate(phi_list):
        res += c[k] * np.log(1.0 + np.abs(fk) + EPS)
    return np.exp(res) - 1.0


def run(degrees):
    """Повний прохід алгоритму для заданих степенів."""
    lam_blocks = compute_lambdas(BLOCKS, y, degrees)
    lam1, lam2, lam3 = lam_blocks

    psi1 = compute_psi(x1, lam1, degrees[0])
    psi2 = compute_psi(x2, lam2, degrees[1])
    psi3 = compute_psi(x3, lam3, degrees[2])

    a_parts = compute_A_coefs([psi1, psi2, psi3], y)
    a1, a2, a3 = a_parts

    f1 = compute_phi_k(psi1, a1)
    f2 = compute_phi_k(psi2, a2)
    f3 = compute_phi_k(psi3, a3)

    c = compute_C([f1, f2, f3], y)
    y_hat = reconstruct_Y([f1, f2, f3], c)

    err_rms = float(np.sqrt(np.mean((y - y_hat) ** 2)))

    return dict(
        degrees=degrees,
        lam1=lam1, lam2=lam2, lam3=lam3,
        psi1=psi1, psi2=psi2, psi3=psi3,
        a1=a1, a2=a2, a3=a3,
        f1=f1, f2=f2, f3=f3,
        c=c, y_hat=y_hat, err=err_rms,
    )

# ──────────────────────────────────────────────────────────────────────────────
# 5. Запуск кількох конфігурацій степенів
# ──────────────────────────────────────────────────────────────────────────────
CONFIGS = [
    (2, 2, 2),
    (3, 3, 3),
    (4, 3, 4),
    (3, 4, 4),
    (2, 4, 3),
    (4, 4, 4),
]

results = []
for cfg in CONFIGS:
    r = run(cfg)
    results.append(r)
    print(f"Degrees {cfg}: RMS похибка = {r['err']:.6f}")

best = min(results, key=lambda r: r['err'])
print(f"\nНайкраща конфігурація: {best['degrees']}, RMS = {best['err']:.6f}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Графіки
# ──────────────────────────────────────────────────────────────────────────────
q_idx = np.arange(1, Q + 1)

for r in results:
    deg = r['degrees']
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(q_idx, y, 'b-', linewidth=1.5, label="Вибірка Y (нормована)")
    ax.plot(q_idx, r['y_hat'], 'orange', linewidth=1.5, linestyle='--', label="Апроксимація Φ(x)")
    ax.set_xlabel("q — номер спостереження")
    ax.set_ylabel("Y (нормоване)")
    ax.set_title(f"Степені p₁={deg[0]}, p₂={deg[1]}, p₃={deg[2]}   |   RMS = {r['err']:.6f}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fname = OUT / f"plot_Y1_p{deg[0]}_{deg[1]}_{deg[2]}.png"
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"  Збережено: {fname}")

# ──────────────────────────────────────────────────────────────────────────────
# 7. Зведений графік похибок
# ──────────────────────────────────────────────────────────────────────────────
labels  = [f"p=({r['degrees'][0]},{r['degrees'][1]},{r['degrees'][2]})" for r in results]
errors  = [r['err'] for r in results]

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(labels, errors, color='steelblue', edgecolor='navy')
ax.bar_label(bars, fmt="%.4f", fontsize=8)
ax.set_ylabel("RMS похибка (нормований простір)")
ax.set_title("Порівняння конфігурацій степенів поліномів")
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot_errors_comparison.png", dpi=150)
plt.close()
print("Збережено: plot_errors_comparison.png")

# ──────────────────────────────────────────────────────────────────────────────
# 8. Текстовий звіт
# ──────────────────────────────────────────────────────────────────────────────
def fmt_vec(v):
    return "  ".join(f"{x:+.8f}" for x in v)

def fmt_mat(m):
    return "\n".join("  " + fmt_vec(row) for row in m)

lines = []
lines.append("=" * 72)
lines.append("ЛАБОРАТОРНА РОБОТА №4")
lines.append("Відновлення функціональних залежностей в мультиплікативній формі")
lines.append("Варіант 7 — Структура II")
lines.append("=" * 72)
lines.append("")
lines.append("БАЗОВА ФУНКЦІЯ (Variant 7):")
lines.append("  phi_0(x) = 0.5")
lines.append("  phi_p(x) = (1 + 2·T*_p(x)) / (U*_{2p}(x) + 2·(2p+1)·U*_p(x))")
lines.append("  де T*_n(x) = T_n(2x-1),  U*_n(x) = U_n(2x-1),  alpha = 2p+1")
lines.append("")
lines.append("СТРУКТУРА II:")
lines.append("  Psi_kj(x)= exp{ lambda_0*ln(1+phi_0) + sum_p lambda_p*ln(1+phi_p(x)) } - 1")
lines.append("  Phi_k(X) = exp{ sum_j a_kj * ln(1 + |Psi_kj(x)|) } - 1")
lines.append("  Phi_i(X) = exp{ sum_k c_k  * ln(1 + |Phi_k(X)|) } - 1")
lines.append("")
lines.append("ДАНІ:")
lines.append(f"  Q  = {Q}  (спостережень)")
lines.append(f"  n1 = {N1}, n2 = {N2}, n3 = {N3}  (розмірності блоків)")
lines.append(f"  m  = {M}  (цільових функцій)")
lines.append(f"  X: [{X_lo.round(4).tolist()}] .. [{X_hi.round(4).tolist()}]")
lines.append(f"  Y: [{Y_lo[0]:.4f}] .. [{Y_hi[0]:.4f}]")
lines.append("")
lines.append("-" * 72)
lines.append("РЕЗУЛЬТАТИ ПО КОНФІГУРАЦІЯХ")
lines.append("-" * 72)
for r in results:
    deg = r['degrees']
    lines.append(f"\n### p1={deg[0]}, p2={deg[1]}, p3={deg[2]}   RMS={r['err']:.8f} ###")
    lines.append("")
    lines.append("Lambda-матриця 1 (блок X1):")
    lines.append(fmt_mat(r['lam1']))
    lines.append("Lambda-матриця 2 (блок X2):")
    lines.append(fmt_mat(r['lam2']))
    lines.append("Lambda-матриця 3 (блок X3):")
    lines.append(fmt_mat(r['lam3']))
    lines.append("")
    lines.append(f"Матриця A (коефіцієнти для Phi_k):")
    lines.append(f"  a1 = {fmt_vec(r['a1'])}")
    lines.append(f"  a2 = {fmt_vec(r['a2'])}")
    lines.append(f"  a3 = {fmt_vec(r['a3'])}")
    lines.append("")
    lines.append(f"Вектор C (коефіцієнти для Phi_i):")
    lines.append(f"  c = {fmt_vec(r['c'])}")
    lines.append("")
    lines.append("Відновлена нормована функція:")
    c = r['c']
    a1v, a2v, a3v = r['a1'], r['a2'], r['a3']
    l1, l2, l3 = r['lam1'], r['lam2'], r['lam3']
    lines.append(f"  Phi(x1,x2,x3) = exp(")
    lines.append(f"    + {c[0]:+.9f} * ln(1 + Phi1(x1))")
    lines.append(f"    + {c[1]:+.9f} * ln(1 + Phi2(x2))")
    lines.append(f"    + {c[2]:+.9f} * ln(1 + Phi3(x3))")
    lines.append(f"  ) - 1")
    lines.append("")
    for k, (ak, lk, bname, ni) in enumerate(zip([a1v,a2v,a3v],[l1,l2,l3],BLOCK_NAMES,[N1,N2,N3]),1):
        lines.append(f"  Phi{k}({bname}) = exp(")
        for j in range(ni):
            sign = "+" if ak[j] >= 0 else "-"
            lines.append(f"    {sign} {abs(ak[j]):.9f} * ln(1 + Psi{k}{j+1}(x))")
        lines.append(f"  ) - 1")
        for j in range(ni):
            lines.append(f"  Psi{k}{j+1}(x) = exp(")
            lines.append(f"    {lk[j,0]:+.9f} * ln(1+0.5)")
            for p in range(1, lk.shape[1]):
                lines.append(f"    {lk[j,p]:+.9f} * ln(1 + phi_{p}(x))")
            lines.append(f"  ) - 1")
        lines.append("")

lines.append("-" * 72)
lines.append("ПІДСУМОК")
lines.append("-" * 72)
lines.append(f"\n{'Конфігурація':>20}  {'RMS похибка':>16}")
for r in results:
    d = r['degrees']
    lines.append(f"p=({d[0]},{d[1]},{d[2]})           {r['err']:>16.8f}")

lines.append(f"\nНайкраща: p={best['degrees']}   RMS={best['err']:.8f}")
lines.append("")

report_path = OUT / "report_lab4_v7.txt"
report_path.write_text("\n".join(lines), encoding="utf-8")
print(f"\nЗвіт збережено: {report_path}")

# ──────────────────────────────────────────────────────────────────────────────
# 9. Зберігаємо числові результати
# ──────────────────────────────────────────────────────────────────────────────
for r in results:
    d = r['degrees']
    data_out = np.column_stack([y, r['y_hat']])
    np.savetxt(OUT / f"predictions_p{d[0]}_{d[1]}_{d[2]}.txt",
               data_out, header="Y_norm  Y_hat", fmt="%.10f")

print("\nГотово. Усі файли у:", OUT.resolve())
