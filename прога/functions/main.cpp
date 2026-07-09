#include <iostream>
#include "functions.h"
using namespace std;

int main()
{
    int a = 10;
    cout << "Before: " << a << "  ";
    changeValue(&a, 5);
    cout << "After: " << a << "\n";
    changeValue(a, 10);
    cout << "And After: " << a << "\n";

    return 0;
}