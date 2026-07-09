import random

def generate_matrix(size):
    return [[round(random.uniform(0, 5), 2) for _ in range(size)] for _ in range(size)]

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

def square_matrix(matrix):
    size = len(matrix)
    result = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix[i][k] * matrix[k][j]
                result[i][j] = round(result[i][j], 2)
    return result

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(str(elem) for elem in row)) 
    print('\n')