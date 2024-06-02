from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage


class StorageCRUD():
    '''
    Класс для взаимодействия с БД
    '''

    
    def add_storage(self, storage:Storage) -> None:
        '''
        Добавить склад
        '''


    def add_tool(self, storage:Storage, tool:Tool) -> None:
        '''
        Добавить инструмент на склад
        '''
    

    def delete_tool(self, storage:Storage, tool:Tool) -> None:
        '''
        Удалить инструмент со склада

        При продаже инструмента
        '''
    

    def close(self, storage:Storage) -> None:
        '''
        Закрыть склад
        '''
    

    def work(self, storage:Storage) -> None:
        '''
        Возобновить работу склада
        '''