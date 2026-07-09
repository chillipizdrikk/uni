#pragma once
#include <iostream>
#include <string>
using namespace std;

struct Car
{
	string CarBrand;
	string CarModel;
	int CarYear;

	Car();
	Car(string brand, string model, int year);
	Car(const Car& C);
};


istream& operator >> (istream& in, Car& C);
ostream& operator << (ostream& out, const Car& C);

void printCarsFormatted(const Car& C, int brandWidth, int modelWidth);
Car* readFromFile(const string& fileName, size_t& n);
