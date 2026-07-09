#include"carlist.h"
#include"car.h"
#include<fstream>
#include<string>

void addBack(CarList& list, const Car& C)
{
	if (list.head == nullptr)
	{
		list.head = new CarNode(C);
		return;
	}
	CarNode* now = list.head;
	while (now->next != nullptr)
	{
		now = now->next;
	}
	now->next = new CarNode(C);
}
void addFront(CarList& list, const Car& C)
{
	if (list.head == nullptr)
	{
		list.head = new CarNode(C);
		return;
	}
	CarNode* firstNode = new CarNode(C);
	firstNode->next = list.head;
	list.head = firstNode;
	firstNode = nullptr;
}
void printCarsFormatted(const CarList& list)
{
	if (list.head == nullptr)
	{
		cout << "Sorry, your list is empty.\n";
		return;
	}
	int maxBrandWidth = 20;
	int maxModelWidth = 5;
	CarNode* now = list.head;
	while (now != nullptr)
	{
		int nowBrandWidth = now->data.CarBrand.length();
		int nowModelWidth = now->data.CarModel.length();
		if (nowBrandWidth > maxBrandWidth) maxBrandWidth = nowBrandWidth;
		if (nowModelWidth > maxModelWidth) maxModelWidth = nowModelWidth;

		now = now->next;
	}

	cout.width(maxBrandWidth); cout.setf(ios_base::right, ios_base::adjustfield); cout << "Brand"; cout << " | ";
	cout.width(maxModelWidth); cout.setf(ios_base::left, ios_base::adjustfield); cout << "Model"; cout << " | " << "Year\n";
	cout << "            --------------------------\n";

	now = list.head;
	while (now != nullptr)
	{
		printCarsFormatted(now->data, maxBrandWidth, maxModelWidth);
		now = now->next;
	}
	cout << "\n\n";
}


void deleteFromTheBeginEnd(CarList& list)
{
	if (list.head == nullptr)
	{
		cout << "Sorry, your list is empty.\n";
		return;
	}
	list.head = list.head->next;
	CarNode* now = list.head;
	while (now->next->next != nullptr)
	{
		now = now->next;
	}
	now->next = nullptr;
}

CarList* makeListFromFile(const string& fileName, size_t& n)
{
	ifstream iFile(fileName);
	iFile >> n;
	CarList* list = new CarList();
	Car tempCar;
	for (size_t i = 0; i < n; ++i)
	{
		iFile >> tempCar;
		addBack(*list, tempCar);
	}
	iFile.close();
	return list;
}

void printCarsToFile(CarList* list, const string& fileName, size_t n)
{
	ofstream iFile(fileName);
	CarNode* currentNode = list->head;
	for (size_t i = 0; i < n; ++i)
	{
		if (currentNode->data.CarYear > 2000) 
		{
			iFile << currentNode->data;
		}
		currentNode = currentNode->next;
	}
	iFile.close();
}