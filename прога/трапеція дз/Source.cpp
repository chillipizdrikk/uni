#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
using namespace std;
//Task 1 (Option 25)
int main()
{
	cout << "Input a, b: ";
	double a, b;
	cin >> a >> b;
	cout << "Input gamma: ";
	int gamma;
	cin >> gamma;
	double g = M_PI * gamma / 180.0;
	double h = a + b / 2;                    
	double c = h / sin(g);                   
	double P = a + b + 2 * c;                
	double S = (a + b / 2) * h;               
	double d = sqrt(c * c + a * b);           
	cout << "P =" << P << '\n'
		<< "S =" << S << '\n'
		<< "h =" << h << '\n'
		<< "d =" << d << "\n";
	system("pause");


	return 0;
}