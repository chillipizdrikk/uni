#include "functions.h"
#include <iostream>
#include <cmath>
using namespace std;



void printArray(const int* a, size_t n)
{
    cout << "Array: ";
    for (size_t i = 0; i < n; ++i)
    {
        cout << a[i] << "  ";
    }
    cout << "\n";
}



// <index>: <value>
void printWithIndex(const int* a, size_t n)
{
    cout << "Array of integers\n";
    for (size_t i = 0; i < n; ++i)
    {
        cout << i << ": " << a[i] << "\n";
    }
    cout << "\n";
}



int f(const int* a, size_t n, int y)
{
    int sum = 0;
    for (size_t i = 0; i < n; ++i)
    {
        sum += a[i] * y;
    }
    return sum;
}



int maxValue(const int* a, size_t n)
{
    int max = a[0];
    for (size_t i = 1; i < n; ++i)
    {
        if (a[i] > max)
        {
            max = a[i];
        }
    }
    return max;
}



size_t maxIndex(const int* a, size_t n)
{
    size_t maxIndex = 0;
    for (size_t i = 1; i < n; ++i)
    {
        if (a[i] > a[maxIndex])
        {
            maxIndex = i;
        }
    }
    return maxIndex;
}

void fillArray(int* a, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        a[i] = (i + i) * 2;
    }
}

//---Функція заповнення---------------
void mass_in(int m) {
    int i;
    double* x = new double[m];
    for (i = 0; i < m; i++) {
        cout << "Enter the elements " << i + 1 << ": ";
        cin >> x[i];
    }
    cout << endl << endl;


    double result;
    for (int j = 0; j <= m; ++j) {
        result = sin(x[i]);
        cout << result;
        cout << endl;
    }
}
//sin
double* generateSinArray(size_t n)
{
    double* arr = new double[n];
    double x = 0;
    double h = 2 * 3.14 / (double)n;
        for (size_t i = 0; i < n; ++i)
        {
            arr[i] = sin(x);
            x += h;
        }
        
        return arr;
}

//cos проміжок [0;pi]
double* generateCosArray(size_t n)
{
    double* arr = new double[n];
    double x = 0;
    double h = 3.14 / (double)n;
    for (size_t i = 0; i < n; ++i)
    {
        arr[i] = cos(x);
        x += h;
    }
    return arr;
}

int* readArray(size_t n)
{
    cout << "Enter array of " << n << " integers\n";
    int* arr = new int[n];
    for (size_t i = 0; i < n; ++i)
    {
        cout << "Enter element: " << i << ": ";
        cin >> arr[i];
    }
    cout << "Done.\n";
    return arr;
}

int calculateP(int x, const int* arr, size_t n)
{
    // P = arr[0]*x^0 + arr[1]*x^1 + ... + arr[n-1]*x^(n-1)
    int P = 0;
    for (size_t i = 0; i < n; ++i)
    {
        P += arr[i] * pow((double)x, i);
    }
    return P;
}

void task8()
{
    cout << "Task 8\n";
    int s, t;
    cout << "Enter s: "; cin >> s;
    cout << "Enter t: "; cin >> t;
    int* a = readArray(13);
    // p(1) - p(t) + p2(s-t) - p3(1)
    int p_1 = calculateP(1, a, 13);
    int p_t = calculateP(t, a, 13);
    int p_st = calculateP(s-t, a, 13);
    int result = p_1 - p_t + p_st * p_st - p_1 * p_1 * p_1;
    cout << "Result: " << result << "\n\n";
    delete[] a;
}

void sayHi()
{
    cout << "Hi!\n";
}

void printName(const char* name)
{
    cout << "My name is: " << name << "\n";
}

void printCat(const char* catName)
{
    cout << "My pussy cat: " << catName << " is the best.\n";
}

double addValues(double a, double b)
{
    return a + b;
}
double multiplyValues(double a, double b)
{
    return a * b;
}
double subtractValues(double a, double b)
{
    return a - b;
}
double divideValues(double a, double b)
{
    return a / b;
}


void increaseValue(int& a)
{
    a *= 2;
}
void decreaseValue(int& a)
{
    a /= 2;
}
void modifyArray(int* arr, size_t n, void(*ptrF)(int&))
{
    for (size_t i = 0; i < n; ++i)
    {
        ptrF(arr[i]);
    }
}


/*
void modify(int a)
{
    a += 10;
}



void modifyPtr(int* a)
{
    *a += 10;
}



void modifyRef(int& a)
{
    a += 10;
}
*/