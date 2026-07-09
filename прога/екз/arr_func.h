#pragma once

double* createArray(double x,size_t n);
void printArray(const double* arr, size_t n);

double maxValue(const double* arr, size_t n);
size_t maxIndex(const double* arr, size_t n);
double minValueAndIndex(const double* arr, size_t n, size_t& minIndex);

//[begin, end)
double sumInRange(double* begin, double* end);