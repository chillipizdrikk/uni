# Інтерпретація формул загальних алгебраїчних правил (розширений варіант)
"""
--------- розширене синтаксичне визначення формули ------------
arith_expr ::= term ( ( "+" | "-" ) term ) *
term       ::= factor ( ( "*" | "/" | "//" | "%" ) factor ) *
factor     ::= [( "+" | "-" )] ( number | "(" arith_expr ")" | function )
               [( "**" factor )*]
function   ::= "sin(" arith_expr ")" | "cos(" arith_expr ")"
number     ::= cipher cipher* [ "." cipher cipher* ]
               [ ("e"|"E") ["+"|"-"] cipher cipher* ]
cipher     ::= "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
--------------------------------------------------------------
Новини порівняно з базовим arithexpr.py:
  5.1  бінарні операції  //  і  %
  5.2  піднесення до степеня  **  (вищий ранг, ніж * / // %)
  5.3  функції sin() і cos()
  5.4  унарні операції  +  і  -  перед будь-яким множником/доданком
  5.5  дійсні числа: фіксована крапка і експоненціальна форма
"""
import math


class errorexpr(Exception):
    pass


class ArithexprInterpret:

    # --- Коди лексем ---
    empty        = 0   # #  – обмежувач списку
    number       = 1   # числова константа (int або float)
    openbracket  = 3   # (
    closebracket = 4   # )
    add          = 5   # +
    subtract     = 6   # -
    multiply     = 7   # *
    divide       = 8   # /
    floordiv     = 9   # //   (5.1)
    modulo       = 10  # %    (5.1)
    power        = 11  # **   (5.2)
    funcsin      = 12  # sin  (5.3)
    funccos      = 13  # cos  (5.3)

    errscan = 'Недопустима літера в тексті формули:\n'
    errcalc = 'Помилка обчислення виразу:\n'

    def __init__(self, text):
        self.text = text   # текст формули
        self.leks = []     # список лексем
        self.i    = 0      # позиція сканера в тексті
        self.k    = 0      # поточна лексема при аналізі

    # ------------------------------------------------------------------ #
    #   Головний метод                                                     #
    # ------------------------------------------------------------------ #
    def calc(self):
        self.delblank()
        if not self.scanner():
            return (False, self.errscan + self.text[:self.i] +
                    "  '" + self.text[self.i] + "'")
        res = None
        try:
            res = self.arithexpr()
        except Exception:
            temp = "".join(str(m[1]) for m in self.leks[:self.k])
            return (False, self.errcalc + temp +
                    "  '" + str(self.leks[self.k][1]) + "'")
        if self.k < len(self.leks) - 1:
            temp = "".join(str(m[1]) for m in self.leks[:self.k])
            return (False, self.errcalc + temp +
                    "  '" + str(self.leks[self.k][1]) + "'")
        return (True, res)

    # ------------------------------------------------------------------ #
    #   Підготовчий крок                                                  #
    # ------------------------------------------------------------------ #
    def delblank(self):
        """Видалити всі пропуски з тексту формули."""
        self.text = self.text.replace(' ', '')

    # ------------------------------------------------------------------ #
    #   Перший перегляд: сканер                                           #
    # ------------------------------------------------------------------ #
    def scanner(self):
        """Розбити текст на лексеми; повертає True або False при помилці."""
        while self.i < len(self.text):
            c = self.text[self.i]
            if   c == '(': self.leks.append((self.openbracket, '('))
            elif c == ')': self.leks.append((self.closebracket, ')'))
            elif c == '+': self.leks.append((self.add, '+'))
            elif c == '-': self.leks.append((self.subtract, '-'))
            elif c == '%': self.leks.append((self.modulo, '%'))
            elif c == '*':
                # ** або *
                if self.i + 1 < len(self.text) and self.text[self.i + 1] == '*':
                    self.leks.append((self.power, '**'))
                    self.i += 1          # пропустити другий *
                else:
                    self.leks.append((self.multiply, '*'))
            elif c == '/':
                # // або /
                if self.i + 1 < len(self.text) and self.text[self.i + 1] == '/':
                    self.leks.append((self.floordiv, '//'))
                    self.i += 1          # пропустити другий /
                else:
                    self.leks.append((self.divide, '/'))
            elif c.isdigit():
                self.onenumber()         # читати число (ціле або дійсне)
                self.i -= 1             # компенсація наступного i+=1
            elif c.isalpha():
                if not self.funcname(): # читати ім'я функції
                    return False
                self.i -= 1             # компенсація наступного i+=1
            else:
                return False            # недопустима літера
            self.i += 1
        self.leks.append((self.empty, '#'))   # обмежувач
        return True

    def onenumber(self):
        """Читати ціле або дійсне число (фіксована крапка / E-форма). (5.5)"""
        num = ""
        # Цілова частина
        while self.i < len(self.text) and self.text[self.i].isdigit():
            num += self.text[self.i];  self.i += 1
        # Дробова частина
        if self.i < len(self.text) and self.text[self.i] == '.':
            num += '.';  self.i += 1
            while self.i < len(self.text) and self.text[self.i].isdigit():
                num += self.text[self.i];  self.i += 1
        # Показник степеня (e або E)
        if self.i < len(self.text) and self.text[self.i] in ('e', 'E'):
            num += self.text[self.i];  self.i += 1
            if self.i < len(self.text) and self.text[self.i] in ('+', '-'):
                num += self.text[self.i];  self.i += 1
            while self.i < len(self.text) and self.text[self.i].isdigit():
                num += self.text[self.i];  self.i += 1
        if num:
            val = float(num) if ('.' in num or 'e' in num or 'E' in num) else int(num)
            self.leks.append((self.number, val))

    def funcname(self):
        """Читати ім'я функції sin або cos. (5.3)"""
        name = ""
        while self.i < len(self.text) and self.text[self.i].isalpha():
            name += self.text[self.i];  self.i += 1
        if   name == 'sin': self.leks.append((self.funcsin, 'sin'))
        elif name == 'cos': self.leks.append((self.funccos, 'cos'))
        else: return False      # невідома функція
        return True

    # ------------------------------------------------------------------ #
    #   Другий перегляд: рекурсивний спуск                               #
    # ------------------------------------------------------------------ #
    def arithexpr(self):
        """arith_expr ::= term ( ( "+" | "-" ) term ) *"""
        y = self.term()
        while self.leks[self.k][0] in (self.add, self.subtract):
            opr = self.leks[self.k][0]
            self.GetNextToken()
            y = y + self.term() if opr == self.add else y - self.term()
        return y

    def term(self):
        """term ::= factor ( ( "*" | "/" | "//" | "%" ) factor ) *   (5.1)"""
        z = self.factor()
        while self.leks[self.k][0] in (self.multiply, self.divide,
                                        self.floordiv, self.modulo):
            opr = self.leks[self.k][0]
            self.GetNextToken()
            f = self.factor()
            if   opr == self.multiply: z = z * f
            elif opr == self.divide:   z = z / f
            elif opr == self.floordiv: z = z // f
            else:                      z = z % f
        return z

    def factor(self):
        """
        factor ::= [( "+" | "-" )] ( number | "(" arith_expr ")" | function )
                   [( "**" factor )*]
        Унарний знак (5.4) → база → піднесення до степеня (5.2)
        """
        # --- Унарна операція (5.4) ---
        unary = None
        if self.leks[self.k][0] == self.add:
            unary = self.add;  self.GetNextToken()
        elif self.leks[self.k][0] == self.subtract:
            unary = self.subtract;  self.GetNextToken()

        # --- База ---
        code = self.leks[self.k][0]
        if code == self.number:                       # просте число
            self.GetNextToken()
            val = self.leks[self.k - 1][1]

        elif code == self.openbracket:                # ( arith_expr )
            self.GetNextToken()
            val = self.arithexpr()
            if self.leks[self.k][0] == self.closebracket:
                self.GetNextToken()
            else:
                raise errorexpr

        elif code in (self.funcsin, self.funccos):    # sin() або cos() (5.3)
            func = code
            self.GetNextToken()
            if self.leks[self.k][0] != self.openbracket:
                raise errorexpr
            self.GetNextToken()
            arg = self.arithexpr()
            if self.leks[self.k][0] != self.closebracket:
                raise errorexpr
            self.GetNextToken()
            val = math.sin(arg) if func == self.funcsin else math.cos(arg)

        else:
            raise errorexpr

        # --- Піднесення до степеня (5.2); правоасоціативно через рекурсію ---
        if self.leks[self.k][0] == self.power:
            self.GetNextToken()
            val = val ** self.factor()   # рекурсія = правоасоціативність

        # --- Застосувати унарний мінус (5.4) ---
        if unary == self.subtract:
            val = -val

        return val

    def GetNextToken(self):
        """Перейти до наступної лексеми або згенерувати помилку."""
        if self.k < len(self.leks) - 1:
            self.k += 1
        else:
            raise errorexpr


# ====================================================================== #
#   Тести (частина 1 і 2)                                                #
# ====================================================================== #
if __name__ == "__main__":
    tests = [
        # Базові (частина 1)
        ("49 - 108 / (6 + 11) * (100 - 94)",  "≈10.88"),
        # 5.1  // і %
        ("17 // 5",                            "3"),
        ("17 % 5",                             "2"),
        ("100 // 7 + 100 % 7",                 "14+2=16"),
        # 5.2  **
        ("2 ** 10",                            "1024"),
        ("2 ** 3 ** 2",                        "2^9=512  (правоасоціативно)"),
        # 5.3  sin, cos
        ("sin(0)",                             "0.0"),
        ("cos(0)",                             "1.0"),
        ("sin(3) * sin(3) + cos(3) * cos(3)",  "≈1.0"),
        # 5.4  унарні + і -
        ("-2 + -6",                            "-8"),
        ("4 * -2",                             "-8"),
        ("-3 ** 2",                            "-9  (унарний після **)"),
        ("4 * +8",                             "32"),
        # 5.5  дійсні числа
        ("45.02 + 0.98",                       "46.0"),
        ("1.0e-5 * 1e5",                       "1.0"),
        ("28e2 / 4",                           "700.0"),
        # Комбіновані
        ("sin(0) + cos(0) * 2 ** 3",          "8.0"),
        ("-1.5e1 + 17 // 3 * 2",              "-15+10=-5.0"),
    ]

    print("=" * 60)
    print("  ТЕСТИ розширеного інтерпретатора")
    print("=" * 60)
    for formula, expected in tests:
        res = ArithexprInterpret(formula).calc()
        status = "OK" if res[0] else "ERR"
        val    = res[1] if res[0] else f"[{res[1]}]"
        print(f"[{status}]  {formula}")
        print(f"       результат={val}   (очікується: {expected})")
        print()
