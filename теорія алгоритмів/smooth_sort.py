import matplotlib.pyplot as plt
import time
import random

def smooth_sort(arr):
    n = len(arr)
 
    # Визначаємо числа Леонардо
    # Точна складність: O(n), асимптотична складність: O(n)
    def leonardo(k):
        if k < 2:
            return 1
        return leonardo(k - 1) + leonardo(k - 2) + 1
 
    # Будуємо купу Леонардо, об'єднавши пари сусідніх дерев
    # Точна складність: O(n^2), асимптотична складність: O(n^2)
    def heapify(start, end):
        i = start
        j = 0
        k = 0
 
        while k < end - start + 1:
            if k % 2 == 0:  
                j = j + i
                i = i // 2 
            else:
                i = i + j
                j = j // 2 
 
            k = k + 1
 
        while i > 0:
            j = j // 2 
            k = i + j
            while k < end:
                if arr[k] > arr[k - i]:
                    break
                arr[k], arr[k - i] = arr[k - i], arr[k]
                k = k + i
 
            i = j
 
    
    p = n - 1
    q = p
    r = 0
    while p > 0:
        if r % 4 == 0:
            heapify(r, q)
 
        if leonardo(r) == p:
            r = r + 1
        else:
            r = r - 1
            q = q - leonardo(r)
            heapify(r, q)
            q = r - 1
            r = r + 1
 
        arr[0], arr[p] = arr[p], arr[0]
        p = p - 1
 
    # Перетворюємо купу Леонардо назад в масив
    # Точна складність: O(n^2), асимптотична складність: O(n^2)
    for i in range(n - 1):
        j = i + 1
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j = j - 1
 
    return arr

def gnomeSort(arr):
    index = 0
    while index < len(arr):
        if index == 0:
            index += 1
        if arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

# Розміри списків, які ми будемо сортувати
sizes = [0, 100, 200, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]

# Часи виконання для кожного розміру списку
smooth_sort_times = []
gnome_sort_times = []

for size in sizes:
    arr = [random.randint(1, 1000) for _ in range(size)]

    start_time = time.time()
    smooth_sort(arr.copy())
    smooth_sort_times.append(time.time() - start_time)

    start_time = time.time()
    gnomeSort(arr.copy())
    gnome_sort_times.append(time.time() - start_time)

# Будуємо графік
plt.plot(sizes, smooth_sort_times, label='Smooth Sort')
plt.plot(sizes, gnome_sort_times, label='Gnome Sort')
plt.xlabel('Розмір списку')
plt.ylabel('Час виконання (секунди)')
plt.legend()
plt.show()



# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import pandas as pd
# import random
# import time

# def smooth_sort(arr):
#     n = len(arr)
 
#     # Визначаємо числа Леонардо
#     # Точна складність: O(n), асимптотична складність: O(n)
#     def leonardo(k):
#         if k < 2:
#             return 1
#         return leonardo(k - 1) + leonardo(k - 2) + 1
 
#     # Будуємо купу Леонардо, об'єднавши пари сусідніх дерев
#     # Точна складність: O(n^2), асимптотична складність: O(n^2)
#     def heapify(start, end):
#         i = start
#         j = 0
#         k = 0
 
#         while k < end - start + 1:
#             if k % 2 == 0:  
#                 j = j + i
#                 i = i // 2 
#             else:
#                 i = i + j
#                 j = j // 2 
 
#             k = k + 1
 
#         while i > 0:
#             j = j // 2 
#             k = i + j
#             while k < end:
#                 if arr[k] > arr[k - i]:
#                     break
#                 arr[k], arr[k - i] = arr[k - i], arr[k]
#                 k = k + i
 
#             i = j
 
    
#     p = n - 1
#     q = p
#     r = 0
#     while p > 0:
#         if r % 4 == 0:
#             heapify(r, q)
 
#         if leonardo(r) == p:
#             r = r + 1
#         else:
#             r = r - 1
#             q = q - leonardo(r)
#             heapify(r, q)
#             q = r - 1
#             r = r + 1
 
#         arr[0], arr[p] = arr[p], arr[0]
#         p = p - 1
 
#     # Перетворюємо купу Леонардо назад в масив
#     # Точна складність: O(n^2), асимптотична складність: O(n^2)
#     for i in range(n - 1):
#         j = i + 1
#         while j > 0 and arr[j] < arr[j - 1]:
#             arr[j], arr[j - 1] = arr[j - 1], arr[j]
#             j = j - 1
 
#     return arr
 
# arr = [1, 7, 8, 2, 3, 5, 4, 6]
 
# print('Input:   ', arr)
# print("Output:  ", smooth_sort(arr))

# def gnomeSort(arr):
#     index = 0
#     while index < len(arr):
#         if index == 0:
#             index += 1
#         if arr[index] >= arr[index - 1]:
#             index += 1
#         else:
#             arr[index], arr[index - 1] = arr[index - 1], arr[index]
#             index -= 1
#     return arr

# # Приклад використання
# arr = [1, 7, 8, 2, 3, 5, 4, 6]
# sorted_arr = gnomeSort(arr)
# print("Відсортована послідовність:", sorted_arr)


# # Розміри списків, які ми будемо сортувати
# sizes = [0, 100, 200, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]

# # Часи виконання для кожного розміру списку
# smooth_sort_times = []
# gnome_sort_times = []

# for size in sizes:
#     arr = sorted([random.randint(1, 1000) for _ in range(size // 2)]) + [random.randint(1, 1000) for _ in range(size // 2)]

#     start_time = time.time()
#     smooth_sort(arr.copy())
#     smooth_sort_times.append(time.time() - start_time)

#     start_time = time.time()
#     gnomeSort(arr.copy())
#     gnome_sort_times.append(time.time() - start_time)

# # Будуємо графік
# plt.plot(sizes, smooth_sort_times, label='Smooth Sort')
# plt.plot(sizes, gnome_sort_times, label='Gnome Sort')
# plt.xlabel('Розмір списку')
# plt.ylabel('Час виконання (секунди)')
# plt.legend()
# plt.show()





# def smooth_sort(arr):
#     n = len(arr)
#     steps = [list(arr)]  # Зберігатиме кроки сортування

#     # Визначаємо числа Леонардо
#     def leonardo(k):
#         if k < 2:
#             return 1
#         return leonardo(k - 1) + leonardo(k - 2) + 1

#     # Будуємо купу Леонардо, об'єднавши пари сусідніх дерев
#     def heapify(start, end):
#         i = start
#         j = 0
#         k = 0

#         while k < end - start + 1:
#             if k % 2 == 0:  
#                 j = j + i
#                 i = i // 2 
#             else:
#                 i = i + j
#                 j = j // 2 

#             k = k + 1

#         while i > 0:
#             j = j // 2 
#             k = i + j
#             while k < end:
#                 if arr[k] > arr[k - i]:
#                     break
#                 arr[k], arr[k - i] = arr[k - i], arr[k]
#                 k = k + i

#             i = j

#         # Додаємо копію масиву після кожного кроку сортування
#         steps.append(arr.copy())

#     p = n - 1
#     q = p
#     r = 0
#     while p > 0:
#         if r % 4 == 0:
#             heapify(r, q)

#         if leonardo(r) == p:
#             r = r + 1
#         else:
#             r = r - 1
#             q = q - leonardo(r)
#             heapify(r, q)
#             q = r - 1
#             r = r + 1

#         arr[0], arr[p] = arr[p], arr[0]
#         p = p - 1

#     # Перетворюємо купу Леонардо назад в масив
#     for i in range(n - 1):
#         j = i + 1
#         while j > 0 and arr[j] < arr[j - 1]:
#             arr[j], arr[j - 1] = arr[j - 1], arr[j]
#             j = j - 1

#     # Додаємо останній відсортований масив
#     steps.append(arr.copy())

#     return steps

# # Приклад використання
# arr = [1, 7, 8, 2, 3, 5, 4, 6]
# steps = smooth_sort(arr)

# # Вивід послідовності масивів на кожному кроці сортування
# for step, step_arr in enumerate(steps):
#     print(f"Step {step + 1}: {step_arr}")




#графік

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
#         smooth_sort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted_with_swaps)
#         end_time = time.time()
#         times_sorted_with_swaps.append(end_time - start_time)

#     # Будуємо графіки
#     plt.plot(sizes, times_random, label='Випадкові числа')
#     plt.plot(sizes, times_sorted, label='Впорядковані числа')
#     plt.plot(sizes, times_semi_sorted, label='Частково впорядковані числа')
#     plt.plot(sizes, times_sorted_with_swaps, label='Впорядковані числа з перестановками')
#     plt.xlabel('Розмір масиву')
#     plt.ylabel('Час виконання (сек)')
#     plt.title('Часова складність алгоритму Smooth Sort')
#     plt.legend()
#     plt.show()

# generate_data_and_plot()




#таблички

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
#         smooth_sort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted_with_swaps)
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
#         smooth_sort(arr_random)
#         end_time = time.time()
#         times_random.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted)
#         end_time = time.time()
#         times_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_semi_sorted)
#         end_time = time.time()
#         times_semi_sorted.append(end_time - start_time)

#         start_time = time.time()
#         smooth_sort(arr_sorted_with_swaps)
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


# def visualize_sorting(steps):
#     fig, ax = plt.subplots()
#     ax.set_title('Smooth Sort Algorithm')
#     bar_rects = ax.bar(range(len(steps[0])), steps[0], align='edge')

#     def update_fig(iteration, arr, rects):
#         for rect, val in zip(rects, arr[iteration]):
#             rect.set_height(val)
#         # Змінюємо колір стовпця, який відповідає поточному кроку
#         if iteration < len(rects):
#             rects[iteration].set_color('skyblue')
#         if iteration > 0 and iteration-1 < len(rects):
#             rects[iteration-1].set_color('purple')

#     anim = animation.FuncAnimation(fig, update_fig, frames=range(len(steps)), fargs=(steps, bar_rects), interval=500, repeat=True)
#     plt.show()

# # Приклад масиву для сортування
# arr = [1, 7, 8, 2, 3, 5, 4, 6]
# steps = smooth_sort(arr)

# # Візуалізація сортування
# visualize_sorting(steps)