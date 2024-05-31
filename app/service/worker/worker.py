from app.entities.construction import Construction
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.entities.worker import Worker
import enum


class StatusWorker(enum.Enum):
    '''
    Статус работника
    '''
    # Работает
    works = True
    # Уволен
    fired = False
    # В отпуске
    on_holiday = False
    # болеет
    sick = False
    

class WorkerManager():
    '''
    Работник
    '''

    def __init__(self, worker: Worker) -> None:
        
        self.worker = worker

    
    def get_sick(self) -> None:
        '''
        Работник заболевает
        '''
        workerCRUD.sick(self.worker)


    def dismiss(self) -> None:
        '''
        Уволить работника
        '''
        if workerCRUD.is_brigadir(self.worker):
            # Если работник являтеся ответственным на объекте,
            # то вызывает исключение
            pass
        workerCRUD.dismiss(self.worker)
        

    def get_well(self) -> None:
        '''
        Работник выздоравливает
        '''     
        workerCRUD.get_well(self.worker)


    def change_construction(self, constr:Construction) -> None:
        '''
        Сменить объект
        '''
        if not constr.status:
            # Если объект не работает,
            # то вызывает исключение
            pass
        workerCRUD.change_construction(self.worker, constr)