from dataclasses import dataclass
from datetime import datetime


@dataclass
class Storage():
    '''
    Склад
    '''

    id: int = None
    # название склада
    name: str = None
    # адрес склада
    address: str = None
    # статус склада
    status: bool = None
    # дата начала работы склада
    start_date: datetime = None
    # дата окончания работы склада
    end_date: datetime = None