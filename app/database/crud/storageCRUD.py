from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD


class StorageCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table="storage")


    def get_tools(self, storage:Storage) -> dict:
        '''
        Получить инструменты на складе 


        Выдает словарь в виде id: Tool 
        '''
        
        return {Tool.id: Tool}