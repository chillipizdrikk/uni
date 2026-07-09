import random
import time

def quick_sort(arr):
    size = len(arr)
    if size <= 1:
        return arr

    stack = [(0, size - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            pi = partition(arr, low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def smooth_sort(arr):
    n = len(arr)
 
    # Визначаємо числа Леонардо
    def leonardo(k):
        if k < 2:
            return 1
        return leonardo(k - 1) + leonardo(k - 2) + 1
 
    # Будуємо купу Леонардо, об'єднавши пари сусідніх дерев
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
    for i in range(n - 1):
        j = i + 1
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j = j - 1
 
    return arr

def gnome_sort(arr):
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


def generate_random_array(length):
    return [random.randint(1, 1000) for _ in range(length)]

sizes = [10, 100, 1000, 5000, 10000]
print("Час виконання Smooth Sort:")
for size in sizes:
    random_array = generate_random_array(size)
    start_time = time.time()
    smooth_sort(random_array.copy())
    end_time = time.time()
    print(f"Розмір {size}: {end_time - start_time:.5f} сек")

print("\nЧас виконання Gnome Sort:")
for size in sizes:
    random_array = generate_random_array(size)
    start_time = time.time()
    gnome_sort(random_array.copy())
    end_time = time.time()
    print(f"Size {size}: {end_time - start_time:.5f} сек")
# import matplotlib.pyplot as plt
# import timeit
# import random
# import copy

# def generate_random_array(size):
#     return [random.randint(1, 1000) for _ in range(size)]

# def generate_sorted_array(size):
#     return [i for i in range(1, size + 1)]

# def generate_reversed_array(size):
#     return [i for i in range(size, 0, -1)]

# def generate_partial_sorted_array(size, num_segments):
#     segment_size = size // num_segments
#     array = []
#     for i in range(num_segments):
#         segment = [j for j in range(i * segment_size + 1, (i + 1) * segment_size + 1)]
#         array.extend(segment)
#     return array

# def generate_swapped_array(size, num_swaps):
#     array = [i for i in range(1, size + 1)]
#     for _ in range(num_swaps):
#         i, j = random.randint(0, size - 1), random.randint(0, size - 1)
#         array[i], array[j] = array[j], array[i]
#     return array

# def plot_algorithm_performance(algorithm, array_generators, array_sizes, num_trials=5, low=None, high=None):
#     for array_generator_name, array_generator in array_generators.items():
#         x_vals = []
#         y_vals = []
#         for size in array_sizes:
#             times = []
#             for _ in range(num_trials):
#                 array = array_generator(size)
#                 start_time = timeit.default_timer()
#                 if low is None or high is None:
#                     algorithm(copy.deepcopy(array))
#                 else:
#                     algorithm(copy.deepcopy(array), low, high)
#                 end_time = timeit.default_timer()
#                 times.append(end_time - start_time)
#             avg_time = sum(times) / num_trials
#             x_vals.append(size)
#             y_vals.append(avg_time)
#         plt.plot(x_vals, y_vals, label=array_generator_name)

#     plt.xlabel('Середній розмір')
#     plt.ylabel('Cередній час')
#     plt.title('Робота алгоритму на різних видах масивів')
#     plt.legend()
#     plt.show()

# def smooth_sort(arr):
#     n = len(arr)
 
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
 
#     return arr

# def gnome_sort(arr):
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

# # Задаємо типи масивів і їхні генератори
# array_generators = {
#     'Random': generate_random_array,
#     'Sorted': generate_sorted_array,
#     'Reversed': generate_reversed_array,
#     'Partial Sorted': lambda size: generate_partial_sorted_array(size, 5),
#     'Swapped': lambda size: generate_swapped_array(size, size // 10)
# }

# # Задаємо розміри масивів для тестування
# array_sizes = [100, 500, 1000]

# # Побудова графіку для Smooth Sort і Gnome Sort
# plot_algorithm_performance(smooth_sort, array_generators, array_sizes)
# plot_algorithm_performance(gnome_sort, array_generators, array_sizes)
