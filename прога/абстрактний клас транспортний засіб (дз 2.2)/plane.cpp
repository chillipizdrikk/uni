#include "plane.h"
using namespace std;

Plane::Plane()
	: Vehicle(), planeName(""), planePrice(0), planePlace(0)
{}

Plane::Plane(const std::string& maker, const string& name, double price, double place)
	: Vehicle(maker), planeName(name), planePrice(price), planePlace(place)
{}

Plane::Plane(const Plane& P)
	: Vehicle(P), planeName(P.planeName), planePrice(P.planePrice), planePlace(P.planePlace)
{}

Plane::~Plane()
{}

void Plane::print() const
{
	cout << "Name: " << planeName << "\n"; Vehicle::print(); cout << "\n";
	cout << "Places amount: " << planePlace << "\n";
	cout << "Price: " << planePrice << " uah\n";
	cout << "Total price: " << getPrice() << " uah\n\n";
}

double Plane::getPrice() const
{
	return (planePrice * planePlace) * (1 + (planePlace * 0.001));
}

char Plane::getType() const
{
	return 'P';
}

void Plane::readFrom(istream& in)
{
	Vehicle::readFrom(in);
	in >> planeName >> planePrice >> planePlace;
}

void Plane::writeTo(ostream& out) const
{
	Vehicle::writeTo(out);
	out << ' ' << planeName << ' ' << planePrice << ' ' << planePlace;
}