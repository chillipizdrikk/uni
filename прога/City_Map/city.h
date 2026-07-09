#pragma once
#include <string>
#include <iostream>

class City {
public:
    City(const std::string& name = "", unsigned people = 0);
    City(const City& c);
    ~City();

    void Print() const;
    void ReadFrom(std::istream& in);
    void WriteTo(std::ostream& out) const;

    std::string get_name() const;
    unsigned get_population() const;

    bool operator<(const City& c) const {
        return get_population() < c.get_population();
    }

private:
    std::string city_name_;
    unsigned city_people_;
};

std::istream& operator >> (std::istream& in, City& c);
std::ostream& operator << (std::ostream& out, const City& c);