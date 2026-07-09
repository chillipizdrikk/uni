#include"rectangle.h"
using namespace std;

Rectangle::Rectangle() 
	:sidea(0.0), sideb(0.0){}

Rectangle::Rectangle(double a, double b)
	:sidea(a), sideb(b){}

Rectangle::Rectangle(const Rectangle& R)
	:sidea(R.sidea), sideb(R.sideb){}


std::ostream& operator << (std::ostream& out, const Rectangle& R)
{
	out << R.sidea << ' ' << R.sideb;
	return out;
}

std::istream& operator >> (std::istream& in, Rectangle& R)
{
	in >> R.sidea >> R.sideb;
	return in;
}

void printRectangle(const Rectangle& R)
{
	cout << "Rectangle info: \n" <<"side a = " << R.sidea << "\t" <<"side b = "<< R.sideb << "\n";
}

double Perimeter(const Rectangle& R)
{
	return (R.sidea + R.sideb) * 2;
}

double Square(const Rectangle& R)
{
	return R.sidea * R.sideb;
}

void fiveRectanglesArray(Rectangle* arr, size_t n)
{
	for (size_t i = 0; i < n; ++i)
	{
		cout << "Enter 2 sides of rectangle: \n" << i << ": ";
		cin >> arr[i];
	}
}


void printRectanglesArray(const Rectangle* arr, size_t n)
{
	cout << "Array of " << n << " rectangles\n";
	for (size_t i = 0; i < n; ++i)
	{
		printRectangle(arr[i]);
	}
	cout << "\n\n";
}


double totalPerimetr(const Rectangle* arr, size_t n)
{
	double Per = 0.0;
	double totPer = 0.0;
	for (size_t i = 0; i < n; ++i)
	{
		Per = (arr[i].sidea + arr[i].sideb) * 2;
		totPer += Per;
	}
	return totPer;
}


double totalSquare(const Rectangle* arr, size_t n)
{
	double Squ = 1.0;
	double totSqu = 0.0;
	for (size_t i = 0; i < n; ++i)
	{
		Squ = arr[i].sidea * arr[i].sideb;
		totSqu += Squ;
	}
	return totSqu;
}


double maxPerimeter(const Rectangle* arr, size_t n, size_t& index)
{
	double Per = 0.0;
	index = 0;
	double maxPer = (arr[0].sidea + arr[0].sideb) * 2;
	for (size_t i = 1; i < n; ++i)
	{
		Per = (arr[i].sidea + arr[i].sideb) * 2;
		if (Per > maxPer)
		{
			maxPer = Per;
			index = i;
		}
	}
	return maxPer;
	
}


double minSquare(const Rectangle* arr, size_t n, size_t& index)
{
	double Squ = 1.0;
	index = 0;
	double minSqu = arr[0].sidea * arr[0].sideb;
	for (size_t i = 1; i < n; ++i)
	{
		Squ = arr[i].sidea * arr[i].sideb;
		if (Squ < minSqu)
		{
			minSqu = Squ;
			index = i;
		}
			
	}
	return minSqu;
}

