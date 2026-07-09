#include <iostream>
#include <fstream>
#include "student.h"
using namespace std;

int main()
{
	size_t n;
	Student* allStudents = readFromFile("list.txt", n);

	Student* arr1 = new Student[n];
	Student* arr2 = new Student[n];
	Student* arr3 = new Student[n];

	size_t size1, size2, size3;

	sortByGroups(allStudents, n, arr1, size1, arr2, size2, arr3, size3);
	printStudents(allStudents, n);

	makeTheFile("pmi_16.txt", arr1, size1);
	makeTheFile("pmi_23.txt", arr2, size2);
	makeTheFile("pmi_31.txt", arr3, size3);

	size_t maxIndex = theHighestGrade(arr1, size1);
	cout << "The highest grade in PMI-16: " << arr1[maxIndex].StAvGrade << " (" << arr1[maxIndex].StName << " " << arr1[maxIndex].StSurname << ")\n\n";
	size_t minIndex = theLowestGrade(arr2, size2);
	cout << "The lowest grade in PMI-23: " << arr2[minIndex].StAvGrade << " (" << arr2[minIndex].StName << " " << arr2[minIndex].StSurname << ")\n\n";
	cout << "The average grade in PMI-31: " << totalGrade(arr3, size3) << "\n\n";


	delete[] allStudents;
	return 0;
}

