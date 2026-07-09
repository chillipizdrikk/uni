#include <iostream>    //динамічні масиви
#include <cmath>
using namespace std;

int main()
{
	//Task 4_a
	
	size_t n;
	cout << "Enter n: "; cin >> n;
	double* arr = new double[n];
	arr[0] = 0.0;
	arr[1] = 5.0 / 8.0;
	double sum = arr[0] + arr[1];
	double prod = arr[1];
	for (size_t i = 2; i < n; ++i)
	{
		arr[i] = 0.5 * arr[i - 1] + 0.75 * arr[i - 2];
		sum += arr[i];
		prod *= arr[i];
	}

	cout << "Task 4_a Array\n";
	for (size_t i = 0; i < n; ++i)
	{
		cout << i << ":" << arr[i] << "\n";
	}
	cout << "SUM:  " << sum << "\n";
	cout << "PROD: " << prod << "\n\n";

	delete[] arr;
	
	//Task 5
	cout << "Task 5\n";
	cout << "Enter n:"; cin >> n;
	double * a_arr = new double[n];
	double * b_arr = new double[n];
	cout << "Enter array of " << n << "double elements\n ";
	for (size_t i = 0; i < n; ++i)
	{
		cout << "a[" << i << "] ="; cin >> a_arr[i];
		if (a_arr[i] < 0.0)
			b_arr[i] = a_arr[i] + 0.5;
		else
			b_arr[i] = 0.1;

	}
	cout << "i:    a[i]     b[i]\n";
	for (size_t i = 0; i < n; ++i)
	{
		cout << i << ": " << a_arr[i] << "  " << b_arr[i] << "\n";
	}
	cout << "\n\n";

	delete[] a_arr;
	delete[] b_arr;
	/*
	//Task 6_b
	cout << "Task 6\n";
	cout << "Enter n:"; cin >> n;
	a_arr = new double[n];
	size_t k = 0; //nof elements in [3;7]
	cout << "Enter array of " << n << "double elements\n ";
	for (size_t i = 0; i < n; ++i)
	{
		cout << "a[" << i << "] ="; cin >> a_arr[i];
		if (a_arr[i] >= 3.0 && a_arr[i] <= 7.0)
			++k;
	}
	cout << "Array a: ";
	for (size_t i = 0; i < n; ++i)
	{
		cout << a_arr[i] << "  ";
	}
	cout << "\nNof elements in [3; 7]: " << k << "\n\n";

	b_arr = new double[k];
	sum = 0.0;
	size_t j = 0;
	for (size_t i = 0; i < n; ++i)
	{
		if (a_arr[i] >= 3.0 && a_arr[i] <= 7.0)
		{
			b_arr[j] = a_arr[i];
			sum += b_arr[j];
			++j;
		}
	}

	cout << "Array b: ";
	for (j = 0; j < k; ++j)
	{
		cout << b_arr[j] << "  ";
	}
	cout << "\nSum of elements: " << sum << "\n\n";

	delete[] a_arr;
	delete[] b_arr;

	//Task 11
	cout << "Task 11\n";
	cout << "Enter n:"; cin >> n;
	int* x_arr = new int[n];
	cout << "Enter array of" << n << "integers\n";
	for(size_t i =0; i<n; ++i)
	{
		cout << i << ": ";
		cin >> x_arr[i];
	}

	cout << "Array: ";
	for (size_t i = 0; i < n; ++i)
	{
		cout << x_arr[i] << "  ";
	}
	cout << "\n\n";

	cout << "Enter value A: ";
	int A; cin >> A;
	size_t index = n;   //index of element with value A
	for (size_t i = 0; i < n; ++i)
	{
		if (x_arr[i] == A)
		{
			index = 1;
			break;
		}
	}
	if (index < n)
	{
	// Bingo
	cout << "Value found! Index: " << index << " Check: " << x_arr[index] << "\n\n";
	}
	else
	{
	// Failure
	cout << "Value not found.\n";
	}
	delete[] x_arr;



	*/
	return 0;
} 