from app.errors.base_exception import BaseException



class IncorrectLogin(BaseException):
    '''
    Вызывается при попытке использовать несуществующий аккаунт
    '''

    def __init__(self):
        
        message = "Некорректный логин"
        super().__init__(message)
    

class IncorrectPassword(BaseException):
    '''
    Вызывается, если при авторизации введенный 
    пароль не совпадает с сохраненным
    '''

    def __init__(self):
        
        message = "Неправильный пароль"
        super().__init__(message)


class LoginExists(BaseException):
    '''
    Вызывается, если при создании аккаунта
    указывается уже существующий логин
    '''

    def __init__(self):
        
        message = "Этот логин уже используется"
        super().__init__(message)



class EmailExists(BaseException):
    '''
    Вызывается, если при создании аккаунта
    указывается уже используемая на другом
    аккаунте почта
    '''

    def __init__(self):
        
        message = "Эта почта уже используется"
        super().__init__(message)



class CodeDoesntMatch(BaseException):
    '''
    Вызывается, если не совпадает проверочный код
    '''

    def __init__(self):
        
        message = "Код не совпадает"
        super().__init__(message)
