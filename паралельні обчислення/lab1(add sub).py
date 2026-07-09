import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count  # Додаємо імпорт cpu_count

def matrix_addition_sequential(A, B):
    start_time = time.time()
    C_sum = A + B
    end_time = time.time()
    elapsed_time = end_time - start_time
    return C_sum, elapsed_time

def matrix_subtraction_sequential(A, B):
    start_time = time.time()
    C_diff = A - B
    end_time = time.time()
    elapsed_time = end_time - start_time
    return C_diff, elapsed_time

def matrix_addition_chunk(A_chunk, B_chunk):
    return A_chunk + B_chunk

def matrix_subtraction_chunk(A_chunk, B_chunk):
    return A_chunk - B_chunk

def matrix_addition_parallel(A, B, k):
    n, m = A.shape
    chunk_size = n // k
    remainder = n % k
    chunks = [(A[i*chunk_size + min(i, remainder):(i+1)*chunk_size + min(i+1, remainder)], 
               B[i*chunk_size + min(i, remainder):(i+1)*chunk_size + min(i+1, remainder)]) for i in range(k)]
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=k) as executor:
        futures_sum = [executor.submit(matrix_addition_chunk, chunk[0], chunk[1]) for chunk in chunks]
        C_sum_chunks = [future.result() for future in as_completed(futures_sum)]
    end_time = time.time()
    
    C_sum = np.vstack(C_sum_chunks)
    elapsed_time = end_time - start_time
    return C_sum, elapsed_time

def matrix_subtraction_parallel(A, B, k):
    n, m = A.shape
    chunk_size = n // k
    remainder = n % k
    chunks = [(A[i*chunk_size + min(i, remainder):(i+1)*chunk_size + min(i+1, remainder)], 
               B[i*chunk_size + min(i, remainder):(i+1)*chunk_size + min(i+1, remainder)]) for i in range(k)]
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=k) as executor:
        futures_diff = [executor.submit(matrix_subtraction_chunk, chunk[0], chunk[1]) for chunk in chunks]
        C_diff_chunks = [future.result() for future in as_completed(futures_diff)]
    end_time = time.time()
    
    C_diff = np.vstack(C_diff_chunks)
    elapsed_time = end_time - start_time
    return C_diff, elapsed_time

if __name__ == '__main__':
    # Приклад використання
    n, m = 1000, 1000  # Розмірність матриць
    A = np.random.rand(n, m)
    B = np.random.rand(n, m)

    # Послідовний алгоритм для суми
    C_sum_seq, sum_seq_time = matrix_addition_sequential(A, B)
    print(f"Послідовний час обчислення суми: {sum_seq_time:.6f} секунд")

    # Послідовний алгоритм для різниці
    C_diff_seq, diff_seq_time = matrix_subtraction_sequential(A, B)
    print(f"Послідовний час обчислення різниці: {diff_seq_time:.6f} секунд")

    # Паралельний алгоритм для суми
    k = min(4, cpu_count())  # Кількість потоків, не більше ніж кількість ядер процесора
    C_sum_par, sum_par_time = matrix_addition_parallel(A, B, k)
    print(f"Паралельний час обчислення суми: {sum_par_time:.6f} секунд")

    # Паралельний алгоритм для різниці
    C_diff_par, diff_par_time = matrix_subtraction_parallel(A, B, k)
    print(f"Паралельний час обчислення різниці: {diff_par_time:.6f} секунд")

    # Обчислення прискорення та ефективності для суми
    sum_speedup = sum_seq_time / sum_par_time
    sum_efficiency = sum_speedup / k
    print(f"Прискорення для суми: {sum_speedup:.2f}")
    print(f"Ефективність для суми: {sum_efficiency:.2f}")

    # Обчислення прискорення та ефективності для різниці
    diff_speedup = diff_seq_time / diff_par_time
    diff_efficiency = diff_speedup / k
    print(f"Прискорення для різниці: {diff_speedup:.2f}")
    print(f"Ефективність для різниці: {diff_efficiency:.2f}")
