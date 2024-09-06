from app.errors.base_exception import BaseApplicationException


class ImpossibleDismiss(BaseApplicationException):
    '''
    Вызывается, если пользователь
    пытается уволить работника,
    который является ответственным на объекте
    '''

    def __init__(self):
        
        message = "Этот работник является ответственным лицом на объекте"
        super().__init__(message)


class WorkerDoesntWork(BaseApplicationException):
    '''
    Вызывается, если пользователь
    пытается переместить на объект
    не работающего работника
    '''

    def __init__(self):
        
        message = "Этот работник не может работать"
        super().__init__(message)