using System.Diagnostics;
using System;

namespace FloydAlgorithm
{
    public class FloydAlgorithm
    {
        private int[,] W;
        public const int INF = 99999;
        public int numberOfThreads = 4;

        public FloydAlgorithm(int[,] W)
        {
            this.W = W;
        }

        public void MatrixFloydAlgorithm(bool IsParallel)
        {
            int N = W.GetLength(0);

            if (!IsParallel)
            {
                for (int k = 0; k < N; k++)
                {
                    for (int i = 0; i < N; ++i)
                    {
                        for (int j = 0; j < N; ++j)
                        {
                            if (W[i, k] != INF && W[k, j] != INF)
                            {
                                W[i, j] = Math.Min(W[i, j], W[i, k] + W[k, j]);
                            }
                        }
                    }
                }
            }
            else
            {
                Thread[] threads = new Thread[numberOfThreads];
                int rowsPerThread = N / numberOfThreads;
                int extraRows = N % numberOfThreads;

                for (int threadIndex = 0; threadIndex < numberOfThreads; threadIndex++)
                {
                    int startRow, endRow;
                    if (threadIndex < extraRows)
                    {
                        startRow = threadIndex * (rowsPerThread + 1);
                        endRow = startRow + rowsPerThread + 1;
                    }
                    else
                    {
                        startRow = threadIndex * rowsPerThread + extraRows;
                        endRow = startRow + rowsPerThread;
                    }

                    threads[threadIndex] = new Thread(() =>
                    {
                        for (int k = 0; k < N; k++)
                        {
                            UpdateMatrixInParallel(startRow, endRow, k);
                        }
                    });
                    threads[threadIndex].Start();
                }

                foreach (var thread in threads)
                {
                    if (thread != null)
                    {
                        thread.Join();
                    }
                }
            }
        }

        private void UpdateMatrixInParallel(int startRow, int endRow, int k)
        {
            int N = W.GetLength(0);
            for (int i = startRow; i < endRow; ++i)
            {
                for (int j = 0; j < N; ++j)
                {
                    if (W[i, k] != INF && W[k, j] != INF)
                    {
                        W[i, j] = Math.Min(W[i, j], W[i, k] + W[k, j]);
                    }
                }
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            int[] graphSizes = { 100, 150,300, 500};
            int[] threadCounts = { 2, 4, 8 };

            Console.WriteLine("|Розмір графа\t|Потоки\t\t|Послідовно (мс)\t|Паралельно (мс)\t|Прискорення\t|Ефективність");

            foreach (int size in graphSizes)
            {
                int[,] matrix = GenerateRandomMatrix(size);

                FloydAlgorithm floyd = new FloydAlgorithm((int[,])matrix.Clone());

                var watch = Stopwatch.StartNew();
                floyd.MatrixFloydAlgorithm(false);
                watch.Stop();
                long timeNonParallel = watch.ElapsedMilliseconds;

                foreach (int threads in threadCounts)
                {
                    floyd = new FloydAlgorithm((int[,])matrix.Clone());
                    floyd.numberOfThreads = threads;

                    watch.Restart();
                    floyd.MatrixFloydAlgorithm(true);
                    watch.Stop();
                    long timeParallel = watch.ElapsedMilliseconds;

                    double speedup = (double)timeNonParallel / timeParallel;
                    double efficiency = speedup / threads;

                    Console.WriteLine($"|{size}\t\t|{threads}\t\t|{timeNonParallel}\t\t\t|{timeParallel}\t\t\t|{speedup:F2}\t\t|{efficiency:F2}      ");
                }
            }
        }

        public static int[,] GenerateRandomMatrix(int N, int maxWeight = 10)
        {
            int[,] W = new int[N, N];
            Random rand = new Random();

            for (int i = 0; i < N; i++)
            {
                W[i, i] = 0;
            }

            for (int i = 0; i < N; i++)
            {
                for (int j = 0; j < N; j++)
                {
                    if (i != j)
                    {
                        if (rand.NextDouble() < 0.7)
                        {
                            W[i, j] = rand.Next(1, maxWeight + 1);
                        }
                        else
                        {
                            W[i, j] = FloydAlgorithm.INF;
                        }
                    }
                }
            }

            EnsureGraphConnectivity(W, N);

            return W;
        }

        private static void EnsureGraphConnectivity(int[,] W, int N)
        {
            Random rand = new Random();

            for (int i = 0; i < N; i++)
            {
                bool hasOutgoingEdge = false;
                bool hasIncomingEdge = false;

                for (int j = 0; j < N; j++)
                {
                    if (W[i, j] != FloydAlgorithm.INF && i != j)
                        hasOutgoingEdge = true;
                    if (W[j, i] != FloydAlgorithm.INF && i != j)
                        hasIncomingEdge = true;
                }

                if (!hasOutgoingEdge)
                {
                    int randomTarget = (i + 1) % N;
                    W[i, randomTarget] = rand.Next(1, 11);
                }

                if (!hasIncomingEdge)
                {
                    int randomSource = (i + 1) % N;
                    W[randomSource, i] = rand.Next(1, 11);
                }
            }
        }
    }
}


























//using System;
//using System.Diagnostics;
//using System.Threading;

//class FloydWarshall
//{
//    static void Main(string[] args)
//    {
//        int[] graphSizes = { 100, 500, 1000 }; // Розміри графів
//        int[] threadCounts = { 2, 4, 8 }; // Кількість потоків
//        int startNode = 0; // Вихідна вершина

//        foreach (int size in graphSizes)
//        {
//            int endNode = size - 1; // Кінцева вершина

//            foreach (int k in threadCounts)
//            {
//                Console.WriteLine($"Розмір графа: {size}, Кількість потоків: {k}");

//                // Генерація випадкового графа
//                double[,] graph = GenerateGraph(size);

//                // Послідовне виконання алгоритму Флойда-Варшалла
//                double[,] sequentialResult = (double[,])graph.Clone();
//                Stopwatch stopwatch = new Stopwatch();
//                stopwatch.Start();
//                FloydWarshallSequential(sequentialResult, size);
//                stopwatch.Stop();
//                long sequentialTime = stopwatch.ElapsedMilliseconds;
//                Console.WriteLine($"Послідовне виконання: {sequentialTime} мс");

//                // Паралельне виконання алгоритму Флойда-Варшалла з потоками
//                double[,] parallelResult = (double[,])graph.Clone();
//                stopwatch.Restart();
//                FloydWarshallParallel(parallelResult, size, k);
//                stopwatch.Stop();
//                long parallelTime = stopwatch.ElapsedMilliseconds;
//                Console.WriteLine($"Паралельне виконання (потоки): {parallelTime} мс");

//                // Обчислення прискорення та ефективності
//                double speedup = (double)sequentialTime / parallelTime;
//                double efficiency = speedup / k;
//                Console.WriteLine($"Прискорення: {speedup:F2}");
//                Console.WriteLine($"Ефективність: {efficiency:F2}\n");

//                //// Отримання найкоротшого шляху між вузлами startNode та endNode
//                //double shortestPathSequential = GetShortestPath(sequentialResult, startNode, endNode);
//                //double shortestPathParallel = GetShortestPath(parallelResult, startNode, endNode);
//                //Console.WriteLine($"Найкоротший шлях між вузлами {startNode} та {endNode} (послідовно): {shortestPathSequential}");
//                //Console.WriteLine($"Найкоротший шлях між вузлами {startNode} та {endNode} (паралельно): {shortestPathParallel}");
//                //Console.WriteLine();
//            }
//        }
//    }

//    // Функція для генерації випадкового графа
//    static double[,] GenerateGraph(int n)
//    {
//        Random rand = new Random();
//        double[,] graph = new double[n, n];
//        for (int i = 0; i < n; i++)
//        {
//            for (int j = 0; j < n; j++)
//            {
//                if (i == j)
//                    graph[i, j] = 0;
//                else
//                    graph[i, j] = rand.NextDouble() > 0.2 ? rand.Next(1, 100) : double.MaxValue;
//            }
//        }
//        return graph;
//    }

//    // Послідовне виконання алгоритму Флойда-Варшалла
//    static void FloydWarshallSequential(double[,] graph, int n)
//    {
//        for (int k = 0; k < n; k++)
//        {
//            for (int i = 0; i < n; i++)
//            {
//                for (int j = 0; j < n; j++)
//                {
//                    if (graph[i, k] < double.MaxValue && graph[k, j] < double.MaxValue)
//                    {
//                        graph[i, j] = Math.Min(graph[i, j], graph[i, k] + graph[k, j]);
//                    }
//                }
//            }
//        }
//    }

//    // Паралельне виконання алгоритму Флойда-Варшалла
//    static void FloydWarshallParallel(double[,] graph, int n, int k)
//    {
//        for (int step = 0; step < n; step++)
//        {
//            Parallel.For(0, n, new ParallelOptions { MaxDegreeOfParallelism = k }, i =>
//            {
//                for (int j = 0; j < n; j++)
//                {
//                    if (graph[i, step] < double.MaxValue && graph[step, j] < double.MaxValue)
//                    {
//                        graph[i, j] = Math.Min(graph[i, j], graph[i, step] + graph[step, j]);
//                    }
//                }
//            });
//        }
//    }
