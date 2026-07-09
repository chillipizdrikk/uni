#include <iostream>
#include <bitset>
using namespace std;
void main()
{
	_int32 arr = 11327400;
	_int32 res = 0;
	cout << "Binary array: " << bitset<24>(arr) << endl;
	_asm
	{
		mov ecx, 8 //кількість ітерацій
		mov eax, 5 //маска - 101
	start:
		mov edx, arr //поміщаємо масив в edx
		and edx, eax //накладаємо маску
		cmp edx, eax //перевіряємо чи знайшли потрібну послідовність бітів
		jne go_next //якщо не знайшли, то переходимо на мітку go_next
		xor res, 5 //якщо знайшли, то застосовуємо "виключне або" до res
	go_next :
		shl eax, 3 //зсув на 3 біти ліворуч
		dec ecx //зменшуємо значення регістру ecx на одиницю
		jnz start //якщо ecx не дорівнює нулю, то переходимо до мітки
	}
	cout << "Result: " << bitset<3>(res) << endl;
	system("pause");
}