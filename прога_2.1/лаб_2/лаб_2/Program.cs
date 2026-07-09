using System;
using System.Drawing;

class Program
{
    static void Main()
    {
        //завдання 1
        Console.Write("Завдання №1\n");
        Console.Write("Введіть довжину першого масиву: ");
        int n1 = int.Parse(Console.ReadLine());

        Console.Write("Введіть довжину другого масиву: ");
        int n2 = int.Parse(Console.ReadLine());

        int[] array1 = GenerateRandomArray(n1);
        int[] array2 = GenerateRandomArray(n2);

        Console.WriteLine("Перший масив:");
        PrintArray(array1);

        Console.WriteLine("Другий масив:");
        PrintArray(array2);

        int sum1 = CalculateSum(array1);
        int sum2 = CalculateSum(array2);

        if (sum1 > sum2)
        {
            Console.WriteLine($"Перший масив має більшу суму: {sum1}");
        }
        else if (sum2 > sum1)
        {
            Console.WriteLine($"Другий масив має більшу суму: {sum2}");
        }
        else
        {
            Console.WriteLine("Суми масивів рівні");
        }
    //завдання 2
    Console.Write("\nЗавдання №2\n");

        Console.Write("Введіть кількість точок: ");
        int n = int.Parse(Console.ReadLine());
        //двовимірний масив точок з координатами x і y
        double[,] points = new double[n, 2];

        for (int i = 0; i < n; i++)
        {
            Console.Write($"Введіть координати точки {i + 1} (x y): ");
            string[] input = Console.ReadLine().Split();
            points[i, 0] = double.Parse(input[0]);
            points[i, 1] = double.Parse(input[1]);
        }

        bool isCollinear = CheckCollinearity(points);

        if (isCollinear)
        {
            Console.WriteLine("Точки лежать на одній прямій.");
        }
        else
        {
            Console.WriteLine("Точки не лежать на одній прямій.");
        }

        //завдання 3
        Console.Write("\nЗавдання №3\n");
        int[,] matrix = {
            { 3, 3, 1, 1 },
            { 2, 2, 1, 2 },
            { 1, 1, 1, 2 }
        };

        Console.WriteLine("Початковий масив:");
        PrintMatrix(matrix);

        DiagonalSort(matrix);

        Console.WriteLine("\nВідсортований масив:");
        PrintMatrix(matrix);

        //завдання 4
        Console.Write("\nЗавдання №4\n");
        int[,] queens = {
            { 1, 1 },
            { 1, 2 },
            { 4, 3 },
            { 5, 3 }
        };

        int[] king = { 2, 3 };

        var attackingQueens = FindAttackingQueens(queens, king);

        Console.WriteLine("Ферзі, які можуть напряму атакувати короля:");
        foreach (var queen in attackingQueens)
        {
            Console.WriteLine($"[{queen[0]}, {queen[1]}]");
        }

        //завдання 5
        Console.Write("\nЗавдання №5\n");
        int[,] binaryArray = {
        { 0, 1, 0, 1, 0 },
        { 1, 0, 1, 1, 1 },
        { 0, 1, 0, 0, 0 },
        { 1, 1, 0, 1, 1 },
        { 0, 1, 0, 1, 0 }
        };

        Console.WriteLine("Початкова матриця:");
        PrintMatrix(binaryArray);

        int maxSize = FindLargestConnectedGroup(binaryArray);
        Console.WriteLine($"Розмір найбільшої групи одиниць: {maxSize}");
    }
    //1
    static int[] GenerateRandomArray(int length)
    {
        Random random = new Random();
        int[] array = new int[length];
        for (int i = 0; i < length; i++)
        {
            array[i] = random.Next(1, 11); // Випадкове число від 1 до 10
        }
        return array;
    }
    static int CalculateSum(int[] arr)
    {
        int sum = 0;
        foreach (int element in arr)
        {
            sum += element;
        }
        return sum;
    }

    static void PrintArray(int[] arr)
    {
        foreach (int element in arr)
        {
            Console.Write(element + " ");
        }
        Console.WriteLine();
    }


    //2
    static bool CheckCollinearity(double[,] points)
    {
        //вектор між першою і другою точкою
        double dx1 = points[1, 0] - points[0, 0];
        double dy1 = points[1, 1] - points[0, 1];

        for (int i = 2; i < points.GetLength(0); i++)
        {
            //вектор між першою точкою і поточною точкою
            double dx2 = points[i, 0] - points[0, 0];
            double dy2 = points[i, 1] - points[0, 1];

            //перевірка, чи вектори спрямовані вздовж однієї лінії
            if (dx1 * dy2 != dx2 * dy1)
            {
                return false;
            }
        }

        return true;
    }

    //3
   static void DiagonalSort(int[,] matrix)
   {
       int rows = matrix.GetLength(0);
       int cols = matrix.GetLength(1);
   
       // Сортування верхніх діагоналей (починаючи з верхнього рядка)
       for (int i = 0; i < rows; i++)
       {
           SortDiagonal(matrix, i, 0);
       }
   
       // Сортування нижніх діагоналей (починаючи з першого стовпця)
       for (int j = 1; j < cols; j++)
       {
           SortDiagonal(matrix, 0, j);
       }
   }
   
   static void SortDiagonal(int[,] matrix, int row, int col)
   {
       int len = Math.Min(matrix.GetLength(0) - row, matrix.GetLength(1) - col);
       int[] diagonal = new int[len];
        //заповнюєм масив diagonal елементами з діагоналі
       for (int i = 0; i < len; i++)
       {
           diagonal[i] = matrix[row + i, col + i];
       }
   
       Array.Sort(diagonal);

       //замінюєм елементи діагоналі в масиві matrix відсортованими значеннями.
       for (int i = 0; i < len; i++)
       {
           matrix[row + i, col + i] = diagonal[i];
       }
   }
   static void PrintMatrix(int[,] matrix)
   {
       for (int i = 0; i < matrix.GetLength(0); i++)
       {
           for (int j = 0; j < matrix.GetLength(1); j++)
           {
               Console.Write(matrix[i, j] + " ");
           }
           Console.WriteLine();
       }
   }
    //4
    static bool IsAttacking(int[] queen, int[] king, int[,] queens)
    {
        //перевірка по горизонталі, вертикалі та діагоналі
        return queen[0] == king[0] ||
               queen[1] == king[1] ||
               Math.Abs(queen[0] - king[0]) == Math.Abs(queen[1] - king[1]) ||
               IsBlockedByOtherQueen(queen, king, queens);
    }

    static bool IsBlockedByOtherQueen(int[] queen, int[] king, int[,] queens)
    {
        //перевірка, чи перед ферзем не стоїть інший ферзь
        for (int i = 0; i < queens.GetLength(0); i++)
        {
            if (i != king[0] && i != queen[0] && //перевіряємо ферзя та короля
                queens[i, 1] == queen[1] && //перевіряємо по вертикалі
                Math.Abs(queens[i, 0] - queen[0]) == Math.Abs(queens[i, 1] - queen[1])) //перевіряємо по діагоналі
            {
                return true; //ферзь заблокований
            }
        }
        return false; //не заблокований
    }

    static int[][] FindAttackingQueens(int[,] queens, int[] king)
    {
        var result = new List<int[]>();

        for (int i = 0; i < queens.GetLength(0); i++)
        {
            if (IsAttacking(new int[] { queens[i, 0], queens[i, 1] }, king, queens) &&
                !IsBlockedByOtherQueen(new int[] { queens[i, 0], queens[i, 1] }, king, queens))
            {
                result.Add(new int[] { queens[i, 0], queens[i, 1] });
            }
        }

        return result.ToArray();
    }



    //5
    static int FindLargestConnectedGroup(int[,] binaryArray)
    {
        int rows = binaryArray.GetLength(0);
        int cols = binaryArray.GetLength(1);
        int maxSize = 0;

        //Depth-First Search
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (binaryArray[i, j] == 1)
                {
                    int currentSize = DFS(binaryArray, i, j);
                    maxSize = Math.Max(maxSize, currentSize);
                }
            }
        }

        return maxSize;
    }

    static int DFS(int[,] binaryArray, int i, int j)
    {
        int rows = binaryArray.GetLength(0);
        int cols = binaryArray.GetLength(1);

        if (i < 0 || i >= rows || j < 0 || j >= cols || binaryArray[i, j] == 0)
        {
            return 0;
        }

        //позначаємо відвідану одиницю і продовжуємо DFS.
        binaryArray[i, j] = 0;

        //запускаємо DFS для сусідів.
        int size = 1;
        size += DFS(binaryArray, i - 1, j); // Вгору
        size += DFS(binaryArray, i + 1, j); // Вниз
        size += DFS(binaryArray, i, j - 1); // Вліво
        size += DFS(binaryArray, i, j + 1); // Вправо

        return size;
    }

}
