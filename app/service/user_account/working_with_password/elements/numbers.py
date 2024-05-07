from random import randint


class UniqueNumber():
    '''
    Цифра
    '''

    def __init__(self) -> None:
        
        pass

    
    def get_number(self) -> str:
        '''
        Возвращает случайную цифру
        '''
        return str(randint(0, 9))