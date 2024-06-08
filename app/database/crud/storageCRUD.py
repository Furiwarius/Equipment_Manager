from app.entities.tool import Tool
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import StorageTable


class StorageCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table="storage")


    def add(self, storage:Storage) -> None:
        '''
        Добавляет объект в бд
        '''
        result = StorageTable(name=storage.name,
                                   address=storage.address,
                                   status=storage.status,
                                   start_date=storage.start_date,
                                   end_date=storage.end_date)
        super().add(result)


    def get_tools(self, storage:Storage) -> dict:
        '''
        Получить инструменты на складе 


        Выдает словарь в виде id: Tool 
        '''
        
        return {Tool.id: Tool}