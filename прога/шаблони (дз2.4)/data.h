#pragma once
#include<iostream>
#include<string>

template<typename TDate>
class Date
{
public:
	Date();
	Date(int day, TDate month, int year);
	Date(const Date& d);
	~Date();

	void Print()const;
	void DayModify();
	void MonthModify();
	void YearModify();
	void WriteTo(std::ostream& out);

private:
	int day;
	TDate month;
	int year;
};

template <typename TDate>
Date<TDate>::Date()
	:day(0), month(), year(0)
{}

template <typename TDate>
Date<TDate>::Date(int day, TDate month, int year)
	: day(day), month(month), year(year)
{}

template <typename TDate>
Date<TDate>::Date(const Date& d)
	: day(d.day), month(d.month), year(d.year)
{}

template <typename TDate>
Date<TDate>::~Date()
{}

template <typename TDate>
void Date<TDate>::Print()const
{
	std::cout << "Day   " << "Month   " << "Year" << "\n";
	std::cout << day << "     " << month << "       " << year;
}

template <typename TDate>
void Date<TDate>::DayModify()
{
	if (day >= 5)
		day = day * (0.5);
}

template <typename TDate>
void Date<TDate>::MonthModify()
{
	if (month <= 5)
		month = month + 1;
}

template <typename TDate>
void Date<TDate>::YearModify()
{
	if (year >= 2023)
		year = year - 5;
}

template <typename TDate>
void Date<TDate>::WriteTo(std::ostream& out)
{
	out << day << "   " << month << "   " << year << "   ";
}

template <typename TDate>
std::ostream& operator << (std::ostream& out, const Date<TDate>& d) {
	d.WriteTo(out);
	return out;
}
