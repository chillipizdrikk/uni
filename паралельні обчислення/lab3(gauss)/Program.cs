using System;
using System.Diagnostics;
using System.Threading;
using System.Collections.Generic;

class Program
{
    // Генерація матриці з випадковими значеннями
    public static double[,] GenerateMatrix(int n, int m)
    {
        double[,] matrix = new double[n, m];
        Random rnd = new Random();
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                matrix[i, j] = rnd.Next(1, 10);  //Уникаємо 0 для стабільності
            }
        }
        return matrix;
    }

    // Перевірка діагоналі на наявність нулів
    public static void CheckZerosOnDiagonal(double[,] matrix)
    {
        for (int i = 0; i < matrix.GetLength(0); i++)
        {
            if (matrix[i, i] == 0) throw new DivideByZeroException();
        }
    }

    // Послідовний метод вирішення
    public static TimeSpan SequentialMethod(double[,] matrix)
    {
        int N = matrix.GetLength(0);

        Stopwatch stopWatch = new Stopwatch();
        stopWatch.Start();

        // Прямий хід
        for (int rowNum = 0; rowNum < N; rowNum++)
        {
            for (int i = rowNum + 1; i < N; i++)
            {
                double factor = matrix[i, rowNum] / matrix[rowNum, rowNum];
                for (int j = rowNum; j <= N; j++)
                {
                    matrix[i, j] -= factor * matrix[rowNum, j];
                }
            }
        }

        CheckZerosOnDiagonal(matrix);

        double[] result = new double[N];

        // Обернений хід
        for (int rowNum = N - 1; rowNum >= 0; rowNum--)
        {
            result[rowNum] = matrix[rowNum, N];
            for (int j = rowNum + 1; j < N; j++)
            {
                result[rowNum] -= matrix[rowNum, j] * result[j];
            }
            result[rowNum] /= matrix[rowNum, rowNum];
        }

        stopWatch.Stop();
        return stopWatch.Elapsed;
    }

    // Паралельний метод вирішення
    public static TimeSpan ParallelMethod(double[,] matrix, int numThreads)
    {
        int N = matrix.GetLength(0);
        Stopwatch stopWatch = new Stopwatch();
        stopWatch.Start();

        List<Thread> threads = new List<Thread>();
        int rowsPerThread = N / numThreads;

        // Прямий хід (паралельний)
        for (int i = 0; i < numThreads; i++)
        {
            int startRow = i * rowsPerThread;
            int endRow = (i == numThreads - 1) ? N : startRow + rowsPerThread;

            Thread thread = new Thread((object range) =>
            {
                int[] rangeArray = (int[])range;
                int startRange = rangeArray[0];
                int endRange = rangeArray[1];

                for (int rowNum = startRange; rowNum < endRange; rowNum++)
                {
                    for (int j = rowNum + 1; j < N; j++)
                    {
                        double factor = matrix[j, rowNum] / matrix[rowNum, rowNum];
                        for (int k = rowNum; k <= N; k++)
                        {
                            matrix[j, k] -= factor * matrix[rowNum, k];
                        }
                    }
                }
            });

            threads.Add(thread);
            thread.Start(new int[] { startRow, endRow });
        }

        foreach (var thread in threads)
        {
            thread.Join();
        }

        CheckZerosOnDiagonal(matrix);

        // Обернений хід (послідовний)
        double[] result = new double[N];
        for (int rowNum = N - 1; rowNum >= 0; rowNum--)
        {
            result[rowNum] = matrix[rowNum, N];
            for (int j = rowNum + 1; j < N; j++)
            {
                result[rowNum] -= matrix[rowNum, j] * result[j];
            }
            result[rowNum] /= matrix[rowNum, rowNum];
        }

        stopWatch.Stop();
        return stopWatch.Elapsed;
    }


    // Метод для форматування часу 
    public static string FormatTimeSpan(TimeSpan time)
    {
        return string.Format("{0:00}:{1:00}:{2:00}:{3:00}",
            time.Hours, time.Minutes, time.Seconds, time.Milliseconds / 10); // Округлення мілісекунд до сотих
    }

    static void Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;

        // Розміри матриць та кількість потоків для тестування
        int[] matrixSizes = {1000, 500, 100};  
        int[] threadCounts = {8, 4, 3, 2};  

        foreach (int size in matrixSizes)
        {
            foreach (int threads in threadCounts)
            {
                Console.WriteLine($"Розмір матриці: {size}");
                Console.WriteLine($"Кількість потоків: {threads}");
                

                double[,] matrix = GenerateMatrix(size, size + 1);

                try
                {
                    TimeSpan sync = SequentialMethod(matrix);
                    TimeSpan async = ParallelMethod(matrix, threads);

                    var acceleration = sync.TotalMilliseconds / async.TotalMilliseconds;
                    var efficiency = acceleration / threads;

                    // Використання нового методу для форматування часу
                    Console.WriteLine($"Послідовний метод Гауса: {FormatTimeSpan(sync)}");
                    Console.WriteLine($"Паралельний метод Гауса: {FormatTimeSpan(async)}");
                    Console.WriteLine($"Прискорення: {acceleration:F2}");
                    Console.WriteLine($"Ефективність: {efficiency:F2}");
                }
                catch (DivideByZeroException)
                {
                    Console.WriteLine("Спроба ділення на нуль.");
                }

                Console.WriteLine();
            }
        }
    }
}
