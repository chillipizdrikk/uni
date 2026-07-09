using System;

class Vector
{
    private int[] array; // Поле для зберігання масиву цілих чисел

    // Конструктор за замовчуванням
    public Vector()
    {
        // Ініціалізуємо масив замовчуваними значеннями (наприклад, нулями)
        array = new int[0];
    }

    // Конструктор із параметром, що задає початковий розмір масиву
    public Vector(int initialSize)
    {
        if (initialSize < 0)
        {
            throw new ArgumentException("Початковий розмір масиву повинен бути не менше нуля.");
        }

        // Ініціалізуємо масив заданим розміром
        array = new int[initialSize];
    }

    // Метод для виведення елементів масиву
    public void PrintArray()
    {
        Console.Write("Масив: ");
        foreach (int element in array)
        {
            Console.Write(element + " ");
        }
        Console.WriteLine();
    }

    // Метод Add для додавання нового елементу в кінець списку
    public void Add(int value)
    {
        Array.Resize(ref array, array.Length + 1);
        array[array.Length - 1] = value;
    }

    // Метод Remove для видалення елементу із певної позиції в списку
    public void Remove(int index)
    {
        if (index < 0 || index >= array.Length)
        {
            throw new IndexOutOfRangeException("Неприпустимий індекс для видалення.");
        }

        for (int i = index; i < array.Length - 1; i++)
        {
            array[i] = array[i + 1];
        }

        Array.Resize(ref array, array.Length - 1);
    }

    // Метод Insert для вставки елементу на певну позицію в списку
    public void Insert(int index, int value)
    {
        if (index < 0 || index > array.Length)
        {
            throw new IndexOutOfRangeException("Неприпустимий індекс для вставки.");
        }

        Array.Resize(ref array, array.Length + 1);

        for (int i = array.Length - 1; i > index; i--)
        {
            array[i] = array[i - 1];
        }

        array[index] = value;
    }

    // Індексатор для доступу до певного елемента списку
    public int this[int index]
    {
        get
        {
            if (index < 0 || index >= array.Length)
            {
                throw new IndexOutOfRangeException("Неприпустимий індекс доступу.");
            }

            return array[index];
        }
        set
        {
            if (index < 0 || index >= array.Length)
            {
                throw new IndexOutOfRangeException("Неприпустимий індекс доступу.");
            }

            array[index] = value;
        }
    }

    // Головний метод (entry point) програми
    public static void Main()
    {
        Console.WriteLine("Завдання №1: ");
        // Створення об'єкта Vector
        Vector myVector = new Vector();

        // Задання розміру масиву
        Console.Write("Введiть розмiр масиву: ");
        int size = int.Parse(Console.ReadLine());

        // Ініціалізація масиву
        for (int i = 0; i < size; i++)
        {
            Console.Write($"Введiть елемент з iндексом {i}: ");
            int element = int.Parse(Console.ReadLine());
            myVector.Add(element);
        }

        // Виведення початкового стану масиву
        myVector.PrintArray();

        // Додавання елементу
        Console.Write("Введiть елемент для додавання: ");
        int valueToAdd = int.Parse(Console.ReadLine());
        myVector.Add(valueToAdd);

        // Виведення масиву після додавання
        myVector.PrintArray();

        // Вилучення елементу
        Console.Write("Введiть iндекс елементу для вилучення: ");
        int indexToRemove = int.Parse(Console.ReadLine());
        myVector.Remove(indexToRemove);

        // Виведення масиву після вилучення
        myVector.PrintArray();

        // Вставка елементу
        Console.Write("Введiть iндекс для вставки елементу: ");
        int indexToInsert = int.Parse(Console.ReadLine());
        Console.Write("Введiть значення для вставки: ");
        int valueToInsert = int.Parse(Console.ReadLine());
        myVector.Insert(indexToInsert, valueToInsert);

        // Виведення масиву після вставки
        myVector.PrintArray();

        // Доступ до елемента з певним індексом
        Console.Write("Введiть iндекс для доступу: ");
        int indexToAccess = int.Parse(Console.ReadLine());
        Console.WriteLine($"Елемент з iндексом {indexToAccess}: {myVector[indexToAccess]}");
    }
}
