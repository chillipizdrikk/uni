#pragma once
#include "Points.h"
#include <fstream>

template <typename T>
CPoint<T>* ReadPoint(std::ifstream& fin)
{
	char name; fin >> name;
	T x, y; fin >> x >> y; fin.get();
	if (name == '_') return new CPoint<T>(x, y);
	else return new NamedPoint<T>(name, x, y);
}
