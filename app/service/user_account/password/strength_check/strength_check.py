from ..password_generator.elements.letters import UniqueLetter
from ..password_generator.elements.symbols import UniqueSymbol


class PasswordStrengthCheck():

    '''
    Класс, проверяющий надежность пароля
    '''

    def __init__(self, password:str) -> None:

        self.password = tuple(password)
        self.result_coefficient = 1


    def password_check(self) -> int:
        '''
        Проверка пароля
        Возвращает коэффициент надежности пароля:
        1 - ненадежный,
        2 - слабый,
        3 - средний,
        4 - надежный,
        5 - очень надежный
        '''

        # проверка размера пароля
        self.size_check()
        # проверка на наличие символов
        self.elem_check(UniqueSymbol.symbols)
        # проверка на наличие цифр
        self.elem_check(tuple(map(str,range(10))))
        # проверка на наличие букв
        self.elem_check(UniqueLetter.letters)
    
        return self.result_coefficient
    
    def elem_check(self, elems:tuple) -> None:
        '''
        Проверка на наличие элементов из передаваемого кортежа
        '''
        symbols = set(elems)
        # False если передаваемый список и пароль имеют общие данные
        if symbols.isdisjoint(self.password)==False:
            self.result_coefficient+=1
    
    
    def size_check(self) -> None:
        '''
        Проверка длины пароля
        '''
        if len(self.password)>=12:
            self.result_coefficient+=1


    