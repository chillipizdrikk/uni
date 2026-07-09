# import numpy as np

# def alt_harmonic(n):
#     return sum([(-1)**(i+1) / (2*i-1) for i in range(1, n+1)])

# def set_negative_to_zero(array):
#     copy = np.copy(array)
#     copy[copy < 0] = 0
#     return copy

# def create_block_matrix():
#     A = np.array([[0, 2, 3], [1, 3, 5]])
#     B = np.array([[3, 0, 3], [3, 3, 3], [3, 3, 3]])
#     C = np.array([[-2, 0, 0], [0, 0, -2]])

#     top = np.hstack((A, B))
#     bottom = np.hstack((C, np.zeros((2, 3))))

#     block_matrix = np.vstack((top, bottom))

#     return block_matrix




# def row_stochastic(matrix):
#     row_sums = matrix.sum(axis=1)
#     return matrix / row_sums[:, np.newaxis]

# # Виклик функцій
# print(alt_harmonic(5))
# print(set_negative_to_zero(np.array([-1, 2, -3, 4, -5])))
# print(create_block_matrix())
# print(row_stochastic(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))


import numpy as np

import numpy as np

def create_block_matrix():
    A = np.array([[0, 2, 3], [1, 3, 5],[0, 0, -2]])
    B = np.array([[3, 0, 3], [3, 3, 3], [3, 3, 3]])
    C = np.array([[-2, 0, 0], [0, 0, -2],[0, 0, -2]])
    I = np.eye(3)
    Z = np.zeros((3, 3))

    top = np.hstack((A, Z, I))
    bottom = np.hstack((Z, C, Z))

    block_matrix = np.vstack((top, bottom))

    return block_matrix


print(create_block_matrix())
