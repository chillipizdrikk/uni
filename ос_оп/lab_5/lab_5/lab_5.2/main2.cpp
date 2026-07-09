#include <windows.h>
#include <iostream>
using namespace std;

// Прототипи
INT CountAboveThresholdWin(INT* arr, INT size, INT threshold);
DOUBLE AverageOfPositiveWin(DOUBLE* arr, INT size);
BOOL IsArithmeticProgressionWin(DOUBLE a, DOUBLE b, DOUBLE c);
CHAR ToUpperCharWin(CHAR ch);
INT CountWordsStartingWithLetterWin(LPSTR text, CHAR letter);

// 1
INT CountAboveThresholdWin(INT* arr, INT size, INT threshold) {
    INT count = 0;
    for (INT i = 0; i < size; i++) {
        if (arr[i] > threshold) {
            count++;
        }
    }
    return count;
}

// 2
DOUBLE AverageOfPositiveWin(DOUBLE* arr, INT size) {
    DOUBLE sum = 0.0;
    INT count = 0;

    for (INT i = 0; i < size; i++) {
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

// 3
BOOL IsArithmeticProgressionWin(DOUBLE a, DOUBLE b, DOUBLE c) {
    return ((b - a) == (c - b)) ? TRUE : FALSE;
}

// 4
CHAR ToUpperCharWin(CHAR ch) {
    if (ch >= 'a' && ch <= 'z') {
        return ch - 32;
    }
    return ch;
}

// 5
INT CountWordsStartingWithLetterWin(LPSTR text, CHAR letter) {
    INT count = 0;
    BOOL newWord = TRUE;

    for (INT i = 0; text[i] != '\0'; i++) {
        if (text[i] == ' ') {
            newWord = TRUE;
        }
        else {
            if (newWord) {
                CHAR first = text[i];
                if (first >= 'A' && first <= 'Z') {
                    first = first + 32;
                }

                CHAR needed = letter;
                if (needed >= 'A' && needed <= 'Z') {
                    needed = needed + 32;
                }

                if (first == needed) {
                    count++;
                }
                newWord = FALSE;
            }
        }
    }

    return count;
}

int main() {
    cout << "===== Main2.cpp =====" << endl;
    INT arr1[] = { 3, 7, 10, 2, 8, 1 };
    INT size1 = 6;
    cout << "CountAboveThresholdWin = "
        << CountAboveThresholdWin(arr1, size1, 5) << endl;

    DOUBLE arr2[] = { -2.5, 3.0, 4.5, -1.0, 2.5 };
    INT size2 = 5;
    cout << "AverageOfPositiveWin = "
        << AverageOfPositiveWin(arr2, size2) << endl;

    cout << "IsArithmeticProgressionWin(2, 4, 6) = "
        << IsArithmeticProgressionWin(2, 4, 6) << endl;

    cout << "IsArithmeticProgressionWin(1, 3, 8) = "
        << IsArithmeticProgressionWin(1, 3, 8) << endl;

    cout << "ToUpperCharWin('b') = "
        << ToUpperCharWin('b') << endl;

    CHAR text[] = "Apple banana apricot Berry avocado";
    cout << "CountWordsStartingWithLetterWin(text, 'a') = "
        << CountWordsStartingWithLetterWin(text, 'a') << endl;

    return 0;
}