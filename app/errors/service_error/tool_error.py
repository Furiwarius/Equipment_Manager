

class ToolBroken(Exception):
    '''
    Вызывается, если попытаться переместить
    сломанный инструмент на объект строительства
    '''

    def __init__(self):
        
        message = "Этот инструмент сломан"
        super().__init__(message)