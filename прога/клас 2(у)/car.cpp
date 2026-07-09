#include "car.h"
using namespace std;



Car::Car()
    : carBrand("no brand"), carYear(0), carPrice(0.0)
{
    calculateMarketPrice();
}



Car::Car(const string& brand, int year, double price)
    : carBrand(brand), carYear(year), carPrice(price)
{
    calculateMarketPrice();
}



Car::Car(const Car& C)
    : carBrand(C.carBrand), carYear(C.carYear), carPrice(C.carPrice)
{
    calculateMarketPrice();
}


Car::~Car()
{}



string Car::getBrand() const
{
    return carBrand;
}



int Car::getYear() const
{
    return carYear;
}



double Car::getPrice() const
{
    return carPrice;
}


void Car::print() const
{
    cout << "Brand: " << carBrand;
    cout << " Year: " << carYear;
    cout << " Price: " << carPrice << " uah.";
    cout << " Market price: " << carMarketPrice << " uah.\n";
}


double Car::getMarketPrice() const
{
    return carMarketPrice;
}


void Car::setBrand(const std::string& brand)
{
    carBrand = brand;
}



void Car::setYear(int year)
{
    carYear = year;
    calculateMarketPrice();
}



void Car::setPrice(double price)
{
    carPrice = price;
    calculateMarketPrice();
}


void Car::calculateMarketPrice()
{
    carMarketPrice = (carYear >= 2021) ? (carPrice * 1.1) : carPrice;



    /*
    if (carYear >= 2021)
    {
        carMarketPrice = carPrice * 1.1;
    }
    else
    {
        carMarketPrice = carPrice;
    }
    */
}


ostream& operator << (ostream& out, const Car& C)
{
    out << C.getBrand() << ' ' << C.getYear() << ' ' << C.getPrice();
    return out;
}

istream& operator >> (istream& in, Car& C)
{
    string brand; int year; double price;
    in >> brand >> year >> price;
    C.setBrand(brand);
    C.setYear(year);
    C.setPrice(price);
}