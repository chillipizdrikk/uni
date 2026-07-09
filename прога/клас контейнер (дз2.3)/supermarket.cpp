#include "supermarket.h"
#include <fstream>
#include "candy.h"
#include "device.h"
using std::cout;
using std::ifstream;



namespace goods {
    const size_t DEFFAULT_SIZE = 5;
    SuperMarket::SuperMarket()
        : market_name_("")
        , market_size_(DEFFAULT_SIZE)
        , market_count_(0)
        , market_arr_(new Product* [DEFFAULT_SIZE]) {
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
            cout << "\n";
        }
        cout << "Capacity: " << market_size_ << " Count: " << market_count_ << "\n";
        cout << "-----------------------------\n";
    }

    void SuperMarket::AdjustSize() {
        if (market_count_ < market_size_)
            return;

        market_size_ += DEFFAULT_SIZE;
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

    double SuperMarket::TotalPrice() const {
        double total = 0.0;
        for (size_t i = 0; i < market_count_; ++i)
        {
            total += market_arr_[i]->get_price();
        }
        return total;
    }

     double SuperMarket::TotalPriceOfType(char type) const {
         double total = 0.0;
         if (type == 'C') {
             for (size_t i = 0; i < market_count_; ++i)
             {
                 if (market_arr_[i]->get_type() == 'C') {
                     total += market_arr_[i]->get_price();
                 }
             }
         }
         else if (type == 'D') {
             for (size_t i = 0; i < market_count_; ++i)
             {
                 if (market_arr_[i]->get_type() == 'D') {
                     total += market_arr_[i]->get_price();
                 }
             }
         }
         else {
             cout << "Error\n";
         }
         return total;
     }
}