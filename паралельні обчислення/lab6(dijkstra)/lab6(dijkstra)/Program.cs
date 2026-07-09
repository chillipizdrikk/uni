using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

class Program
{
    // Генерація випадкового зваженого графа
    public static int[,] GenerateGraph(int numVertices)
    {
        var random = new Random();
        var graph = new int[numVertices, numVertices];
        for (int i = 0; i < numVertices; i++)
        {
            for (int j = 0; j < numVertices; j++)
            {
                graph[i, j] = (i != j && random.NextDouble() < 0.2) ? random.Next(1, 10) : int.MaxValue;
            }
        }
        return graph;
    }

    // Послідовний алгоритм Дейкстри
    public static TimeSpan SequentialDijkstra(int[,] graph, int startNode)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        int[] distances = Dijkstra(graph, startNode);

        stopwatch.Stop();
        return stopwatch.Elapsed;
    }

    public static int[] Dijkstra(int[,] graph, int startNode)
    {
        int numVertices = graph.GetLength(0);
        int[] distances = new int[numVertices];
        bool[] visited = new bool[numVertices];

        Array.Fill(distances, int.MaxValue);
        distances[startNode] = 0;

        for (int count = 0; count < numVertices - 1; count++)
        {
            int u = -1;
            for (int i = 0; i < numVertices; i++)
            {
                if (!visited[i] && (u == -1 || distances[i] < distances[u]))
                    u = i;
            }

            if (distances[u] == int.MaxValue)
                break;

            visited[u] = true;

            for (int v = 0; v < numVertices; v++)
            {
                if (!visited[v] && graph[u, v] != int.MaxValue && distances[u] + graph[u, v] < distances[v])
                {
                    distances[v] = distances[u] + graph[u, v];
                }
            }
        }

        return distances;
    }

    // Паралельний алгоритм Дейкстри
    public static TimeSpan ParallelDijkstra(int[,] graph, int startNode, int numThreads)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        int numVertices = graph.GetLength(0);
        int[] distances = new int[numVertices];
        bool[] visited = new bool[numVertices];
        var threads = new List<Thread>();
        int verticesPerThread = numVertices / numThreads;
        var lockObj = new object();

        Array.Fill(distances, int.MaxValue);
        distances[startNode] = 0;

        for (int i = 0; i < numThreads; i++)
        {
            int start = i * verticesPerThread;
            int end = (i == numThreads - 1) ? numVertices : start + verticesPerThread;

            Thread thread = new Thread(() =>
            {
                for (int count = 0; count < numVertices - 1; count++)
                {
                    int u = -1;

                    lock (lockObj)
                    {
                        for (int i = start; i < end; i++)
                        {
                            if (!visited[i] && (u == -1 || distances[i] < distances[u]))
                                u = i;
                        }

                        if (u == -1 || distances[u] == int.MaxValue)
                            return;

                        visited[u] = true;
                    }

                    for (int v = 0; v < numVertices; v++)
                    {
                        if (!visited[v] && graph[u, v] != int.MaxValue && distances[u] + graph[u, v] < distances[v])
                        {
                            lock (lockObj)
                            {
                                if (distances[u] + graph[u, v] < distances[v])
                                    distances[v] = distances[u] + graph[u, v];
                            }
                        }
                    }
                }
            });

            threads.Add(thread);
            thread.Start();
        }

        foreach (var thread in threads)
        {
            thread.Join();
        }

        stopwatch.Stop();
        return stopwatch.Elapsed;
    }

    // Форматування часу
    public static string FormatTimeSpan(TimeSpan time)
    {
        return string.Format("{0:00}:{1:00}:{2:00}:{3:00}",
            time.Hours, time.Minutes, time.Seconds, time.Milliseconds / 10);
    }


    static void Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;

        // Визначення розмірів графів та кількості потоків для тестування
        int[] graphSizes = { 1000, 1500, 2000, 3000 };  // Розміри графів
        int[] threadCounts = { 2, 4, 8 };  // Кількість потоків
        int startNode = 0; // Вихідна вершина

        foreach (int size in graphSizes)
        {
            foreach (int threads in threadCounts)
            {
                Console.WriteLine($"Розмір графа: {size}, Кількість потоків: {threads}");

                int[,] graph = GenerateGraph(size);

                TimeSpan sequentialTime = SequentialDijkstra(graph, startNode);
                TimeSpan parallelTime = ParallelDijkstra(graph, startNode, threads);

                double acceleration = sequentialTime.TotalMilliseconds / parallelTime.TotalMilliseconds;
                double efficiency = acceleration / threads;

                // Виведення результатів
                Console.WriteLine($"Послідовний алгоритм Дейкстри: {FormatTimeSpan(sequentialTime)}");
                Console.WriteLine($"Паралельний алгоритм Дейкстри: {FormatTimeSpan(parallelTime)}");
                Console.WriteLine($"Прискорення: {acceleration:F2}");
                Console.WriteLine($"Ефективність: {efficiency:F2}");
                Console.WriteLine();
            }
        }
    }
}
