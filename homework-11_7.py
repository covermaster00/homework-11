class Complex:
    def __init__(self, a, b):
        self.a, self.b = self.DigitCheck(a), self.DigitCheck(b)

    def DigitCheck(self, x):
        try:
            return int(str(x))
        except:
            try:
                return float(str(x).replace(',', '.'))
            except:
                raise ValueError(f'Нечисловые данные: {x}')

    def __str__(self):
        return (f'{self.a}{"+" if self.b >= 0 else ""}{self.b}i')

    def __add__(self, other):
        return Complex(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Complex(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        return Complex(self.a * other.a - self.b * other.b, self.a * other.b + self.b * other.a)

d1 = Complex(-1, -2)
print(d1)
d2 = Complex(3, 5)
print(d2)
d3 = Complex(0.5, 0.3)
print(d3)
d4 = Complex('0,1', '0,1')
print(d4)
print(f'Операция d1 + d2 - d3 + d4 = {d1 + d2 - d3 + d4}')
print(f'Операция d1 * d2 = {d1 * d2}')
