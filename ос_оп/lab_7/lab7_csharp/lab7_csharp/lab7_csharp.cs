using System;
using System.IO;
using System.Runtime.InteropServices;

class Lab7_CSharp
{
    // ============================================================
    //  Явне завантаження DLL через WinAPI (щоб вказати шлях)
    // ============================================================

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    private static extern IntPtr LoadLibrary(string lpFileName);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool FreeLibrary(IntPtr hModule);

    [DllImport("kernel32.dll", CharSet = CharSet.Ansi)]
    private static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    // ============================================================
    //  Делегати — сигнатури функцій DLL
    // ============================================================

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    delegate int CountAboveThresholdDelegate(int[] arr, int size, int threshold);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    delegate double AverageOfPositiveDelegate(double[] arr, int size);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    delegate bool IsArithmeticProgressionDelegate(double a, double b, double c);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    delegate byte ToUpperCharDelegate(byte ch);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    delegate int CountWordsStartingWithLetterDelegate(
        [MarshalAs(UnmanagedType.LPStr)] string text, byte letter);

    // ============================================================
    //  Допоміжний метод — отримати делегат із DLL
    // ============================================================

    static T GetFunction<T>(IntPtr hLib, string name) where T : Delegate
    {
        IntPtr ptr = GetProcAddress(hLib, name);
        if (ptr == IntPtr.Zero)
            throw new Exception($"[Помилка] Функцію '{name}' не знайдено у DLL.");
        return Marshal.GetDelegateForFunctionPointer<T>(ptr);
    }

    // ============================================================
    //  Допоміжні методи виведення масивів
    // ============================================================

    static void PrintIntArr(string label, int[] arr)
    {
        Console.Write($"{label}: [");
        for (int i = 0; i < arr.Length; i++)
        {
            Console.Write(arr[i]);
            if (i < arr.Length - 1) Console.Write(", ");
        }
        Console.WriteLine("]");
    }

    static void PrintDblArr(string label, double[] arr)
    {
        Console.Write($"{label}: [");
        for (int i = 0; i < arr.Length; i++)
        {
            Console.Write(arr[i]);
            if (i < arr.Length - 1) Console.Write(", ");
        }
        Console.WriteLine("]");
    }

    // ============================================================
    //  Main
    // ============================================================

    static void Main()
    {
        // Шлях до DLL: шукаємо поруч з .exe
        string dllPath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory, "Lab5_DLL1.dll");

        Console.WriteLine("====================================================");
        Console.WriteLine("  Тест DLL - мова C# (явне завантаження через WinAPI)");
        Console.WriteLine("====================================================");
        Console.WriteLine($"Шлях до DLL: {dllPath}");
        Console.WriteLine();

        IntPtr hLib = LoadLibrary(dllPath);
        if (hLib == IntPtr.Zero)
        {
            int err = Marshal.GetLastWin32Error();
            Console.Error.WriteLine($"[Помилка] Не вдалося завантажити Lab5_DLL1.dll");
            Console.Error.WriteLine($"Код помилки Win32: {err}");
            Console.Error.WriteLine($"Переконайтесь, що файл існує: {dllPath}");
            Console.ReadKey();
            return;
        }
        Console.WriteLine("[OK] Lab5_DLL1.dll успішно завантажено.\n");

        try
        {
            // Отримуємо покажчики на функції
            var CountAbove = GetFunction<CountAboveThresholdDelegate>(hLib, "CountAboveThresholdWin");
            var AvgPositive = GetFunction<AverageOfPositiveDelegate>(hLib, "AverageOfPositiveWin");
            var IsAP = GetFunction<IsArithmeticProgressionDelegate>(hLib, "IsArithmeticProgressionWin");
            var ToUpper = GetFunction<ToUpperCharDelegate>(hLib, "ToUpperCharWin");
            var CountWords = GetFunction<CountWordsStartingWithLetterDelegate>(hLib, "CountWordsStartingWithLetterWin");

            Console.WriteLine("[OK] Всі функції знайдено у DLL.\n");

            // --- 1. CountAboveThresholdWin ---
            Console.WriteLine("--- 1. CountAboveThresholdWin ---");

            int[] arr1a = { 3, 7, 1, 9, 4, 12, 2, 8 };
            PrintIntArr("Масив", arr1a);
            Console.WriteLine("Поріг: 5");
            Console.WriteLine($"Кількість елементів > 5: {CountAbove(arr1a, arr1a.Length, 5)}  (очікується: 4)\n");

            int[] arr1b = { 1, 2, 3 };
            PrintIntArr("Масив", arr1b);
            Console.WriteLine("Поріг: 10");
            Console.WriteLine($"Кількість елементів > 10: {CountAbove(arr1b, arr1b.Length, 10)}  (очікується: 0)\n");

            int[] arr1c = { -1, -2, -3 };
            PrintIntArr("Масив", arr1c);
            Console.WriteLine("Поріг: -5");
            Console.WriteLine($"Кількість елементів > -5: {CountAbove(arr1c, arr1c.Length, -5)}  (очікується: 3)\n");

            // --- 2. AverageOfPositiveWin ---
            Console.WriteLine("--- 2. AverageOfPositiveWin ---");

            double[] arr2a = { -3.0, 5.0, -1.5, 4.0, 0.0, 2.5 };
            PrintDblArr("Масив", arr2a);
            Console.WriteLine($"Середнє додатних: {AvgPositive(arr2a, arr2a.Length):F4}  (очікується: {(5.0 + 4.0 + 2.5) / 3.0:F4})\n");

            double[] arr2b = { -1.0, -2.0, 0.0 };
            PrintDblArr("Масив", arr2b);
            Console.WriteLine($"Середнє додатних: {AvgPositive(arr2b, arr2b.Length):F4}  (очікується: 0.0000)\n");

            double[] arr2c = { 1.0, 3.0, 5.0, 7.0 };
            PrintDblArr("Масив", arr2c);
            Console.WriteLine($"Середнє додатних: {AvgPositive(arr2c, arr2c.Length):F4}  (очікується: 4.0000)\n");

            // --- 3. IsArithmeticProgressionWin ---
            Console.WriteLine("--- 3. IsArithmeticProgressionWin ---");
            Console.WriteLine($"(2, 4, 6): {(IsAP(2, 4, 6) ? "TRUE" : "FALSE")}  (очікується: TRUE)");
            Console.WriteLine($"(9, 6, 3): {(IsAP(9, 6, 3) ? "TRUE" : "FALSE")}  (очікується: TRUE)");
            Console.WriteLine($"(1, 2, 4): {(IsAP(1, 2, 4) ? "TRUE" : "FALSE")}  (очікується: FALSE)");
            Console.WriteLine($"(5, 5, 5): {(IsAP(5, 5, 5) ? "TRUE" : "FALSE")}  (очікується: TRUE)\n");

            // --- 4. ToUpperCharWin ---
            Console.WriteLine("--- 4. ToUpperCharWin ---");
            var testChars = new (char ch, char exp)[]
            {
                ('a','A'), ('z','Z'), ('m','M'), ('A','A'),
                ('Z','Z'), ('5','5'), (' ',' ')
            };
            foreach (var (ch, exp) in testChars)
            {
                char res = (char)ToUpper((byte)ch);
                Console.WriteLine($"ToUpperCharWin('{ch}') = '{res}'  (очікується: '{exp}')");
            }
            Console.WriteLine();

            // --- 5. CountWordsStartingWithLetterWin ---
            Console.WriteLine("--- 5. CountWordsStartingWithLetterWin ---");

            string text1 = "bear Big ball run Boy best";
            Console.WriteLine($"Рядок: \"{text1}\"");
            Console.WriteLine($"Слів на 'b'/'B': {CountWords(text1, (byte)'b')}  (очікується: 5)\n");

            string text2 = "Sun sets slowly Sometimes sky shines";
            Console.WriteLine($"Рядок: \"{text2}\"");
            Console.WriteLine($"Слів на 's'/'S': {CountWords(text2, (byte)'S')}  (очікується: 6)\n");

            string text3 = "hello world";
            Console.WriteLine($"Рядок: \"{text3}\"");
            Console.WriteLine($"Слів на 'z': {CountWords(text3, (byte)'z')}  (очікується: 0)\n");

            Console.WriteLine("====================================================");
            Console.WriteLine("  Всі функції DLL викликано успішно!");
            Console.WriteLine("====================================================");
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"[Виняток] {ex.Message}");
        }
        finally
        {
            FreeLibrary(hLib);
            Console.WriteLine("\n[OK] DLL вивантажено (FreeLibrary).");
        }

        Console.ReadKey();
    }
}