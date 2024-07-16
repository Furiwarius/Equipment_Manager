from dataclasses import dataclass
from datetime import datetime



@dataclass
class Construction():
    '''
    Объект
    '''

    id: int = None
    # название объекта
    name: str = None
    # номер проекта или договора подряда
    project: str = None
    # адрес объекта
    address: str = None
    # статус объекта
    status: bool = None
    # дата начала работы объекта
    start_date: datetime = None
    # дата окончания работы объекта
    end_date: datetime = None