from dataclasses import dataclass


@dataclass
class Storage():
    '''
    Склад
    '''

    id: int
    # название склада
    name: str