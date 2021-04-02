import re

class Date:
    class UncorrectDataFormat(Exception):
        def __init__(self, txt=''):
            self.txt = txt

    @classmethod
    def get_digits(cls, d_str):
        try:
            if cls.valid_date(d_str):
                _ = d_str.split('-')
                return int(_[0]), int(_[1]), int(_[2])
            else:
                raise cls.UncorrectDataFormat(f'Некорректная дата {d_str}')
        except cls.UncorrectDataFormat:
            raise

    @staticmethod
    def valid_date(d_str):
        RE_DATE = re.compile(r'^\d\d-\d\d-\d{4}$')
        if bool(len(RE_DATE.findall(d_str))):
            t_ = []
            [t_.append(int(i)) for i in d_str.split('-')]
            if t_[0] > 0 and t_[1] > 0 and t_[2] > 0 and t_[2] < 10000:
                if ((t_[1] == 1 or t_[1] == 3 or t_[1] == 5 or t_[1] == 7 or t_[1] == 8 or  t_[1] == 10 or t_[1] == 12) and t_[0] > 31):
                    return False
                elif ((t_[1] == 4 or t_[1] == 6 or t_[1] == 9 or t_[1] == 11) and t_[0] > 30):
                    return False
                elif t_[1] == 2 and t_[0] > 29:
                    return False                # февраль
                elif t_[1] == 2 and t_[0] == 29 and (t_[2] % 4 != 0 or (t_[2] % 100 == 0 and t_[2] % 400 != 0)):
                    return False                # февраль в высокосном году
                else:
                    return True
            else:
                return False
        else:
            return False

    def __init__(self, d_str):
        self.day, self.mount, self.year = self.get_digits(d_str)

    def __str__(self):
        return f'{self.day:02}.{self.mount:02}.{self.year:0004}'

d1 = '29-02-1992'           # Високосный год
d2 = '31-12-1991'
d3_obj = Date('12-01-2001')
d4_obj = Date('15-11-1999')

print(f'{d1} является датой - {Date.valid_date(d1)}')
print(f'{d2} является датой - {Date.valid_date(d2)}')
print(f'{d3_obj}')
print(f'{d4_obj}')
print(Date.get_digits('29-02-1992'))
print(Date.get_digits('AA-02-1992'))