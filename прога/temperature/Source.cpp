#include <iostream>
#include <iomanip>
using namespace std;
int main()
{
	float tF = 0;
	cout << "Temperature list\n\n";
	cout << "Degree on Celsius: " << "   " << "Degree on Fahrenheit: \n";
	for (int tC = 0; tC <= 100; tC++)
	{
		tF = (9.0 / 5.0) * tC + 32;
		cout << setw(2) << "\t" << tC << "\t\t\t" << tF << "\n";
	}
	cout << "\n";
	return 0;
}