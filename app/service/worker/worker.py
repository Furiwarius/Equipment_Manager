from app.entities.construction import Construction
from app.entities.worker import Worker
from app.errors.service_error.worker_error import ImpossibleDismiss
import enum
from app.errors.service_error.construction_error import ConstructionClosed
from app.database.crud.workerCRUD import WorkerCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.service.validator.validator import ValidatorEssence, DataValidator



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


    # Классы валидаторы
    valid_essence = ValidatorEssence()
    valid_data = DataValidator()


    def __init__(self, worker: Worker) -> None:
        
        self.worker_crud = WorkerCRUD()
        self.constr_crud = ConstructionCRUD()

        if worker.id is None:
            self.valid_essence.validate_worker(worker)
            
            self.worker = self.worker_crud.add(worker)
            
        else: 
            self.worker = worker



    def get_sick(self) -> None:
        '''
        Работник заболевает
        '''
        self.worker_crud.modify_status(self.worker.id, False)
        self.worker.status = False



    def dismiss(self) -> None:
        '''
        Уволить работника
        '''
        if self.worker_crud.is_brigadir(self.worker):
            raise ImpossibleDismiss
        
        self.worker_crud.retire(self.worker.id)
        

    def get_well(self) -> None:
        '''
        Работник выздоравливает
        '''     
        self.worker_crud.modify_status(self.worker.id, True)
        self.worker.status = True



    def change_construction(self, constr:Construction) -> None:
        '''
        Сменить объект
        '''
        if not constr.status:
            raise ConstructionClosed
            
        self.constr_crud.transfer_worker(constr_id=constr.id, worker_id=self.worker.id, brigadir=False)