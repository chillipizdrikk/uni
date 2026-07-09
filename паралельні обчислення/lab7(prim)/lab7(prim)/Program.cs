using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;

class Program
{
    class Edge
    {
        public int Source { get; }
        public int Destination { get; }
        public int Weight { get; }

        public Edge(int source, int destination, int weight)
        {
            Source = source;
            Destination = destination;
            Weight = weight;
        }
    }

    class Graph
    {
        public int VerticesCount { get; }
        private List<Edge>[] adjacencyList;

        public Graph(int verticesCount)
        {
            VerticesCount = verticesCount;
            adjacencyList = new List<Edge>[verticesCount];
            for (int i = 0; i < verticesCount; i++)
            {
                adjacencyList[i] = new List<Edge>();
            }
        }

        public void AddEdge(int source, int destination, int weight)
        {
            adjacencyList[source].Add(new Edge(source, destination, weight));
            adjacencyList[destination].Add(new Edge(destination, source, weight));
        }

        public List<Edge> GetEdges(int vertex)
        {
            return adjacencyList[vertex];
        }
    }

    static void Main(string[] args)
    {
        int[] vertexCounts = { 200, 500, 1000, 2000 };
        int[] threadCounts = { 2, 4, 8 };

        foreach (int vertexCount in vertexCounts)
        {
            Console.WriteLine($"Vertices: {vertexCount}");
            Graph graph = GenerateGraph(vertexCount);

            // Sequential Execution
            Stopwatch stopwatch = Stopwatch.StartNew();
            PrimSequential(graph, 0);
            stopwatch.Stop();
            long sequentialTime = stopwatch.ElapsedMilliseconds;
            Console.WriteLine($"Sequential Time: {sequentialTime*10} ms");

            foreach (int threadCount in threadCounts)
            {
                // Parallel Execution
                stopwatch.Restart();
                PrimParallel(graph, 0, threadCount);
                stopwatch.Stop();
                long parallelTime = stopwatch.ElapsedMilliseconds;
                Console.WriteLine($"Parallel Time with {threadCount} threads: {parallelTime} ms");

                // Speedup and Efficiency
                double speedup = (double)sequentialTime*10 / parallelTime;
                double efficiency = speedup / threadCount;
                Console.WriteLine($"Speedup: {speedup:F2}");
                Console.WriteLine($"Efficiency: {efficiency:F2}");
            }
            Console.WriteLine();
        }
    }

    static Graph GenerateGraph(int vertexCount)
    {
        Random rnd = new Random();
        Graph graph = new Graph(vertexCount);
        for (int i = 0; i < vertexCount; i++)
        {
            for (int j = i + 1; j < vertexCount; j++)
            {
                graph.AddEdge(i, j, rnd.Next(1, 100));
            }
        }
        return graph;
    }

    static void PrimSequential(Graph graph, int startVertex)
    {
        bool[] inMST = new bool[graph.VerticesCount];
        int[] key = new int[graph.VerticesCount];
        int[] parent = new int[graph.VerticesCount];

        for (int i = 0; i < graph.VerticesCount; i++)
        {
            key[i] = int.MaxValue;
            parent[i] = -1;
        }

        key[startVertex] = 0;

        for (int count = 0; count < graph.VerticesCount - 1; count++)
        {
            int u = MinKey(key, inMST);
            inMST[u] = true;

            foreach (var edge in graph.GetEdges(u))
            {
                int v = edge.Destination;
                if (!inMST[v] && edge.Weight < key[v])
                {
                    key[v] = edge.Weight;
                    parent[v] = u;
                }
            }
        }
    }

    static void PrimParallel(Graph graph, int startVertex, int threadCount)
    {
        bool[] inMST = new bool[graph.VerticesCount];
        int[] key = new int[graph.VerticesCount];
        int[] parent = new int[graph.VerticesCount];
        object lockObj = new object();

        for (int i = 0; i < graph.VerticesCount; i++)
        {
            key[i] = int.MaxValue;
            parent[i] = -1;
        }

        key[startVertex] = 0;

        for (int count = 0; count < graph.VerticesCount - 1; count++)
        {
            int u = MinKey(key, inMST);
            inMST[u] = true;

            var partitioner = Partitioner.Create(graph.GetEdges(u), true);
            Parallel.ForEach(partitioner, new ParallelOptions { MaxDegreeOfParallelism = threadCount }, edge =>
            {
                int v = edge.Destination;
                lock (lockObj)
                {
                    if (!inMST[v] && edge.Weight < key[v])
                    {
                        key[v] = edge.Weight;
                        parent[v] = u;
                    }
                }
            });
        }
    }

    static int MinKey(int[] key, bool[] inMST)
    {
        int min = int.MaxValue, minIndex = -1;
        for (int v = 0; v < key.Length; v++)
        {
            if (!inMST[v] && key[v] < min)
            {
                min = key[v];
                minIndex = v;
            }
        }
        return minIndex;
    }
}
