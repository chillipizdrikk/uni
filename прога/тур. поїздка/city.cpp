#include "city.h"
using namespace std;

City::City()
	: cityName(""), countryName("")
{}

City::City(const string& city, const string& country)
	: cityName(city), countryName(country)
{}

City::City(const City& C)
	: cityName(C.cityName), countryName(C.countryName)
{}

City::~City()
{}

string City::getCityName() const
{
	return cityName;
}

string City::getCountry() const
{
	return countryName;
}

void City::printCityInfo() const
{
	cout << "City: " << cityName << " Country: " << countryName;
	cout << "\n";
}

void City::writeCityTo(ostream& out) const
{
	out << cityName << '  ' << countryName;
}

void City::readCityFrom(istream& in)
{
	in >> cityName >> countryName;
}

bool City::operator<(const City& C) const
{
	if (countryName.compare(C.getCountry()) == 0)
		return cityName.compare(C.getCityName()) < 0;
		return countryName.compare(C.getCountry()) < 0;
}

istream& operator>>(istream& in, City& C)
{
	C.readCityFrom(in);
	return in;
}

ostream& operator<<(ostream& out, const City& C)
{
	C.writeCityTo(out);
	return out;
}




