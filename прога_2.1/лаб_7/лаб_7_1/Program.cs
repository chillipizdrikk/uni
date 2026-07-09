/*using System;
using System.Collections.Generic;

public static class LinqExtensions
{
    public static double Expectation<T>(this IEnumerable<T> data,
        Func<T, double> valueSelector,
        Func<T, double> probabilitySelector)
    {
        double expectation = 0;
        foreach (var item in data)
        {
            expectation += valueSelector(item) * probabilitySelector(item);
        }
        return expectation;
    }

    public static double StandardDeviation<T>(this IEnumerable<T> data,
        Func<T, double> valueSelector,
        Func<T, double> probabilitySelector)
    {
        double expectation = data.Expectation(valueSelector, probabilitySelector);
        double variance = 0;
        foreach (var item in data)
        {
            variance += Math.Pow(valueSelector(item) - expectation, 2) * probabilitySelector(item);
        }
        return Math.Sqrt(variance);
    }
}

class Program
{
    static void Main(string[] args)
    {
        var data = new List<(double Value, double Probability)>
        {
            (10, 0.2),
            (20, 0.3),
            (30, 0.5)
        };

        double expectation = data.Expectation(item => item.Value, item => item.Probability);
        double standardDeviation = data.StandardDeviation(item => item.Value, item => item.Probability);

        Console.WriteLine($"Математичне сподiвання: {expectation}");
        Console.WriteLine($"Cереднє квадратичне вiдхилення: {standardDeviation}");
    }
}*/








using System;
using System.Collections.Generic;

public static class RandomVariableExtensions
{
    // Власний метод для обчислення суми
    public static double MySum<T>(this IEnumerable<T> source, Func<T, double> selector)
    {
        double sum = 0;
        foreach (var item in source)
        {
            sum += selector(item);
        }
        return sum;
    }

    // Метод розширення для обчислення математичного сподівання
    public static double Mean<T>(this IEnumerable<(T value, double probability)> randomVariable)
        where T : struct, IConvertible
    {
        return randomVariable.MySum(pair => Convert.ToDouble(pair.value) * pair.probability);
    }

    // Метод розширення для обчислення стандартного відхилення
    public static double StandardDeviation<T>(this IEnumerable<(T value, double probability)> randomVariable)
       where T : struct, IConvertible
    {
        double mean = randomVariable.Mean();
        double variance = randomVariable.MySum(pair => Math.Pow(Convert.ToDouble(pair.value) - mean, 2) * pair.probability);
        return Math.Sqrt(variance);
    }
}

class Program
{
    static void Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;

        // Приклад використання
        var discreteRandomVariable = new (int value, double probability)[]
        {
            (1, 0.2),
            (2, 0.3),
            (3, 0.5)
        };

        // Обчислення математичного сподівання
        double mean = discreteRandomVariable.Mean();
        Console.WriteLine("Математичне сподівання: " + mean);

        // Обчислення стандартного відхилення
        double stdDeviation = discreteRandomVariable.StandardDeviation();
        Console.WriteLine("Стандартне відхилення: " + stdDeviation);
    }
}

