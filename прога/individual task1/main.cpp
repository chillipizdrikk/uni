#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;


int main()
{
	cout << "Task 1\n";
	int m;
	cout << "Enter an integer (n):"; cin >> m;
	double y;
	cout << "Enter a real number (x):"; cin >> y;
	cout << "\n";
	double sum = 0.0;
	for (size_t i = 0; i < m; ++i)
		sum += pow(sin(y), i);
	cout << "Result: " << sum << "\n\n";


	cout << "Task 2\n\n";
	double x,p,n;
	cout << "Enter x : "; cin >> x;
	cout << "Enter p : "; cin >> p;
	cout << "Enter n : "; cin >> n;
	double* arr = new double[n+1];
	arr[0] = 1.;
	for (size_t i = 1; i < n; i++)
	{
		arr[i] = arr[i - 1] * (p - i) * x;
	}
		

	cout << "Array: \n";

	double sum2 = 0;
	long double prod = 1.0;

	for (size_t i = 0; i < n+1; ++i)
	{
		sum2 += arr[i];
		prod *= arr[i];
		cout << i << ":" <<fixed << arr[i] << "\n";
	}

	cout << setprecision(2) << fixed << "Summary: " << sum2 << "\n";
	cout << setprecision(2) << fixed << "Product: " << prod << "\n";
	cout << "\n\n";

	return 0;
}
