from dataclasses import dataclass, field
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
    # Фирмы, в который аккаунт имеет роли
    firms: list[int] = field(default_factory=list)