#include "book.h"
using namespace std;

Book::Book() 
	: author("no author"), title("no title"), price(0.0)
{
	//cout << "Book - Default\n";
}
Book::Book(string auth, string tit, double pr)
	:author(auth), title(tit), price(pr)
{
	//cout << "Book - Parameter\n";
}
Book::Book(const Book& B)
	: author(B.author), title(B.title), price(B.price)
{
	//cout << "Book - Copy\n";
}

void printBook(const Book& B)
{
	cout << "Book info: " << B.author << " " << B.title << " (" << B.price << " uah)\n";
}

std::ostream& operator <<(std::ostream& out, const Book& B)
{
	out << B.author << ' ' << B.title << ' ' << B.price;
	return out;
}

void printBookArray(const Book* arr, size_t n)
{
	cout << "Library (" << n << " books)\n";
	for(size_t i=0;i<n;++i)
	{
//		cout << arr[i] << "\n";
		printBook(arr[i]);
	}
	cout << "\n\n";
}

std::istream& operator >> (std::istream& in, Book& B)
{
	in >> B.author >> B.title >> B.price;
	return in;
}

double totalBookPrice(const Book* arr, size_t n)
{
	double totSum = 0.0;
	for (size_t i = 0; i < n; ++i)
	{
		totSum += arr[i].price;
	}
	return totSum;
}

Book maxBook(const Book* arr, size_t n)
{
	Book maxB = arr[0];
	for(size_t i=1; i<n; ++i)
	{
		if(arr[i].price> maxB.price)
		{
			maxB = arr[i];
		}
	}
	return maxB;
}

size_t maxBookIndex(const Book* arr, size_t n)
{
	size_t maxI = 0;
	for (size_t i = 1; i < n; ++i)
	{
		if (arr[i] > arr[maxI])
		{
			maxI = i;
		}
	}
	return maxI;
}

bool operator > (const Book& B1, const Book& B2)
{
	return B1.price > B2.price;
}

void applyBookSale(Book* arr, size_t n, size_t sale)
{
	for (size_t i = 0; i < n; ++i)
	{
		double saleValue = arr[i].price * (double)sale * 0.01;
		arr[i].price -= saleValue;
	}
}

void saleBook(Book& B, size_t sale)
{
	double saleValue = B.price * (double)sale * 0.01;
	B.price -= saleValue;
}



void increaseBook(Book& B, size_t sale)
{
	double increaseValue = B.price * (double)sale * 0.01;
	B.price += increaseValue;
}
void modifyBookArray(Book* arr, size_t n, void (*ptrF)(Book&, size_t))
{
	for (size_t i = 0; i < n; ++i)
	{
		ptrF(arr[i], 15);
	}
}