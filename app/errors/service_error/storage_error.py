

class StockClosed(Exception):
    '''
    Вызывается, если попытаться переместить
    инструмент на закрытый склад
    '''

    def __init__(self):
        
        message = "Этот склад закрыт. На него нельзя перемещать инструмент"
        super().__init__(message)


class ImpossibleCloseStock(Exception):
    '''
    Вызывается, если попытаться закрыть склад,
    на котором хранится инструмент
    '''

    def __init__(self):
        
        message = "Этот склад нельзя закрыть, потому что на нем хранится инструмент"
        super().__init__(message)