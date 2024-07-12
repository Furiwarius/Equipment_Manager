import enum
from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.storage_error import StockClosed
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD


class ToolStatus(enum.Enum):
    '''
    Описание статуса инструмента
    '''
    # Работает
    works = True
    # Сломан
    faulty = False


class ToolManager():
    '''
    Инструмент
    '''

    def __init__(self, tool:Tool) -> None:
        
        self.constr_crud = ConstructionCRUD()
        self.tool_crud = ToolCRUD()
        self.storage_cud = StorageCRUD()

        self.tool = tool
            

    def move_tool_to_construction(self, constr: Construction) -> None:
        '''
        Переместить инструмент на объект
        '''
        if not constr.status:
            raise ConstructionClosed
        
        elif self.tool.status is ToolStatus.faulty:
            raise ToolBroken

        elif self.constr_crud.get_responsible(constr.id) is None:
            raise ResponsibleAbsent

        self.tool_crud.move_to(self.tool, constr)

    
    def move_tool_to_storage(self, storage: Storage) -> None:
        '''
        Переместить инструмент на склад
        '''
        if not storage.status:
            raise StockClosed
            
        self.tool_crud.move_to(self.tool, storage)


    def break_tool(self) -> None:
        '''
        Сломать инструмент
        '''
        self.tool_crud.modify_status(self.tool.id, False)
    


    def fix_tool(self) -> None:
        '''
        Починить инструмент
        '''
        self.tool_crud.modify_status(self.tool.id, True)
