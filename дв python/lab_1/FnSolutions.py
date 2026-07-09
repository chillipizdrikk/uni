import os

def FnSol1(nums):
    """
    Задача 1. nums - список цілих чисел, що закінчується нулем (0).
    Повертає:
      (кількість додатніх, кількість від'ємних, середнє арифметичне від'ємних)
    """
    pos = sum(1 for x in nums if x > 0)
    neg_list = [x for x in nums if x < 0]
    neg = len(neg_list)
    avg_neg = sum(neg_list)/neg if neg > 0 else 0
    return pos, neg, avg_neg

def FnSol2(a, b, c):
    """
    Задача 2. Вхід: три числа a, b, c (int/float).
    Повертає:
      (чи можуть бути довжинами відрізків,
       якщо так, чи можна утворити трикутник і який він)
    """
    segs = all(x > 0 for x in (a, b, c))
    triangle = False
    t_type = None
    if segs:
        if (a+b > c) and (a+c > b) and (b+c > a):
            triangle = True
            if a == b == c:
                t_type = "рівносторонній"
            elif a == b or b == c or a == c:
                t_type = "рівнобедрений"
            else:
                t_type = "різносторонній"
    return segs, triangle, t_type

def FnSol3(sentence):
    """
    Задача 3. Вхід: рядок - речення.
    Повертає: список слів речення.
    """
    # Ділимо за пробілом, видаляючи порожні елементи
    return [w for w in sentence.strip().split() if w]

def FnSol4(matrix):
    """
    Задача 4. Вхід: двовимірний список NxN додатніх, від'ємних і нульових цілих чисел.
    Повертає: максимальна сума підпрямокутника.
    """
    N = len(matrix)
    max_sum = None
    for r1 in range(N):
        for r2 in range(r1, N):
            for c1 in range(N):
                for c2 in range(c1, N):
                    s = sum(matrix[r][c] for r in range(r1, r2+1) for c in range(c1, c2+1))
                    if max_sum is None or s > max_sum:
                        max_sum = s
    return max_sum

def Testorg():
    """
    Організація тестування. Запитує номер задачі, визначає файл вхідних даних,
    виконує тести, записує результати у файл протоколу ResultAll.txt
    """
    test_files = {
        '1': 'InData1.txt',
        '2': 'InData2.txt',
        '3': 'InData3.txt',
        '4': 'InData4.txt',
    }
    print("Введіть номер задачі для тестування (1-4): ", end='')
    num = input().strip()
    if num not in test_files:
        print("Невірний номер задачі.")
        return

    in_file = test_files[num]
    if not os.path.isfile(in_file):
        print(f"Файл {in_file} не знайдено.")
        return

    with open(in_file, encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if num == '1':
            test_type = f"Тест {i+1} (функціональний/деструктивний/зручності)"
            nums = list(map(int, line.split()))
            out = FnSol1(nums)
            results.append(f"{test_type}\nвхід: {nums}\nвихід: Додатніх: {out[0]}, Від'ємних: {out[1]}, Середнє від'ємних: {out[2]:.3f}\n")
        elif num == '2':
            test_type = f"Тест {i+1} (функціональний/деструктивний/зручності)"
            vals = list(map(float, line.split()))
            if len(vals) != 3:
                results.append(f"{test_type}\nвхід: {line}\nвихід: Невірна кількість параметрів\n")
            else:
                out = FnSol2(*vals)
                results.append(
                    f"{test_type}\nвхід: {vals}\nвихід: "
                    f"Відрізки: {out[0]}, Трикутник: {out[1]}, Тип: {out[2]}\n"
                )
        elif num == '3':
            test_type = f"Тест {i+1} (функціональний/деструктивний/зручності)"
            out = FnSol3(line)
            results.append(
                f"{test_type}\nвхід: \"{line}\"\nвихід:\n" +
                "\n".join(out) + "\n"
            )
        elif num == '4':
            test_type = f"Тест {i+1} (функціональний/деструктивний/зручності)"
            try:
                rows = [list(map(int, row.strip().split()))
                        for row in line.split(';')]
                out = FnSol4(rows)
                results.append(
                    f"{test_type}\nвхід: {rows}\nвихід: Максимальна сума підпрямокутника: {out}\n"
                )
            except Exception as e:
                results.append(f"{test_type}\nвхід: {line}\nвихід: Помилка: {e}\n")

    with open('ResultAll.txt', 'a', encoding='utf-8') as fout:
        fout.write(f"\n=== Результати тестування задачі {num} ===\n")
        fout.write('\n'.join(results))
        fout.write('\n')

if __name__ == '__main__':
    Testorg()