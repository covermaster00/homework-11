class NoDigitList (Exception):
    def __init__(self, txt):
        self.txt = txt
        print(txt)


lst = []
while True:
    x = input('Введите цифру (stop - для выхода): ')
    if x == 'stop':
        break
    try:
        lst.append(int(x))
    except:
        try:
            lst.append(float(x.replace(',','.')))
        except:
            raise NoDigitList('Цифру же, Кэп, просили же!')
        finally:
            continue
    finally:
        continue

print(f'Вот что получилось: {lst}')
