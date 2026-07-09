#include <iostream>
#include <chrono>
#include <cstdlib> // Для rand()
#include "MatrixMultiplication.cuh" // Заголовок для функцій CUDA

double* GenerateMatrix(int rows, int cols) {
    double* matrix = new double[rows * cols];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i * cols + j] = static_cast<double>(rand()) / RAND_MAX; // Заповнення випадковими числами
        }
    }
    return matrix;
}

int main() {
    int n = 100; // Розмірність матриці
    int m = 100;

    // Генерація матриць
    double* A = GenerateMatrix(n, m);
    double* B = GenerateMatrix(m, n);
    double* C = new double[n * n];

    // Вимірювання часу множення CUDA
    auto start = std::chrono::high_resolution_clock::now();
    matrixMultiply(A, B, C, n, m);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Час множення CUDA: " << elapsed.count() * 1000 << " мс" << std::endl;

    // Звільнення пам'яті
    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}
