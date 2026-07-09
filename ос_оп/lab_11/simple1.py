import math

class SimpleInterpret:

    def __init__(self, text):
        self.text = text  # копія тексту формули
        self.leks = []    # список лексем
        self.i = 0        # поточна позиція сканування

    def calc(self):
        """ Виконати повну процедуру обчислення """
        self.delblank()
        
        # 1. Лексичний аналіз (Сканер)
        scan_res = self.scanner()
        if not scan_res[0]:
            return (False, f"Синтаксична помилка на позиції {scan_res[1]}: '{self.text[scan_res[1]]}'")
        
        if not self.leks:
            return (False, "Помилка: Порожній вираз")

        # 2. Синтаксичний аналіз та інтерпретація
        try:
            ptr = 0
            # Перший елемент завжди має бути числом
            current_val = self.parse_number(self.leks[ptr])
            if current_val is None:
                return (False, f"Очікувалось число, отримано '{self.leks[ptr]}'")
            ptr += 1

            while ptr < len(self.leks):
                token = self.leks[ptr]
                ptr += 1

                # Унарні операції (постфіксні)
                if token in ['sqrt', 'sin', 'abs']:
                    if token == 'sqrt':
                        if current_val < 0: return (False, "Арифметична помилка: sqrt від від'ємного числа")
                        current_val = math.sqrt(current_val)
                    elif token == 'sin':
                        current_val = math.sin(current_val)
                    elif token == 'abs':
                        current_val = abs(current_val)
                
                # Бінарні операції
                elif token in ['+', '-', '*', '/', '%', '^', 'min', 'max']:
                    if ptr >= len(self.leks):
                        return (False, f"Очікувався операнд після '{token}'")
                    
                    next_num_token = self.leks[ptr]
                    ptr += 1
                    next_val = self.parse_number(next_num_token)
                    
                    if next_val is None:
                        return (False, f"Очікувалось число після '{token}', отримано '{next_num_token}'")

                    if token == '+': current_val += next_val
                    elif token == '-': current_val -= next_val
                    elif token == '*': current_val *= next_val
                    elif token == '/':
                        if next_val == 0: return (False, "Помилка: ділення на нуль")
                        current_val /= next_val
                    elif token == '%':
                        if next_val == 0: return (False, "Помилка: ділення на нуль (%)")
                        current_val %= next_val
                    elif token == '^': current_val = current_val ** next_val
                    elif token == 'min': current_val = min(current_val, next_val)
                    elif token == 'max': current_val = max(current_val, next_val)
                else:
                    return (False, f"Невідома операція або символ: '{token}'")

            return (True, current_val)
            
        except Exception as e:
            return (False, f"Критична помилка обчислення: {str(e)}")

    def delblank(self):
        """ Видалити пропуски """
        self.text = self.text.replace(' ', '')

    def scanner(self):
        """ Розбити текст на лексеми (числа, оператори, функції) """
        while self.i < len(self.text):
            # Перевірка на текстові операції/функції
            found_text_op = False
            for op in ['min', 'max', 'sqrt', 'sin', 'abs']:
                if self.text.startswith(op, self.i):
                    self.leks.append(op)
                    self.i += len(op)
                    found_text_op = True
                    break
            if found_text_op: continue

            # Односимвольні оператори
            if self.text[self.i] in ['+', '-', '*', '/', '%', '^']:
                self.leks.append(self.text[self.i])
                self.i += 1
                continue

            # Числа (Hex, Bin, Dec)
            if self.text.startswith('0x', self.i):
                start = self.i
                self.i += 2
                while self.i < len(self.text) and self.text[self.i] in '0123456789abcdefABCDEF':
                    self.i += 1
                self.leks.append(self.text[start:self.i])
                continue
            elif self.text.startswith('0b', self.i):
                start = self.i
                self.i += 2
                while self.i < len(self.text) and self.text[self.i] in '01':
                    self.i += 1
                self.leks.append(self.text[start:self.i])
                continue
            elif self.text[self.i].isdigit() or self.text[self.i] == '.':
                start = self.i
                while self.i < len(self.text) and (self.text[self.i].isdigit() or self.text[self.i] == '.'):
                    self.i += 1
                self.leks.append(self.text[start:self.i])
                continue

            # Якщо нічого не підійшло - помилка
            return (False, self.i)
        return (True, None)

    def parse_number(self, token):
        """ Конвертація лексеми-числа у float/int """
        try:
            if token.startswith('0x'): return int(token, 16)
            if token.startswith('0b'): return int(token, 2)
            return float(token)
        except:
            return None

if __name__ == "__main__":
    tests = [
        "10 + 5 * 2",
        "0b1010 + 0xA",
        "100 / 0",
        "25 sqrt + 5",
        "10 min 20 max 5",
        "10 - 20 abs sin"
    ]
    for t in tests:
        res = SimpleInterpret(t).calc()
        print(f"Формула: {t:20} -> Результат: {res}")
