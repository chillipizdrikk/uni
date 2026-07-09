#pragma once
#include <string>
#include <iostream>

class Car
{
private:
	std::string carBrand;
	int carYear;
	double carPrice;
	double carMarketPrice;

	void calculateMarketPrice();


public:
	Car();
	Car(const std::string& brand, int year, double price);
	Car(const Car& C);
	~Car();

	std::string getBrand() const;
	int getYear() const;
	double getPrice() const;
	double getMarketPrice() const;

	void print() const;

	void setBrand(const std::string& brand);
	void setYear(int year);
	void setPrice(double price);
};

std::ostream& operator << (std::ostream& out, const Car& C);
std::istream& operator >> (std::istream& in, Car& C);