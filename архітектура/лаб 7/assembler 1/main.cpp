#include <iostream>
using namespace std;
char FORMAT[] = "%s %s %s %s %s %s\n";
char DESIGNED[] = "Designed";
char BY[] = "by";
char NAME[] = "Marta";
char SURNAME[] = "Tryhub";
char COMA[] = ",";
char YEAR[] = "2023";
void main() {
	__asm { // початок асемблерного коду
		mov eax, offset YEAR // присвоєння
		push eax // заштовхування в стек
		mov eax, offset COMA
		push eax
		mov eax, offset SURNAME
		push eax
		mov eax, offset NAME 
		push eax
		mov eax, offset BY
		push eax
		mov eax, offset DESIGNED
		push eax
		mov eax, offset FORMAT
		push eax
		mov edi, printf // вивід тексту на консоль
		call edi 
		pop ebx // очищення стеку
		pop ebx
		pop ebx
		pop ebx
		pop ebx
		pop ebx
		pop ebx
	} // кінець асемблерного коду
	system("pause");
}


