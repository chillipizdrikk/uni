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
    if (brand.empty())
        throw BrandException(brand);
    if (brand == "Nyva")
        throw BrandException(brand);



    carBrand = brand;
}



void Car::setYear(int year)
{
    carYear = year;
    calculateMarketPrice();
}



void Car::setPrice(double price)
{
    if (price < 0 || price > 100000)
        throw PriceException(price);



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



// Option 1 - via getters & setters
/*
ostream& operator << (ostream& out, const Car& C)
{
    out << C.getBrand() << ' ' << C.getYear() << ' ' << C.getPrice();
    return out;
}



istream& operator >> (istream& in, Car& C)
{
    string brand; in >> brand; C.setBrand(brand);
    int year; in >> year; C.setYear(year);
    double price; in >> price; C.setPrice(price);
    return in;
}
*/



// Option 2 - via friend
/*
ostream& operator << (ostream& out, const Car& C)
{
    out << C.carBrand << ' ' << C.carYear << ' ' << C.carPrice;
    return out;
}



istream& operator >> (istream& in, Car& C)
{
    in >> C.carBrand >> C.carYear >> C.carPrice;
    C.calculateMarketPrice();
    return in;
}
*/



std::string& Car::getBrand()
{
    return carBrand;
}



int& Car::getYear()
{
    return carYear;
}



double& Car::getPrice()
{
    return carPrice;
}



// Option 3 - via getters
/*
ostream& operator << (ostream& out, const Car& C)
{
    out << C.getBrand() << ' ' << C.getYear() << ' ' << C.getPrice();
    return out;
}



istream& operator >> (istream& in, Car& C)
{
    in >> C.getBrand() >> C.getYear() >> C.getPrice();
    // market price not initialized
    C.setYear(C.getYear());
    return in;
}
*/



void Car::readFrom(std::istream& in)
{
    in >> carBrand >> carYear >> carPrice;
    calculateMarketPrice();
}



void Car::writeTo(std::ostream& out) const
{
    out << carBrand << ' ' << carYear << ' ' << carPrice;
}



ostream& operator << (ostream& out, const Car& C)
{
    C.writeTo(out);
    return out;
}



istream& operator >> (istream& in, Car& C)
{
    C.readFrom(in);
    return in;
}




void printCarsArray(const Car* arr, size_t n)
{
    for (size_t i = 0; i < n; ++i)
    {
        arr[i].print();
    }
    cout << "\n\n";
}