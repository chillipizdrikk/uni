#pragma once
#include "car.h"
#include <iostream>
#include <string>
using namespace std;
struct CarNode
{
	Car data;
	CarNode* next;

	CarNode() : data(), next(nullptr) {}
	CarNode(const Car& C) : data(C), next(nullptr) {}
	CarNode(const CarNode& N) : data(N.data), next(nullptr) {}
};

struct CarList
{
	CarNode* head;


	CarList() :head(nullptr) {}
	CarList(CarNode* headNode) : head(headNode) {}
};

void addBack(CarList& list, const Car& C);
void addFront(CarList& list, const Car& C);
void deleteFromTheBeginEnd(CarList& list);
void printCarsFormatted(const CarList& list);

CarList* makeListFromFile(const string& fileName, size_t& n);
void printCarsToFile(CarList* list, const string& fileName, size_t n);

