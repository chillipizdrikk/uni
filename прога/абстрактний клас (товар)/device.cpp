#include "device.h"
using namespace std;

Device::Device()
	: Product()
	, deviceName("")
	, devicePrice(0.0)
{}



Device::Device(const std::string& maker, const std::string& name, double price)
	: Product(maker)
	, deviceName(name)
	, devicePrice(price)
{}



Device::Device(const Device& D)
	: Product(D)
	, deviceName(D.deviceName)
	, devicePrice(D.devicePrice)
{}



Device::~Device()
{}

void Device::print() const
{
	/*
	Device: mixer Manufacturer: Bosh
	Price: __ uah
	*/
	cout << "Device: " << deviceName << " ";
	Product::print(); cout << "\n";
	cout << "Price: " << devicePrice << " uah\n\n";
}

double Device::getPrice() const
{
	return devicePrice;
}

char Device::getType() const
{
	return 'D';
}

void Device::readFrom(istream& in)
{
	Product::readFrom(in);
	in >> deviceName >> devicePrice;
}
void Device::writeTo(ostream& out) const
{
	Product::writeTo(out);
	out << ' ' << deviceName << ' ' << devicePrice;
}