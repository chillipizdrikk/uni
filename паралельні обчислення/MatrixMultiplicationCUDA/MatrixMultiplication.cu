#include <iostream>
#include <cuda_runtime.h>

__global__ void matrixMultiplyKernel(double* A, double* B, double* C, int n, int m) {
    // Визначення глобальних індексів для рядка та стовпця
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    // Перевірка меж
    if (row < n && col < n) {
        double value = 0; // Змінна для збереження обчисленого значення
        // Обчислення значення для C[row][col]
        for (int k = 0; k < m; k++) {
            value += A[row * m + k] * B[k * n + col];
        }
        C[row * n + col] = value; // Запис значення в результуючу матрицю
    }
}

void matrixMultiply(double* h_A, double* h_B, double* h_C, int n, int m) {
    double* d_A, * d_B, * d_C;
    size_t size_A = n * m * sizeof(double); // Розмір матриці A
    size_t size_B = m * n * sizeof(double); // Розмір матриці B
    size_t size_C = n * n * sizeof(double); // Розмір матриці C

    // Виділення пам'яті на пристрої
    cudaMalloc((void**)&d_A, size_A);
    cudaMalloc((void**)&d_B, size_B);
    cudaMalloc((void**)&d_C, size_C);

    // Копіювання даних з хоста на пристрій
    cudaMemcpy(d_A, h_A, size_A, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size_B, cudaMemcpyHostToDevice);

    // Визначення розмірів блоків і сіток
    dim3 threadsPerBlock(16, 16); // Кількість потоків у блоці
    dim3 numBlocks((n + threadsPerBlock.x - 1) / threadsPerBlock.x, (n + threadsPerBlock.y - 1) / threadsPerBlock.y);

    // Запуск ядра
    matrixMultiplyKernel << <numBlocks, threadsPerBlock >> > (d_A, d_B, d_C, n, m);

    // Копіювання результату назад на хост
    cudaMemcpy(h_C, d_C, size_C, cudaMemcpyDeviceToHost);

    // Звільнення пам'яті на пристрої
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
}
