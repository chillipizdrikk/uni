#pragma once
#include <string>
#include <iostream>

struct Book
{
	std::string author;
	std::string title;
	double price;

	Book();
	Book(std::string auth, std::string tit, double pr);
	Book(const Book& B);
};

std::ostream& operator <<(std::ostream& out, const Book& B);
std::istream& operator >> (std::istream& in, Book& B);
bool operator > (const Book& B1, const Book& B2);

void printBook(const Book& B);
void printBookArray(const Book* arr, size_t n);
double totalBookPrice(const Book* arr, size_t n);

Book maxBook(const Book* arr, size_t n);
size_t maxBookIndex(const Book* arr, size_t n);
void applyBookSale(Book* arr, size_t n, size_t sale);

void saleBook(Book& B, size_t sale);
void increaseBook(Book& B, size_t sale);
void modifyBookArray(Book* arr, size_t n, void (*ptrF)(Book&, size_t)); 
