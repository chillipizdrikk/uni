# Операторне виконання (Частина 3)
"""
--------- граматика мінімізованої ~Python-мови -------------------
prog        ::= stmt *
stmt        ::= assign | print_stmt
assign      ::= varname "=" arith_expr
print_stmt  ::= "print" "(" arith_expr ")"
varname     ::= letter ( letter | digit | "_" ) *

arith_expr / term / factor  – та сама граматика, що й у розширеному
інтерпретаторі (arithexpr_extended.py), але factor може містити
також varname для читання значення змінної.
-------------------------------------------------------------------
Алгоритм: кожен рядок програми розбирається окремо.
  1) Якщо рядок починається з "print(" – виконати print_stmt.
  2) Якщо рядок містить "=" (і не є порівнянням) – виконати assign.
  Таблиця змінних (словник Python) спільна для всього виконання.
"""
import math


class errorexpr(Exception):
    pass


# ====================================================================== #
#   Інтерпретатор виразів (з підтримкою змінних)                        #
# ====================================================================== #
class ExprInterpret:
    # Коди лексем
    empty        = 0
    number       = 1
    varname      = 2   # ідентифікатор змінної
    openbracket  = 3
    closebracket = 4
    add          = 5
    subtract     = 6
    multiply     = 7
    divide       = 8
    floordiv     = 9
    modulo       = 10
    power        = 11
    funcsin      = 12
    funccos      = 13

    errscan = 'Недопустима літера:\n'
    errcalc = 'Помилка обчислення:\n'

    def __init__(self, text, variables=None):
        self.text      = text
        self.leks      = []
        self.i         = 0
        self.k         = 0
        self.variables = variables if variables is not None else {}

    def calc(self):
        self.delblank()
        if not self.scanner():
            ch = self.text[self.i] if self.i < len(self.text) else '?'
            return (False, self.errscan + self.text[:self.i] + f"  '{ch}'")
        try:
            res = self.arithexpr()
        except Exception:
            temp = "".join(str(m[1]) for m in self.leks[:self.k])
            return (False, self.errcalc + temp +
                    f"  '{self.leks[self.k][1]}'")
        if self.k < len(self.leks) - 1:
            temp = "".join(str(m[1]) for m in self.leks[:self.k])
            return (False, self.errcalc + temp +
                    f"  '{self.leks[self.k][1]}'")
        return (True, res)

    def delblank(self):
        self.text = self.text.replace(' ', '')

    # --- Сканер ---
    def scanner(self):
        while self.i < len(self.text):
            c = self.text[self.i]
            if   c == '(': self.leks.append((self.openbracket, '('))
            elif c == ')': self.leks.append((self.closebracket, ')'))
            elif c == '+': self.leks.append((self.add, '+'))
            elif c == '-': self.leks.append((self.subtract, '-'))
            elif c == '%': self.leks.append((self.modulo, '%'))
            elif c == '*':
                if self.i + 1 < len(self.text) and self.text[self.i + 1] == '*':
                    self.leks.append((self.power, '**'));  self.i += 1
                else:
                    self.leks.append((self.multiply, '*'))
            elif c == '/':
                if self.i + 1 < len(self.text) and self.text[self.i + 1] == '/':
                    self.leks.append((self.floordiv, '//'));  self.i += 1
                else:
                    self.leks.append((self.divide, '/'))
            elif c.isdigit():
                self.onenumber();  self.i -= 1
            elif c.isalpha() or c == '_':
                self.scan_name();  self.i -= 1
            else:
                return False
            self.i += 1
        self.leks.append((self.empty, '#'))
        return True

    def onenumber(self):
        num = ""
        while self.i < len(self.text) and self.text[self.i].isdigit():
            num += self.text[self.i];  self.i += 1
        if self.i < len(self.text) and self.text[self.i] == '.':
            num += '.';  self.i += 1
            while self.i < len(self.text) and self.text[self.i].isdigit():
                num += self.text[self.i];  self.i += 1
        if self.i < len(self.text) and self.text[self.i] in ('e', 'E'):
            num += self.text[self.i];  self.i += 1
            if self.i < len(self.text) and self.text[self.i] in ('+', '-'):
                num += self.text[self.i];  self.i += 1
            while self.i < len(self.text) and self.text[self.i].isdigit():
                num += self.text[self.i];  self.i += 1
        if num:
            val = float(num) if ('.' in num or 'e' in num or 'E' in num) else int(num)
            self.leks.append((self.number, val))

    def scan_name(self):
        """Читати ідентифікатор: відрізняємо вбудовані функції від змінних."""
        name = ""
        while self.i < len(self.text) and (self.text[self.i].isalnum() or
                                            self.text[self.i] == '_'):
            name += self.text[self.i];  self.i += 1
        if   name == 'sin': self.leks.append((self.funcsin, 'sin'))
        elif name == 'cos': self.leks.append((self.funccos, 'cos'))
        else:               self.leks.append((self.varname, name))

    # --- Рекурсивний спуск ---
    def arithexpr(self):
        y = self.term()
        while self.leks[self.k][0] in (self.add, self.subtract):
            opr = self.leks[self.k][0];  self.GetNextToken()
            y = y + self.term() if opr == self.add else y - self.term()
        return y

    def term(self):
        z = self.factor()
        while self.leks[self.k][0] in (self.multiply, self.divide,
                                        self.floordiv, self.modulo):
            opr = self.leks[self.k][0];  self.GetNextToken()
            f = self.factor()
            if   opr == self.multiply: z = z * f
            elif opr == self.divide:   z = z / f
            elif opr == self.floordiv: z = z // f
            else:                      z = z % f
        return z

    def factor(self):
        # Унарний знак
        unary = None
        if   self.leks[self.k][0] == self.add:      unary = self.add;      self.GetNextToken()
        elif self.leks[self.k][0] == self.subtract:  unary = self.subtract; self.GetNextToken()

        code = self.leks[self.k][0]

        if code == self.number:                        # числова константа
            self.GetNextToken();  val = self.leks[self.k - 1][1]

        elif code == self.varname:                     # змінна
            name = self.leks[self.k][1];  self.GetNextToken()
            if name not in self.variables:
                raise errorexpr(f"Невизначена змінна: {name}")
            val = self.variables[name]

        elif code == self.openbracket:                 # ( arith_expr )
            self.GetNextToken()
            val = self.arithexpr()
            if self.leks[self.k][0] != self.closebracket: raise errorexpr
            self.GetNextToken()

        elif code in (self.funcsin, self.funccos):     # sin() / cos()
            func = code;  self.GetNextToken()
            if self.leks[self.k][0] != self.openbracket: raise errorexpr
            self.GetNextToken()
            arg = self.arithexpr()
            if self.leks[self.k][0] != self.closebracket: raise errorexpr
            self.GetNextToken()
            val = math.sin(arg) if func == self.funcsin else math.cos(arg)

        else:
            raise errorexpr

        # Піднесення до степеня (правоасоціативне)
        if self.leks[self.k][0] == self.power:
            self.GetNextToken()
            val = val ** self.factor()

        if unary == self.subtract:
            val = -val
        return val

    def GetNextToken(self):
        if self.k < len(self.leks) - 1: self.k += 1
        else: raise errorexpr


# ====================================================================== #
#   Інтерпретатор операторів (присвоювання + print)                      #
# ====================================================================== #
class StmtInterpret:
    """
    Виконує програму як послідовність рядків.
    Граматика:
      prog        ::= stmt *
      stmt        ::= assign | print_stmt
      assign      ::= varname "=" arith_expr
      print_stmt  ::= "print(" arith_expr ")"
    """

    def __init__(self, prog_text):
        self.prog_text = prog_text
        self.variables = {}   # таблиця змінних

    def run(self):
        """Запустити виконання всіх операторів програми."""
        lines = self.prog_text.strip().split('\n')
        for lineno, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue    # пропустити порожні рядки та коментарі
            ok, msg = self._exec_stmt(lineno, line)
            if not ok:
                print(f"[Помилка, рядок {lineno}]: {msg}")

    # --- Розбір одного оператора ---
    def _exec_stmt(self, lineno, line):
        stripped = line.replace(' ', '')

        if stripped.startswith('print(') and stripped.endswith(')'):
            return self._exec_print(line, stripped)

        if '=' in line:
            return self._exec_assign(line)

        return False, f"Невідомий оператор: {line}"

    def _exec_assign(self, line):
        """assign ::= varname "=" arith_expr"""
        eq_pos = line.index('=')
        varname  = line[:eq_pos].strip()
        expr_str = line[eq_pos + 1:].strip()

        if not varname.isidentifier():
            return False, f"Невірне ім'я змінної: '{varname}'"

        res = ExprInterpret(expr_str, self.variables).calc()
        if res[0]:
            self.variables[varname] = res[1]
            return True, res[1]
        return False, res[1]

    def _exec_print(self, line, stripped):
        """print_stmt ::= "print(" arith_expr ")" """
        expr_str = stripped[6:-1]       # вирізати між print( і )
        res = ExprInterpret(expr_str, self.variables).calc()
        if res[0]:
            print(res[1])
            return True, res[1]
        return False, res[1]


# ====================================================================== #
#   Тестові програми (частина 3)                                         #
# ====================================================================== #
PROG1 = """
# Програма 1 – базова арифметика з присвоюванням і виводом
x = 10
y = 3
q = x // y
r = x % y
print(q)
print(r)
print(x * y + 2)
sum_sq = x ** 2 + y ** 2
print(sum_sq)
"""

PROG2 = """
# Програма 2 – дійсні числа, функції, унарні операції
a = 2.5
b = 1.5e1
c = a + b
print(c)
d = 2 ** 8
e = sin(0) + cos(0)
print(d)
print(e)
neg = -3 * -4
print(neg)
half = 7 // 2 + 7 % 2
print(half)
"""


if __name__ == "__main__":
    print("=" * 55)
    print("  ПРОГРАМА 1")
    print("=" * 55)
    StmtInterpret(PROG1).run()

    print()
    print("=" * 55)
    print("  ПРОГРАМА 2")
    print("=" * 55)
    StmtInterpret(PROG2).run()
