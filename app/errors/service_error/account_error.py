

class IncorrectLogin(Exception):
    '''
    Вызывается при попытке использовать несуществующий аккаунт
    '''

    def __init__(self):
        
        message = "Некорректный логин"
        super().__init__(message)
    

class IncorrectPassword(Exception):
    '''
    Вызывается, если при авторизации введенный 
    пароль не совпадает с сохраненным
    '''

    def __init__(self):
        
        message = "Неправильный пароль"
        super().__init__(message)


class LoginExists(Exception):
    '''
    Вызывается, если при создании аккаунта
    указывается уже существующий логин
    '''

    def __init__(self):
        
        message = "Этот логин уже используется"
        super().__init__(message)


class CodeDoesntMatch(Exception):
    '''
    Вызывается, если не совпадает проверочный код
    '''

    def __init__(self):
        
        message = "Код не совпадает"
        super().__init__(message)
