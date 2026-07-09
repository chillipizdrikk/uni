using System;
using System.Collections.Generic;
using System.Collections.Specialized;

class Program
{
    static void Main(string[] args)
    {
        
        //завдання 1
        Console.WriteLine($"---Завдання № 1---\n");
        int[] arr = { 1, 2, 3, 1, 1, 3, 2 };
        var pairs = FindPairs(arr);
        Console.WriteLine($"Знайдено {pairs.Count} пари");
        foreach (var pair in pairs)
        {
            Console.WriteLine($"Пара з iндексами ({pair.Item1}, {pair.Item2})");
        }
        Console.WriteLine();

        //завдання 2
        Console.WriteLine($"---Завдання № 2---\n");
        Console.Write("Введiть число n: ");
        int n = Convert.ToInt32(Console.ReadLine());
        Console.WriteLine($"{n}-те число Фiбоначчi: {Fibonacci(n)}");
        
        //завдання 3
        Console.WriteLine($"\n---Завдання № 3---\n");
        Console.Write("Введiть число m: ");
        int m = Convert.ToInt32(Console.ReadLine());
        bool isPerfect = IsPerfect(m);
        if (isPerfect)
        {
            Console.WriteLine($"{m} є досконалим числом.");
        }
        else
        {
            Console.WriteLine($"{m} не є досконалим числом.");
        }
        
        //завдання 4
        Console.WriteLine($"\n---Завдання № 4---\n");
        if (args.Length != 2)
        {
            Console.WriteLine("Потрiбно передати два аргументи - двiйковi числа.");
            return;
        }

        string binary1 = args[0];
        string binary2 = args[1];

        //перевірка, чи введені рядки є правильними двійковими числами
        if (!IsBinaryNumber(binary1) || !IsBinaryNumber(binary2))
        {
            Console.WriteLine("Введені рядки не є двійковими числами.");
            return;
        }

        //gереведення двійкових чисел у цілі числа та їх додавання
        int result = Convert.ToInt32(binary1, 2) + Convert.ToInt32(binary2, 2);

        Console.WriteLine($"Результат додавання: {Convert.ToString(result, 2)}");
    }
    
    //завдання 1
    static List<Tuple<int, int>> FindPairs(int[] arr)
    {
        var pairs = new List<Tuple<int, int>>();
        for (int i = 0; i < arr.Length; i++)//перший цикл for проходиться по кожному елементу масиву
        {
            for (int j = i + 1; j < arr.Length; j++)//другий цикл for проходиться по решті елементів масиву, починаючи з наступного після поточного елемента першого циклу
            {
                if (arr[i] == arr[j]) 
                {
                    pairs.Add(new Tuple<int, int>(i, j));
                }
            }
        }
        return pairs;
    }

    //завдання 2
    static int Fibonacci(int n)
    {
        if (n <= 0)
        {
            return 0;
        }
        else if (n == 1)
        {
            return 1;
        }
        else
        {
            int twoPrev = 0;
            int prev = 1;
            int result = 0;

            for (int i = 2; i <= n; i++)
            {
                result = prev + twoPrev;
                twoPrev = prev;
                prev = result;
            }

            return result;
        }
    }
    
    //завдання 3
    static bool IsPerfect(int m)
    {
        int sum = 0;
        for (int i = 1; i < m; i++)
        {
            if (m % i == 0)
            {
                sum += i;
            }
        }
        return sum == m;
    }
    

    //завдання 4
    static bool IsBinaryNumber(string input)
    {
        foreach (char digit in input)
        {
            if (digit != '0' && digit != '1')
            {
                return false;
            }
        }
        return true;
    }
}

