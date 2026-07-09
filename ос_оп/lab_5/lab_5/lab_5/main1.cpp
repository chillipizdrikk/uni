#include <iostream>
#include <cstring>
using namespace std;

// Прототипи функцій
int CountAboveThreshold(int* arr, int size, int threshold);
double AverageOfPositive(double* arr, int size);
bool IsArithmeticProgression(double a, double b, double c);
char ToUpperChar(char ch);
int CountWordsStartingWithLetter(char* text, char letter);

// 1. Кількість елементів масиву, більших за поріг
int CountAboveThreshold(int* arr, int size, int threshold) {
    int count = 0;
    for (int i = 0; i < size; i++) {
        if (arr[i] > threshold) {
            count++;
        }
    }
    return count;
}

// 2. Середнє арифметичне додатних елементів
double AverageOfPositive(double* arr, int size) {
    double sum = 0.0;
    int count = 0;

    for (int i = 0; i < size; i++) {
        if (arr[i] > 0) {
            sum += arr[i];
            count++;
        }
    }

    if (count == 0) {
        return 0.0;
    }

    return sum / count;
}

// 3. Перевірка арифметичної прогресії
bool IsArithmeticProgression(double a, double b, double c) {
    return (b - a) == (c - b);
}

// 4. Переведення символу в верхній регістр
char ToUpperChar(char ch) {
    if (ch >= 'a' && ch <= 'z') {
        return ch - 32;
    }
    return ch;
}

// 5. Підрахунок слів, що починаються з заданої літери
int CountWordsStartingWithLetter(char* text, char letter) {
    int count = 0;
    bool newWord = true;

    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] == ' ') {
            newWord = true;
        }
        else {
            if (newWord) {
                char first = text[i];
                if (first >= 'A' && first <= 'Z') {
                    first = first + 32;
                }

                char needed = letter;
                if (needed >= 'A' && needed <= 'Z') {
                    needed = needed + 32;
                }

                if (first == needed) {
                    count++;
                }
                newWord = false;
            }
        }
    }

    return count;
}

int main() {
    cout << "===== Main1.cpp =====" << endl;
    // Тест 1
    int arr1[] = { 3, 7, 10, 2, 8, 1 };
    int size1 = 6;
    cout << "CountAboveThreshold = "
        << CountAboveThreshold(arr1, size1, 5) << endl;

    // Тест 2
    double arr2[] = { -2.5, 3.0, 4.5, -1.0, 2.5 };
    int size2 = 5;
    cout << "AverageOfPositive = "
        << AverageOfPositive(arr2, size2) << endl;

    // Тест 3
    cout << "IsArithmeticProgression(2, 4, 6) = "
        << IsArithmeticProgression(2, 4, 6) << endl;
    cout << "IsArithmeticProgression(1, 3, 8) = "
        << IsArithmeticProgression(1, 3, 8) << endl;

    // Тест 4
    cout << "ToUpperChar('b') = "
        << ToUpperChar('b') << endl;

    // Тест 5
    char text[] = "Apple banana apricot Berry avocado";
    cout << "CountWordsStartingWithLetter(text, 'a') = "
        << CountWordsStartingWithLetter(text, 'a') << endl;

    return 0;
}