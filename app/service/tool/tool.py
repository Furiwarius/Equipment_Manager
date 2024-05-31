import enum
from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.storage_error import StockClosed


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
            # Если обьект закрыт,
            # то вызывает исключение
            pass
        elif self.tool.status is ToolStatus.faulty:
            raise ToolBroken

        elif constructionCRUD.get_responsible(constr) is None:
            # Если у объекта нет ответственного,
            # то вызывает исключение
            pass

        # Если все нормально, то выполняет операции по перемещению
        toolCRUD.move_to_construction(self.tool, constr)

    
    def move_tool_to_storage(self, storage: Storage) -> None:
        '''
        Переместить инструмент на склад
        '''
        if not storage.status:
            raise StockClosed
            
        toolCRUD.move_to_storage(self.tool, storage)


    def break_tool(self) -> None:
        '''
        Сломать инструмент
        '''
        toolCRUD.break_tool(self.tool)
    


    def fix_tool(self) -> None:
        '''
        Починить инструмент
        '''
        toolCRUD.fix_tool(self.tool)
