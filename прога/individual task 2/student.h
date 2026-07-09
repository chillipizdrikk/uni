#pragma once
#include <iostream>
#include <string>
using namespace std;

struct Student
{
	string StName;
	string StSurname;
	string StGroup;
	int StAvGrade;

	Student();
	Student(string name,string surname, string group, int avgrade);
	Student(const Student& S);
};

istream& operator >> (istream& in, Student& S);
ostream& operator << (ostream& out, const Student& S);

Student* readFromFile(const string& fileName, size_t& n);

void printStudents(const Student* arr, size_t n);
void sortByGroups(Student* arr, size_t n, Student*& arr1, size_t& size1, Student*& arr2, size_t& size2, Student*& arr3, size_t& size3);
void makeTheFile(const string& fileName, Student* arr, size_t size);

size_t theHighestGrade(Student*, size_t);
size_t theLowestGrade(Student*, size_t);
double totalGrade(Student*, size_t);
