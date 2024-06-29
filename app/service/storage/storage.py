import enum
from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.storage_error import StockClosed, ImpossibleCloseStock
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.toolCRUD import ToolCRUD


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

        ToolCRUD.add(self.storage, tool)
    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удалить инструмент со склада

        При продаже инструмента
        '''
        StorageCRUD.retire(tool)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перемещение инструмента на объект
        '''
        if not where.status:
            raise ConstructionClosed

        elif not tool.status:
            raise ToolBroken

        elif ConstructionCRUD.get_responsible(where) is None:
            raise ResponsibleAbsent

        ToolCRUD.move_to(tool, where)


    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перемещение инструмента на другой склад
        
        В бд в таблице tool_on_storage меняет
        значение поля DT_end на текущую дату.
        После чего делает новую запись с новым складом.
        '''
        if where.status:
            ToolCRUD.move_to(tool, where)
        else:
            raise StockClosed

    
    def close(self) -> None:
        '''
        Закрыть склад
        '''
        
        if self.tools:
            raise ImpossibleCloseStock
            
        StorageCRUD.increase(self.storage)


    def restore(self) -> None:
        '''
        Возобновить работу склада
        '''
        StorageCRUD.retire(self.storage)
    
    
    def __works_check(self) -> None:
        '''
        Проверка на работоспособность склада
        
        Если склад закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.storage.status is StorageStatus.close:
            raise StockClosed
