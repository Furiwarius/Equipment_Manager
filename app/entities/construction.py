from dataclasses import dataclass
from datetime import datetime



@dataclass
class ConstructionTable():
    '''
    Объект
    '''

    id: str
    # название объекта
    name: str
    # номер проекта или договора подряда
    project: str
    # адрес объекта
    address: str
    # статус объекта
    status: bool
    # дата начала работы объекта
    start_date: datetime
    # дата окончания работы объекта
    end_date: datetime