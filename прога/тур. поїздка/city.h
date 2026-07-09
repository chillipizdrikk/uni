#pragma once
#include <string>
#include <iostream>

class City
{
private:
	std::string cityName;
	std::string countryName;

public:
	City();
	City(const std::string& city, const std::string& country);
	City(const City& C);
	~City();

	std::string getCityName() const;
	std::string getCountry() const;


	void printCityInfo() const;
	void writeCityTo(std::ostream& out) const;
	void readCityFrom(std::istream& in);

	bool operator<(const City& C) const;
};

std::istream& operator>>(std::istream& in, City& C);
std::ostream& operator<<(std::ostream& out, const City& C);