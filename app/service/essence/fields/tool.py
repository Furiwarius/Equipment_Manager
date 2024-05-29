from datetime import datetime
from dataclasses import dataclass
import enum

class ToolStatus(enum.Enum):
    '''
    Описание статуса инструмента
    '''
    # Работает
    works = True
    # Сломан
    faulty = False


@dataclass
class Tool():
    '''
    Инструмент
    '''

    id: int
    name: str
    import_date: datetime
    status: ToolStatus
    # Информация об объекте не храниться в бд
    # Нужна для более простого изменения взаимосвязей между классами
    # id Объекта строительства
    construction: int


    # В этом нет необходимости,
    # можно просто обратиться к параметру tool.id
    def get_id(self) -> int:
        '''
        Получение id объекта
        '''
        return self.id


    def get_status(self) -> ToolStatus:
        '''
        Получение статуса объекта
        '''
        return self.status


    def get_import_date(self) -> datetime:
        '''
        Получение даты перемещения объекта
        '''
        return self.import_date


    def get_construction(self) -> int:
        '''
        Возвращает id объекта, склада на котором находится инструмент
        '''
        return self.construction

    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует

    def change_date(self, new_date:datetime) -> None:
        '''
        Измененние даты перемещения инструмента
        '''
        self.import_date = new_date


    def move_tool(self, construction: int) -> None:
        '''
        Переместить инструмент
        '''
        self.construction = construction


    def break_tool(self) -> None:
        '''
        Сломать инструмент
        '''
        self.status = ToolStatus.faulty


    def fix_tool(self) -> None:
        '''
        Починить инструмент
        '''
        self.status = ToolStatus.works
