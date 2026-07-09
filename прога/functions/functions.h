#pragma once

void sayHello(int n = 1);
double addValues(double a, double b);

double modify(double val);
int modify(int val);
int modify(int val, int coef);

void changeValue(int* val, int coef);
void changeValue(int& val, int coef);