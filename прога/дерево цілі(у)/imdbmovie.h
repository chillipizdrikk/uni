#pragma once
#include <string>
#include <iostream>



class ImdbMovie
{
private:
    std::string name;
    double rate;



public:
    ImdbMovie();
    ImdbMovie(const std::string& nm, double rt);
    ImdbMovie(const ImdbMovie& M);
    ~ImdbMovie();

    std::string getName() const;
    double getRate() const;
    std::string& getName();
    double& getRate();

    void setName(const std::string& movieName);
    void setRate(double movieRate);
    void modifyRate(double rateChange);

    void read();
    void print();
};

std::istream& operator>>(std::istream& in, ImdbMovie& M);
std::ostream& operator<<(std::ostream& out, const ImdbMovie& M);