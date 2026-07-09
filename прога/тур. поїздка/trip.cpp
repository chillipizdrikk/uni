#include "trip.h"
#include <fstream>
using namespace std;

Trip::Trip()
    : tripDestination(), tripDuration(0), tripPrice(0.0)
{}

Trip::Trip(const City& destination, int duration, double price)
    : tripDestination(destination), tripDuration(duration), tripPrice(price)
{}

Trip::Trip(const string& destCity, const string& destCountry, int duration, double price)
    : tripDestination(destCity, destCountry), tripDuration(duration), tripPrice(price)
{}



Trip::Trip(const Trip& T)
    : tripDestination(T.tripDestination), tripDuration(T.tripDuration), tripPrice(T.tripPrice)
{}



Trip::~Trip()
{}



bool Trip::operator< (const Trip& T) const
{
    return tripPrice < T.getTripPrice();
}



void Trip::printTripInfo() const
{
    cout << "--- Trip Info ---\n";
    tripDestination.printCityInfo();
    cout << "Duration: " << tripDuration << " days\n";
    cout << "Price: " << tripPrice << " uah\n";
    cout << "--- --- ---\n\n";
}



void Trip::readTripFrom(istream& in)
{
    in >> tripDestination >> tripDuration >> tripPrice;
}



void Trip::writeTripTo(ostream& out) const
{
    out << tripDestination << ' ' << tripDuration << ' ' << tripPrice;
}

const City& Trip::getTripDestination() const
{
    return tripDestination;
}

double Trip::getTripPrice() const
{
    return tripPrice;
}

istream& operator>> (istream& in, Trip& T)
{
    T.readTripFrom(in);
    return in;
}

ostream& operator<< (ostream& out, const Trip& T)
{
    T.writeTripTo(out);
    return out;
}

void printTripArray(const Trip* arr, size_t n)
{
    cout << "Travel Agency PMI-16\n";
    for (size_t i = 0; i < n; ++i)
    {
        arr[i].printTripInfo();
    }
    cout << "\n";
}

Trip* readTripArray(const std::string& fileName, size_t& n)
{
    ifstream iFile(fileName);
    iFile >> n;
    Trip* arr = new Trip[n];



    for (size_t i = 0; i < n; ++i)
    {
        iFile >> arr[i];
    }



    iFile.close();
    return arr;
}

void writeTripArray(const std::string& fileName, const Trip* arr, size_t n)
{
    ofstream oFile(fileName);
    oFile << n << "\n";
    for (size_t i = 0; i < n; ++i)
    {
        oFile << arr[i] << "\n";
    }



    oFile.close();
}

void sortTripArray(Trip* arr, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        size_t M = i;
        for (size_t j = i + 1; j < n; ++j)
        {
            if (arr[j] < arr[M])
                M = j;
        }



        if (M != i)
        {
            Trip temp = arr[i];
            arr[i] = arr[M];
            arr[M] = temp;
        }
    }
}

bool findCityInArray(const City* arr, size_t n, const City& C)
{
    for (size_t i = 0; i < n; ++i)
    {
        if (arr[i].getCityName() == C.getCityName() &&
            arr[i].getCountry() == C.getCountry())
            return true;
    }
    return false;
}