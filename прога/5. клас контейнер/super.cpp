#include "super.h"

#include <fstream>
#include "candy.h"
#include "device.h"

using std::cout;
using std::ifstream;

namespace goods {
	const size_t DEFAULT_SIZE = 5;

	SuperMarket::SuperMarket()
		: market_name_("")
		, market_size_(DEFAULT_SIZE)
		, market_count_(0)
		, market_arr_(new Product* [DEFAULT_SIZE]) {
	}

	SuperMarket::SuperMarket(const std::string& name, size_t size)
		: market_name_(name)
		, market_size_(size)
		, market_count_(0)
		, market_arr_(new Product* [size]) {
	}

	SuperMarket::SuperMarket(const SuperMarket& sm)
		: market_name_(sm.market_name_)
		, market_size_(sm.market_size_)
		, market_count_(sm.market_count_)
		, market_arr_(new Product* [sm.market_size_]) {
		for (size_t i = 0; i < sm.market_count_; ++i) {
			//market_arr_[i] = sm.market_arr_[i]->Clone();
		}
	}

	SuperMarket::~SuperMarket() {
		for (size_t i = 0; i < market_count_; ++i) {
			delete market_arr_[i];
		}
		delete[] market_arr_;
	}

	void SuperMarket::AddProduct(Product* p) {
		AdjustSize();

		market_arr_[market_count_] = p;
		++market_count_;
	}

	void SuperMarket::AddFront(Product* p) {
		AdjustSize();
		for (size_t i = market_count_; i > 0; --i) {
			market_arr_[i] = market_arr_[i - 1];
		}
		market_arr_[0] = p;
		++market_count_;
	}

	void SuperMarket::PrintAll() const {
		cout << "Products from " << market_name_ << "\n";
		for (size_t i = 0; i < market_count_; ++i) {
			market_arr_[i]->Print();
		}
		cout << "Capacity: " << market_size_ << " Count: " << market_count_ << "\n";
		cout << "-----------------------------\n";
	}

	void SuperMarket::AdjustSize() {
		if (market_count_ < market_size_)
			return;

		market_size_ += DEFAULT_SIZE;
		Product** temp = new Product * [market_size_];
		for (size_t i = 0; i < market_count_; ++i) {
			temp[i] = market_arr_[i];
			market_arr_[i] = nullptr;
		}
		delete[] market_arr_;
		market_arr_ = temp;
		temp = nullptr;
	}

	void SuperMarket::ReadProductFromFile(const std::string& file_name) {
		ifstream fin(file_name);
		while (!fin.eof()) {
			char type; fin >> type;
			if (type == 'C') {
				Product* candy = new Candy();
				fin >> *candy;
				AddProduct(candy);
			}
			else if (type == 'D') {
				Product* device = new Device();
				fin >> *device;
				AddProduct(device);
			}
			else {
				char line[256];
				fin.getline(line, 256, '\n');
			}
		}
		fin.close();
	}
}