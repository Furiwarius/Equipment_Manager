from app.errors.base_exception import BaseApplicationException



class ToolBroken(BaseApplicationException):
    '''
    Вызывается, если попытаться переместить
    сломанный инструмент на объект строительства
    '''

    def __init__(self):
        
        message = "Этот инструмент сломан"
        super().__init__(message)