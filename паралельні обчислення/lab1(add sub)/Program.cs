using System;
using System.Diagnostics;
using System.Threading.Tasks;

class MatrixOperations
{
    static void Main(string[] args)
    {
        int n = 5000; // Розмірність матриці
        int m = 5000;
        int k = 4; // Кількість потоків

        double[,] A = GenerateMatrix(n, m);
        double[,] B = GenerateMatrix(n, m);
        double[,] C = new double[n, m];

        // Послідовне додавання
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();
        SequentialAdd(A, B, C, n, m);
        stopwatch.Stop();
        long sequentialAddTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Послідовне додавання: {sequentialAddTime} мс");

        // Паралельне додавання
        stopwatch.Restart();
        ParallelAdd(A, B, C, n, m, k);
        stopwatch.Stop();
        long parallelAddTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Паралельне додавання: {parallelAddTime} мс");

        // Обчислення прискорення та ефективності для додавання
        double addSpeedup = (double)sequentialAddTime / parallelAddTime;
        double addEfficiency = addSpeedup / k;
        Console.WriteLine($"Прискорення (додавання): {addSpeedup}");
        Console.WriteLine($"Ефективність (додавання): {addEfficiency}");

        // Послідовне віднімання
        stopwatch.Restart();
        SequentialSubtract(A, B, C, n, m);
        stopwatch.Stop();
        long sequentialSubtractTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Послідовне віднімання: {sequentialSubtractTime} мс");

        // Паралельне віднімання
        stopwatch.Restart();
        ParallelSubtract(A, B, C, n, m, k);
        stopwatch.Stop();
        long parallelSubtractTime = stopwatch.ElapsedMilliseconds;
        Console.WriteLine($"Паралельне віднімання: {parallelSubtractTime} мс");

        // Обчислення прискорення та ефективності для віднімання
        double subtractSpeedup = (double)sequentialSubtractTime / parallelSubtractTime;
        double subtractEfficiency = subtractSpeedup / k;
        Console.WriteLine($"Прискорення (віднімання): {subtractSpeedup}");
        Console.WriteLine($"Ефективність (віднімання): {subtractEfficiency}");
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

    static void SequentialAdd(double[,] A, double[,] B, double[,] C, int n, int m)
    {
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                C[i, j] = A[i, j] + B[i, j];
            }
        }
    }

    static void ParallelAdd(double[,] A, double[,] B, double[,] C, int n, int m, int k)
    {
        int chunkSize = (n + k - 1) / k; // Розмір частини для кожного потоку
        Parallel.For(0, k, thread =>
        {
            int start = thread * chunkSize;
            int end = Math.Min(start + chunkSize, n);
            for (int i = start; i < end; i++)
            {
                for (int j = 0; j < m; j++)
                {
                    C[i, j] = A[i, j] + B[i, j];
                }
            }
        });
    }

    static void SequentialSubtract(double[,] A, double[,] B, double[,] C, int n, int m)
    {
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                C[i, j] = A[i, j] - B[i, j];
            }
        }
    }

    static void ParallelSubtract(double[,] A, double[,] B, double[,] C, int n, int m, int k)
    {
        int chunkSize = (n + k - 1) / k; // Розмір частини для кожного потоку
        Parallel.For(0, k, thread =>
        {
            int start = thread * chunkSize;
            int end = Math.Min(start + chunkSize, n);
            for (int i = start; i < end; i++)
            {
                for (int j = 0; j < m; j++)
                {
                    C[i, j] = A[i, j] - B[i, j];
                }
            }
        });
    }
}
