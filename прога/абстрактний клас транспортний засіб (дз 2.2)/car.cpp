#include "car.h"
using namespace std;

Car::Car()
	: Vehicle(), carBrand(""), carPrice(0.0), carYear(0)
{}

Car::Car(const std::string& maker, const std::string& brand, double price, double year)
	: Vehicle(maker), carBrand(brand), carPrice(price), carYear(year)
{}

Car::Car(const Car& C)
	: Vehicle(C), carBrand(C.carBrand), carPrice(C.carPrice), carYear(C.carYear)
{}

Car::~Car()
{}

void Car::print() const
{

	cout << "Car: " << carBrand << "\n";
	Vehicle::print(); cout << "\n";
	cout << "Price: " << carPrice << " uah\n";
	cout << "Total price: " << getPrice() << " uah\n\n";
}

double Car::getPrice() const
{
	return carPrice * (1 - (carYear * 0.01));
}

char Car::getType() const
{
	return 'C';
}

void Car::readFrom(istream& in)
{
	Vehicle::readFrom(in);
	in >> carBrand >> carPrice >> carYear;
}

void Car::writeTo(ostream& out) const
{
	Vehicle::writeTo(out);
	out << ' ' << carBrand << ' ' << carPrice << ' ' << carYear;
}
