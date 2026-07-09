#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main()
{
	//Task 3
	const size_t n = 20;
	double arr[n];
	arr[0] = 1;
	arr[1] = 0.3;
	for (size_t i = 2; i < n; ++i)
	{
		arr[i] = (i + 1) * arr[i - 2];
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
	return 0;
}