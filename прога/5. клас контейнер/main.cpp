#include <iostream>
#include "candy.h"
#include "device.h"
#include "super.h"
using std::cout;
using goods::Candy;
using goods::Device;
using goods::SuperMarket;

int main() {
	SuperMarket atb("ATB", 4);
	atb.ReadProductFromFile("goods.txt");
	//atb.AddProduct(new Candy("Romashka", 37.5, 0.9));
	//atb.AddProduct(new Device("iPhone", "Mobile", 100.7));
	//atb.AddProduct(new Candy("Milka", 27.1, 0.3));
	//atb.PrintAll();

	//cout << "Add 2 more products...\n\n";
	//atb.AddProduct(new Device("Bosch", "Mixer", 350.6));
	//atb.AddProduct(new Candy("Korivka", 30.1, 1.1));
	//atb.AddFront(new Device("Tefal", "Iron", 277.1));
	atb.PrintAll();

	return 0;
}