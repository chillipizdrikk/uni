#pragma once
#include "product.h"

namespace goods {
	class SuperMarket {
	public:
		SuperMarket();
		SuperMarket(const std::string& name, size_t size);
		SuperMarket(const SuperMarket& sm);
		~SuperMarket();

		void AddProduct(Product* p);
		void AddFront(Product* p);
		void PrintAll() const;
		void ReadProductFromFile(const std::string& file_name);

		double TotalPrice() const; 
		double TotalPriceOfType(char type) const; 

	private:
		void AdjustSize();

		std::string market_name_;
		size_t market_size_; // total capacity
		size_t market_count_; // number of filled elements
		Product** market_arr_; // collection
	};
}