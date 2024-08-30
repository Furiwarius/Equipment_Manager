from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ToolTable
from app.database.tables.essence import StorageTable
from sqlalchemy.orm import Session
from app.database.tables.summary import ToolsOnConstructions as ToolsOnConstr
from app.database.tables.summary import ToolsOnStorage
from app.database.tables.essence import ConstructionTable as ConstrTable
from datetime import datetime
from app.database.database import Database
from app.database.converter import convertertation



class ToolCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''        

    def __init__(self) -> None:
        
        super().__init__(table=ToolTable)



    def __repr__(self) -> str:
        return f"{__class__.__name__}"


     
    @convertertation
    @BaseCRUD.logger.info
    def add(self, tool:Tool, where:Storage|Construction) -> Tool:
        '''
        Добавить инструмент
        
        Для добавления нового инструмента, нужно также
        указать объект или склад, где он будет хранится.
        '''
        with Database() as db:

            db.add(tool)     # добавляем в бд
            db.commit()

            self.__move(db, tool, where)
            
            db.commit()     # сохраняем изменения
  
            return db.query(self.table).order_by(self.table.id.desc()).first()
    


    @convertertation
    @BaseCRUD.logger.info
    def move_to(self, tool:Tool, where:Construction|Storage) -> None:
        '''
        Перевезти инструмент на другой объект
        '''

        with Database() as db:
            
            location = self.__locate(db, tool.id)
            
            self.__close_post(db, location)
            
            self.__move(db, tool, where)
            
            db.commit() # сохраняем изменения
    


    @BaseCRUD.logger.info
    def __move(self, db:Session, tool:Tool, where:Storage|StorageTable|Construction|ConstrTable) -> None:
        '''
        Добавить запись о храненнии инструмента
        '''

        if isinstance(where, StorageTable|Storage):
            place = ToolsOnStorage
        elif isinstance(where, ConstrTable|Construction): 
            place = ToolsOnConstr

        post = place(tool_id=tool.id,
                     place_id=where.id)

        db.add(post)

    
    @BaseCRUD.logger.info
    def __locate(self, db:Session, tool_id:int) -> ToolsOnConstr|ToolsOnStorage:
        '''
        Определить местоположение инструмента
        '''

        constr = db.query(ToolsOnConstr).filter(ToolsOnConstr.tool_id==tool_id,
                                                ToolsOnConstr.end_date==None).all()
        storage = db.query(ToolsOnStorage).filter(ToolsOnStorage.tool_id==tool_id,
                                                ToolsOnStorage.end_date==None).all()

        if constr:
            return constr[0]
        else:
            return storage[0]
            

    @BaseCRUD.logger.info
    def __close_post(self, db:Session, location:ToolsOnConstr|ToolsOnStorage) -> None:
        '''
        Записывает дату окончания хранения 
        инструмента на объекте строительства
        '''

        db.query(type(location)).filter(type(location).id == location.id
                                           ).update({type(location).end_date:datetime.now()}, synchronize_session = False)
    


    @convertertation
    @BaseCRUD.logger.info
    def get_construction(self, tool_id:int) -> Construction|None:
        '''
        Получить объект, на котором
        находится инструмент
        ''' 

        with Database() as db:
            place = db.query(ToolsOnConstr.place_id).filter(ToolsOnConstr.tool_id==tool_id, 
                                                                  ToolsOnConstr.end_date==None).all()
            if place:
                constr = db.get(ConstrTable, place[0])
            else:
                place = db.query(ToolsOnStorage.place_id).filter(ToolsOnStorage.tool_id==tool_id, 
                                                                  ToolsOnStorage.end_date==None).all()
                constr = db.get(StorageTable, place[0])
            
            return constr
    


    def retire(self, tool_id:int) -> None:
        '''
        Удалить инструмент

        Ставит дату закрытия (продажи, списания)
        '''
        with Database() as db:
            
            location = self.__locate(db, tool_id)
            self.__close_post(db, location)

            db.query(self.table).filter(self.table.id == tool_id).update({self.table.end_date:datetime.now()}, synchronize_session = False)
            
            db.commit()