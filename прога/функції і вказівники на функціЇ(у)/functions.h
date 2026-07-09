#pragma once
#include <cstdio>

void printArray(const int* a, size_t n);
void printWithIndex(const int* a, size_t n);
int f(const int* a, size_t n, int y);
int maxValue(const int* a, size_t n);
size_t maxIndex(const int* a, size_t n);

// (i+1)*2
void fillArray(int* a, size_t n);

void mass_in(int m);
double* generateSinArray(size_t n);
double* generateCosArray(size_t n);

int* readArray(size_t n); //create and read
int calculateP(int x, const int* arr, size_t n); // calculate formula P
void task8(); //(void executeFunctions();)

void sayHi();
void printName(const char* name);
void printCat(const char* catName);

double addValues(double a, double b);
double multiplyValues(double a, double b);
double subtractValues(double a, double b);
double divideValues(double a, double b);

void increaseValue(int& a);
void decreaseValue(int& a);
void modifyArray(int* arr, size_t n, void(*ptrF)(int&));