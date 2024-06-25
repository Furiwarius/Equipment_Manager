import enum
from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.storage_error import StockClosed
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent
from database.crud.constructionCRUD import ConstructionCRUD
from database.crud.toolCRUD import ToolCRUD


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
        
        self.tool = tool
            

    def move_tool_to_construction(self, constr: Construction) -> None:
        '''
        Переместить инструмент на объект
        '''
        if not constr.status:
            raise ConstructionClosed
        
        elif self.tool.status is ToolStatus.faulty:
            raise ToolBroken

        elif ConstructionCRUD.get_responsible(constr) is None:
            raise ResponsibleAbsent

        ToolCRUD.move_to(self.tool, constr)

    
    def move_tool_to_storage(self, storage: Storage) -> None:
        '''
        Переместить инструмент на склад
        '''
        if not storage.status:
            raise StockClosed
            
        ToolCRUD.move_to(self.tool, storage)


    def break_tool(self) -> None:
        '''
        Сломать инструмент
        '''
        ToolCRUD.downgrade(self.tool)
    


    def fix_tool(self) -> None:
        '''
        Починить инструмент
        '''
        ToolCRUD.increase(self.tool)
