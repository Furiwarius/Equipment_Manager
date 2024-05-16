from elements.letters import UniqueLetter
from elements.numbers import UniqueNumber
from elements.symbols import UniqueSymbol
from random import randint

class PasswordGenerator():
    '''
    Генератор паролей
    '''

    def __init__(self) -> None:
        
        self.kit = (UniqueLetter(), UniqueNumber(), UniqueSymbol())


    def run_generation(self, size:int) -> str:
        '''
        Метод, генерирующий пароль заданной длины
        '''
        result = [self.kit[randint(0, len(self.kit)-1)].generation() for _ in range(size)]
        return ''.join(result)