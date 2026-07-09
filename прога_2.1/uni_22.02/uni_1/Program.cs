using System;

class Program
{
    static void Main()
    {
        Console.Write("Введіть кількість рядків: ");
        int n = Convert.ToInt32(Console.ReadLine());

        for (int i = 0; i < n; i++)
        {
            int[] row = new int[i + 1];
            row[0] = 1;
            row[i] = 1;

            for (int j = 1; j < i; j++)
            {
                row[j] = PascalTriangle(i - 1, j - 1) + PascalTriangle(i - 1, j);
            }

            Console.WriteLine(string.Join(" ", row));
        }
    }

    static int PascalTriangle(int n, int k)
    {
        if (k == 0 || k == n)
        {
            return 1;
        }
        else
        {
            return PascalTriangle(n - 1, k - 1) + PascalTriangle(n - 1, k);
        }
    }
}
