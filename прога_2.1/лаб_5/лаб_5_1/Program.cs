using System;
using System.Collections.Generic;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

public delegate void SortDelegate<T>(IList<T> collection);

public class SortingService
{
    public static void Sort<T>(IList<T> collection, SortDelegate<T> sortAlgorithm)
    {
        sortAlgorithm(collection);
    }
}

public class SortingBenchmarks
{
    private static readonly int[] intArray = new int[] { 5, 2, 9, 1, 5, 6 };
    private static readonly List<int> intList = new List<int> { 5, 2, 9, 1, 5, 6 };

    [Benchmark]
    public void QuickSortBenchmark()
    {
        SortingService.Sort(intArray, QuickSort);
    }

    [Benchmark]
    public void BubbleSortBenchmark()
    {
        SortingService.Sort(intList, BubbleSort);
    }

    // QuickSort
    static void QuickSort<T>(IList<T> collection) where T : IComparable<T>
    {
        QuickSort(collection, 0, collection.Count - 1);
    }

    static void QuickSort<T>(IList<T> collection, int left, int right) where T : IComparable<T>
    {
        if (left < right)
        {
            int partitionIndex = Partition(collection, left, right);

            QuickSort(collection, left, partitionIndex - 1);
            QuickSort(collection, partitionIndex + 1, right);
        }
    }

    static int Partition<T>(IList<T> collection, int left, int right) where T : IComparable<T>
    {
        T pivot = collection[right];
        int i = left - 1;

        for (int j = left; j < right; j++)
        {
            if (collection[j].CompareTo(pivot) <= 0)
            {
                i++;
                Swap(collection, i, j);
            }
        }

        Swap(collection, i + 1, right);
        return i + 1;
    }

    // BubbleSort
    static void BubbleSort<T>(IList<T> collection) where T : IComparable<T>
    {
        bool swapped;
        int n = collection.Count;
        do
        {
            swapped = false;
            for (int i = 0; i < n - 1; i++)
            {
                if (collection[i].CompareTo(collection[i + 1]) > 0)
                {
                    Swap(collection, i, i + 1);
                    swapped = true;
                }
            }
            n--;
        } while (swapped);
    }

    static void Swap<T>(IList<T> collection, int i, int j)
    {
        T temp = collection[i];
        collection[i] = collection[j];
        collection[j] = temp;
    }
}

class Program
{
    static void Main()
    {
        var summary = BenchmarkRunner.Run<SortingBenchmarks>();

        Console.ReadLine(); //щоб консольне вікно не закрилося занадто швидко
    }
}
//dotnet run -c Release