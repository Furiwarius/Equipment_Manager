from app.errors.base_exception import BaseException


class ImpossibleDismiss(BaseException):
    '''
    Вызывается, если пользователь
    пытается уволить работника,
    который является ответственным на объекте
    '''

    def __init__(self):
        
        message = "Этот работник является ответственным лицом на объекте"
        super().__init__(message)


class WorkerDoesntWork(BaseException):
    '''
    Вызывается, если пользователь
    пытается переместить на объект
    не работающего работника
    '''

    def __init__(self):
        
        message = "Этот работник не может работать"
        super().__init__(message)