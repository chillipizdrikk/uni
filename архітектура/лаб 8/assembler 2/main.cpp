#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    bool is_right_triangle = false;

    cout << "Enter 3 sides of triangle separated by space: " << endl;//ввід сторін трикутника
    cin >> a >> b >> c;

    __asm {
        mov eax, a //копіює значення a до регістру eax
        mov ebx, b //копіює значення b до регістру ebx
        cmp eax, ebx //порівнює значення регістру eax зі значенням регістру ebx
        jnz not_right_triangle //перевіряє, чи значення eax не дорівнює значенню ebx
        mov ecx, c //копіює значення c до регістру ecx
        cmp eax, ecx //порівнює значення регістру eax зі значенням регістру ecx
        jnz not_right_triangle //перевіряє, чи значення eax не дорівнює значенню ecx
        mov is_right_triangle, 1 //якщо попередні перевірки не пройшли, то трикутник є правильним
        not_right_triangle: //якщо трикутник не є правильним то виконання переходить сюди
    }

    if (is_right_triangle) {//вивід результату
        cout << "Entered triangle is right." << endl;
    }
    else {
        cout << "Entered triangle is not right." << endl;
    }
    system("pause");
}