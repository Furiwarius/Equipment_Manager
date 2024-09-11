

class InvalidToken(Exception):
    '''
    Вызывается при передаче неправильного токена
    '''

    def __init__(self):
        
        message = "Неподходящий токен"
        super().__init__(message)