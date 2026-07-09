#pragma once
#include<iostream>

class Triangle
{
private:
	double sideA;
	double sideB;
	double sideC;


public:
	Triangle();
	Triangle(double a, double b, double c);
	Triangle(const Triangle& T);
	~Triangle();

	bool operator < (const Triangle& T) const;

	double perimeter() const;
	double square() const;
	void scaleBy(double coef);
	void readFrom(std::istream& in);
	void writeTo(std::ostream& out) const;
};

std::istream& operator >> (std::istream& in, Triangle& T);
std::ostream& operator << (std::ostream& out, const Triangle& T);