from functions import generate_matrix, trace, print_matrix, square_matrix

matrix1 = generate_matrix(3)
matrix2 = generate_matrix(3)

trace1 = trace(matrix1)
trace2 = trace(matrix2)

print("Матриця 1:")
print_matrix(matrix1)

print("Матриця 2:")
print_matrix(matrix2)

if trace1 < trace2:
    print("Слід матриці 1 є меншим, отже ось її квадрат::")
    print_matrix(square_matrix(matrix1))
elif trace1 > trace2:
    print("Слід матриці 2 є меншим, отже ось її квадрат:")
    print_matrix(square_matrix(matrix2))
else:
    print("Сліди матриць є однаковими")
