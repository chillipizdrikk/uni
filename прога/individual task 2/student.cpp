#include"student.h"
#include <fstream>

Student::Student()
:StName("no name"), StSurname("no surname"), StGroup("no group"), StAvGrade(0) {}

Student::Student(string name, string surname, string group, int avgrade)
:StName(name), StSurname(surname), StGroup(group), StAvGrade(avgrade) {}

Student::Student(const Student& S)
:StName(S.StName),StSurname(S.StSurname),StGroup(S.StGroup),StAvGrade(S.StAvGrade) {}

istream& operator >> (istream& in, Student& S)
{
	in >> S.StName >> S.StSurname >> S.StGroup >> S.StAvGrade;
	return in;
}

ostream& operator << (ostream& out, const Student& S)
{
	out << "Name: " << S.StName << "\n";
	out << "Surname: " << S.StSurname << "\n";
	out << "Group: " << S.StGroup << "\n";
	out << "Grade: " << S.StAvGrade << "\n";
	return out;
}

Student* readFromFile(const string& fileName, size_t& n)
{
    ifstream iFile(fileName);
    iFile >> n;
    Student* arr = new Student[n];
    for (size_t i = 0; i < n; ++i)
    {
        iFile >> arr[i];
    }
    iFile.close();
    return arr;
}

void printStudents(const Student* arr, size_t n)
{
    cout << "All students: \n\n";
    for (size_t i = 0; i < n; ++i)
    {
        cout << arr[i] << "\n";
    }
    cout << "\n\n";
}

void sortByGroups(Student* arr, size_t n, Student*& arr1, size_t& size1, Student*& arr2, size_t& size2, Student*& arr3, size_t& size3)
{
    size1 = 0; size2 = 0; size3 = 0;
    for (size_t i = 0; i < n; ++i) 
    {
        if (arr[i].StGroup == "PMI-16") 
        {
            arr1[size1] = arr[i];
            size1++;
        }
        else if (arr[i].StGroup == "PMI-23") 
        {
            arr2[size2] = arr[i];
            size2++;
        }
        else if (arr[i].StGroup == "PMI-31") 
        {
            arr3[size3] = arr[i];
            size3++;
        }
    }
}

void makeTheFile(const string& fileName, Student* arr, size_t size) 
{
    ofstream myFile(fileName);
    for (size_t i = 0; i < size; ++i)
    {
        myFile << arr[i] << endl;
    }
    myFile.close();
}

size_t theHighestGrade(Student* arr, size_t size) 
{
    double max = arr[0].StAvGrade;
    size_t index = 0;
    for (size_t i = 0; i < size; ++i) 
    {
        if (arr[i].StAvGrade > max) 
        {
            max = arr[i].StAvGrade;
            index = i;
        }
    }
    return index;
}
size_t theLowestGrade(Student* arr, size_t size) 
{
    double min = arr[0].StAvGrade;
    size_t index = 0;
    for (size_t i = 0; i < size; ++i) 
    {
        if (arr[i].StAvGrade < min) 
        {
            min = arr[i].StAvGrade;
            index = i;
        }
    }
    return index;
}
double totalGrade(Student* arr, size_t size) 
{
    double total = 0.0;
    for (size_t i = 0; i < size; ++i) 
    {
        total += arr[i].StAvGrade;
    }
    return total;
}