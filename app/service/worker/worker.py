from app.entities.construction import Construction
from app.entities.worker import Worker
from app.errors.service_error.worker_error import ImpossibleDismiss
import enum
from app.errors.service_error.construction_error import ConstructionClosed
from app.database.crud.workerCRUD import WorkerCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD

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
        WorkerCRUD.downgrade(self.worker)


    def dismiss(self) -> None:
        '''
        Уволить работника
        '''
        if WorkerCRUD.is_brigadir(self.worker):
            raise ImpossibleDismiss
        
        WorkerCRUD.retire(self.worker)
        

    def get_well(self) -> None:
        '''
        Работник выздоравливает
        '''     
        WorkerCRUD.increase(self.worker)


    def change_construction(self, constr:Construction) -> None:
        '''
        Сменить объект
        '''
        if not constr.status:
            raise ConstructionClosed
            
        ConstructionCRUD.transfer_worker(construction=constr, worker=self.worker, brigadir=False)