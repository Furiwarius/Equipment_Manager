from datetime import datetime

from dataclasses import dataclass

@dataclass
class Tool():
    '''
    Инструмент
    '''

    id: int = None
    # id фирмы, к которой принадлежит инструмент
    firm_id:int = None
    # название инструмента
    name: str = None
    # статус инструмента
    status: bool = None
    # заводской номер
    factory_number: str = None
    # дата начала работы инструмента
    start_date: datetime = None
    # Время обновления данных
    update_date: datetime = None
    # дата окончания работы инструмента
    end_date: datetime = None