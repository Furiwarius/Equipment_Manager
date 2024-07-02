

class ImpossibleDismiss(Exception):
    '''
    Вызывается, если пользователь
    пытается уволить работника,
    который является ответственным на объекте
    '''

    def __init__(self):
        
        message = "Этот работник является ответственным лицом на объекте"
        super().__init__(message)


class WorkerDoesntWork(Exception):
    '''
    Вызывается, если пользователь
    пытается переместить на объект
    не работающего работника
    '''

    def __init__(self):
        
        message = "Этот работник не может работать"
        super().__init__(message)


class WorkerValid(Exception):
    '''
    Вызывается при попытке добавить
    в БД некорректные данные
    '''

    def __init__(self):
        
        message = "Получены некорректные данные для добавления в бд"
        super().__init__(message)