#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <iostream>
#include <string>
#include <stack>
using namespace std;

int getPrecedence(char oper) { //функція для визначення пріоритету
    if (oper == '+' || oper == '-') {
        return 1;
    }
    else if (oper == '*' || oper == '/') {
        return 2;
    }
    else {
        return 0;
    }
}

string toRPN(string input) { //функція перетворює інфіксну нотацію на зворотню польську нотацію 
    stack<char> operators;
    string output; 

    for (int i = 0; i < input.length(); i++) { //цикл для проходження по вхідному рядку зліва направо
        char c = input[i];
        if (isdigit(c)) { //якщо символ, який ми читаємо є цифрою
            string numStr;
            while (i < input.length() && isdigit(input[i])) { //зчитуємо все число
                numStr += input[i];
                i++;
            }
            i--;
            output += numStr + " "; //додаємо число до вихідного рядка
        }
        else if (c == '(') { //якщо символ, який ми читаємо є відкриваючою дужкою, то додаємо його до стеку операторів
            operators.push(c);
        }
        else if (c == ')') { //якщо символ, який ми читаємо є закриваючою дужкою, то видаляємо всі оператори зі стеку поки не зустрінемо відкриваючу дужку
            while (!operators.empty() && operators.top() != '(') {
                output += operators.top();
                output += " ";
                operators.pop();
            }
            if (!operators.empty()) { //видаляємо відкриваючу дужку
                operators.pop();
            }
        }
        else {  //якщо символ, який ми читаємо є оператором, то дивимось на пріоритет
            int currPrec = getPrecedence(c);
            while (!operators.empty() && operators.top() != '(' && getPrecedence(operators.top()) >= currPrec) { 
                //оператори, які мають більший або рівний пріоритет за поточний оператор видаляємо і додаємо їх до вихідного рядка
                output += operators.top();
                output += " ";
                operators.pop();
            }
            operators.push(c); //додаємо поточний оператор до стеку операторів
        }
    }

    while (!operators.empty()) { //всі оператори зі стеку,що залишились додаємо до вихідного рядка
        output += operators.top();
        output += " ";
        operators.pop();
    }

    return output; //повертаємо отриманий вихідний рядок в зворотній польській нотації
}


int evaluateRPN(string rpn) { //функція, що обчислює отриманий вихідний рядок зворотньої польської нотації
    stack<int> s;

    for (int i = 0; i < rpn.length(); i++) {
        if (isdigit(rpn[i])) { //якщо символ є цифрою, то зчитуємо все число
            string numtoStr;
            while (i < rpn.length() && (isdigit(rpn[i]) || rpn[i] == '-')) {
                numtoStr += rpn[i];
                i++;
            }
            i--;
            s.push(stoi(numtoStr)); //додавання числа до стеку після перетворення його в int
        }
        else if (rpn[i] == '+' || rpn[i] == '-' || rpn[i] == '*' || rpn[i] == '/') {  //якщо символ є оператором, то беремо два останніх числа зі стеку
            int b = s.top(); s.pop();
            int a = s.top(); s.pop();
            if (rpn[i] == '+') s.push(a + b); //виконання потрібної операції і додавання результату до стеку
            else if (rpn[i] == '-') s.push(a - b);
            else if (rpn[i] == '*') s.push(a * b);
            else if (rpn[i] == '/') s.push(a / b);
        }
    }

    return s.top(); //повернення останнього елемента у стеці, який є результатом обчислень
}

TEST_CASE("getPrecedence") {
    CHECK_EQ(getPrecedence('+'), 1);
    CHECK_EQ(getPrecedence('-'), 1);
    CHECK_EQ(getPrecedence('*'), 2);
    CHECK_EQ(getPrecedence('/'), 2);
    CHECK_EQ(getPrecedence('^'), 0);
}

TEST_CASE("toRPN") {
    CHECK_EQ(toRPN("3+4"), "3 4 + ");
    CHECK_EQ(toRPN("(3+4)*5"), "3 4 + 5 * ");
    CHECK_EQ(toRPN("1+2*3+4"), "1 2 3 * + 4 + ");
    CHECK_EQ(toRPN("2*(3+4)"), "2 3 4 + * ");
}

TEST_CASE("evaluateRPN") {
    CHECK_EQ(evaluateRPN("3 4 + "), 7);
    CHECK_EQ(evaluateRPN("3 4 + 5 * "), 35);
    CHECK_EQ(evaluateRPN("1 2 3 * + 4 + "), 11);
    CHECK_EQ(evaluateRPN("2 3 4 + * "), 14);
}
