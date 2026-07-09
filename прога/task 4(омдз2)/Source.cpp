#include <iostream>
#include <cmath>
using namespace std;

int main()
{
//Task 4
size_t n;
cout << "Enter n:"; cin >> n;
double* a_arr = new double[n];
double* b_arr = new double[n];
double sum = 0.0;
size_t k = 0; //nof elements in [1;2]
size_t k1 = 0, k2 = 0;
cout << "Enter array of " << n << " double elements\n ";
for (size_t i = 0; i < n; ++i)
{
	cout << "a[" << i << "] ="; cin >> a_arr[i];
	b_arr[i] = a_arr[i];
	if (a_arr[i] < 0)
		++k1; // k1 - кількість від'ємних
	else if (a_arr[i] <= 2 && a_arr[i] >= 1)
		++k2; // k2 - кількість таких, що належать проміжку
	else if (a_arr[i] != 0)
		b_arr[i] = 1;
	sum += a_arr[i];
}

cout << "i:    a[i]     b[i]\n";
for (size_t i = 0; i < n; ++i)
{
	cout << i << ": " << "\t" << a_arr[i] << " \t" << b_arr[i] << "\n";
}

cout << "\n Number of negative elements: " << k1 << "\n";
cout << "\n Number of elements in the interval [1; 2]: " << k2 << "\n\n";

delete[] a_arr;
delete[] b_arr;




return 0;
}

