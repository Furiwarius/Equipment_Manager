from datetime import datetime
from dataclasses import dataclass
import enum
from construction import Construction

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
    construction: Construction


    def __nonzero__(self) -> bool:
        return self.status
    

    def get_id(self) -> int:
        return self.id


    def get_import_date(self) -> datetime:
        return self.import_date
    

    def get_construction(self) -> Construction:
        '''
        Возвращает объект, склад на котором находится инструмент
        '''
        return self.construction

    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует

    def change_date(self, new_date:datetime) -> None:
        '''
        Измененние даты перемещения инструмента
        '''
        self.import_date = new_date


    def move_tool(self, construction: Construction) -> None:
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
