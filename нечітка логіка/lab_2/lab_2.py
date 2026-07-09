import json
import numpy as np


def load_relations(filename="relations.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

     # Перевірка наявності ключів
    if "R1" not in data or "R2" not in data:
        raise KeyError("У файлі повинні бути ключі 'R1' і 'R2'.")

    R1 = np.array(data["R1"], dtype=float)
    R2 = np.array(data["R2"], dtype=float)

    # Перевірка розмірів
    if R1.shape != R2.shape:
        raise ValueError("R1 і R2 повинні мати однаковий розмір.")

    # Перевірка, що матриці квадратні
    if R1.ndim != 2 or R2.ndim != 2:
        raise ValueError("R1 і R2 повинні бути двовимірними матрицями.")

    if R1.shape[0] != R1.shape[1] or R2.shape[0] != R2.shape[1]:
        raise ValueError("Матриці R1 і R2 повинні бути квадратними.")

    # Перевірка значень у межах [0, 1]
    if np.any((R1 < 0) | (R1 > 1)) or np.any((R2 < 0) | (R2 > 1)):
        raise ValueError("Усі елементи R1 і R2 повинні належати відрізку [0, 1].")

    return R1, R2

# Операції над нечіткими відношеннями

def max_min_composition(A, B):
    n, m = A.shape[0], B.shape[1]
    C = np.zeros((n, m), dtype=float)

    for i in range(n):
        for j in range(m):
            C[i, j] = max(min(A[i, k], B[k, j]) for k in range(B.shape[0]))

    return C

def max_prod_composition(A, B):
    n, m = A.shape[0], B.shape[1]
    C = np.zeros((n, m), dtype=float)

    for i in range(n):
        for j in range(m):
            C[i, j] = max(A[i, k] * B[k, j] for k in range(B.shape[0]))

    return C

def fuzzy_difference(A, B):
    # A \ B = A ∩ B^c
    return np.minimum(A, 1 - B)

def fuzzy_symmetric_difference(A, B):
    # (A \ B) ∪ (B \ A)
    return np.maximum(np.minimum(A, 1 - B), np.minimum(B, 1 - A))

# Перевірка властивостей

def check_properties(R):
    n = R.shape[0]
    diag = np.diag(R)

    reflexive = np.allclose(diag, 1.0)
    irreflexive = np.allclose(diag, 0.0)
    symmetric = np.allclose(R, R.T)

    antisymmetric = True
    for i in range(n):
        for j in range(n):
            if i != j and min(R[i, j], R[j, i]) > 1e-9:
                antisymmetric = False
                break
        if not antisymmetric:
            break

    asymmetric = irreflexive and antisymmetric
    transitive = np.all(max_min_composition(R, R) <= R + 1e-9)

    return {
        "Рефлексивність": reflexive,
        "Іррефлексивність": irreflexive,
        "Симетричність": symmetric,
        "Антисиметричність": antisymmetric,
        "Асиметричність": asymmetric,
        "Транзитивність": transitive
    }

# Вивід
def format_number(x, width=6):
    return f"{x:.2f}".rjust(width)

def matrix_to_string(name, M):
    lines = []
    lines.append(f"{name}:")
    lines.append("-" * (len(name) + 1))

    header = "      " + "".join(f"{j+1:>6}" for j in range(M.shape[1]))
    lines.append(header)

    for i, row in enumerate(M):
        row_str = f"{i+1:>4} | " + "".join(format_number(x) for x in row)
        lines.append(row_str)

    return "\n".join(lines)

def properties_to_string(props):
    lines = ["Властивості R1:", "---------------"]
    for key, value in props.items():
        lines.append(f"{key:<20} : {'Так' if value else 'Ні'}")
    return "\n".join(lines)

def save_results(filename, results, properties):
    with open(filename, "w", encoding="utf-8") as f:
        for name, matrix in results.items():
            f.write(matrix_to_string(name, matrix))
            f.write("\n\n")

        f.write(properties_to_string(properties))
        f.write("\n")

def main():
    try:
        R1, R2 = load_relations("relations.json")
    except Exception as e:
        print("Помилка при зчитуванні файлу:", e)
        return

    union = np.maximum(R1, R2)
    intersection = np.minimum(R1, R2)
    difference = fuzzy_difference(R1, R2)
    sym_difference = fuzzy_symmetric_difference(R1, R2)
    complement_R1 = 1 - R1
    max_min = max_min_composition(R1, R2)
    max_prod = max_prod_composition(R1, R2)

    properties = check_properties(R1)

    results = {
        "R1": R1,
        "R2": R2,
        "R1 ∪ R2": union,
        "R1 ∩ R2": intersection,
        "R1 \\ R2": difference,
        "R1 Δ R2": sym_difference,
        "R1 ∘ R2 (max-min)": max_min,
        "R1 ∘ R2 (max-prod)": max_prod,
        "¬R1": complement_R1
    }

    print("\n" + "=" * 60)

    for name, matrix in results.items():
        print(matrix_to_string(name, matrix))
        print()

    print(properties_to_string(properties))

    save_results("results.txt", results, properties)
    print("\nРезультати збережено у файл: results.txt")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()