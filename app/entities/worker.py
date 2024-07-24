from dataclasses import dataclass
from datetime import datetime

@dataclass
class Worker():
    '''
    Работник
    '''

    id: int = None
    # id аккаунта, к которому привязан этот работник
    account_id: int = None
    # id фирмы, к которой принадлежит работник
    firm_id:int = None
    # Имя 
    name: str = None
    # Фамилия
    surname: str = None
    # Номер телефона
    phone_number: str = None
    # Должность работника
    job_title: str = None
    # дата начала работы работника
    start_date: datetime = None
    # дата окончания работы работника
    end_date: datetime = None
    # Статус работника
    status: bool = None