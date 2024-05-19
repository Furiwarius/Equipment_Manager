from dataclasses import dataclass
from datetime import datetime
import enum
from tool import Tool
from worker import Worker


class ConstructionStatus(enum.Enum):
    '''
    Статус объекта
    '''
    under_construction = True
    stopped = True
    finished = False


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
    # дата создания
    date_creation: datetime

    # Ответственный
    worker: Worker = None
    # Список инструментов
    tools: list


    def __nonzero__(self) -> bool:
        return {self.status}
    

    def __str__(self) -> str:
        return f"{self.name} {self.project}"


    def get_id(self) -> int:
        '''
        Получение id
        '''
        return self.id


    def get_date(self) -> datetime:
        '''
        Получение даты начала работ на объекте
        '''
        return self.date_creation
    

    def get_worker(self) -> Worker:
        '''
        Получить ответственного за этот объект

        Вернет None, если ответственный не назначен
        '''
        return self.worker
    

    def get_tools(self) -> list:
        '''
        Получение списка инструментов
        '''
        return self.tools
    

    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует.
    

    def add_worker(self, worker:Worker) -> None:
        '''
        Назначить ответственного
        '''
        self.worker = worker


    def add_tool(self, tool:Tool) -> None:
        '''
        Добавить инструмент

        Если не назначен ответственный
        работник или он не может работать, 
        то вызывает исключение
        '''
        if self.worker:
            self.tools.append(tool)
        else:
            raise ValueError("У объекта отсутствует ответственное лицо или оно нерабочее")
    

    def delete_tool(self, tool:Tool) -> None:
        '''
        Удалить объект
        '''
        self.tools.remove(tool)


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
