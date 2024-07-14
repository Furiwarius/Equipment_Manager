from app.database.tables.base import Base
from app.entities.construction import Construction as Constr
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from app.database.database import Database
from sqlalchemy.orm import Session
from app.database.converter import Converter
from datetime import datetime
from app.loggers.database_logger.db_logger import DatabaseLogger


class BaseCRUD():
    '''
    Базовый класс для взаимодействия с БД
    '''

    logger = DatabaseLogger()
    logger.get_logger()


    def __init__(self, table:Base) -> None:
        
        self.table:Base = table
        self.coverter = Converter()


    @logger.info
    def add(self, obj:Worker|Constr|Storage) -> Worker|Constr|Storage:
        '''
        Добавить сущности
        '''
        obj = self.coverter.conversion_to_table(obj)
        with Database() as db:

            db.add(obj)     # добавляем в бд
            db.commit()     # сохраняем изменения
            
            result = db.query(self.table).order_by(self.table.id.desc()).first()

        return self.coverter.conversion_to_data(result)



    @logger.info
    def get_all(self) -> list:
        '''
        Получить id сущност

        Метод смотрит поле table,
        и по нему ищет данные в БД
        '''

        with Database() as db:
            result = db.query(self.table.id).all()
            result = [item[0] for item in result]

        return list(result)
            

    @logger.info
    def get_by_id(self, id:int) -> Tool|Constr|Storage|Worker:
        '''
        Получить сущность по id
        '''
        
        with Database() as db:
            result = db.get(self.table, id)
        
        return self.coverter.conversion_to_data(result)
    


    @logger.info
    def modify_status(self, obj_id:int, status:bool) -> None:
        '''
        Поменять статус
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == obj_id).update({self.table.status:status}, synchronize_session = False)
            db.commit()



    @logger.info
    def retire(self, obj_id:int) -> None:
        '''
        Удалить объект

        Ставит дату закрытия (увольнения)
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == obj_id).update({self.table.end_date:datetime.now()}, synchronize_session = False)
            db.commit()
    


    def get_last_one(self) -> Constr|Storage|Tool|Worker:
        '''
        Получить последнего добавленного в таблицу
        '''
        with Database() as db:
            result = db.query(self.table).order_by(self.table.id.desc()).first()

        return self.coverter.conversion_to_data(result)

