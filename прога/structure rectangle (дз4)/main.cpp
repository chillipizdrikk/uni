#include<iostream>
#include<fstream>
#include"rectangle.h"
using namespace std;

int main()
{
	Rectangle R;
	cout << "Enter side a of rectangle: \n";
	cin >> R.sidea;
	cout << "Enter side b of rectangle: \n";
	cin >> R.sideb;
	
	printRectangle(R);
	cout << "Your rectangle perimetr: " << Perimeter(R) <<"\n";
	cout << "Your rectangle square: " << Square(R) << "\n\n";

	cout << "Array of 5 rectangles:\n";
	size_t n = 5;
	Rectangle* sidesrec = new Rectangle[n];
	fiveRectanglesArray(sidesrec, n);
	printRectanglesArray(sidesrec, n);

	size_t minindex = 0, maxindex = 0;
	cout << "Summary of all rectangles perimeters: " << totalPerimetr(sidesrec, n) << "\n"; 
	cout << "Summary of all rectangles squres: " << totalSquare(sidesrec, n) << "\n";
	cout << "Max perimeter of your rectangles: " << maxPerimeter(sidesrec, n, maxindex) << " (rectangle #" << maxindex << ")\n";
	cout << "Min square of your rectangles: " << minSquare(sidesrec, n, minindex) << "(rectangle #" << minindex << ")\n";

	delete[] sidesrec;
	return 0;
}