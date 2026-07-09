using System;
using System.Collections.Generic;
using System.Linq;

public class CollectionWrapper<T>
{
    public IEnumerable<T> collection;

    public CollectionWrapper(IEnumerable<T> collection)
    {
        this.collection = collection;
    }

    public CollectionWrapper<TOutput> Map<TOutput>(Func<T, TOutput> mapFunc)
    {
        return new CollectionWrapper<TOutput>(this.collection.Select(mapFunc));
    }

    public CollectionWrapper<T> Filter(Func<T, bool> filterFunc)
    {
        return new CollectionWrapper<T>(this.collection.Where(filterFunc));
    }

    public TOutput Reduce<TOutput>(Func<TOutput, T, TOutput> reduceFunc, TOutput initialValue)
    {
        return this.collection.Aggregate(initialValue, reduceFunc);
    }

}

public class Program
{
    public static void Main()
    {
        // Створюємо новий об'єкт CollectionWrapper з колекцією чисел
        var numbers = new CollectionWrapper<int>(new List<int> { 1, 2, 3, 4, 5 });

        // Використовуємо метод Map для створення нової колекції, де кожне число помножено на 2
        var doubled = numbers.Map(x => x * 2);
        Console.WriteLine("Map: " + string.Join(", ", doubled.collection));

        // Використовуємо метод Filter для створення нової колекції, що містить лише парні числа
        var even = numbers.Filter(x => x % 2 == 0);
        Console.WriteLine("Filter: " + string.Join(", ", even.collection));

        // Використовуємо метод Reduce для отримання суми всіх чисел в колекції
        var sum = numbers.Reduce((acc, x) => acc + x, 0);
        Console.WriteLine("Reduce: " + sum);
    }
}