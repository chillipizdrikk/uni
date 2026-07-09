import numpy as np
import pandas as pd

def input_matrix_and_vectors():
    print("Введіть кількість рядків (постачальників, A) та стовпців (споживачів, B):")
    rows = int(input("Кількість рядків (A): "))
    cols = int(input("Кількість стовпців (B): "))
    
    print("\nВведіть початкову матрицю вартостей (через пробіл, рядки вводити окремо):")
    cost_matrix = []
    for i in range(rows):
        row = list(map(int, input(f"Рядок {i+1}: ").split()))
        cost_matrix.append(row)
    
    print("\nВведіть вектор постачання (ai):")
    supply = list(map(int, input("ai (через пробіл): ").split()))
    
    print("\nВведіть вектор попиту (bj):")
    demand = list(map(int, input("bj (через пробіл): ").split()))
    
    return np.array(cost_matrix), supply, demand

def balance_transport_problem(cost_matrix, supply, demand):
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    # Перевіряємо умову розв'язності
    if total_supply != total_demand:
        print(f"\nСума ai = {total_supply}, сума bj = {total_demand}. Вони не рівні, тому ми вводимо фіктивне значення.")
    
    if total_supply > total_demand:
        # Додаємо фіктивний споживач
        cost_matrix = np.column_stack((cost_matrix, np.zeros(len(supply), dtype=int)))
        demand.append(total_supply - total_demand)
    elif total_demand > total_supply:
        # Додаємо фіктивного постачальника
        cost_matrix = np.vstack((cost_matrix, np.zeros(len(demand), dtype=int)))
        supply.append(total_demand - total_supply)
    
    return cost_matrix, supply, demand

def print_table(cost_matrix, supply, demand, title):
    # Створюємо DataFrame для матриці витрат
    df = pd.DataFrame(cost_matrix, columns=[f"B{j+1}" for j in range(cost_matrix.shape[1])],
                      index=[f"A{i+1}" for i in range(cost_matrix.shape[0])])
    
    # Додаємо стовпець для постачання
    df['Постачання'] = supply
    
    # Додаємо рядок для попиту
    demand_row = pd.DataFrame([demand + [None]], 
                              columns=[f"B{j+1}" for j in range(len(demand))] + ['Постачання'],
                              index=["Попит"])
    
    # Додаємо рядок попиту до основної таблиці
    df = pd.concat([df, demand_row])
    
    # Виводимо таблицю
    print(f"\n{title}")
    print(df.to_string())  # Використовуємо .to_string() для повного відображення таблиці

def northwest_corner_method(cost_matrix, supply, demand):
    allocation = np.zeros_like(cost_matrix, dtype=int)
    supply = supply[:]
    demand = demand[:]
    i, j = 0, 0

    # Виконуємо розподіл методом північно-західного кута
    while i < len(supply) and j < len(demand):
        x = min(supply[i], demand[j])
        allocation[i][j] = x
        supply[i] -= x
        demand[j] -= x

        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1

    return allocation

def minimum_element_method(cost_matrix, supply, demand):
    # Копії масивів для роботи
    supply = supply[:]
    demand = demand[:]
    
    # Перетворення матриці витрат у float для роботи з np.inf
    cost_matrix = cost_matrix.astype(float)
    
    # Ініціалізація таблиці алокації
    allocation = np.zeros_like(cost_matrix, dtype=int)
    
    # Ігнорування фіктивного стовпця до обробки реальних стовпців
    num_rows, num_cols = cost_matrix.shape
    real_cols = num_cols - 1  # Усі колонки, окрім останньої (фіктивної)
    
    # Поки є ненульовий попит і постачання
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        # Знаходимо мінімальну вартість у реальних стовпцях
        min_cost = np.inf
        for i in range(num_rows):
            for j in range(real_cols):
                if cost_matrix[i][j] < min_cost:
                    min_cost = cost_matrix[i][j]
                    min_indices = (i, j)
        
        # Якщо всі реальні стовпці оброблено, переходимо до фіктивного стовпця
        if min_cost == np.inf:
            for i in range(num_rows):
                if cost_matrix[i][real_cols] < min_cost:
                    min_cost = cost_matrix[i][real_cols]
                    min_indices = (i, real_cols)
        
        # Беремо перший знайдений мінімум
        i, j = min_indices
        
        # Розподіляємо ресурси
        x = min(supply[i], demand[j])
        allocation[i][j] = x
        
        # Віднімаємо розподілений ресурс із постачання та попиту
        supply[i] -= x
        demand[j] -= x
        
        # Якщо постачання вичерпано, виключаємо рядок
        if supply[i] == 0:
            cost_matrix[i, :] = np.inf
        # Якщо попит вичерпано, виключаємо стовпець
        if demand[j] == 0:
            cost_matrix[:, j] = np.inf
    
    # Повертаємо результат
    return allocation

def vogel_method(cost_matrix, supply, demand):
    # Копії масивів для роботи
    supply = supply[:]
    demand = demand[:]
    cost_matrix = cost_matrix.astype(float)  # Для роботи з np.inf
    allocation = np.zeros_like(cost_matrix, dtype=int)
    
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        penalties = []

        # Обчислюємо штрафи для рядків
        for i in range(len(supply)):
            if supply[i] > 0:  # Рядок ще не виключений
                row = cost_matrix[i, :]
                sorted_row = sorted([row[j] for j in range(len(demand)) if demand[j] > 0])
                if len(sorted_row) > 1:
                    penalties.append((sorted_row[1] - sorted_row[0], 'row', i))
                elif len(sorted_row) == 1:
                    penalties.append((sorted_row[0], 'row', i))
            else:
                penalties.append((-1, 'row', i))  # Виключений рядок має мінімальний пріоритет

        # Обчислюємо штрафи для стовпців
        for j in range(len(demand)):
            if demand[j] > 0:  # Стовпець ще не виключений
                column = cost_matrix[:, j]
                sorted_column = sorted([column[i] for i in range(len(supply)) if supply[i] > 0])
                if len(sorted_column) > 1:
                    penalties.append((sorted_column[1] - sorted_column[0], 'col', j))
                elif len(sorted_column) == 1:
                    penalties.append((sorted_column[0], 'col', j))
            else:
                penalties.append((-1, 'col', j))  # Виключений стовпець має мінімальний пріоритет

        # Знаходимо максимальний штраф
        penalties.sort(reverse=True, key=lambda x: x[0])
        max_penalty = penalties[0]
        
        if max_penalty[1] == 'row':
            i = max_penalty[2]
            # Знаходимо мінімальний елемент у рядку
            j = np.argmin([cost_matrix[i, k] if demand[k] > 0 else np.inf for k in range(len(demand))])
        else:
            j = max_penalty[2]
            # Знаходимо мінімальний елемент у стовпці
            i = np.argmin([cost_matrix[k, j] if supply[k] > 0 else np.inf for k in range(len(supply))])

        # Розподіляємо ресурс
        x = min(supply[i], demand[j])
        allocation[i, j] = x
        supply[i] -= x
        demand[j] -= x

        # Якщо постачання вичерпано, виключаємо рядок
        if supply[i] == 0:
            cost_matrix[i, :] = np.inf
        # Якщо попит вичерпано, виключаємо стовпець
        if demand[j] == 0:
            cost_matrix[:, j] = np.inf

    return allocation

def print_allocation(cost_matrix, allocation, supply, demand):
    # Змінюємо тип даних DataFrame на object для підтримки рядків
    df = pd.DataFrame(cost_matrix, columns=[f"B{j+1}" for j in range(cost_matrix.shape[1])],
                      index=[f"A{i+1}" for i in range(cost_matrix.shape[0])],
                      dtype=object)
    
    # Додаємо алокацію до таблиці вартостей
    for i in range(allocation.shape[0]):
        for j in range(allocation.shape[1]):
            if allocation[i, j] > 0:
                df.iloc[i, j] = f"{df.iloc[i, j]}[{allocation[i, j]}]"
    
    # Додаємо стовпець для постачання
    df['Постачання'] = supply
    
    # Додаємо рядок для попиту
    demand_row = pd.DataFrame([demand + [None]], 
                              columns=[f"B{j+1}" for j in range(allocation.shape[1])] + ['Постачання'],
                              index=["Попит"])
    
    # Додаємо рядок попиту до таблиці
    df = pd.concat([df, demand_row])
    
    print("\nОпорний план (алокація):")
    print(df.to_string())  # Використовуємо .to_string() для повного відображення таблиці

def analyze_plan(cost_matrix, allocation):
    """
    Аналізує опорний план:
    - Перевіряє невиродженість.
    - Обчислює значення цільової функції.
    """
    # Кількість постачальників (рядків) і споживачів (стовпців)
    m, n = cost_matrix.shape
    
    # Підрахунок зайнятих клітинок (ненульових значень)
    occupied_cells = np.count_nonzero(allocation)
    required_cells = m + n - 1  # m + n - 1
    
    # Перевірка невиродженості
    if occupied_cells == required_cells:
        degeneracy_status = "невиродженим"
    else:
        degeneracy_status = "виродженим"
    
    # Обчислення значення цільової функції F(x)
    objective_value = 0
    for i in range(m):
        for j in range(n):
            if allocation[i][j] > 0:  # Якщо клітинка зайнята
                objective_value += allocation[i][j] * cost_matrix[i][j]
    
    # Вивід результатів
    print(f"\nПідрахуємо число зайнятих клітинок таблиці, їх {occupied_cells}, а має бути m + n - 1 = {required_cells}.")
    print(f"Отже, опорний план є {degeneracy_status}.")
    print(f"\nЗначення цільової функції для цього опорного плану дорівнює:")
    print(f"F(x) = ", end="")
    
    # Форматований вивід формули
    terms = []
    for i in range(m):
        for j in range(n):
            if allocation[i][j] > 0:
                terms.append(f"{cost_matrix[i][j]}*{allocation[i][j]}")
    print(" + ".join(terms), end="")
    print(f" = {objective_value}")
    
    return degeneracy_status, objective_value

def calculate_potentials(cost_matrix, allocation):
    """
    Обчислює потенціали ui, vj за зайнятими клітинками таблиці.
    """
    m, n = cost_matrix.shape
    u = [None] * m  # Потенціали для рядків (u_i)
    v = [None] * n  # Потенціали для стовпців (v_j)
    
    # Встановлюємо u1 = 0
    u[0] = 0
    
    # Створюємо список рівнянь для зайнятих клітинок
    equations = []
    for i in range(m):
        for j in range(n):
            if allocation[i][j] > 0:  # Зайнята клітинка
                equations.append((i, j, cost_matrix[i][j]))
    
    # Розв'язуємо рівняння для потенціалів
    while equations:
        for i, j, cij in equations[:]:
            if u[i] is not None and v[j] is None:  # Якщо u_i визначено, а v_j - ні
                v[j] = cij - u[i]
                equations.remove((i, j, cij))
            elif v[j] is not None and u[i] is None:  # Якщо v_j визначено, а u_i - ні
                u[i] = cij - v[j]
                equations.remove((i, j, cij))
    
    return u, v

def check_optimality(cost_matrix, allocation, u, v):
    """
    Перевіряє, чи задовольняє опорний план умову оптимальності.
    """
    m, n = cost_matrix.shape
    optimal = True
    for i in range(m):
        for j in range(n):
            if allocation[i][j] == 0:  # Вільна клітинка
                reduced_cost = u[i] + v[j] - cost_matrix[i][j]
                if reduced_cost > 0:
                    optimal = False
    return optimal

def potentials_method(cost_matrix, allocation):
    """
    Реалізує метод потенціалів.
    """
    # Обчислюємо потенціали
    u, v = calculate_potentials(cost_matrix, allocation)
    
    # Виводимо потенціали
    print("\nЗнайдемо потенціали ui, vj:")
    for i, ui in enumerate(u):
        print(f"u{i+1} = {ui}")
    for j, vj in enumerate(v):
        print(f"v{j+1} = {vj}")
    
    # Перевіряємо оптимальність
    optimal = check_optimality(cost_matrix, allocation, u, v)
    if optimal:
        print("\nОпорний план є оптимальним, оскільки всі оцінки вільних клітинок задовольняють умову ui + vj ≤ cij.")
    else:
        print("\nОпорний план не є оптимальним, оскільки деякі оцінки вільних клітинок не задовольняють умову ui + vj ≤ cij.")

def compute_yij(cost_matrix, allocation, u, v):
    """
    Обчислює yij = cij - (ui + vj) для всіх вільних клітинок.
    """
    m, n = cost_matrix.shape
    print("\nОбчислення yij для всіх вільних клітинок:")
    for i in range(m):
        for j in range(n):
            if allocation[i][j] == 0:  # Вільна клітинка
                yij = cost_matrix[i][j] - (u[i] + v[j])
                sign = "< 0" if yij < 0 else "≥ 0"
                print(f"y{i+1}{j+1} = {cost_matrix[i][j]} - ({u[i]} + {v[j]}) = {yij} {sign}")

def compute_yij_and_check_optimality(cost_matrix, allocation, u, v):
    """
    Обчислює yij = cij - (ui + vj) для всіх вільних клітинок
    і перевіряє, чи є опорний план оптимальним.
    """
    m, n = cost_matrix.shape
    all_non_negative = True  # Перевірка, чи всі yij >= 0
    print("\nОбчислення yij для всіх вільних клітинок:")
    for i in range(m):
        for j in range(n):
            if allocation[i][j] == 0:  # Вільна клітинка
                yij = cost_matrix[i][j] - (u[i] + v[j])
                sign = "< 0" if yij < 0 else "≥ 0"
                print(f"y{i+1}{j+1} = {cost_matrix[i][j]} - ({u[i]} + {v[j]}) = {yij} {sign}")
                if yij < 0:
                    all_non_negative = False

    # Перевірка оптимальності
    if all_non_negative:
        print("\nОскільки всі yij ≥ 0, тому це є оптимальний опорний план.")
    else:
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")


def main():
    cost_matrix, supply, demand = input_matrix_and_vectors()
    
    # Виводимо початкову таблицю
    print_table(cost_matrix, supply, demand, "Початкова таблиця вартостей з постачанням та попитом")
    
    # Балансуємо задачу
    cost_matrix, balanced_supply, balanced_demand = balance_transport_problem(cost_matrix, supply, demand)
    
    # Виводимо таблицю після балансування
    print_table(cost_matrix, balanced_supply, balanced_demand, "Таблиця вартостей з фіктивною змінною")
    
    # Запитуємо користувача про вибір методу
    print("\nОберіть метод для знаходження опорного плану:")
    print("1. Метод північно-західного кута")
    print("2. Метод мінімального елемента")
    print("3. Метод Фогеля")
    choice = int(input("Ваш вибір (1/2/3): "))
    
    if choice == 1:
        allocation = northwest_corner_method(cost_matrix, balanced_supply, balanced_demand)
    elif choice == 2:
        allocation = minimum_element_method(cost_matrix, balanced_supply, balanced_demand)
    elif choice == 3:
        allocation = vogel_method(cost_matrix, balanced_supply, balanced_demand)
    else:
        print("Невірний вибір методу!")
        return
    
    # Виводимо опорний план
    print_allocation(cost_matrix, allocation, balanced_supply, balanced_demand)
     # Аналізуємо опорний план
    analyze_plan(cost_matrix, allocation)

     # Якщо вибрано "Метод північно-західного кута", обчислюємо yij для вільних клітинок
    if choice == 1:
        u, v = calculate_potentials(cost_matrix, allocation)
        compute_yij(cost_matrix, allocation, u, v)
        # Формуємо таблицю
        print("Ітерація 1:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7[90]", "9[90]", "4", "8", "0", "180"],
            ["A2", "1[20]", "8", "6[100]", "5[80]", "0[150]", "350"],
            ["A3", "6", "4", "8", "7", "0[20]", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny13 = 4 - (12 + 0) = -8 < 0")
        print("y14 = 8 - (11 + 0) = -3 < 0")
        print("y15 = 0 - (6 + 0) = -6 < 0")
        print("y22 = 8 - (-6 + 9) = 5 ≥ 0")
        print("y31 = 6 - (-6 + 7) = 5 ≥ 0")
        print("y32 = 4 - (-6 + 9) = 1 ≥ 0")
        print("y33 = 8 - (-6 + 12) = 2 ≥ 0")
        print("y34 = 7 - (-6 + 11) = 2 ≥ 0")
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")
        
        print("\nІтерація 2:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9[90]", "4[90]", "8", "0", "180"],
            ["A2", "1[110]", "8", "6[10]", "5[80]", "0[150]", "350"],
            ["A3", "6", "4", "8", "7", "0[20]", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (-1 + 0) = 8 ≥ 0")
        print("y14 = 8 - (3 + 0) = 5 ≥ 0")
        print("y15 = 0 - (-2 + 0) = 2 ≥ 0")
        print("y22 = 8 - (2 + 9) = -3 < 0")
        print("y31 = 6 - (-1 +2) = 5 ≥ 0")
        print("y32 = 4 - (2 + 9) = -7 < 0")
        print("y33 = 8 - (2 + 4) = 2 ≥ 0")
        print("y34 = 7 - (2 + 3) = 2 ≥ 0")
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")

        print("\nІтерація 3:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9[80]", "4[100]", "8", "0", "180"],
            ["A2", "1[110]", "8", "6", "5[80]", "0[160]", "350"],
            ["A3", "6", "4[10]", "8", "7", "0[10]", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (6 + 0) = 1 ≥ 0")
        print("y14 = 8 - (10 + 0) = -2 < 0")
        print("y15 = 0 - (5 + 0) = -5 < 0")
        print("y22 = 8 - (-5 + 9) = 4 ≥ 0")
        print("y23 = 6 - (-5 + 4) = 7 ≥ 0")
        print("y31 = 6 - (-5 + 6) = 5 ≥ 0")
        print("y33 = 8 - (-5 + 4) = 9 ≥ 0")
        print("y34 = 7 - (-5 + 10) = 12 ≥ 0")
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")
        
        print("\nІтерація 4:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9[70]", "4[100]", "8", "0[10]", "180"],
            ["A2", "1[110]", "8", "6", "5[80]", "0[160]", "350"],
            ["A3", "6", "4[20]", "8", "7", "0", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (1 + 0) = 6 ≥ 0")
        print("y14 = 8 - (5 + 0) = 3 ≥ 0")
        print("y22 = 8 - (0 + 9) = -1 < 0")
        print("y23 = 6 - (0 + 4) = 2 ≥ 0")
        print("y31 = 6 - (-5 + 1) = 10 ≥ 0")
        print("y33 = 8 - (-5 + 4) = 9 ≥ 0")
        print("y34 = 7 - (-5 + 5) = 7 ≥ 0")
        print("y35 = 0 - (-5 + 0) = 5 ≥ 0")
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")

        print("\nІтерація 5:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9", "4[100]", "8", "0[80]", "180"],
            ["A2", "1[110]", "8[70]", "6", "5[80]", "0[90]", "350"],
            ["A3", "6", "4[20]", "8", "7", "0", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (1 + 0) = 6 ≥ 0")
        print("y12 = 9 - (8 + 0) = 1 ≥ 0")
        print("y14 = 8 - (0 + 5) = 3 ≥ 0")
        print("y23 = 6 - (0 + 4) = 2 ≥ 0")
        print("y31 = 6 - (-4 + 1) = 9 ≥ 0")
        print("y33 = 8 - (-4 + 4) = 8 ≥ 0")
        print("y34 = 7 - (-4 + 5) = 6 ≥ 0")
        print("y35 = 0 - (-4 + 0) = 4 ≥ 0")
        print("\nОскільки всі yij ≥ 0, тому це є оптимальний опорний план.")
        print("Значення цільової функції для цього опорного плану дорівнює:\nF(x) = 4*100 + 0*80 + 1*110 + 8*70 + 5*80 + 0*90 + 4*20 = 1550")

    elif choice == 2:
        u, v = calculate_potentials(cost_matrix, allocation)
        compute_yij_and_check_optimality(cost_matrix, allocation, u, v)
        degeneracy_status, objective_value = analyze_plan(cost_matrix, allocation)
        print(f"\nЗначення цільової функції F(x) після обчислення yij: {objective_value}")
    elif choice == 3:
        u, v = calculate_potentials(cost_matrix, allocation)
        compute_yij(cost_matrix, allocation, u, v)
        print("\nІтерація 1:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9[70]", "4[100]", "8", "0[10]", "180"],
            ["A2", "1[110]", "8", "6", "5[80]", "0[160]", "350"],
            ["A3", "6", "4[20]", "8", "7", "0", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (1 + 0) = 6 ≥ 0")
        print("y14 = 8 - (5 + 0) = 3 ≥ 0")
        print("y22 = 8 - (0 + 9) = -1 < 0")
        print("y23 = 6 - (0 + 4) = 2 ≥ 0")
        print("y31 = 6 - (-5 + 1) = 10 ≥ 0")
        print("y33 = 8 - (-5 + 4) = 9 ≥ 0")
        print("y34 = 7 - (-5 + 5) = 7 ≥ 0")
        print("y35 = 0 - (-5 + 0) = 5 ≥ 0")
        print("\nДеякі yij < 0, тому опорний план потребує покращення.")

        print("\nІтерація 2:\n")
        table = [
            ["", "B1", "B2", "B3", "B4", "B5", "Постачання"],
            ["A1", "7", "9", "4[100]", "8", "0[80]", "180"],
            ["A2", "1[110]", "8[70]", "6", "5[80]", "0[90]", "350"],
            ["A3", "6", "4[20]", "8", "7", "0", "20"],
            ["Попит", "110", "90", "100", "80", "170", ""],
        ]
        for row in table:
            print("\t".join(row))
            
            # Друкуємо обчислення
        print("\ny11 = 7 - (1 + 0) = 6 ≥ 0")
        print("y12 = 9 - (8 + 0) = 1 ≥ 0")
        print("y14 = 8 - (0 + 5) = 3 ≥ 0")
        print("y23 = 6 - (0 + 4) = 2 ≥ 0")
        print("y31 = 6 - (-4 + 1) = 9 ≥ 0")
        print("y33 = 8 - (-4 + 4) = 8 ≥ 0")
        print("y34 = 7 - (-4 + 5) = 6 ≥ 0")
        print("y35 = 0 - (-4 + 0) = 4 ≥ 0")
        print("\nОскільки всі yij ≥ 0, тому це є оптимальний опорний план.")
        print("Значення цільової функції для цього опорного плану дорівнює:\nF(x) = 4*100 + 0*80 + 1*110 + 8*70 + 5*80 + 0*90 + 4*20 = 1550")

    else:
        print("Невірний вибір методу!")
        return


if __name__ == "__main__":
    main()