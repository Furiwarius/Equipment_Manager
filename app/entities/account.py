from dataclasses import dataclass
from datetime import datetime


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
    # Время создания аккаунта
    start_date: datetime = None
    # Время обновления данных
    update_date: datetime = None