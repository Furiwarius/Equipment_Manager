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
    # Почта пользователя для отправки на нее уведомлений
    email:str
    # Статус подтверждения
    confirmation_status:bool