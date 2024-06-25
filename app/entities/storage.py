from dataclasses import dataclass
from datetime import datetime


@dataclass
class Storage():
    '''
    Склад
    '''

    id: int
    # название склада
    name: str
    # адрес склада
    address: str
    # статус склада
    status: bool
    # дата начала работы склада
    start_date: datetime
    # дата окончания работы склада
    end_date: datetime