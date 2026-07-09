#include "functions.h"
#include <iostream>
using namespace std;

void sayhello(int n)
{
    for (int i = 0; i < n; ++i)
        cout << "Hello!\n";
    cout << "\n";
}
double addValues(double a, double b)
{
	return a + b;
}
double modify(double val)
{
    cout << "Modify DOUBLE\n";
    return val * 10.0;
}

int modify(int val)
{
    cout << "Modify INT\n";
    return val / 2;
}

int modify(int val, int coef)
{
    cout << "Modify INT with coef: " << coef << "\n";
    return val + coef;
}

void changeValue(int* val, int coef)
{
    (*val) += coef;
}
void changeValue(int& val, int coef)
{
    val += coef;
}