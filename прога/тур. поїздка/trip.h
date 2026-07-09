#pragma once
#include"city.h"

class Trip
{
private:
	City tripDestination;
	int tripDuration;
	double tripPrice;

public:
	Trip();
	Trip(const City& destination, int duration, double price);
	Trip(const std::string& destCity, const std::string& destCountry, int duration, double price);
	Trip(const Trip& T);
	~Trip();

	bool operator<(const Trip& T) const;

	void printTripInfo() const;
	void readTripFrom(std::istream& in);
	void writeTripTo(std::ostream& out) const;

	const City& getTripDestination() const;
	double getTripPrice() const;

};

std::istream& operator >>(std::istream& in, Trip& T);
std::ostream& operator <<(std::ostream& out, const Trip& T);

void printTripArray(const Trip* arr, size_t n);
Trip* readTripArray(const std::string& fileName, size_t& n);
void writeTripArray(const std::string& fileName, const Trip* arr, size_t n);
void sortTripArray(Trip* arr, size_t n);
bool findCityInArray(const City* arr, size_t n, const City& C);