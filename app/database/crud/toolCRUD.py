from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ToolTable
from sqlalchemy.orm import Session
from app.database.tables.summary import ToolsOnConstructions, ToolsOnStorage
from datetime import datetime

class ToolCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''        

    def __init__(self) -> None:
        
        super().__init__(table=ToolTable)


    def add(self, tool:Tool, where:Storage|Construction) -> None:
        '''
        Добавить инструмент
        
        Для добавления нового инструмента, нужно также
        указать объект или склад, где он будет хранится.
        '''
        tool = self.coverter.conversion_to_table(tool)
        with Session(autoflush=False, bind=self.engine) as db:

            db.add(tool)     # добавляем в бд
            db.commit()

            if isinstance(where, Storage):
                storage = self.coverter.conversion_to_table(where)
                where = ToolsOnStorage(tool_id=tool.id,
                                         storage_id=storage.id,
                                         DT_start=datetime.now(),
                                         DT_end=None)

            else:
                constr = self.coverter.conversion_to_table(where)
                where = ToolsOnConstructions(tool_id=tool.id,
                                         construction_id=constr.id,
                                         DT_start=datetime.now(),
                                         DT_end=None)
            
            db.add(where)
            db.commit()     # сохраняем изменения


    def move_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перевезти инструмент на другой склад
        '''
    

    def move_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перевезти инструмент на другой объект
        '''
    
