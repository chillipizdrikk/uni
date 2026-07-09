#include <iostream>
#include <fstream>
#include "book.h"
using namespace std;

int main()
{
	ifstream iFile("info.txt");
	size_t n; iFile >> n;
	Book* studBooks = new Book[n];
	for (size_t i = 0; i < n; ++i)
	{
		iFile >> studBooks[i];
	}

	iFile.close();
	printBookArray(studBooks, n);
	double sum = totalBookPrice(studBooks, n);
	cout << "Total price: " << sum << "\n\n";

	Book M = maxBook(studBooks, n);
	cout << "Most expensive Book: " << M << "\n\n";

	size_t index = maxBookIndex(studBooks, n);
	studBooks[index].price -= 100;
	printBookArray(studBooks, n);

	/*size_t sale;
	cout << "Enter sale %: "; cin >> sale;
	applyBookSale(studBooks, n, sale);
	printBookArray(studBooks, n);

	cout << "Sale 15%\n";
	modifyBookArray(studBooks, n, saleBook);
	printBookArray(studBooks, n);


	cout << "Increase 15%\n";
	modifyBookArray(studBooks, n, increaseBook);
	printBookArray(studBooks, n);*/

	delete [] studBooks;
	/*
	Book B1;
	B1.author = "Franko";
	B1.title = "Kameniar";
	B1.price = 520.75;
	printBook(B1);

	Book B2("Scherbyna", "Dyskretna Matematyka", 520.0);
	Book B3(B2);
	printBook(B2);
	printBook(B3);

	cout << "\nAll books\n"; 
	cout << B1 << "\n" << B2 << "\n";
	cout << B3 << "\n\n";

	cout << "\n\n Array\n";
	size_t n; cin >> n;
	Book* lib = new Book[n];
	lib[0] = B1;
	lib[1] = B2;
	lib[2] = B3;
	lib[2].title = "Artificial Intelligence";
	lib[2].price += 100.5;

	cout << "Enter Book info (auth, tit, price)\n";
	cin >> lib[3];
	cout << "Enter Book info (auth, tit, price)\n";
	cin >> lib[4];
	printBookArray(lib, n);

	delete[] lib;
	*/
	return 0;
}