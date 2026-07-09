#pragma once
#include <iostream>
#include <string>

class Vehicle
{
protected:
	std::string vehicleMaker;
public:
	Vehicle();
	Vehicle(const std::string& maker);
	Vehicle(const Vehicle& V);
	virtual ~Vehicle();

	virtual void print() const;
	virtual double getPrice() const = 0;
	virtual char getType() const = 0;
	virtual void readFrom(std::istream& in);
	virtual void writeTo(std::ostream& out) const;

	std::string getManufacturer() const;
	bool operator<(const Vehicle& V) const;
	
};

std::istream& operator>> (std::istream& in, Vehicle& V);
std::ostream& operator<< (std::ostream& out, const Vehicle& V);

size_t readVehiclesFromFile(Vehicle**& arr, size_t& n, const std::string& fileName);
void printVehiclesArray(Vehicle**& arr, size_t n);
