from dataclasses import dataclass
from datetime import datetime
import enum


class ConstructionStatus(enum.Enum):
    '''
    Статус объекта
    '''
    under_construction = True
    stopped = True
    finished = False


class Warehouse(enum.Enum):
    '''
    Является ли объект складом
    '''
    warehouse = True
    not_warehouse = False


@dataclass
class Construction():
    '''
    Объект
    '''

    id: int
    # название объекта
    name: str
    # номер проекта или договора подряда
    project: str
    # статус объекта
    status: ConstructionStatus
    # Является ли складом
    warehouse: Warehouse
    # дата создания
    date_creation: datetime


    def __nonzero__(self) -> bool:
        return {self.status}
    

    def __str__(self) -> str:
        return f"{self.name} {self.project}"


    def get_id(self) -> int:
        '''
        Получение id
        '''
        return self.id


    def warehouse(self) -> bool:
        '''
        Является ли объект складом
        '''
        return self.warehouse


    def get_date(self) -> datetime:
        '''
        Получение даты начала работ на объекте
        '''
        return self.date_creation
    

    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует
    

    def change_date(self, new_date:datetime) -> None:
        '''
        Изменение даты начала работ на объекте
        '''
        self.date_creation = new_date


    def change_name(self, new_name:str) -> None:
        '''
        Изменение названия объекта
        '''
        self.name = new_name
    

    def change_project(self, new_project:str) -> None:
        '''
        Изменение номера проекта или договора
        '''
        self.project = new_project
    

    def close_construction(self) -> None:
        '''
        Закрытие объекта строительства
        '''
        self.status = ConstructionStatus.finished
    

    def open_construction(self):
        '''
        Возобновление строительства
        '''
        self.status = ConstructionStatus.under_construction