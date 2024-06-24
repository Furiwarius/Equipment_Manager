from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ToolTable
from app.database.tables.essence import StorageTable
from app.database.tables.essence import ConstructionTable
from sqlalchemy.orm import Session
from app.database.tables.summary import ToolsOnConstructions as ToolsOnConstr
from app.database.tables.summary import ToolsOnStorage
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

            where = self.coverter.conversion_to_table(where)
            self.__move(db, tool, where)
            
            db.commit()     # сохраняем изменения
  

    def move_to(self, tool:Tool, where:Construction|Storage) -> None:
        '''
        Перевезти инструмент на другой объект
        '''

        with Session(autoflush=False, bind=self.engine) as db:
            
            location = self.__locate(db, tool)
            
            self.__close_post(db, location)
            
            self.__move(db, tool, where)
            
            db.commit() # сохраняем изменения
    

    def __move(self, db:Session, tool:Tool, where:Storage|Construction) -> None:
        '''
        Добавить запись о храненнии инструмента
        '''

        if isinstance(where, StorageTable):
            place = ToolsOnStorage
        elif isinstance(where, ConstructionTable): 
            place = ToolsOnConstr

        post = place(tool_id=tool.id,
                     place_id=where.id,
                     DT_start=datetime.now(),
                     DT_end=None)

        db.add(post)

    
    def __locate(self, db:Session, tool:Tool) -> ToolsOnConstr|ToolsOnStorage:
        '''
        Определить местоположение инструмента
        '''

        constr = db.query(ToolsOnConstr).filter(ToolsOnConstr.tool_id==tool.id,
                                                ToolsOnConstr.DT_end==None).all()
        storage = db.query(ToolsOnStorage).filter(ToolsOnStorage.tool_id==tool.id,
                                                ToolsOnStorage.DT_end==None).all()

        if constr:
            return constr[0]
        else:
            return storage[0]
            

    def __close_post(self, db:Session, location:ToolsOnConstr|ToolsOnStorage) -> None:
        '''
        Записывает дату окончания хранения 
        инструмента на объекте строительства
        '''

        db.query(type(location)).filter(type(location).id == location.id
                                           ).update({type(location).DT_end:datetime.now()}, synchronize_session = False)
    
