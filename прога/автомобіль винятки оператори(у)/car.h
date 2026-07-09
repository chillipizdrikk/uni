#pragma once
#include <string>
#include <iostream>

class BrandException
{
private:
    std::string carBrand;
public:
    BrandException(const std::string& brand) : carBrand(brand) {}
    void printBrandError() const
    {
        std::cout << "Brand (" << carBrand << ") is not accepted.\n";
    }
};


class PriceException
{
private:
    double carPrice;
public:
    PriceException(double price) : carPrice(price) {}
    void printPriceError() const
    {
        if (carPrice < 0)
        {
            std::cout << "Price can not be negative.\n";
        }
        else
        {
            std::cout << "Price (" << carPrice << " uah) is not accepted.\n";
        }
    }
};


class Car
{
private:
    std::string carBrand;
    int carYear;
    double carPrice;
    double carMarketPrice;



    void calculateMarketPrice();



public:
    Car();
    Car(const std::string& brand, int year, double price);
    Car(const Car& C);
    ~Car();



    std::string getBrand() const;
    int getYear() const;
    double getPrice() const;
    double getMarketPrice() const;



    std::string& getBrand();
    int& getYear();
    double& getPrice();



    void print() const;



    void setBrand(const std::string& brand);
    void setYear(int year);
    void setPrice(double price);



    void readFrom(std::istream& in);
    void writeTo(std::ostream& out) const;



    //friend std::ostream& operator << (std::ostream& out, const Car& C);
    //friend std::istream& operator >> (std::istream& in, Car& C);
};



std::ostream& operator << (std::ostream& out, const Car& C);
std::istream& operator >> (std::istream& in, Car& C);



void printCarsArray(const Car* arr, size_t n);
