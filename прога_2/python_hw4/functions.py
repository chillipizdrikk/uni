def max_sum_submatrix(matrix):
    if not matrix:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    max_sum = float('-inf')
    max_submatrix = None

    for row_start in range(rows):
        for row_end in range(row_start, rows):
            for col_start in range(cols):
                for col_end in range(col_start, cols):
                    current_sum = sum(matrix[i][j] for i in range(row_start, row_end+1) 
                                                   for j in range(col_start, col_end+1))
                    if current_sum > max_sum:
                        max_sum = current_sum
                        max_submatrix = [row[col_start:col_end+1] for row in matrix[row_start:row_end+1]]

    return max_sum, max_submatrix

