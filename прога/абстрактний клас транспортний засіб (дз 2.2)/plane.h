#pragma once
#include "vehicle.h"

class Plane : public Vehicle
{
private:
	std::string planeName;
	double planePrice;
	double planePlace;
	 

public:
	Plane();
	Plane(const std::string& maker, const std::string& name, double price, double place);
	Plane(const Plane& P);
	virtual ~Plane();

	virtual void print() const override;
	virtual double getPrice() const override;
	virtual char getType() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};