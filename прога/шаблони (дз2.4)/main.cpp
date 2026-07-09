#include<iostream>
#include"function.h"
#include"data.h"
using namespace std;

int main()
{
	cout << "-----Task 1-----\n";
	cout << "Summary for integer: " << Function<int>(37, 12, 2) << "\n";
	cout << "Summary for double: " << Function<double>(4.2, 2.7, 3);
	cout << "\n\n";

	cout << "-----Task 2-----\n";
	double arr[5] = { 5,6,7,8,9 };
	cout << "Found min value: " << MinValue<double>(arr, 5) << "\n";
	int brr[5] = { 1,2,3,4,5 };
	cout << "First found element index: " << FindValue<int>(brr, 5, 2);
	cout << "\n\n";

	cout << "-----Task 3-----\n";
	cout << "Date(int): \n";
	Date <int>date_int(8, 7, 2026);
	date_int.Print();

	cout << "\nModified date:\n";
	date_int.YearModify();
	date_int.MonthModify();
	date_int.DayModify();
	date_int.Print();

	cout << "\n\nDate(string):\n";
	Date<string>date_string(8, "July", 2030);
	date_string.Print();
	cout << "\n\n";

	return 0;
}