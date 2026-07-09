#include <iostream>
#include "car.h"
#include "plane.h"
#include "vehicle.h"
using namespace std;

int main()
{
	size_t nAll, n;
	Vehicle** vehicles = nullptr;
	n = readVehiclesFromFile(vehicles, nAll, "vehicles.txt");
	printVehiclesArray(vehicles, n);

	size_t planeCount = 0; size_t carCount = 0;
	double planePrice = 0;  double carPrice = 0; double totalPrice = 0;
	for (size_t i = 0; i < n; ++i)
	{
		totalPrice += vehicles[i]->getPrice();
		if (vehicles[i]->getType() == 'P')
		{
			++planeCount;
			planePrice += vehicles[i]->getPrice();
		}
		else
		{
			++carCount;
			carPrice += vehicles[i]->getPrice();
		}
	}

	cout << "Planes amount: " << planeCount <<"\n";
	cout << "Total planes` price : " << planePrice << " uah\n";
	cout << "Cars amount: " << carCount <<"\n";
	cout << "Total cars` price: " << carPrice << " uah\n";
	cout << "TOTAL: " << totalPrice << " UAH\n\n";

	for (size_t i = 0; i < n; ++i)
	delete vehicles[i];
	delete[] vehicles;


	return 0;
}