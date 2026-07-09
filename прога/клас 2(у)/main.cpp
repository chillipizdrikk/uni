#include <iostream>
#include"car.h"
using namespace std;

int main()
{
	Car C1;
	Car C2("Seat", 2022, 50452);
	Car C3(C2);

	C1.setBrand("Fiat");
	C1.setYear(1985);
	C1.setPrice(90500);

	C3.setYear(2001);

	cout << "All cars:\n";
	cout << C1.getBrand() << "  " << C1.getPrice() << "  " << C1.getYear() << "\n";
	cout << C2.getBrand() << "  " << C2.getPrice() << "  " << C2.getYear() << "\n";
	cout << C3.getBrand() << "  " << C3.getPrice() << "  " << C3.getYear() << "\n";


	cout << "\n\nCar info\n";
	C1.print(); C2.print(); C3.print();



	cout << "\nCar prices\n";
	cout << "Original: " << C1.getPrice() << " uah. Market: " << C1.getMarketPrice() << " uah\n";
	cout << "Original: " << C2.getPrice() << " uah. Market: " << C2.getMarketPrice() << " uah\n";





	return 0;
}