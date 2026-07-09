class Fraction:
    def __init__(self):
        self.num = int(input('Введіть чисельник: '))
        self.den = int(input('Введіть знаменник: '))

    def __str__(self):
        if self.den == 1:
            return f"{self.num}"
        
        return f"{self.num} / {self.den}"

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def to_proper_fraction(self):
        div = self.gcd(self.num, self.den)
        self.num //= div
        self.den //= div
