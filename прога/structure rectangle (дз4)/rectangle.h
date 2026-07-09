#pragma once
#include <iostream>


struct Rectangle
{
	double sidea;
	double sideb;

	Rectangle();
	Rectangle(double a, double b);
	Rectangle(const Rectangle& R);
};

std::ostream& operator << (std::ostream& out, const Rectangle& R);
std::istream& operator >> (std::istream& in, Rectangle& R);

void printRectangle(const Rectangle& R);

double Perimeter(const Rectangle& R);
double Square(const Rectangle& R);

void fiveRectanglesArray(Rectangle* arr, size_t n);
void printRectanglesArray(const Rectangle* arr, size_t n);

double totalPerimetr(const Rectangle* arr, size_t n);
double totalSquare(const Rectangle* arr, size_t n);
double maxPerimeter(const Rectangle* arr, size_t n, size_t& index);
double minSquare(const Rectangle* arr, size_t n, size_t& index);