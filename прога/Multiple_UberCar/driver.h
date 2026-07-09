#pragma once
#include <string>

namespace taxi {
	class Driver {
	public:
		Driver();
		Driver(const std::string& name, unsigned age);
		Driver(const Driver& d);
		virtual ~Driver();

		std::string get_driver_name() const;
		virtual void PrintDriverInfo() const;

	private:
		std::string driver_name_;
		unsigned driver_age_;
	};
}