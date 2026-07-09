#include "candy.h"
#include <fstream>

istream& operator>>(istream& in, Candy& C)
{
	C.readFromFile(in);
	return in;
}

ostream& operator<<(ostream& out, const Candy& C)
{
	C.writeIntoFile(out);
	return out;
}

string Candy::getName() const { return candyName; }
double Candy::getPrice() const { return candyPrice; }
double Candy::getWeight() const { return candyWeight; }
double Candy::getBoxPrice() const { return candyBoxPrice; }

void Candy::setName(const string& name) { candyName = name; }
void Candy::setPrice(double price) { candyPrice = price; }
void Candy::setWeight(double weight) { candyWeight = weight; }

void Candy::readFromFile(istream& in)
{
	in >> candyName >> candyPrice >> candyWeight;
	calculateCandyPrice();
}

void Candy::writeIntoFile(ostream& out) const
{
	out << candyName<< "\t" << candyPrice << "\t" << candyWeight;
}

void Candy::calculateCandyPrice()
{
	candyBoxPrice = candyPrice * candyWeight;
}

void Candy::printCandy() const
{
	cout << "Name: " << candyName << "\tPrice: " << candyPrice << " kg/uah ";
	cout << "\tBox weight: " << candyWeight << " kg ";
	cout << "\tBox price: " << getBoxPrice() << " uah\n";
}

void printCandyArray(const Candy* arr, size_t n)
{
	for (size_t i = 0; i < n; ++i)
	{
		arr[i].printCandy();
	}
	cout << "\n\n";
}