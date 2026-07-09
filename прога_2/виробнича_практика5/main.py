import numpy as np

def selection_sort(arr, ascending=True):
    for i in range(len(arr)):
        extreme_index = i
        for j in range(i+1, len(arr)):
            if (ascending and arr[j] < arr[extreme_index]) or (not ascending and arr[j] > arr[extreme_index]):
                extreme_index = j
        arr[i], arr[extreme_index] = arr[extreme_index], arr[i]
    return arr

numbers = np.arange(10)
np.random.shuffle(numbers)

print("Numbers from 0 to 9 in random order:", numbers)

sorted_numbers_asc = selection_sort(numbers.copy(), ascending=True)
print("Numbers sorted in ascending order:", sorted_numbers_asc)

sorted_numbers_desc = selection_sort(numbers.copy(), ascending=False)
print("Numbers sorted in descending order:", sorted_numbers_desc)
