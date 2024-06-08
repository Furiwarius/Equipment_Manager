from app.database.tables.essence import ConstructionTable as ConstrTable
from app.database.tables.essence import StorageTable
from app.database.tables.essence import WorkerTable
from app.database.tables.essence import ToolTable
from app.entities.construction import Construction as Constr
from app.database.tables.summary import ToolsOnConstructions
from app.database.tables.summary import WorksOnConstructions
from app.database.tables.summary import ToolsOnStorage
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from app.database.database import Database
from sqlalchemy.orm import Session


class BaseCRUD():
    '''
    Базовый класс для взаимодействия с БД
    '''

    def __init__(self, table:str) -> None:
        
        self.table = table
        db = Database()
        self.engine = db.new_engine()

    

    def add(self, object:WorkerTable|ConstrTable|StorageTable) -> None:
        '''
        Добавить сущности

        Метод для добавления работника,
        склада или объекта строительства.
        Добавляет в ту таблицу, которая 
        указана в поле table.
        '''

        with Session(autoflush=False, bind=self.engine) as db:

            db.add(object)     # добавляем в бд
            db.commit()     # сохраняем изменения
    

    def get_all(self) -> list:
        '''
        Получить сущности

        Метод смотрит поле table,
        и по нему ищет данные в БД
        '''
    

    def get_by_id(self, id:int) -> Tool|Constr|Storage|Worker:
        '''
        Получить сущность по id

        Ищет в таблице указанной
        в поле table.
        '''
    

    def downgrade(self, object:ToolTable|ConstrTable|StorageTable|WorkerTable) -> None:
        '''
        Поменять статус на False
        '''
    

    def increase(self, object:ToolTable|ConstrTable|StorageTable|WorkerTable) -> None:
        '''
        Поменять статус объекта на True
        '''
    

    def retire(self, object:ToolTable|ConstrTable|StorageTable|WorkerTable) -> None:
        '''
        Удалить объект

        Ставит дату закрытия (увольнения)
        '''
