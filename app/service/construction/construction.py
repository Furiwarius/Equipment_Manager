import enum
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.storage_error import StockClosed
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent
from app.errors.service_error.construction_error import ImpossibleCloseConstruction
from app.errors.service_error.worker_error import WorkerDoesntWork
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.toolCRUD import ToolCRUD


class ConstructionStatus(enum.Enum):
    '''
    Статус объекта
    '''
    works = True
    finished = False


class ConstructionManager():
    '''
    Управляющий класс для стройки
    '''
    
    def __init__(self, constr:Construction) -> None:

        self.constr = constr       


    def appointment_responsible(self, worker:Worker) -> None:
        '''
        Назначить ответственного
        '''
        self.__works_check()
        if not worker.status:
            raise WorkerDoesntWork

        ConstructionCRUD.transfer_worker(construction=self.constr, worker=worker, brigadir=True)
    

    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''

        self.__works_check()

        if not worker.status:
            raise WorkerDoesntWork

        ConstructionCRUD.transfer_worker(construction=self.constr, worker=worker, brigadir=False)


    def add_tool(self, tool:Tool) -> None:
        '''
        Добавить инструмент на объект
        '''

        self.__works_check()

        if not tool.status:
            raise ToolBroken

        elif ConstructionCRUD.get_responsible(self.constr) is None:
            raise ResponsibleAbsent

        ToolCRUD.move_to(self.constr, tool)
        

    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перевезти инструмент с объекта на склад
        '''
        if not where.status:
            raise StockClosed

        ToolCRUD.move_to_storage(tool, where)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перевезти инструмент с объекта на объект
        '''
        if not where.status:
            raise ConstructionClosed
        
        elif not tool.status:
            raise ToolBroken

        ToolCRUD.move_to(tool, where)


    def close_construction(self) -> None:
        '''
        Закрытие объекта строительства
        '''
        if ConstructionCRUD.get_tools(): 
            raise ImpossibleCloseConstruction
        
        ConstructionCRUD.downgrade(self.constr)
    

    def open_construction(self):
        '''
        Возобновление строительства
        '''
        ConstructionCRUD.increase(self.constr)
    

    def __works_check(self) -> None:
        '''
        Проверка на работоспособность объекта
        
        Если объект закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.constr.status is ConstructionStatus.finished:
            raise ConstructionClosed

