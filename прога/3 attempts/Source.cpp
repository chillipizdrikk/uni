#include <iostream>
using namespace std;

//Task 2
int main()
{
	double integer = 0;
	int answer = 0;
	cout << "Enter an integer x between 1 and 10 which other user have to guess:";
	cin >> integer;
	for (;;)
	{
		if (integer >= 1 && integer <= 10)
		{
			break;
		}
		else
		{
			cout << "This number contradicts the condition! Try again!\n";
			cout << "Enter an integer x between 1 and 10:";
			cin >> integer;
		}
	}
	system("cls");

	cout << "You have three attempts to guess the number x. This is an integer between 1 and 10.\n";
	cout << "Enter an integer x between 1 and 10:";
	double x; cin >> x;
	for (;;)
	{
		if (x < 1 || x > 10)
		{
			cout << "This number contradicts the condition! Try again!\n";
			cout << "Enter an integer x between 1 and 10:";
			cin >> x;
		}
		else
		{
			break;
		}
	}
	for (int i = 1; i < 3; ++i)
	{
		if (x != integer)
		{
			cout << "You entered the wrong number! Try again!\n";
			cout << "Enter an integer x between 1 and 10:";
			cin >> x;
		}
		else
		{
			break;
		}
	}
	for (int i = 1; i < 3; ++i)
	{
		if (x == integer)
		{
			cout << "Congratulations! You entered the correct number!\n";
			break;
		}
		else
		{
			cout << "You entered the wrong number!\nYou have run out of attempts!";
			break;
		}
	}

	
	return 0;
}