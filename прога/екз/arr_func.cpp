#include "arr_func.h"
#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

double* createArray(double x, size_t n)
{
    double* arr = new double[n];
    double two = 1.0;
    for (size_t i = 0; i < n; ++i)
    {
        if (i % 2 == 0)
        {
            arr[i] = (x * cos(i * x)) / two;
        }
        else
        {
            arr[i] = 1.0 + sin(i * x) / (double)i;
        }
        two *= 2.0;
    }
    return arr;
}


void printArray(const double* arr, size_t n)
{
	// i: value, width = 8, std::fixed
	cout << "Array\n";
	for (size_t i = 0; i < n; ++i)
	{
		cout << i << ": ";
        cout.width(10); cout.precision(6); cout << std::right<<std::fixed << arr[i];
		cout << "\n";
	}
	cout << "\n";
}


double maxValue(const double* arr, size_t n)
{
    double maxV = arr[0];
    for (size_t i = 1; i < n; ++i)
    {
        if (arr[i] > maxV)
        {
            maxV = arr[i];
        }
    }
    return maxV;
}


size_t maxIndex(const double* arr, size_t n)
{
    size_t maxI = 0;
    for (size_t i = 1; i < n; ++i)
    {
        if (arr[i] > arr[maxI])
        {
            maxI = i;
        }
    }
    return maxI;
}


double minValueAndIndex(const double* arr, size_t n, size_t& minIndex)
{
    minIndex = 0;
    for (size_t i = 1; i < n; ++i)
    {
        if (arr[i] < arr[minIndex])
        {
            minIndex = i;
        }
    }
    return arr[minIndex];
}


double sumInRange(double* begin, double* end)
{
    double sum = 0.0;
    while (begin != end)
    {
        sum += *begin;
        ++begin;
    }
    return sum;
}