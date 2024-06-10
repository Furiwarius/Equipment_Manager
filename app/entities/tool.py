from datetime import datetime

from dataclasses import dataclass

@dataclass
class Tool():
    '''
    Инструмент
    '''

    id: int
    # название инструмента
    name: str
    # статус инструмента
    status: bool
    # заводской номер
    factory_number: str
    # дата начала работы инструмента
    start_date: datetime
    # дата окончания работы инструмента
    end_date: datetime