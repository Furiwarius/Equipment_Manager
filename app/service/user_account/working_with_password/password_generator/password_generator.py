from app.service.user_account.working_with_password.password_generator.elements.letters import UniqueLetter
from app.service.user_account.working_with_password.password_generator.elements.numbers import UniqueNumber
from app.service.user_account.working_with_password.password_generator.elements.symbols import UniqueSymbol
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