from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage


class ToolCRUD():
    '''
    Класс для взаимодействия с БД
    '''


    def add_tool(self, tool:Tool, where:Storage|Construction) -> None:
        '''
        Добавить инструмент
        
        Для добавления нового инструмента, нужно также
        указать объект или склад, где он будет хранится
        '''
        

    def move_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перевезти инструмент на другой склад
        '''
    

    def move_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перевезти инструмент на другой объект
        '''
    

    def break_tool(self, tool:Tool) -> None:
        '''
        Сломать инструмент
        '''
    

    def fix_tool(self, tool:Tool) -> None:
        '''
        Починить инструмент
        '''
    