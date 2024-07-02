from app.entities.construction import Construction
from app.entities.worker import Worker
from app.errors.service_error.worker_error import ImpossibleDismiss, WorkerValid
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
        
        self.worker_crud = WorkerCRUD()
        self.constr_crud = ConstructionCRUD()

        if worker.id is None:
            if not self._validate_worker(worker):
                raise WorkerValid
            
            self.worker_crud.add(worker)
            self.worker = self.worker_crud.get_all()[-1]

        else: 
            self.worker = worker


    def _validate_worker(self, worker:Worker) -> bool:
        '''
        Метод для проверки получаемых данных
        '''


    def get_sick(self) -> None:
        '''
        Работник заболевает
        '''
        self.worker_crud.downgrade(self.worker)


    def dismiss(self) -> None:
        '''
        Уволить работника
        '''
        if self.worker_crud.is_brigadir(self.worker):
            raise ImpossibleDismiss
        
        self.worker_crud.retire(self.worker)
        

    def get_well(self) -> None:
        '''
        Работник выздоравливает
        '''     
        self.worker_crud.increase(self.worker)


    def change_construction(self, constr:Construction) -> None:
        '''
        Сменить объект
        '''
        if not constr.status:
            raise ConstructionClosed
            
        self.constr_crud.transfer_worker(construction=constr, worker=self.worker, brigadir=False)