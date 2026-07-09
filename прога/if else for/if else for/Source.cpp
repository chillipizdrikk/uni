#include <iostream>
#include <cmath>
using namespace std;
int main()
{
	/*int x;
	char t;
	do
	{
		cout << "Enter value: ";
		cin >> x;
		if ((x % 2 == 0) && (x % 5 == 0))
		{
			cout << "Even and Mult Five!\n";
		}
		else if (x % 2 == 0)
		{
			cout << "This is an even value!\n";
		}
		else if (x % 5 == 0)
		{
			cout << "Multiple Five!\n";
		}
		else
		{
			cout << "Not my value...\n";
		}
		cout << "Continue? Y/N:";
		cin >> t;
	}
	while ((t == 'Y') || (t == 'y'));
	cout << "End of program.\n";*/
	

	 /*
	  //Task 2
	  double x, y;
	  cout << "Enter x:"; cin >> x;
	  cout << "Enter y:"; cin >> y;
	  if (x >= y)
	  {
		  cout << "max is: x" << x << "\n";
		  cout << "min is: y" << y << "\n";
	  }
	  else
	  {
		  cout << "max is: y" << y << "\n";
		  cout << "max is: x" << x << "\n";
	  }
	  double sum = x + y;
	  double prod = x * y;
	  cout << " SUM: " << sum << "\n";
	  cout << " PROD: " << prod << "\n";
	  cout << " Max is: " << ((sum >= prod) ? sum : prod) << "\n";
	  */

	  /*
	 //Task 3
	 //int i;
	 for (int i = 0; i < 10; i+=2) // i = i + 2 --> i += 2
	 {
		 cout << i << " ";
		 cout << "hi!\n";
	 }
	 cout << "***\n";
	 */

	 /*
	 //Task 4
	 int n;
	 cout << "Enter power: ";
	 cin >> n;
	 int x = 1;
	 cout << "0:" << x << endl;
	 for (int i = 1; i <= n; ++i)
	 {
		 x *= 2;
		 cout << i << ":" << x << "\n";
	 }
	 cout << "\n\n";
	 */

	 /*
	  //Task 5
	 int n, x;
	 cout << "Enter n:";
	 cin >> n;
	 x = 1;
	 for (int i = 1; i <= n; ++ i)
	 {
		 x *= i;
		 cout << i << ":" << x << "\n";
	 }
	 cout << "n! is " << x << "\n\n";
	 */

	 
	 //Task 6
	 int n;
	 double a;
	 cout << "Enter n:"; cin >> n;
	 cout << "Enter a:"; cin >> a;
	 double sum = 0.0;
	 double sinX = 1.0;
	 for (int i = 1; i <= n; ++i)
	 {
		 sinX *= sin(a);
		 sum += sinX;

		 cout << i << ": sin = " << sinX << " sum = " << sum << "\n";
	 }
	 cout << "Result: " << sum << "\n\n";
	 

	 /*
	 //Task 7
	int n, a;
	cout << "Enter n:"; cin >> n;
	cout << "Enter a:"; cin >> a;
	double num = 0.0;
	double denom = 1.0;
	double sum = 0.0;
	for (int i = 1; i <= n; ++i)
	{
		num = a + cos(i * a);
		denom *= 2.0;
		double item = num / denom;
		sum += item;
		cout << i << ": item:" << item << "sum:" << sum << "\n";
	}
	cout << "Result:" << sum << "\n\n";
	*/

/*
//Task 8
double a;
cout << "Enter a:"; cin >> a;
double k = 1.0;
double elem= 1.0;
while (elem <= a)
{
	k += 1.0;
	elem += 1.0 / k;

	cout << k << ":" << elem << "\n";
}
cout << "RESULT Value:" << elem << "\n";
*/

	return 0;
}
