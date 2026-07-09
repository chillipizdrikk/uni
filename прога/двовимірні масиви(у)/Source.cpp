#include "functions.h"
#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main()
{
	sayHello();
	loginUser("Marta Tryhub");

	double x, y; cin >> x >> y;
	double sum = calcSum(x, y);
	double prod = calcProd(x, y);
	cout << "Sum: " << sum << "\n";
	cout << "Prod: " << prod << "\n";
	/*
	const size_t N = 3;
	const size_t M = 4;
	int A[N][M] = { 1, 2, 3, 4, 2, 4, 6, 8, 3, 6, 9, 12 };
	A[1][1] = 5;
	A[N - 1][M - 1] = 5;

	cout << "Matrix by ROWs\n";
	for (size_t i = 0; i < N; ++i) //rows
	{
		int sumRow = 0;
		for (size_t j = 0; j < M; ++j) //columns
		{
			cout << A[i][j] << " ";
			sumRow += A[i][j];
		}
		cout << "Row sum: " << sumRow << "\n";
	}
	cout << "\n\n";

	cout << "Matrix by COLUMNs\n";
	for (size_t j = 0; j < M; ++j)
	{
		for (size_t i = 0; i < N; ++i)
		{
			cout << A [j][i] << " ";
		}
		cout << "\n";
	}
	cout << "\n\n";

	cout << "Dynamic matrix\n";
	cout << "Enter nof rows: ";
	size_t n_row; cin >> n_row;
	cout << "Enter nof columns: ";
	size_t n_col; cin >> n_col;
	int** B = new int* [n_row];
	for (size_t i = 0; i < n_col; ++i)
	{
		B[i] = new int[n_col];
		for (size_t j = 0; j < n_col; ++i)
		{
			B[i][j] = (i + 1) * (j + 1);
			cout << B[i][j] << " ";
		}
		cout << "\n";
	}
	cout << "\n";

	for (size_t i = 0; i < n_row; ++i)
		delete[] B[i];
	delete[]B;
	*/
	/*
	//Task 1_b
	const size_t N = 5;
	double A[N][N];
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < N; ++j)
		{
			if (i < j)
				A[i][j] = sin((double)(i + j));
			else if (i > j)
				A[i][j] = (double)(i + j) / (double)(2 * i + 3 * j);
			else
				A[i][j] = 1.0;

			cout << setprecision(2) << A[i][j] << " ";
		}
		cout << "\n";
	}
	cout << "\n\n";

	//Task 3_a

	cout << "Enter nof elements: ";
	size_t n; cin >> n;
	double* x = new double[n];
	cout << "Enter " << n << "doubles\n";
	for (size_t i = 0; i < n; ++i)
	{
		cout << i << ": "; cin >> x[i];
	}

	double** x_matrix = new double* [n];
	for (size_t i = 0; i < n; ++i)
	{
		x_matrix[0] = new double[n];
		for (size_t j = 0; j < n; ++j)
		{
			x_matrix[i][j] = pow(x[j], i + 1);
			cout << setprecision << fixed << x_matrix[i][j] << "\t";
		}
		cout << "\n";
	}
	cout << "\n";

	for (size_t i = 0; i < n; ++i)
		delete[] x_matrix[i];
	delete[] x_matrix;
	*/
	/*
	//Task 4
cout << "Enter nof rows: "; size_t n_row; cin >> n_row;
cout << "Enter nof cols: "; size_t n_col; cin >> n_col;

int** A = new int* [n_row];
for (int i = 0; i < n_row; ++i)
{
	A[i] = new int[n_col];
	for (int j = 0; j < n_col; ++j)
		A[i][j] = (i + 1) * (j + 1);

	int temp = A[i][i];
	A[i][i] = A[i][n_col - 1];
	A[i][n_col - 1] = temp;
}
// sum // max // cout // b, c
int* b = new int[n_row];
int* c = new int[n_row];
for (size_t i = 0; i < n_row; ++i)
{
	b[i] = 0;
	c[i] = A[i][0];
	for (size_t j = 0; j < n_col; ++j)
	{
		cout << A[i][j] << "  ";
		b[i] += A[i][j];

		if (A[i][j] > c[i])
			c[i] = A[i][j];
	}
	cout << "Sum: "<< b[i] << "Max: " << c[i] << "\n";
}
cout << "\n";

cout << "All sum: ";
for (size_t i = 0; i < n_row; ++i)
	cout << b[i] << " ";
cout << "\n";
cout << "All max: ";
for (size_t i = 0; i < n_row; ++i)
	cout << c[i] << " ";
cout << "\n\n";
*/







	return 0;
}