#include <iostream>
#include <cmath>
#include "functions.h"
using namespace std;

void modifyArray(int* arr, size_t n, void(*ptrF)(int&));

int main()
{
    size_t n;
    cout << "Enter n: "; cin >> n;
    int* arr = new int[n];
    fillArray(arr, n);
    printArray(arr, n);

    int code;
    cout << "Increase (1) Decrease (2): "; cin >> code;
    void (*ptrModify)(int&);
    if (code == 1)
        ptrModify = increaseValue;
    else
        ptrModify = decreaseValue;

   
    for (size_t i = 0; i < n; ++i)
    {
        ptrModify(arr[i]);
    }
    printArray(arr, n);
    
    modifyArray(arr, n, ptrModify);

    /*
    // void <function name>()
    void (*ptrF)() = sayHi;
    ptrF();

    // void <fff>(const char*)
    void (*ptrPrint)(const char*);
    ptrPrint = printName;
    ptrPrint("Marta");

    ptrPrint = printCat;
    ptrPrint("Busya");
    ptrPrint("Bona");

    // double <fff> (double, double)
    double (*ptrAction)(double, double);
    double x, y;
    cout << "Enter x: "; cin >> x;
    cout << "Enter y: "; cin >> y;
    int code;
    bool endGame = false;
    while (!endGame)
    {
        cout << "Add (1). Subtract (2). Multiply (3). Divide (4). End game (99).";
        cin >> code;
        switch (code)
        {
        case 1:
        {
            ptrAction = addValues;
            break;
        }
        case 2:
        {
            ptrAction = subtractValues;
            break;
        }
        case 3:
        {
            ptrAction = multiplyValues;
            break;
        }
        case 4:
        {
            ptrAction = divideValues;
            break;
        }
        case 99:
        {
            endGame = true;
            ptrAction = nullptr;
            break;
        }
        default:
        {
            ptrAction = nullptr;
            cout << "Enter valid code...\n";
        }
        }
        if (ptrAction != nullptr)
            cout << "Result: " << ptrAction(x, y) << "\n";
    }
    */
    /*
    // Arrays
    const size_t N = 6;
    int arr[N];
    fillArray(arr, N);

    size_t n = 6;
    int* drr = new int[n];
    for (size_t i = 0; i < n; ++i)
    {
        drr[i] = arr[i] + 1;
    }



    printArray(arr, N);
    printWithIndex(drr, n);

    //sin
    cout << "Enter n(for sin):";
    size_t nSin; cin >> nSin;
    double* sinArr = generateSinArray(nSin);
    for (size_t i = 0; i < nSin; ++i)
    {
        cout << i <<": " << sinArr[i] << "\n";
    }
    cout << "\n";
    delete[] sinArr;

    //cos
    cout << "Enter n(for cos):";
    size_t nCos; cin >> nCos;
    double* cosArr = generateCosArray(nCos);
    for (size_t i = 0; i < nCos; ++i)
    {
        cout << i << ": " << cosArr[i] << "\n";
    }
    cout << "\n";
    delete[] cosArr;

    //Task 8
    task8();
    */

    return 0;
}