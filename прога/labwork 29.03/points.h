#pragma once
#include <iostream>

template <typename TNum>
class CPoint
{
	TNum x, y;
public:
	CPoint(TNum a, TNum b) :x(a), y(b) {}
	CPoint() :x(0), y(0) {} // TNum(0) ???
	TNum get_x() const { return x; }
	TNum get_y() const { return y; }
	virtual void print_on(std::ostream& os) const
	{
		os << '(' << x << "; " << y << ')';
	}
	double distance(const CPoint& p) const;
	CPoint operator+(const CPoint& p) const
	{
		return CPoint(this->x + p.x, this->y + p.y);
	}
	CPoint operator-(const CPoint& p) const
	{
		return CPoint(this->x - p.x, this->y - p.y);
	}
};

template<typename TNum>
inline double CPoint<TNum>::distance(const CPoint& p) const
{
	TNum _y = y - p.y;
	return sqrt(pow(x - p.x, 2) + (double)_y * _y);
}

template<typename TNum>
std::ostream& operator<<(std::ostream& os, const CPoint<TNum>& A)
{
	A.print_on(os); return os;
}
//template<>
std::ostream& operator<<(std::ostream& os, const CPoint<double>& A)
{
	os << std::showpoint;
	A.print_on(os); return os;
}

template<typename TNum>
CPoint<TNum> operator*(const CPoint<TNum>& p, TNum n)
{
	return CPoint<TNum>(p.get_x() * n, p.get_y() * n);
}

template <typename T>
class NamedPoint :public CPoint<T>
{
private:
	char name;
public:
	NamedPoint(char n, T a, T b) :CPoint<T>(a, b), name(n) {}
	NamedPoint() :CPoint<T>(), name('O') { }
	char get_name() const { return name; }
	void print_on(std::ostream& os) const override
	{
		os << name;
		CPoint<T>::print_on(os);
	}
};