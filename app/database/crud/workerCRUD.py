from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import WorkerTable


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
    

    def add(self, worker:Worker) -> None:
        '''
        Добавляет объект в бд
        '''
        result = WorkerTable(name=worker.name,
                             surname=worker.surname,
                             phone_number=worker.phone_number,
                             job_title=worker.job_title,
                             start_work=worker.start_work,
                             dismissal_work=worker.dismissal_work,
                             status=worker.status)
        super().add(result)
    

    def is_brigadir(self, worker:Worker) -> Construction:
        '''
        Метод определяющий является
        ли работник ответственным лицом
        '''