#include <iostream>
using namespace std;
int main()
{
	/*
	const int n = 8;
	int arr[n];
	arr[0] = 5;
	arr[1] = 7;
	arr[2] = 9;
	arr[3] = -1;
	arr[4] = 0;
	arr[5] = -2;
	cout << "My elements:" << arr[0] << " " << arr[2] << " " << arr[3] << " " << arr[5] << "\n\n";
	cout << "Enter arr[6]: "; cin >> arr[6];
	cout << "Enter arr[7]: "; cin >> arr[7];
	cout << "Done: " << arr[6] << " " << arr[7] << "\n\n";

	cout << "Array of integers: ";
	for (int i = 0; i < n; ++i)
	{
		cout << arr[i] << " ";
	}
	cout << "\n\n";

	cout << "Adress & Values\n";
	cout << "Of array: " << arr << " " << *arr << "\n";
	cout << "Of arr[0]: " << &arr[0] << " " << *(arr + 0) << "\n";
	cout << "Of arr[1]: " << &arr[1] << " " << *(arr + 1) << "\n";
	cout << "Of arr[7]: " << &arr[n - 1] << " " << *(arr + n - 1) << "\n\n";
	*/
	//Task 1_a
	const int n = 10;    //const size_t n = 10;(цілі невід'ємні числа)
	double pArr[n];
	pArr[0] = 1.0;
	for (int i = 1; i < n; ++i)
	{
		//pArr[i] = pow(2.0, i);
		pArr[i] = pArr[i - 1] * 2.0;
	}
	
	double sum = 0.0;
	double prod = 1.0;
	cout << "Array:\n";
	for (int i = 0; i < n; ++i)
	{
		cout << i << ":" << pArr[i] << "\n";

		sum += pArr[i];     //сума
		prod *= pArr[i];    //добуток      
	}
	cout << "\n";
	cout << "Total sum: " << sum << "\n";
	cout << "Total products " << prod << "\n\n";

	//Task 2_b
	// a, a + 1.1, a + 2.2, a + 3.3, ...
	double a;
	cout << "Enter value: "; cin >> a;
	cout << "Array Task2_b\n";
	pArr[0] = a;
	cout << 0 << " : " << pArr[0] << "\n";
	for (size_t i = 0; i < n; ++i)
	{
		pArr[i] = a + (double)i + (double)i * 0.1;
		cout << i << " : " << pArr[i] << "\n";
	}
	cout << "\n\n";

	return 0;
}