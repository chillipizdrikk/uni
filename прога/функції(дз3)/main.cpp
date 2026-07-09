#include<iostream>
#include "functions.h"
using namespace std;

int main()
{
    //Task 1
    cout << "Task 1" << "\n";
    void (*ptrF)() = sayHi;
    ptrF();

    void printName(const char*);
    printName("Marta");
    void printAge(int age);
    printAge(17);
    cout << "\n\n";

    //Task 2
    cout << "Task 2" << "\n";
    double a;
    cout << "Input a: "; cin >> a;
    double b;
    cout << "Input b: "; cin >> b;
    int code;
    double* ptrAction = &a;
    cout << "Difference(1) Minimum(2) Maximum(3)"; cin >> code;
    if (code == 1)
        *ptrAction = DifValues(a, b);
    else if (code == 2)
        *ptrAction = MinValues(a, b);
    else
        *ptrAction = MaxValues(a, b);
    cout << "Result: " << *ptrAction << "\n\n";


    //Task 3
    cout << "Task 3" << "\n";
    int n;
    cout << "Enter n: "; cin >> n;
    int* arr = new int[n];

    cout << "Now, please enter " << n << " elements: ";
    for (size_t i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    PrintArray(arr, n);

    int mult = MultiplyValues(arr, n);
    cout << "Multiply = " << mult << "\n";
    int min = MinValues(arr, n);
    cout << "Minimum = " << min << "\n\n";

    //Task 5
    cout << "Task 5" << "\n";

    double c, d;
    cout << "Enter sides of rectangle: \n";
    cout << "c = ";
    cin >> c;
    cout << "d = ";
    cin >> d;

    cout << "Perimetr of rectangle = " << pRectangle(c, d) << "\n";
    cout << "Square of rectangle = " << sRectangle(c, d) << "\n";

    double r;
    cout << "Enter radius of circle:";
    cin >> r;

    cout << "Perimetr of circle = " << pCircle(r) << "\n";
    cout << "Square of circle = " << sCircle(r) << "\n\n";





    return 0;
}
