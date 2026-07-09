#include <iostream>
#include <cmath>
using namespace std;

int main()
{
	//Task 1
	const size_t n = 10;
	double arr[n];
	double sum = 0;
	double prod = 1.0;

	for (size_t i = 0; i < n; ++i)
	{
		arr[i] = 1.0 + pow(i, 2.0);
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

	return 0;
}