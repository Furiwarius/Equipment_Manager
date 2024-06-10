from app.database.tables.essence import ConstructionTable as ConstrTable
from app.database.tables.essence import StorageTable
from app.database.tables.essence import WorkerTable
from app.database.tables.essence import ToolTable
from app.database.tables.base import Base
from app.entities.construction import Construction as Constr
from app.database.tables.summary import ToolsOnConstructions
from app.database.tables.summary import WorksOnConstructions
from app.database.tables.summary import ToolsOnStorage
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from app.database.database import Database
from sqlalchemy.orm import Session
from app.database.converter import Converter
from datetime import datetime


class BaseCRUD():
    '''
    Базовый класс для взаимодействия с БД
    '''

    def __init__(self, table:Base) -> None:
        
        self.table:Base = table
        db = Database()
        self.engine = db.new_engine()
        self.coverter = Converter()

    

    def add(self, obj:Worker|Constr|Storage) -> None:
        '''
        Добавить сущности
        '''
        obj = self.coverter.conversion_to_table(obj)
        with Session(autoflush=False, bind=self.engine) as db:

            db.add(obj)     # добавляем в бд
            db.commit()     # сохраняем изменения
    

    def get_all(self) -> list:
        '''
        Получить сущности

        Метод смотрит поле table,
        и по нему ищет данные в БД
        '''

        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(self.table).all()
        
        return [self.coverter.conversion_to_data(item) for item in result]
            

    def get_by_id(self, id:int) -> Tool|Constr|Storage|Worker:
        '''
        Получить сущность по id
        '''
        
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.get(self.table, id)
        
        return self.coverter.conversion_to_data(result)
    

    def downgrade(self, obj:Tool|Constr|Storage|Worker) -> None:
        '''
        Поменять статус на False
        '''
        obj = self.coverter.conversion_to_table(obj)
        with Session(autoflush=False, bind=self.engine) as db:
            db.query(self.table).filter(self.table.id == obj.id).update({self.table.status:False}, synchronize_session = False)
            db.commit()


    def increase(self, obj:Tool|Constr|Storage|Worker) -> None:
        '''
        Поменять статус объекта на True
        '''
        obj = self.coverter.conversion_to_table(obj)
        with Session(autoflush=False, bind=self.engine) as db:
            db.query(self.table).filter(self.table.id == obj.id).update({self.table.status:True}, synchronize_session = False)
            db.commit()


    def retire(self, obj:Tool|Constr|Storage|Worker) -> None:
        '''
        Удалить объект

        Ставит дату закрытия (увольнения)
        '''
        obj = self.coverter.conversion_to_table(obj)
        with Session(autoflush=False, bind=self.engine) as db:
            db.query(self.table).filter(self.table.id == obj.id).update({self.table.end_date:datetime.now()}, synchronize_session = False)
            db.commit()
