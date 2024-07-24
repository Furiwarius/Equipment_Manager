

class IdNotSent(Exception):
    '''
    Вызывается, если попытаться создать фирму
    не передавая account_id в FirmManager
    '''

    def __init__(self):
        
        message = "При создании фирмы не был передан account_id"
        super().__init__(message)



class WrongRolePassed(Exception):
    '''
    Вызывается, если попытатся выдать
    аккаунту роль не admin или visitor
    '''

    def __init__(self):
        
        message = "При выдаче роли аккаунту предано невалидное значение"
        super().__init__(message)