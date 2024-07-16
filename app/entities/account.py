from dataclasses import dataclass


@dataclass
class Account():
    '''
    Аккаунт 
    '''

    id: int = None
    # логин
    login: str = None
    # хешированный пароль
    password: str = None
    # Почта пользователя для отправки на нее уведомлений
    email:str = None
    # Статус подтверждения
    confirmation_status:bool = None
    # Таймзона пользователя
    timezone:str = None