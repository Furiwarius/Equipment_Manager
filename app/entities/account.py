from dataclasses import dataclass


@dataclass
class AccountTable():
    '''
    Аккаунт 
    '''

    id: int
    # логин
    login: str
    # хешированный пароль
    password: str