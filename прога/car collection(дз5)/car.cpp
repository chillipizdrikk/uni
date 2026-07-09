#include <fstream>
#include "car.h"


Car::Car()
:CarBrand("no brand"), CarModel("no model"), CarYear(0) {}

Car::Car(string brand, string model, int year)
:CarBrand(brand),CarModel(model),CarYear(year) {}

Car::Car(const Car& C)
:CarBrand(C.CarBrand),CarModel(C.CarModel),CarYear(C.CarYear) {}


istream& operator >> (istream& in, Car& C)
{
	in >> C.CarBrand >> C.CarModel >> C.CarYear;
	return in;
}

ostream& operator << (ostream& out, const Car& C)
{
	out << C.CarBrand <<" " << C.CarModel << " " << C.CarYear << "\n";
	return out;
}

void printCarsFormatted(const Car& C, int brandWidth, int modelWidth)
{
	cout.width(brandWidth); cout.setf(ios_base::right, ios_base::adjustfield);
	cout << C.CarBrand; cout << " | ";

	cout.width(modelWidth); cout.setf(ios_base::left, ios_base::adjustfield);
	cout << C.CarModel; cout << " | " << C.CarYear << "\n";
}

Car* readFromFile(const string& fileName, size_t& n)
{
	ifstream iFile(fileName);
	iFile >> n;
	Car* arr = new Car[n];
	for (size_t i = 0; i < n; ++i)
	{
		iFile >> arr[i];
	}
	iFile.close();
	return arr;
}
