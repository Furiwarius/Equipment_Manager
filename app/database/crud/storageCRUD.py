from app.entities.tool import Tool
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import StorageTable


class StorageCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=StorageTable)


    def get_tools(self, storage:Storage) -> dict:
        '''
        Получить инструменты на складе 


        Выдает словарь в виде id: Tool 
        '''
        
        return {Tool.id: Tool}