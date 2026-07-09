#include <iostream>
using namespace std;

int main()
{
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