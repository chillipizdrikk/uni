#include <windows.h>
#include <iostream>
#include <iomanip>

// Оголошення типів вказівників на функції DLL
typedef INT(*PFN_CountAboveThreshold)(INT*, INT, INT);
typedef double (*PFN_AverageOfPositive)(double*, INT);
typedef BOOL(*PFN_IsArithmeticProgression)(double, double, double);
typedef CHAR(*PFN_ToUpperChar)(CHAR);
typedef INT(*PFN_CountWordsStartingWithLetter)(LPSTR, CHAR);

// Допоміжні функції виводу масивів
void printIntArr(const char* label, INT* arr, INT size) {
    std::cout << label << ": [";
    for (INT i = 0; i < size; i++) {
        std::cout << arr[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

void printDblArr(const char* label, double* arr, INT size) {
    std::cout << label << ": [";
    for (INT i = 0; i < size; i++) {
        std::cout << arr[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

int main() {
    SetConsoleOutputCP(1251);

    std::cout << "====================================================\n";
    std::cout << "  Тест DLL - ЯВНЕ зв'язування (explicit linking)    \n";
    std::cout << "====================================================\n\n";
    
    // Крок 1: Завантаження бібліотеки
    const TCHAR* dllPath = TEXT("Lab5_DLL1.dll");
    HMODULE hLib = LoadLibrary(dllPath);

    if (hLib == NULL) {
        std::cerr << "[ПОМИЛКА] Не вдалося завантажити бібліотеку Lab5_DLL1.dll\n";
        std::cerr << "Код помилки: " << GetLastError() << "\n";
        std::cerr << "Переконайтесь, що Lab5_DLL1.dll знаходиться поруч з EXE.\n";
        system("pause");
        return 1;
    }
    std::cout << "[OK] Бібліотека Lab5_DLL1.dll успішно завантажена.\n\n";

    // Крок 2: Отримання вказівників на функції
    PFN_CountAboveThreshold        pCountAbove =
        (PFN_CountAboveThreshold)GetProcAddress(hLib, "CountAboveThresholdWin");

    PFN_AverageOfPositive          pAvgPositive =
        (PFN_AverageOfPositive)GetProcAddress(hLib, "AverageOfPositiveWin");

    PFN_IsArithmeticProgression    pIsAP =
        (PFN_IsArithmeticProgression)GetProcAddress(hLib, "IsArithmeticProgressionWin");

    PFN_ToUpperChar                pToUpper =
        (PFN_ToUpperChar)GetProcAddress(hLib, "ToUpperCharWin");

    PFN_CountWordsStartingWithLetter pCountWords =
        (PFN_CountWordsStartingWithLetter)GetProcAddress(hLib, "CountWordsStartingWithLetterWin");

    // Перевірка наявності кожної функції
    bool allOk = true;
    if (!pCountAbove) { std::cerr << "[ПОМИЛКА] CountAboveThresholdWin не знайдено\n";        allOk = false; }
    if (!pAvgPositive) { std::cerr << "[ПОМИЛКА] AverageOfPositiveWin не знайдено\n";          allOk = false; }
    if (!pIsAP) { std::cerr << "[ПОМИЛКА] IsArithmeticProgressionWin не знайдено\n";    allOk = false; }
    if (!pToUpper) { std::cerr << "[ПОМИЛКА] ToUpperCharWin не знайдено\n";                allOk = false; }
    if (!pCountWords) { std::cerr << "[ПОМИЛКА] CountWordsStartingWithLetterWin не знайдено\n"; allOk = false; }

    if (!allOk) {
        FreeLibrary(hLib);
        system("pause");
        return 2;
    }
    std::cout << "[OK] Всі функції успішно знайдені в бібліотеці.\n\n";

    std::cout << std::fixed << std::setprecision(4);

    // Крок 3: Виклики функцій DLL
 
    // --- 1. CountAboveThresholdWin ---
    std::cout << "--- 1. CountAboveThresholdWin ---\n";

    INT arr1[] = { 3, 7, 1, 9, 4, 12, 2, 8 };
    printIntArr("Масив", arr1, 8);
    std::cout << "Поріг: 5\n";
    INT r1 = pCountAbove(arr1, 8, 5);
    std::cout << "Кількість елементів > 5: " << r1 << "  (очікується: 4)\n\n";

    INT arr1b[] = { 1, 2, 3 };
    printIntArr("Масив", arr1b, 3);
    std::cout << "Поріг: 10\n";
    INT r1b = pCountAbove(arr1b, 3, 10);
    std::cout << "Кількість елементів > 10: " << r1b << "  (очікується: 0)\n\n";

    INT arr1c[] = { -1, -2, -3 };
    printIntArr("Масив", arr1c, 3);
    std::cout << "Поріг: -5\n";
    INT r1c = pCountAbove(arr1c, 3, -5);
    std::cout << "Кількість елементів > -5: " << r1c << "  (очікується: 3)\n\n";

    // --- 2. AverageOfPositiveWin ---
    std::cout << "--- 2. AverageOfPositiveWin ---\n";

    double arr2[] = { -3.0, 5.0, -1.5, 4.0, 0.0, 2.5 };
    printDblArr("Масив", arr2, 6);
    double r2 = pAvgPositive(arr2, 6);
    std::cout << "Середнє позитивних: " << r2
        << "  (очікується: " << (5.0 + 4.0 + 2.5) / 3.0 << ")\n\n";

    double arr2b[] = { -1.0, -2.0, 0.0 };
    printDblArr("Масив", arr2b, 3);
    double r2b = pAvgPositive(arr2b, 3);
    std::cout << "Середнє позитивних: " << r2b << "  (очікується: 0.0000)\n\n";

    double arr2c[] = { 1.0, 3.0, 5.0, 7.0 };
    printDblArr("Масив", arr2c, 4);
    double r2c = pAvgPositive(arr2c, 4);
    std::cout << "Середнє позитивних: " << r2c << "  (очікується: 4.0000)\n\n";

    // --- 3. IsArithmeticProgressionWin ---
    std::cout << "--- 3. IsArithmeticProgressionWin ---\n";
    std::cout << "(2, 4, 6):  " << (pIsAP(2.0, 4.0, 6.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n";
    std::cout << "(9, 6, 3):  " << (pIsAP(9.0, 6.0, 3.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n";
    std::cout << "(1, 2, 4):  " << (pIsAP(1.0, 2.0, 4.0) ? "TRUE" : "FALSE")
        << "  (очікується: FALSE)\n";
    std::cout << "(5, 5, 5):  " << (pIsAP(5.0, 5.0, 5.0) ? "TRUE" : "FALSE")
        << "  (очікується: TRUE)\n\n";

    // --- 4. ToUpperCharWin ---
    std::cout << "--- 4. ToUpperCharWin ---\n";
    const char testChars[] = { 'a', 'z', 'm', 'A', 'Z', '5', ' ' };
    const char* expected[] = { "A", "Z", "M", "A", "Z", "5", " " };
    for (int i = 0; i < 7; i++) {
        CHAR res = pToUpper(testChars[i]);
        std::cout << "ToUpperCharWin('" << testChars[i] << "') = '"
            << res << "'  (очікується: '" << expected[i] << "')\n";
    }
    std::cout << "\n";

    // --- 5. CountWordsStartingWithLetterWin ---
    std::cout << "--- 5. CountWordsStartingWithLetterWin ---\n";

    char text1[] = "bear Big ball run Boy best";
    std::cout << "Текст: \"" << text1 << "\"\n";
    INT r5a = pCountWords(text1, 'b');
    std::cout << "Слів на 'b'/'B': " << r5a << "  (очікується: 5)\n\n";

    char text2[] = "Sun sets slowly Sometimes sky shines";
    std::cout << "Текст: \"" << text2 << "\"\n";
    INT r5b = pCountWords(text2, 'S');
    std::cout << "Слів на 's'/'S': " << r5b << "  (очікується: 6)\n\n";

    char text3[] = "hello world";
    std::cout << "Текст: \"" << text3 << "\"\n";
    INT r5c = pCountWords(text3, 'z');
    std::cout << "Слів на 'z': " << r5c << "  (очікується: 0)\n\n";

    // Крок 4: Звільнення бібліотеки
    FreeLibrary(hLib);
    std::cout << "[OK] Бібліотека звільнена (FreeLibrary).\n\n";

    std::cout << "====================================================\n";
    std::cout << "  Тестування завершено успішно!\n";
    std::cout << "====================================================\n";

    system("pause");
    return 0;
}