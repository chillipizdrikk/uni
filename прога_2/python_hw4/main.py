from functions import max_sum_submatrix

matrix = [[1, -2, -1, 4],
          [-8, -3, 4, 2],
          [3, 8, 10, -8],
          [-4, -1, 1, 7]]

max_sum, max_submatrix = max_sum_submatrix(matrix)
print("Матриця:")
for row in matrix:
    print(row)
print("Максимальна сума:", max_sum)
print("Підматриця з максимальною сумою:")
for row in max_submatrix:
    print(row)
