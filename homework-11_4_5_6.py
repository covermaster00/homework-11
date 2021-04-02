"""
Основаной класс Warehouse. При заполнении присваивается уникальынй ID каждому объекту.
Основные методы: add, delete, move
Вспомогательные: exist, get, report
Метод-свойство: next_id

Абстрактный класс Equipment. Требует явное переопределение конструктора
Прямые потомки: Printer, Scaner
Класс Copier наследуется от Printer и Scaner

Для функционального тестирования (и ещё ради понта) используется класс Terminal - наследник Warehouse
Большая часть методов родителя дополнена функционалом интерфейса.
Введены ограничения: 1) внести новое оборудование можно только на склад; 2) удалить можно только со склада

Доступные методы для вызова из терминала:
add - добавление на склад
get - отобразить данные оборудования по ID
move - переместить оборудование между division
del - удалить оборудование со склада
where - обобразить division по ID оборудования
report - отчет либо по всем отделам либо по заданому division

Для каждого метода доступен вызов справки по параметру '?'
"""

from abc import ABC, abstractmethod

class Warehouse():
    def __init__(self):
        self.ids = 0
        self.warehouse = {'Склад': []}

    class NoData(Exception):
        def __init__(self, txt):
            self.txt = txt

    @property
    def next_id(self):
        self.ids = self.ids + 1
        return self.ids

    def exist(self, equipment, division='Склад'):
        '''
        Проверка на существавание устройства в указаном подразделении
        :param equipment: class Equipment
        :param division: Наименование подразделения
        :return: ID или False
        '''
        if bool(self.warehouse.get(division) and self.warehouse.get(division).count(equipment)):
            return equipment.id
        else:
            return False

    def get(self, id, division=0):
        '''
        Возвращает class Equipment по id. Если не найден: None
        :param id: Equipment.id
        :return: Equipment / None
        '''
        for i in self.warehouse.keys():
            for j in self.warehouse[i]:
                try:
                    if j.id == int(id):
                        return i if division else j
                except:
                    return None
        return None


    def add(self, equipment):
        '''
        Добавление устройства на основной склад
        :param equipment: class Equipment
        '''
        if not self.exist(equipment):
            equipment.id = self.next_id
            self.warehouse['Склад'].append(equipment)


    def delete(self, equipment, division):
        '''
        Удаление устройства из базы данных
        :param equipment: class Equipment
        :param division: Наименование подразделения
        :return:
        '''
        try:
            self.warehouse.get(division.capitalize()).remove(equipment)
        except:
            raise self.NoData('Невозможно удалить указаный объект')


    def move(self, equipment, source, dest):
        '''
        Перемещение между подразделениями
        :param equipment: Class Equipment
        :param source: Наименование подраздленеия С КОТОРОГО перемещается
        :param dest: Наименование подразделения КУДА перемещается (по-умолчанию основной склад)
        :return:
        '''
        try:
            dest = dest.capitalize()
            source = source.capitalize()
            if self.warehouse.get(dest):
                self.warehouse[dest].append(equipment)
            else:
                self.warehouse[dest] = [equipment]
            self.warehouse.get(source).remove(equipment)
        except:
            raise self.NoData('Невозможно переместить указаный объект')


    def __str__(self):
        return str(self.warehouse)


    def report(self, key='all'):
        '''
        Печать сводной информации по все отделам или по указанному
        :param key: имя отдела, по умолчанию 'all'
        '''
        try:
            if key == 'all':
                for i in self.warehouse.keys():
                    print(f'{"="*30} {i} {"="*(40-len(i))}')
                    for j in self.warehouse[i]:
                        print(j)
            else:
                key = key.capitalize()
                print(f'{"=" * 30} {key} {"=" * (40 - len(key))}')
                for j in self.warehouse[key]:
                    print(j)
        except:
            raise self.NoData


class Equipment(ABC):
    class UncorrectFormat(Exception):
        def __init__(self, txt):
            self.txt = txt


    @abstractmethod
    def __init__(self, name, is_color):
        self.id = None
        try:
            self.name, self.__is_color = name, bool(is_color)
        except:
            raise self.UncorrectFormat('Некорректные данные при создании класса')


    def __str__(self):
        return f'id: {self.id}; Наименование: {self.name}; {"Цветной" if self.__is_color else "Ч/б"}'


class Printer(Equipment):
    def __init__(self, name, is_color, speed):
        super().__init__(name, is_color)
        try:
            self.speed = int(speed)
        except:
            raise self.UncorrectFormat('Скорость указана некорректно')

    def __str__(self):
        return f'ПРИНТЕР. {super().__str__()}; Скорость печати: {self.speed}'


class Scaner(Equipment):
    def __init__(self, name, is_color, dpi=0):
        super().__init__(name, is_color)
        try:
            self.dpi = int(dpi)
        except:
            raise self.UncorrectFormat('Разрешение сенсора задано некорректно')

    def __str__(self):
        return f'СКАНЕР. {super().__str__()}; Разрешение сенсора: {self.dpi}'


class Copier(Printer, Scaner):
    '''
    Комбинированое устройство, наследуется от Printer и Scaner
    '''
    def __init__(self, name, is_color, speed, dpi):
        super().__init__(name, is_color, speed)
        try:
            self.dpi = int(dpi)
        except:
            raise self.UncorrectFormat('Разрешение сенсора задано некорректно')

    def __str__(self):
        return f'КОПИР. {Equipment.__str__(self)}; Разрешение сенсора: {self.dpi}; Скорость печати: {self.speed}'


# - - - - - - - - - Терминал для тестирования - - - - - - - - -

class Terminal(Warehouse):
    def __init__(self):
        super().__init__()
        self.commands = {'add': self.add, 'get': self.get, 'move': self.move,
                         'delete': self.delete, 'where': self.where, 'report': self.report}

    def add(self, *kwargs):
        if kwargs[0] == '?':
            print('add printer <name> <is color: 0 / 1> <speed>')
            print('add scaner <name> <is color: 0 / 1> <dpi>')
            print('add copier <name> <is color: 0 / 1> <speed> <dpi>')
        elif kwargs[0] == 'printer':
            super().add(Printer(*kwargs[1:]))
        elif kwargs[0] == 'scaner':
            super().add(Scaner(*kwargs[1:]))
        elif kwargs[0] == 'copier':
            super().add(Copier(*kwargs[1:]))
        else:
            print('Указаный объект не является допустимым оборудованием')


    def get(self, *args):
        if args[0] == '?':
            print('get <id>')
        else:
            print(super().get(args[0]))


    def where(self, *args):
        if args[0] == '?':
            print('where <id>')
        else:
            print(super().get(args[0], True))


    def move(self, *args):
        if args[0] == '?':
            print('move <id> <source> <destination>')
        else:
            if super().exist(super().get(args[0]), args[1].capitalize()):
                super().move(super().get(args[0]), *args[1:])
            else:
                print('Объект с заданнымми параметрами не найден')


    def delete(self, *args):
        if args[0] == '?':
            print('delete <id>')
        else:
            super().delete(super().get(args[0]), 'Склад')


    def report(self, key='all'):
        if key == '?':
            print('report [<division>]')
        else:
            super().report(key)

# - - - - - - - - - ТЕСТ - - - - - - - - -

t = Terminal()
t.add('printer', 'Epson', True, 5)
t.add('scaner', 'XP', False, 300)
t.add('copier', 'Xerox', True, 10, 600)

while True:
    c = input('Введите команду (exit - для выхода, ? - список команд): ')
    if c == 'exit':
        break
    elif c == '?':
        print('Доступные команды: ', *t.commands.keys())      # нормализовать
    else:
        c = c.split()
        try:
            t.commands[c[0]](*c[1:])
        except Warehouse.NoData:
            print('Данные не найдены')
        except Equipment.UncorrectFormat:
            print('Параметры оборудования указаны неверно')
        except:
            print('Некорректная команда. Используйте ? для получения справки')
        finally:
            continue

#t.report()
