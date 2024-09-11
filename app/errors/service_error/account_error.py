from app.errors.base_exception import BaseApplicationException



class IncorrectInputData(BaseApplicationException):
    '''
    Вызывается при неправильном введенном логине или пароле
    '''

    def __init__(self):
        
        message = "Некорректный логин или пароль"
        super().__init__(message)



class LoginExists(BaseApplicationException):
    '''
    Вызывается, если при создании аккаунта
    указывается уже существующий логин
    '''

    def __init__(self):
        
        message = "Этот логин уже используется"
        super().__init__(message)



class EmailExists(BaseApplicationException):
    '''
    Вызывается, если при создании аккаунта
    указывается уже используемая на другом
    аккаунте почта
    '''

    def __init__(self):
        
        message = "Эта почта уже используется"
        super().__init__(message)



class CodeDoesntMatch(BaseApplicationException):
    '''
    Вызывается, если не совпадает проверочный код
    '''

    def __init__(self):
        
        message = "Код не совпадает"
        super().__init__(message)
