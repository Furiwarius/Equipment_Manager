from random import randint

class UniqueLetter():
    '''
    Буква
    '''

    letters = ('q', 'w', 'e', 'r', 't', 'y', 'u',
               'i', 'o', 'p', 'a', 's', 'd', 'f',
               'g', 'h', 'j', 'k', 'l', 'z', 'x',
               'c', 'v', 'b', 'n', 'm')
    

    def __init__(self) -> None:

        self.letters = set(UniqueLetter.letters)


    def get_letter(self) -> str:
        '''
        Возвращает букву уникальную букву,
        если уникальные буквы кончились, обновляет 
        множество букв
        '''
        self.replenishment()
        result = self.uppercase_lowercase(self.random_letter())
        return result
    

    def random_letter(self) -> str:
        '''
        Случайная буква
        '''
        result = tuple(self.letters)[randint(0, len(self.letters)-1)]
        self.letters.discard(result)
        return result


    def uppercase_lowercase(self, letter:str) -> str:
        '''
        Делает входящую букву рандомно строчной или заглавной
        '''
        if randint(0, 1):
            return letter.upper()
        return letter.lower()
    

    def replenishment(self) -> None:
        '''
        Восполняет множество букв, в случае,
        если оно пустое
        '''
        if len(self.letters)==0:
            self.letters = set(UniqueLetter.letters)


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



class UniqueSymbol():
    '''
    Символ
    '''

    symbols = ('.', ',', '*', '!', '?', ']', '[', 
               ':', ';', '#', '№', '@', '%', '(',
               ')', '+', '=', '-', '_', '&', '~')


    def __init__(self) -> None:
        
        self.symbols = set(UniqueSymbol.symbols)


    def get_symbol(self) -> str:
        '''
        Возвращает уникальный символ
        '''
        self.replenishment()
        return self.random_symbol()
    

    def random_symbol(self) -> str:
        '''
        Случайный символ
        '''
        result = tuple(self.symbols)[randint(0, len(self.symbols)-1)]
        self.symbols.discard(result)
        return result


    def replenishment(self) -> None:
        '''
        Восполняет множество символов, в случае,
        если оно пустое
        '''
        if len(self.symbols)==0:
            self.symbols = set(UniqueSymbol.symbols)


class PasswordGenerator():
    '''
    Генератор паролей
    '''