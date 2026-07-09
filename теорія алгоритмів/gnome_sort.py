import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import random
import time

def gnomeSort(arr):
    index = 0
    steps = [list(arr)]  # Зберігаємо початковий стан масиву
    while index < len(arr):
        if index == 0:
            index += 1
        if arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
            steps.append(list(arr))  # Зберігаємо проміжний стан масиву
    return steps  # Повертаємо всі проміжні стани

# Візуалізація сортування
arr = [1, 7, 8, 2, 3, 5, 4, 6]
steps = gnomeSort(arr)


# def generate_data_and_plot():
#     sizes = [0, 100, 200, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
#     times_random = []
#     times_sorted = []
#     times_semi_sorted = []
#     times_sorted_with_swaps = []

#     for size in sizes:
#         arr_random = [random.randint(1, 1000) for _ in range(size)]
#         arr_sorted = list(range(size))
#         arr_semi_sorted = []
#         for _ in range(5):
#             arr_semi_sorted += sorted([random.randint(1, 1000) for _ in range(size // 5)])
#         arr_sorted_with_swaps = list(range(size))
#         for _ in range(size // 10):
#             i, j = random.sample(range(size), 2)
#             arr_sorted_with_swaps[i], arr_sorted_with_swaps[j] = arr_sorted_with_swaps[j], arr_sorted_with_swaps[i]

#         start_time = time.time()
#         gnomeSort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted_with_swaps)
#         end_time = time.time()
#         times_sorted_with_swaps.append(end_time - start_time)

#     plt.plot(sizes, times_random, label='Випадкові числа')
#     plt.plot(sizes, times_sorted, label='Впорядковані числа')
#     plt.plot(sizes, times_semi_sorted, label='Частково впорядковані числа')
#     plt.plot(sizes, times_sorted_with_swaps, label='Впорядковані числа з перестановками')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Часова складність алгоритму Gnome Sort')
#     plt.legend()
#     plt.show()

# generate_data_and_plot()



# def generate_data_and_plot():
#     sizes = [0, 100, 200, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]  # Розміри масивів, які ви хочете протестувати
#     times_random = []
#     times_sorted = []
#     times_semi_sorted = []
#     times_sorted_with_swaps = []

#     for size in sizes:
#         # Генеруємо масив випадкових чисел
#         arr_random = [random.randint(1, 1000) for _ in range(size)]
#         # Генеруємо вже впорядкований масив
#         arr_sorted = list(range(size))
#         # Генеруємо масив, розбитий на декілька впорядкованих підмасивів
#         arr_semi_sorted = []
#         for _ in range(5):  # 5 підмасивів
#             arr_semi_sorted += sorted([random.randint(1, 1000) for _ in range(size // 5)])
#         # Генеруємо впорядкований масив з декількома "свопами"
#         arr_sorted_with_swaps = list(range(size))
#         for _ in range(size // 10):  # Додаємо свопи для 10% елементів
#             i, j = random.sample(range(size), 2)
#             arr_sorted_with_swaps[i], arr_sorted_with_swaps[j] = arr_sorted_with_swaps[j], arr_sorted_with_swaps[i]

#         # Засікаємо час виконання для кожного типу масиву
#         start_time = time.time()
#         gnomeSort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted_with_swaps)
#         end_time = time.time()
#         times_sorted_with_swaps.append(end_time - start_time)

#     # Будуємо окремі гістограми для кожного типу масиву
#     plt.figure(figsize=(12, 8))

#     plt.subplot(221)
#     plt.plot(sizes, times_random, 'o-')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Випадкові числа')

#     plt.subplot(222)
#     plt.plot(sizes, times_sorted, 'o-')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Впорядковані числа')

#     plt.subplot(223)
#     plt.plot(sizes, times_semi_sorted, 'o-')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Частково впорядковані числа')

#     plt.subplot(224)
#     plt.plot(sizes, times_sorted_with_swaps, 'o-')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Впорядковані числа з перестановками')

#     plt.tight_layout()
#     plt.show()

# generate_data_and_plot()


# def generate_data_and_plot():
#     sizes = [0, 100, 200, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]  # Розміри масивів, які ви хочете протестувати
#     times_random = []
#     times_sorted = []
#     times_semi_sorted = []
#     times_sorted_with_swaps = []

#     for size in sizes:
#         # Генеруємо масив випадкових чисел
#         arr_random = [random.randint(1, 1000) for _ in range(size)]
#         # Генеруємо вже впорядкований масив
#         arr_sorted = list(range(size))
#         # Генеруємо масив, розбитий на декілька впорядкованих підмасивів
#         arr_semi_sorted = []
#         for _ in range(5):  # 5 підмасивів
#             arr_semi_sorted += sorted([random.randint(1, 1000) for _ in range(size // 5)])
#         # Генеруємо впорядкований масив з декількома "свопами"
#         arr_sorted_with_swaps = list(range(size))
#         for _ in range(size // 10):  # Додаємо свопи для 10% елементів
#             i, j = random.sample(range(size), 2)
#             arr_sorted_with_swaps[i], arr_sorted_with_swaps[j] = arr_sorted_with_swaps[j], arr_sorted_with_swaps[i]

#         # Засікаємо час виконання для кожного типу масиву
#         start_time = time.time()
#         gnomeSort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         gnomeSort(arr_sorted_with_swaps)
#         end_time = time.time()
#         times_sorted_with_swaps.append(end_time - start_time)

#     # Створюємо таблиці
#     data_random = {'Розмір масиву': sizes, 'Час виконання (сек)': times_random}
#     df_random = pd.DataFrame(data_random)
#     print("Випадкові числа:\n", df_random)

#     data_sorted = {'Розмір масиву': sizes, 'Час виконання (сек)': times_sorted}
#     df_sorted = pd.DataFrame(data_sorted)
#     print("\nВпорядковані числа:\n", df_sorted)

#     data_semi_sorted = {'Розмір масиву': sizes, 'Час виконання (сек)': times_semi_sorted}
#     df_semi_sorted = pd.DataFrame(data_semi_sorted)
#     print("\nЧастково впорядковані числа:\n", df_semi_sorted)

#     data_sorted_with_swaps = {'Розмір масиву': sizes, 'Час виконання (сек)': times_sorted_with_swaps}
#     df_sorted_with_swaps = pd.DataFrame(data_sorted_with_swaps)
#     print("\nВпорядковані числа з перестановками:\n", df_sorted_with_swaps)

# generate_data_and_plot()


def visualize_sorting(steps):
    fig, ax = plt.subplots()
    ax.set_title('Gnome Sort Algorithm')
    bar_rects = ax.bar(range(len(steps[0])), steps[0], align='edge')

    def update_fig(iteration, arr, rects):
        for rect, val in zip(rects, arr[iteration]):
            rect.set_height(val)
        # Змінюємо колір стовпця, який відповідає поточному кроку
        if iteration < len(rects):
            rects[iteration].set_color('skyblue')
        if iteration > 0 and iteration-1 < len(rects):
            rects[iteration-1].set_color('purple')

    anim = animation.FuncAnimation(fig, update_fig, frames=range(len(steps)), fargs=(steps, bar_rects), interval=500, repeat=True)
    plt.show()

# Візуалізація сортування
arr = [1, 7, 8, 2, 3, 5, 4, 6]
steps = gnomeSort(arr)
visualize_sorting(steps)