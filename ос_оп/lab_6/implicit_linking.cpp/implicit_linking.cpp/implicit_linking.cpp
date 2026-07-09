#include <windows.h>
#include <iostream>
#include <iomanip>

// Підключення бібліотеки через файл імпорту
#pragma comment(lib, "Lab5_DLL1.lib")

// Оголошення прототипів функцій DLL
extern "C" INT    CountAboveThresholdWin(INT* arr, INT size, INT threshold);
extern "C" double AverageOfPositiveWin(double* arr, INT size);
extern "C" BOOL   IsArithmeticProgressionWin(double a, double b, double c);
extern "C" CHAR   ToUpperCharWin(CHAR ch);
extern "C" INT    CountWordsStartingWithLetterWin(LPSTR text, CHAR letter);

// Допоміжна функція для виводу масиву INT
void printIntArr(const char* label, INT* arr, INT size) {
    std::cout << label << ": [";
    for (INT i = 0; i < size; i++) {
        std::cout << arr[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

// Допоміжна функція для виводу масиву double
void printDblArr(const char* label, double* arr, INT size) {
    std::cout << label << ": [";
    for (INT i = 0; i < size; i++) {
        std::cout << arr[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

int main() {
    SetConsoleOutputCP(1251); // Підтримка кирилиці у консолі (Windows)
    std::cout << "====================================================\n";
    std::cout << "  Тест DLL - НЕЯВНЕ зв'язування (implicit linking)  \n";
    std::cout << "====================================================\n\n";

    // 1. CountAboveThresholdWin
    std::cout << "--- 1. CountAboveThresholdWin ---\n";

    // Тест 1а: кілька елементів вище порогу
    INT arr1[] = { 3, 7, 1, 9, 4, 12, 2, 8 };
    INT size1 = 8, thr1 = 5;
    printIntArr("Масив", arr1, size1);
    std::cout << "Поріг: " << thr1 << "\n";
    INT res1 = CountAboveThresholdWin(arr1, size1, thr1);
    std::cout << "Кількість елементів > " << thr1 << ": " << res1
        << "  (очікується: 4)\n\n";

    // Тест 1б: жоден елемент не вище порогу
    INT arr1b[] = { 1, 2, 3 };
    INT res1b = CountAboveThresholdWin(arr1b, 3, 10);
    printIntArr("Масив", arr1b, 3);
    std::cout << "Поріг: 10\n";
    std::cout << "Кількість елементів > 10: " << res1b
        << "  (очікується: 0)\n\n";

    // Тест 1в: всі елементи вище порогу, від'ємний поріг
    INT arr1c[] = { -1, -2, -3 };
    INT res1c = CountAboveThresholdWin(arr1c, 3, -5);
    printIntArr("Масив", arr1c, 3);
    std::cout << "Поріг: -5\n";
    std::cout << "Кількість елементів > -5: " << res1c
        << "  (очікується: 3)\n\n";

    // 2. AverageOfPositiveWin
    std::cout << "--- 2. AverageOfPositiveWin ---\n";

    // Тест 2а: є позитивні та від'ємні
    double arr2[] = { -3.0, 5.0, -1.5, 4.0, 0.0, 2.5 };
    printDblArr("Масив", arr2, 6);
    double res2 = AverageOfPositiveWin(arr2, 6);
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Середнє позитивних: " << res2
        << "  (очікується: " << (5.0 + 4.0 + 2.5) / 3.0 << ")\n\n";

    // Тест 2б: немає позитивних (має повернути 0)
    double arr2b[] = { -1.0, -2.0, 0.0 };
    printDblArr("Масив", arr2b, 3);
    double res2b = AverageOfPositiveWin(arr2b, 3);
    std::cout << "Середнє позитивних: " << res2b
        << "  (очікується: 0.0000)\n\n";

    // Тест 2в: всі позитивні
    double arr2c[] = { 1.0, 3.0, 5.0, 7.0 };
    printDblArr("Масив", arr2c, 4);
    double res2c = AverageOfPositiveWin(arr2c, 4);
    std::cout << "Середнє позитивних: " << res2c
        << "  (очікується: 4.0000)\n\n";

    // 3. IsArithmeticProgressionWin
    std::cout << "--- 3. IsArithmeticProgressionWin ---\n";

    // Тест 3а: є арифметична прогресія (d=2)
    std::cout << "(2, 4, 6): "
        << (IsArithmeticProgressionWin(2.0, 4.0, 6.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n";

    // Тест 3б: є арифметична прогресія з від'ємним кроком (d=-3)
    std::cout << "(9, 6, 3): "
        << (IsArithmeticProgressionWin(9.0, 6.0, 3.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n";

    // Тест 3в: не є арифметична прогресія
    std::cout << "(1, 2, 4): "
        << (IsArithmeticProgressionWin(1.0, 2.0, 4.0) ? "TRUE" : "FALSE")
        << "  (очікується: FALSE)\n";

    // Тест 3г: крок 0 (всі рівні)
    std::cout << "(5, 5, 5): "
        << (IsArithmeticProgressionWin(5.0, 5.0, 5.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n\n";

    // 4. ToUpperCharWin
    std::cout << "--- 4. ToUpperCharWin ---\n";

    const char testChars[] = { 'a', 'z', 'm', 'A', 'Z', '5', ' ' };
    const char* expected[] = { "A", "Z", "M", "A", "Z", "5", " " };
    for (int i = 0; i < 7; i++) {
        CHAR res = ToUpperCharWin(testChars[i]);
        std::cout << "ToUpperCharWin('" << testChars[i] << "') = '"
            << res << "'  (очікується: '" << expected[i] << "')\n";
    }
    std::cout << "\n";

    // 5. CountWordsStartingWithLetterWin
    std::cout << "--- 5. CountWordsStartingWithLetterWin ---\n";

    // Тест 5а: звичайне речення, пошук 'b' / 'B'
    char text1[] = "bear Big ball run Boy best";
    std::cout << "Текст: \"" << text1 << "\"\n";
    INT res5a = CountWordsStartingWithLetterWin(text1, 'b');
    std::cout << "Слів на 'b'/'B': " << res5a
        << "  (очікується: 5)\n\n";

    // Тест 5б: пошук великої літери 'S'
    char text2[] = "Sun sets slowly Sometimes sky shines";
    std::cout << "Текст: \"" << text2 << "\"\n";
    INT res5b = CountWordsStartingWithLetterWin(text2, 'S');
    std::cout << "Слів на 's'/'S': " << res5b
        << "  (очікується: 6)\n\n";

    // Тест 5в: жодного збігу
    char text3[] = "hello world";
    std::cout << "Текст: \"" << text3 << "\"\n";
    INT res5c = CountWordsStartingWithLetterWin(text3, 'z');
    std::cout << "Слів на 'z': " << res5c
        << "  (очікується: 0)\n\n";

    std::cout << "====================================================\n";
    std::cout << "  Тестування завершено успішно!\n";
    std::cout << "====================================================\n";

    system("pause");
    return 0;
}