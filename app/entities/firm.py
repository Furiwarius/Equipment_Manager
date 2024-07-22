from dataclasses import dataclass
from datetime import datetime

@dataclass
class Firm():
    '''
    Фирма
    '''

    id: int = None
    # название название фирмы
    name: str = None
    # статус фирмы
    status: bool = None
    # дата создания
    start_date: datetime = None
    # дата закрытия
    end_date: datetime = None