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