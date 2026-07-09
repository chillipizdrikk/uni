#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main()
{
	//Task 2
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

	return 0;
	}