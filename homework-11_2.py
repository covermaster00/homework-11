class DivisionByZero (Exception):
    def __init__(self, txt):
        self.txt = txt

a = input('Введите делимое: ')
b = input('Введите делитель: ')

try:
    if int(b) == 0:
        raise DivisionByZero('На 0 делить ни в коем случае нельзя!')
    c = int(a) / int(b)
except DivisionByZero:
    raise
except Exception:
    print('Возникла всякая прочая ошибка, но хоть на 0 не делили')
else:
    print(f'a / b = {c}')
