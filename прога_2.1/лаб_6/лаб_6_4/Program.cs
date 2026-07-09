using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;
using System;
using System.Collections.Generic;

public class CustomSortedDictionary<TKey, TValue> where TKey : IComparable<TKey>
{
    private class Node
    {
        public TKey Key { get; set; }
        public TValue Value { get; set; }
        public Node Left { get; set; }
        public Node Right { get; set; }
    }

    private Node root;

    public void Add(TKey key, TValue value)
    {
        root = AddRecursive(root, key, value);
    }

    private Node AddRecursive(Node current, TKey key, TValue value)
    {
        if (current == null)
        {
            return new Node { Key = key, Value = value };
        }

        if (key.CompareTo(current.Key) < 0)
        {
            current.Left = AddRecursive(current.Left, key, value);
        }
        else if (key.CompareTo(current.Key) > 0)
        {
            current.Right = AddRecursive(current.Right, key, value);
        }
        else
        {
            throw new ArgumentException("An element with the same key already exists in the dictionary.");
        }

        return current;
    }

    public bool ContainsKey(TKey key)
    {
        return FindNode(root, key) != null;
    }

    private Node FindNode(Node current, TKey key)
    {
        if (current == null)
        {
            return null;
        }

        if (key.CompareTo(current.Key) < 0)
        {
            return FindNode(current.Left, key);
        }
        else if (key.CompareTo(current.Key) > 0)
        {
            return FindNode(current.Right, key);
        }
        else
        {
            return current;
        }
    }

    public TValue this[TKey key]
    {
        get
        {
            Node node = FindNode(root, key);
            if (node == null)
            {
                throw new KeyNotFoundException();
            }
            return node.Value;
        }
    }

    public void Remove(TKey key)
    {
        root = RemoveRecursive(root, key);
    }

    private Node RemoveRecursive(Node current, TKey key)
    {
        if (current == null)
        {
            return null;
        }

        if (key.CompareTo(current.Key) < 0)
        {
            current.Left = RemoveRecursive(current.Left, key);
        }
        else if (key.CompareTo(current.Key) > 0)
        {
            current.Right = RemoveRecursive(current.Right, key);
        }
        else
        {
            if (current.Left == null)
            {
                return current.Right;
            }
            else if (current.Right == null)
            {
                return current.Left;
            }

            Node minRight = FindMin(current.Right);
            current.Key = minRight.Key;
            current.Value = minRight.Value;
            current.Right = RemoveRecursive(current.Right, minRight.Key);
        }

        return current;
    }

    private Node FindMin(Node node)
    {
        while (node.Left != null)
        {
            node = node.Left;
        }
        return node;
    }
}

public class Benchmark
{
    private readonly SortedDictionary<int, int> systemDictionary = new SortedDictionary<int, int>();
    private readonly CustomSortedDictionary<int, int> customDictionary = new CustomSortedDictionary<int, int>();

    [Benchmark]
    public void Add_SystemDictionary()
    {
        systemDictionary.Add(1, 1);
    }

    [Benchmark]
    public void Add_CustomDictionary()
    {
        customDictionary.Add(1, 1);
    }

    [Benchmark]
    public void Remove_SystemDictionary()
    {
        systemDictionary.Remove(1);
    }

    [Benchmark]
    public void Remove_CustomDictionary()
    {
        customDictionary.Remove(1);
    }

    [Benchmark]
    public void ContainsKey_SystemDictionary()
    {
        systemDictionary.ContainsKey(1);
    }

    [Benchmark]
    public void ContainsKey_CustomDictionary()
    {
        customDictionary.ContainsKey(1);
    }

    [Benchmark]
    public void Indexer_SystemDictionary()
    {
        int value = systemDictionary[1];
    }

    [Benchmark]
    public void Indexer_CustomDictionary()
    {
        int value = customDictionary[1];
    }
}

class Program
{
    static void Main()
    {
        // Створюємо новий екземпляр CustomSortedDictionary
        /*var customDictionary = new CustomSortedDictionary<int, string>();

        // Додаємо елементи в словник
        customDictionary.Add(1, "One");
        customDictionary.Add(2, "Two");
        customDictionary.Add(3, "Three");

        // Виводимо значення за ключем
        Console.WriteLine($"Key 1: {customDictionary[1]}");
        Console.WriteLine($"Key 2: {customDictionary[2]}");
        Console.WriteLine($"Key 3: {customDictionary[3]}");

        // Перевіряємо, чи містить словник ключ
        Console.WriteLine($"Contains key 2: {customDictionary.ContainsKey(2)}");

        // Видаляємо елемент зі словника
        customDictionary.Remove(2);

        // Перевіряємо, чи містить словник ключ після видалення
        Console.WriteLine($"Contains key 2 after removal: {customDictionary.ContainsKey(2)}");*/
        var summary = BenchmarkRunner.Run<Benchmark>();
    }
}
