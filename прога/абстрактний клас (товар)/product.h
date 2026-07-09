#pragma once
#include <iostream>
#include <string>


class Product
{
protected:
	std::string productMaker;


public:
	Product();
	Product(const std::string& maker);
	Product(const Product& P);
	virtual ~Product();

	virtual void print() const;
	virtual double getPrice() const = 0;
	virtual char getType() const = 0;
	virtual void readFrom(std::istream& in);
	virtual void writeTo(std::ostream& out) const;

	std::string getManufacturer() const;
	bool operator<(const Product& P) const;
};



std::istream& operator>> (std::istream& in, Product& P);
std::ostream& operator<< (std::ostream& out, const Product& P);

size_t readProductsFromFile(Product**& arr, size_t& n, const std::string& fileName);
void printProductsArray(Product**& arr, size_t n);