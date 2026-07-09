using System;
using System.Diagnostics;
using System.Threading;

class MatrixMultiplication
{
    static void Main(string[] args)
    {
        int n = 500; // Розмірність матриці
        int m = 500;
        int k = 4; // Кількість потоків

        double[,] A = GenerateMatrix(n, m);
        double[,] B = GenerateMatrix(m, n);
        double[,] C = new double[n, n];

        // Послідовне множення
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();
        SequentialMultiply(A, B, C, n, m);
        stopwatch.Stop();
        long sequentialTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Послідовне множення: {sequentialTime} мс");

        // Паралельне множення
        stopwatch.Restart();
        ParallelMultiply(A, B, C, n, m, k);
        stopwatch.Stop();
        long parallelTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Паралельне множення: {parallelTime} мс");

        // Обчислення прискорення та ефективності
        double speedup = (double)sequentialTime / parallelTime;
        double efficiency = speedup / k;
        Console.WriteLine($"Прискорення: {speedup}");
        Console.WriteLine($"Ефективність: {efficiency}");
    }

    static double[,] GenerateMatrix(int rows, int cols)
    {
        Random rand = new Random();
        double[,] matrix = new double[rows, cols];
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                matrix[i, j] = rand.NextDouble();
            }
        }
        return matrix;
    }

    static void SequentialMultiply(double[,] A, double[,] B, double[,] C, int n, int m)
    {
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                C[i, j] = 0;
                for (int l = 0; l < m; l++)
                {
                    C[i, j] += A[i, l] * B[l, j];
                }
            }
        }
    }

    static void ParallelMultiply(double[,] A, double[,] B, double[,] C, int n, int m, int k)
    {
        int chunkSize = (n + k - 1) / k; // К-сть рядків на потік
        Thread[] threads = new Thread[k];

        for (int thread = 0; thread < k; thread++)
        {
            int localThread = thread; 
            threads[localThread] = new Thread(() =>
            {
                int start = localThread * chunkSize;
                int end = Math.Min(start + chunkSize, n);
                for (int i = start; i < end; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        C[i, j] = 0;
                        for (int l = 0; l < m; l++)
                        {
                            C[i, j] += A[i, l] * B[l, j];
                        }
                    }
                }
            });
            threads[localThread].Start();
        }

        // Очікуємо завершення всіх потоків
        foreach (var thread in threads)
        {
            thread.Join();
        }
    }
}
