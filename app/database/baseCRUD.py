from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction as Constr
from app.entities.storage import Storage


class BaseCRUD():
    '''
    Базовый класс для взаимодействия с БД
    '''

    def __init__(self, table:str) -> None:
        
        self.table = table
    

    def add(self, object:Worker|Constr|Storage) -> None:
        '''
        Добавить сущности

        Метод для добавления работника,
        склада или объекта строительства.
        Добавляет в ту таблицу, которая 
        указана в поле table.
        '''
    

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
    

    def downgrade(self, object:Tool|Constr|Storage|Worker) -> None:
        '''
        Поменять статус на False
        '''
    

    def increase(self, object:Tool|Constr|Storage|Worker) -> None:
        '''
        Поменять статус объекта на True
        '''
    

    def retire(self, object:Tool|Constr|Storage|Worker) -> None:
        '''
        Удалить объект

        Ставит дату закрытия (увольнения)
        '''
