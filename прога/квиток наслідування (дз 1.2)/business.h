#pragma once
#include "ticket.h"

class BusinessTicket : public Ticket
{
private:
	unsigned percentageValue;

public:
	BusinessTicket();
	BusinessTicket(const std::string& name, double distance, double price, unsigned percentage);
	BusinessTicket(const BusinessTicket& T);
	virtual ~BusinessTicket();

	virtual void print() const override;
	virtual double totalPrice() const override;
	virtual void readFrom(std::istream& in) override;
	virtual void writeTo(std::ostream& out) const override;
};
