import enum
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.tool import Tool
from app.entities.storage import Storage
from app.errors.service_error.storage_error import StockClosed
from app.errors.service_error.tool_error import ToolBroken
from app.errors.service_error.construction_error import ConstructionClosed, ResponsibleAbsent
from app.errors.service_error.construction_error import ImpossibleCloseConstruction, ConstructionValid
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
        '''
        При передаче constr взятого из БД
        продолжает с ним рабоать.
        Если объект новый, то пытается добавить его в БД.
        '''

        self.constr_crud = ConstructionCRUD()
        self.tool_crud = ToolCRUD()

        if constr.id is None:
            if not self._validate_construction(constr):
                raise ConstructionValid
            
            self.constr_crud.add(constr)
            self.constr=self.constr_crud.get_all()[-1]

        else:
            self.constr = constr       


    def _validate_construction(self, constr:Construction) -> bool:
        '''
        Метод для проверки получаемых данных
        '''


    def appointment_responsible(self, worker:Worker) -> None:
        '''
        Назначить ответственного
        '''
        self.__works_check()
        if not worker.status:
            raise WorkerDoesntWork

        self.constr_crud.transfer_worker(construction=self.constr, worker=worker, brigadir=True)
    

    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''

        self.__works_check()

        if not worker.status:
            raise WorkerDoesntWork

        self.constr_crud.transfer_worker(construction=self.constr, worker=worker, brigadir=False)


    def add_tool(self, tool:Tool) -> None:
        '''
        Добавить инструмент на объект
        '''

        self.__works_check()

        if not tool.status:
            raise ToolBroken

        elif self.constr_crud.get_responsible(self.constr) is None:
            raise ResponsibleAbsent

        self.tool_crud.add(tool, self.constr)
        

    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перевезти инструмент с объекта на склад
        '''
        if not where.status:
            raise StockClosed

        self.tool_crud.move_to(tool, where)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перевезти инструмент с объекта на объект
        '''
        if not where.status:
            raise ConstructionClosed
        
        elif not tool.status:
            raise ToolBroken

        self.tool_crud.move_to(tool, where)


    def close_construction(self) -> None:
        '''
        Закрытие объекта строительства
        '''
        if self.constr_crud.get_tools(self.constr): 
            raise ImpossibleCloseConstruction
        
        self.constr_crud.downgrade(self.constr)
    

    def open_construction(self):
        '''
        Возобновление строительства
        '''
        self.constr_crud.increase(self.constr)
    

    def __works_check(self) -> None:
        '''
        Проверка на работоспособность объекта
        
        Если объект закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.constr.status is ConstructionStatus.finished:
            raise ConstructionClosed
