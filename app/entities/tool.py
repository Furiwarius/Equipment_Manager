from dataclasses import dataclass

@dataclass
class ToolTable():
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
