#pragma once
#include<iostream>

template<typename TValue>
TValue FindValue(TValue* arr, size_t n, TValue val)
{
    for (size_t i = 0; i < n; ++i)
    {
        if (arr[i] == val)
        {
            return i;
        }
    }
    return -1;
}

template<typename TValue>
TValue MinValue(const TValue* arr, size_t n)
{
    size_t index = 0;
    for (size_t i = 0; i < n; ++i)
    {
        if (arr[index] > arr[i])
        {
            index = i;
        }
    }
    return arr[index];
}

template<typename TFunc>
TFunc Function(TFunc a, TFunc x, size_t n)
{
    TFunc sum = 0;
    for (size_t i = 1; i < n; ++i)
    {
        sum += pow(a, n - 1) * pow(x, n - 1);
    }
    return sum;
}
