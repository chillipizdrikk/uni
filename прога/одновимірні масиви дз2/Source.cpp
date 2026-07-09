#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main()
{
	
	//Task 1
	/*
	const size_t n = 10;
	double arr[n];
	double sum = 0;
	double prod = 1.0;

	for (size_t i = 0; i < n; ++i)
	{
		arr[i] = 1.0+pow(i, 2.0);
	}
	cout << "Array: \n";

	for (size_t i = 0; i < n; ++i)
	{
		sum += arr[i];
		prod *= arr[i];
		cout << i << ":" << arr[i] << "\n";
	}
	cout << "SUM: " << sum << "\n";
	cout << "PROD: " << prod << "\n";
	cout << "\n\n";
	*/

	//Task 2
	/*
	double a;
	cout << "Enter a: "; cin >> a;
	const size_t n = 10;
	double* arr = new double[n];
	arr[0] = a;

	for (size_t i = 1; i < n; i++)
		arr[i] = (a + i) * arr[i - 1];
	cout << "Array: \n";

	double sum = 0;
	double prod = 1.0;

	for (size_t i = 0; i < n; ++i)
	{
		sum += arr[i];
		prod *= arr[i];
		cout << i << ":" << arr[i] << "\n";
	}
	cout << setprecision(2)<< fixed << "SUM: " << sum << "\n";
	cout << setprecision(2) << fixed << "PROD: " << prod << "\n";
	cout << "\n\n";
	*/

	//Task 3
	/*
	const size_t n = 20;
	double arr[n];
	arr[0] = 1;
	arr[1] = 0.3;
	for (size_t i = 2; i < n; ++i)
	{
		arr[i] = (i + 1)*arr[i-2];
	}

	double sum = 0;
	double prod = 1.0;
	for (size_t i = 0; i < n; ++i)
	{
		sum += arr[i];
		prod *= arr[i];
		cout << i << ":" << arr[i] << "\n";
	}
	cout << setprecision(2) << fixed << "SUM: " << sum << "\n";
	cout << setprecision(2) << fixed << "PROD: " << prod << "\n";
	cout << "\n\n";
	*/


	//Task 4
	/*
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
	*/

	//Task 5
	int n;
	cout << "Enter n:\n"; cin >> n;
	int* a_arr = new int[n];
	double f;
	cout << "Enter " << n << " elements\n";
	for (int i = 0; i < n; ++i)
	{
		cout << "a[" << i << "] ="; cin >> a_arr[i];
	}
	for (int i = 0; i < n; ++i)
	{
		if (a_arr[i] % 3 == 0)
		{
			f = a_arr[i] * a_arr[i];
		}
		else if (a_arr[i] % 2 == 0)
		{
			f = a_arr[i];
		}
		else
			f = a_arr[i] / 3.0;

		cout << "i:" << a_arr[i] << "\t" << "f:" << f << "\n";
	}
	cout << "\n\n";
	delete[] a_arr;


	return 0;
 }