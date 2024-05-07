from random import randint


class UniqueSymbol():
    '''
    Символ
    '''

    symbols = ('.', ',', '*', '!', '?', ']', '[', 
               ':', ';', '#', '№', '@', '%', '(',
               ')', '+', '=', '-', '_', '&', '~')


    def __init__(self) -> None:
        
        self.symbols = set(UniqueSymbol.symbols)


    def generation(self) -> str:
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