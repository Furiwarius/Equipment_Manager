

class ConstructionClosed(Exception):
    '''
    Вызывается, если попытаться переместить
    инструмент на закрытый объект
    '''

    def __init__(self):
        
        message = "Этот объект закрыт. На него нельзя перемещать инструмент"
        super().__init__(message)


class ImpossibleCloseConstruction(Exception):
    '''
    Вызывается, если попытаться закрыть объект,
    на котором хранится инструмент
    '''

    def __init__(self):
        
        message = "Этот объект нельзя закрыть, потому что на нем хранится инструмент"
        super().__init__(message)


class ResponsibleAbsent(Exception):
    '''
    Вызывается, если попытаться перевести инструмент
    на объект, на котором отсутствует ответственный
    '''

    def __init__(self):
        
        message = "На этом объекте не назначен ответственный"
        super().__init__(message)