#include <iostream>
using namespace std;

int y1_values[5]; // Масив для зберігання значень y1
int y2_values[5]; // Масив для зберігання значень y2

int main() {

    int a, x;
    cout << "Input a:"; cin >> a;
    cout << "Input x:"; cin >> x;

    _asm {
        lea eax, y1_values //Завантаження адреси масиву y1_values в регістр eax
        push eax //Зберігання адреси масиву y1_values у стеку
        mov ecx, 5 //Завантаження лічильника циклу

        start:
        mov ebx, 3 //Завантажуємо значення 3 в регістр ebx
            sub ebx, ecx 
            cmp ebx, 3
            jge greater_equal_three; //Якщо ebx >= 3, перехід до мітки greater_equal_three
            add ebx, 7
            jmp result //Безумовний перехід до мітки result

            greater_equal_three :
        mov eax, a 
            cmp eax, 0 //Порівнюємо з 0
            jl a_less_zero //Якщо eax < 0, перехід до мітки a_less_zero
            mov ebx, x
            add ebx, eax //Додаємо eax до ebx
            mov ebx, eax
            jmp result //Безумовний перехід до мітки result

            a_less_zero :
        mov ebx, -2 
            imul ebx //Перемножуємо значення ebx на eax
            mov ebx, eax

            result :
        pop eax
            mov[eax], ebx //Записуємо значення ebx в масив y1_values за адресою eax
            add eax, 4 //Додаємо 4 до eax для переходу до наступного елемента масиву
            push eax //Зберігаємо нову адресу масиву y1_values у стеку
            dec ecx //Зменшуємо значення лічильника циклу(ecx) на 1
            cmp ecx, 0 //Порівнюємо значення лічильника циклу зі значенням 0
            jg start //Якщо ecx > 0, перехід до мітки start

            mov eax, offset y2_values //Завантажуємо адресу масиву y2_values в регістр eax
            push eax //Зберігаємо адресу масиву y2_values у стеку
            mov ecx, 5 //Завантажуємо лічильник циклу зі значенням 5 в регістр ecx

            start2 :
        mov ebx, 1 //Завантажуємо значення 1 в регістр ebx
            sub ebx, ecx //Віднімаємо значення лічильника циклу(ecx) від ebx
            mov eax, 5 //Завантажуємо значення 5 в регістр eax
            cmp ebx, eax //Порівнюємо ebx зі значенням eax
            je greater_five; Якщо ebx = eax, перехід до мітки greater_five
            add eax, a //Додаємо значення змінної a до eax
            mov ebx, eax
            jmp result2 //Безумовний перехід до мітки result2

            greater_five :
        mov ebx, 1 //Завантажуємо значення 1 в регістр ebx
            jmp result2 //Безумовний перехід до мітки result2

            result2 :
        pop eax
            mov[eax], ebx //Записуємо значення ebx в масив y2_values за адресою eax
            add eax, 4 //Додаємо 4 до eax для переходу до наступного елемента масиву
            push eax //Зберігаємо нову адресу масиву y2_values у стеку
            dec ecx //Зменшуємо значення лічильника циклу(ecx) на 1
            cmp ecx, 0 //Порівнюємо значення лічильника циклу зі значенням 0
            jg start2 //Якщо ecx > 0, перехід до мітки start2

            mov eax, offset y1_values //Завантажуємо адресу масиву y1_values в регістр eax
            mov ebx, offset y2_values //Завантажуємо адресу масиву y2_values в регістр ebx
            mov ecx, 5 //Завантажуємо лічильник циклу зі значенням 5 в регістр ecx
    }

    for (int i = 0; i < 5; ++i) {
        cout << y1_values[i] << '\n';
    }
    system("pause");
}