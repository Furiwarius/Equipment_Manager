from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkerTable():
    '''
    Работник
    '''

    id: int
    # Имя
    name: str
    # Фамилия
    surname: str
    # Номер телефона
    phone_number: str
    # Должность работника
    job_title: str
    # Дата приема на работу
    start_work: datetime
    # Дата увольнения
    dismissal_work: datetime
    # Статус работника
    status: bool