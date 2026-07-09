#include<iostream>
#include"car.h"
#include"list.h"
#include"tools.h"
#include<fstream>
using namespace std;
using namespace algo;
using algo::List;

int main()
{
	List<int>num;
	List<int>::Iterator num_it;

	num.AddBack(2);
	num.AddBack(4);
	num.AddBack(5);
	num.AddBack(7);
	num.AddBack(5);
	num.AddBack(12);
	num_it = FindMax(num.Begin(), num.End());
	cout << "Max value:" << *num_it;
	cout << "\n\n";

	List<int>::Iterator max_it;
	num.AddBack(10);
	num.AddBack(20);
	cout << "Max value % 2: \n";
	max_it = FindMaxIf(num.Begin(), num.End(), [](int num) {
		return num % 2 == 0;
		});
	cout << *max_it;
	cout << "\n\n";

	cout << "Replace 5 with 99: \n";
	Replace(num.Begin(), num.End(), 5, 99);
	for_each(num.Begin(), num.End(), [](const auto& elem) {
		cout << elem << " ";
		});
	cout << "\n\n";

	List<Car>car;
	ifstream fin("garage.txt");
	while (!fin.eof())
	{
		Car c;
		fin >> c;
		car.AddBack(c);
	}
	fin.close();
	cout << "All garage: \n";
	PrintRange(car.Begin(), car.End());
	cout << "\n";

	List<Car>::Iterator car_it;
	car_it = FindMax(car.Begin(), car.End());
	cout << "The most expensive car: ";
	cout << (*car_it).get_brand() << "  ";
	cout << (*car_it).get_price() << "  \n";

	cout << "\n";
	cout << "Replacing with BMW: \n";
	Replace(car.Begin(), car.End(), Car{ "Audi", 0 }, Car{ "BMW", 20500 });
	Replace(car.Begin(), car.End(), Car{ "Fiat", 0}, Car{"BMW", 30250 });
	Replace(car.Begin(), car.End(), Car{ "Seat", 0 }, Car{ "BMW", 46500 });
	PrintRange(car.Begin(), car.End());


	return 0;
}