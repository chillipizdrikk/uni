#include <iostream>
#include "filling.h"
#include "choco_bar.h"
#include "candy_bar.h"

using std::cout;
using sweets::Filling;
using sweets::ChocoBar;
using sweets::CandyBar;

int main()
{
	Filling nuts("Almonds", 30);
	Filling coco("Coconut", 45);
	nuts.PrintFillingInfo();
	coco.PrintFillingInfo();
	cout << "\n\n";

	ChocoBar bar("Mars", "Caramel", 35, 32.5);
	bar.PrintFillingInfo();
	cout << "\nChoco bar: " << bar << "\n\n";

	CandyBar candy("Snickers", "Peanuts", 35, 28.1);
	CandyBar bounty("Bounty", coco, 25.7);
	candy.PrintCandyInfo();
	cout << "\nCandy bar: " << bounty << "\n\n";

	return 0;
}