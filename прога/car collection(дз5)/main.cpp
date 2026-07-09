#include <iostream>
#include <fstream>
#include "carlist.h"
#include "car.h"
using namespace std;

int main()
{
	cout << "Task 1: \n";
	cout.width(20); cout.setf(ios_base::right, ios_base::adjustfield); cout << "Brand"; cout << " | ";
	cout.width(7); cout.setf(ios_base::left, ios_base::adjustfield); cout << "Model"; cout << " | " << "Year\n";
	cout << "            --------------------------\n";

	Car C1("Ferrari","Enzo", 1994);
	Car C2("Lamborghini", "Diablo", 1990);
	Car C3("Nissan", "Skyline", 1995);
	Car C4("Ferrari", "f70", 2013);
	Car C5("Nissan", "140sx", 2004);
	Car C6("Lamborghini", "urus", 1997);
	Car C7("Nissan", "gtr", 2007);

	printCarsFormatted(C1, 20, 7);
	printCarsFormatted(C2, 20, 7);
	printCarsFormatted(C3, 20, 7);


	cout << "\nTask 2: \n";
	CarNode N1(C1);
	CarNode N2(C2);
	CarNode N3(C3);

	N1.next = &N2;
	N2.next = &N3;

	CarList carCollection(&N1);
	addFront(carCollection, C4);
	addFront(carCollection, C5);

	addBack(carCollection, C6);
	addBack(carCollection, C7);
	printCarsFormatted(carCollection);

	deleteFromTheBeginEnd(carCollection);
	printCarsFormatted(carCollection);
	

	cout << "Task 3: \n";
	size_t listSize = 0;
	CarList* list = makeListFromFile("cars.txt", listSize);
	cout << "\n               My cars collection:" << "\n\n";
	printCarsFormatted(*list);
	printCarsToFile(list, "result.txt", listSize);


	delete[]list;
	return 0;
}
