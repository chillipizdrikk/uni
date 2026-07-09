#include "functions.h"
#include <iostream>
using namespace std;



void sayHello()
{
    cout << "Hi people!\n";
}



void loginUser(const char* userName)
{
    cout << "User: " << userName << " is logged in.\n";
}
double calcSum(double a, double b)
{
    double sum = a + b;
    return sum;
}



double calcProd(double a, double b)
{
    return a * b;
}