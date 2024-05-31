from app.entities.construction import Construction
from app.entities.worker import Worker
from app.errors.service_error.worker_error import ImpossibleDismiss
import enum
from app.errors.service_error.construction_error import ConstructionClosed


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
            raise ImpossibleDismiss
        
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
            raise ConstructionClosed
            
        workerCRUD.change_construction(self.worker, constr)