#include "pch.h"
#include <windows.h>

extern "C" __declspec(dllexport) INT CountAboveThresholdWin(INT* arr, INT size, INT threshold) {
    INT count = 0;
    for (INT i = 0; i < size; i++) {
        if (arr[i] > threshold) {
            count++;
        }
    }
    return count;
}

extern "C" __declspec(dllexport) double AverageOfPositiveWin(double* arr, INT size) {
    double sum = 0.0;
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

extern "C" __declspec(dllexport) BOOL IsArithmeticProgressionWin(double a, double b, double c) {
    return ((b - a) == (c - b)) ? TRUE : FALSE;
}

extern "C" __declspec(dllexport) CHAR ToUpperCharWin(CHAR ch) {
    if (ch >= 'a' && ch <= 'z') {
        return ch - 32;
    }
    return ch;
}

extern "C" __declspec(dllexport) INT CountWordsStartingWithLetterWin(LPSTR text, CHAR letter) {
    INT count = 0;
    BOOL newWord = TRUE;

    for (INT i = 0; text[i] != '\0'; i++) {
        if (text[i] == ' ') {
            newWord = TRUE;
        }
        else if (newWord) {
            CHAR first = text[i];
            if (first >= 'A' && first <= 'Z') {
                first += 32;
            }

            CHAR needed = letter;
            if (needed >= 'A' && needed <= 'Z') {
                needed += 32;
            }

            if (first == needed) {
                count++;
            }

            newWord = FALSE;
        }
    }

    return count;
}