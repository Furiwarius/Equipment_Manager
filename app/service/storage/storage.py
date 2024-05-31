import enum
from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.storage_error import StockClosed, ImpossibleCloseStock
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent


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


    def add_tool(self, tool: Tool) -> None:
        '''
        Добавить новый инструмент на склад
        '''
        self.__works_check()

        storageCRUD.add_tool(self.storage, tool)
    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удалить инструмент со склада

        При продаже инструмента
        '''
        storageCRUD.delete_tool(self.storage, tool)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перемещение инструмента на объект
        '''
        if not where.status:
            raise ConstructionClosed

        elif not tool.status:
            raise ToolBroken

        elif constructionCRUD.get_responsible(where) is None:
            raise ResponsibleAbsent

        toolCRUD.move_to_construction(tool, where)


    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перемещение инструмента на другой склад
        
        В бд в таблице tool_on_storage меняет
        значение поля DT_end на текущую дату.
        После чего делает новую запись с новым складом.
        '''
        if where.status:
            toolCRUD.move_to_storage(tool, where)
        else:
            raise StockClosed

    
    def close(self) -> None:
        '''
        Закрыть склад
        '''
        
        if self.tools:
            raise ImpossibleCloseStock
            
        storageCRUD.close(self.storage)


    def restore(self) -> None:
        '''
        Возобновить работу склада
        '''
        storageCRUD.work(self.storage)
    
    
    def __works_check(self) -> None:
        '''
        Проверка на работоспособность склада
        
        Если склад закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.storage.status is StorageStatus.close:
            raise StockClosed
