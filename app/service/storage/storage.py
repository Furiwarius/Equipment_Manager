import enum
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.tool import Tool
from app.entities.storage import Storage


class StorageStatus(enum.Enum):
    '''
    Статус склада
    '''
    works = True
    close = False


class StorageManager():
    '''
    Управляющий класс для склада
    '''

    def __init__(self, storage:Storage) -> None:
        
        self.storage = storage

        self.tools = []


    def add_tool(self, tool: Tool) -> None:
        '''
        Добавить новый инструмент на склад

        В бд в таблице tool_on_storage создает новую запись.
        '''
        self.__works_check()

        self.tools.append(tool.id)
    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удалить инструмент со склада

        В бд в таблице tool_on_storage меняет
        значение поля DT_end на текущую дату.
        '''
        self.tools.remove(tool.id)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перемещение инструмента на объект

        В бд в таблице tool_on_storage меняет
        значение поля DT_end на текущую дату.
        После чего делает новую запись в таблице
        tool_on_construction с новым объектом.
        '''
        if not where.status:
            # Если объект не работает,
            # то бросает исключение
            pass

        elif not tool.status:
            # Если инструмент не работает,
            # бросает исключение
            pass

        elif constructionCRUD.get_responsible(where) is None:
            # Если у данного объекта нет ответственного,
            # бросает исключение
            pass

        self.tools.remove(tool.id)


    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перемещение инструмента на другой склад
        
        В бд в таблице tool_on_storage меняет
        значение поля DT_end на текущую дату.
        После чего делает новую запись с новым складом.
        '''
        if where.status:
            self.tools.remove(tool.id)
        else:
            # Кастомное исключение
            pass

    
    def close(self) -> None:
        '''
        Закрыть склад
        '''
        
        if self.tools:
            # Бросает исключение, 
            # если на складе есть инструмент
            pass
        self.storage.status = StorageStatus.close


    def restore(self) -> None:
        '''
        Возобновить работу склада
        '''
        self.storage.status = StorageStatus.works
    
    
    def __works_check(self) -> None:
        '''
        Проверка на работоспособность склада
        
        Если склад закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.storage.status is StorageStatus.close:
            # КАСТОМНОЕ ИСКЛЮЧЕНИЕ
            pass
