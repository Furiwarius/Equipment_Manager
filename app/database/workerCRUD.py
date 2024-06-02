from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.entities.storage import Storage


class WorkerCRUD():
    '''
    Класс для взаимодействия с БД
    '''
    

    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''
    

    def dismiss(self, worker:Worker) -> None:
        '''
        Уволить работника
        '''
    

    def sick(self, worker:Worker) -> None:
        '''
        Работник заболевает
        '''
    

    def get_well(self, worker:Worker) -> None:
        '''
        Работник выздоравливает
        '''
    

    def change_construction(self, worker:Worker, constr:Construction) -> None:
        '''
        Перевести работник на объект
        '''