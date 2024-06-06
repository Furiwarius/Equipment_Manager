from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD


class WorkerCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table="worker")
       
    
    def get_construction(self, worker:Worker) -> Construction:
        '''
        Получить объект, на котором
        находится работник
        ''' 
    

    def is_brigadir(self, worker:Worker) -> Construction:
        '''
        Метод определяющий является
        ли работник ответственным лицом
        '''