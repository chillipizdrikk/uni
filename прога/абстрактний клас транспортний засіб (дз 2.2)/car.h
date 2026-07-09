#pragma once
#include "vehicle.h"


class Car : public Vehicle
{
private:
	std::string carBrand;
	double carPrice;
	double carYear;

public:
	Car();
	Car(const std::string& maker, const std::string& brand, double price, double year);
	Car(const Car& C);
	virtual ~Car();

	virtual void print() const override;
	virtual double getPrice() const override;
	virtual char getType() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};