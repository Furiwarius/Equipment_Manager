from dataclasses import dataclass
from datetime import datetime

@dataclass
class Worker():
    '''
    Работник
    '''

    id: int
    # id аккаунта, к которому привязан этот работник
    account_id: int
    # Имя
    name: str
    # Фамилия
    surname: str
    # Номер телефона
    phone_number: str
    # Должность работника
    job_title: str
    # дата начала работы работника
    start_date: datetime
    # дата окончания работы работника
    end_date: datetime
    # Статус работника
    status: bool