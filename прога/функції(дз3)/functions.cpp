#include "functions.h"
#include <iostream>
#include <cmath>
#include <math.h>
using namespace std;


//Task 1
void sayHi()
{
	cout << "Hi! ";
}
void printName(const char* name)
{
	cout << "My name is " << name << '.';
}
void printAge(int age)
{
	cout << " My age is " << age << '.';
}

//Task 2
double DifValues(double a, double b)
{
	return a - b;
}
double MinValues(double a, double b)
{
		if (a < b)
		{
			return a;
		}
		else
		{
			return b;
		} 
}
double MaxValues(double a, double b)
{
	if (a < b)
	{
		return b;
	}
	else
	{
		return a;
	}
}


//Task 3
double PrintArray(const int* a, size_t n)
{
	cout << "Array of:";
	for (size_t i = 0; i < n; ++i)
	{
		cout << a[i];
	}
	cout << "\n";
	return 0;
}
int MultiplyValues(const int* a, size_t n)
{
	int mult = 1;
	for (size_t i = 0; i < n; ++i)
		mult *= a[i];
	return mult;
	cout << "\n";
}
int MinValues(const int* a, size_t n)
{
	int min = a[0];
	for (size_t i = 0; i < n; ++i)
		if (a[i] < min)
			min = a[i];
	return min;
}

//Task 5
double pRectangle(double c, double d)
{
	double perr = (c + d) * 2;
	return perr;

}
double sRectangle(double c, double d)
{
	double squr = c * d;
	return squr;
}
double pCircle(double r)
{
	double perc = 2 * 3.14 * r;
	return perc;
}
double sCircle(double r)
{
	double squc = 3.14 * r * r;
	return squc;
}
