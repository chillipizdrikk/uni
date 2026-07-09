#include "candy.h"
using namespace std;

Candy::Candy()
	: Product()
	, candyName("Romashka")
	, candyWeight(1)
	, candyPrice(0)
{}

Candy::Candy(const std::string& maker, const string& name, double weight, double kgPrice)
	: Product(maker)
	, candyName(name)
	, candyWeight(weight)
	, candyPrice(kgPrice)
{}

Candy::Candy(const Candy& C)
	: Product(C)
	, candyName(C.candyName)
	, candyWeight(C.candyWeight)
	, candyPrice(C.candyPrice)
{}

Candy::~Candy()
{}

void Candy::print() const
{
	/*
	Romashka Manufacturer: Svitoch
	Weight: 1.2 kg  Price (kg): 45 uah
	Total price: __ uah
	*/
	cout << candyName << " "; Product::print(); cout << "\n";
	cout << "Weight: " << candyWeight << " kg  ";
	cout << "Price (kg): " << candyPrice << " uah\n";
	cout << "Total price: " << getPrice() << " uah\n\n";
}

double Candy::getPrice() const
{
	return candyPrice * candyWeight;
}

char Candy::getType() const
{
	return 'C';
}

void Candy::readFrom(istream& in)
{
	Product::readFrom(in);
	in >> candyName >> candyWeight >> candyPrice;
}

void Candy::writeTo(ostream& out) const
{
	Product::writeTo(out);
	out << ' ' << candyName << ' ' << candyWeight << ' ' << candyPrice;
}