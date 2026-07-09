#pragma once
#include <iostream>
#include <algorithm>

namespace algo {

	template <typename TIter>
	void PrintRange(TIter begin, TIter end) {
		while (begin != end) {
			std::cout << *begin << ' ';
			++begin;
		}
		std::cout << "\n";
	}

	template <typename TVal, typename TIter>
	size_t Count(const TVal& value, TIter begin, TIter end) {
		size_t counter = 0;
		while (begin != end) {
			if (*begin == value) {
				++counter;
			}
			++begin;
		}
		return counter;
	}

	template <typename TVal, typename TIter>
	TIter Find(const TVal& value, TIter begin, TIter end) {
		while (begin != end) {
			if (*begin == value) {
				return begin;
			}
			++begin;
		}
		return nullptr;
	}

	template <typename TIter, typename TFunc>
	size_t CountIf(TIter begin, TIter end, TFunc func) {
		size_t counter = 0;
		while (begin != end) {
			if (func(*begin)) {
				++counter;
			}
			++begin;
		}
		return counter;
	}

	template <typename TIter, typename TFunc>
	TIter FindIf(TIter begin, TIter end, TFunc func) {
		while (begin != end) {
			if (func(*begin)) {
				return begin;
			}
			++begin;
		}
		return nullptr;
	}

	template <typename TIter, typename TFunc>
	void ForEach(TIter begin, TIter end, TFunc func) {
		while (begin != end) {
			func(*begin);
			++begin;
		}
	}

	template <typename TIter>
	TIter FindMax(TIter begin, TIter end)
	{
		TIter maxVal = begin;
		while (++begin != end)
		{
			if (*begin > *maxVal)
			{
				maxVal = begin;
			}
		}
		return maxVal;
	}

	template <typename TIter, typename TFunc>
	TIter FindMaxIf(TIter begin, TIter end, TFunc func)
	{
		TIter maxVal = end;
		while (begin != end)
		{
			if (func(*begin))
			{
				if (maxVal == end)
				{
					maxVal = begin;
				}
				else if (*maxVal < *begin)
				{
					maxVal = begin;
				}
			}
			++begin;
		}
		return maxVal;
	}
	
	template <typename TIter, typename TValue>
	void Replace(TIter begin, TIter end, const TValue& oldValue, const TValue& newValue)
	{
		for (TIter it = begin; it != end; ++it)
		{
			if (*it == oldValue)
			{
				*it = newValue;
			}
		}
	}

	template <typename TIter, typename TFunc, typename TValue>
	void ReplaceIf(TIter begin, TIter end, TFunc func, const TValue& newValue)
	{
		for (TIter it = begin; it != end; ++it)
		{
			if (func(*it))
			{
				*it = newValue;
			}
		}
	}

}