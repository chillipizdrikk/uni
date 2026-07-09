#include "vehicle.h"
#include <fstream>

using namespace std;

Vehicle::Vehicle()
	:vehicleMaker("")
{}

Vehicle::Vehicle(const std::string& maker)
	:vehicleMaker(maker)
{}

Vehicle::Vehicle(const Vehicle& V)
	:vehicleMaker(V.vehicleMaker)
{}

Vehicle::~Vehicle()
{}

void Vehicle::print() const
{
	cout << "Manufacturer: " << vehicleMaker;
}

void Vehicle::readFrom(std::istream& in)
{
	in >> vehicleMaker;
}
void Vehicle::writeTo(std::ostream& out) const
{
	out << vehicleMaker;
}

string Vehicle::getManufacturer() const
{
	return vehicleMaker;
}

bool Vehicle:: operator<(const Vehicle& V) const
{
	return getPrice() < V.getPrice();
}

std::istream& operator>> (std::istream& in, Vehicle& V)
{
	V.readFrom(in);
	return in;
}

std::ostream& operator<< (std::ostream& out, const Vehicle& V)
{
	V.writeTo(out);
	return out;
}

size_t readVehiclesFromFile(Vehicle**& arr, size_t& n, const std::string& fileName)
{
    ifstream iFile(fileName);
    iFile >> n;
    arr = new Vehicle * [n];
    char type;
    size_t counter = 0;
    for (size_t i = 0; i < n; ++i)
    {
        iFile >> type;
        if (type == 'P')
        {
            arr[counter] = new Plane();
            iFile >> *arr[counter];
            ++counter;
        }
        else if (type == 'C')
        {
            arr[counter] = new Car();
            iFile >> *arr[counter];
            ++counter;
        }
        else
        {
            char temp[256];
            iFile.getline(temp, 256);
        }
    }

    iFile.close();
    return counter;
}


void printVehiclesArray(Vehicle**& arr, size_t n)
{
    cout << "Collection of all vehicles\n";
    for (size_t i = 0; i < n; ++i)
    {
        arr[i]->print();
    }
    cout << "\n";
}
