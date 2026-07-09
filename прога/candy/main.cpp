#include <iostream>
#include <fstream>
#include "candy.h"

int main()
{
	Candy C1;
	cout << "Enter candy:\n";
	cin >> C1; 
	cout << "\nYour candy: "<< C1<<"\n\n";
	cout << "Candies:\n";

	ifstream iFile("candy.txt");
	size_t n; iFile >> n;
	Candy* arr = new Candy[n];
	for (size_t i = 0; i < n; ++i)
	{
		iFile >> arr[i];
	}
	iFile.close();

	printCandyArray(arr, n);

	delete[] arr;
	return 0;
}