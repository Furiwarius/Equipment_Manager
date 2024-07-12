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
from app.service.validator.validator import ValidatorEssence, DataValidator


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
    
    # Классы валидаторы
    valid_essence = ValidatorEssence()
    valid_data = DataValidator()


    def __init__(self, constr:Construction) -> None:
        '''
        При передаче constr взятого из БД
        продолжает с ним рабоать.
        Если объект новый, то пытается добавить его в БД.
        '''

        self.constr_crud = ConstructionCRUD()
        self.tool_crud = ToolCRUD()


        if constr.id is None:
            self.valid_essence.validate_construction(constr)
            
            self.constr=self.constr_crud.add(constr)

        else:
            self.constr = constr     



    def appointment_responsible(self, worker:Worker) -> None:
        '''
        Назначить ответственного
        '''
        self.__works_check()
        if not worker.status:
            raise WorkerDoesntWork

        self.constr_crud.transfer_worker(constr_id=self.constr.id, worker_id=worker.id, brigadir=True)
    


    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''

        self.__works_check()

        if not worker.status:
            raise WorkerDoesntWork

        self.constr_crud.transfer_worker(constr_id=self.constr.id, worker_id=worker.id, brigadir=False)



    def add_tool(self, tool:Tool) -> Tool:
        '''
        Добавить инструмент на объект
        '''

        self.valid_essence.validate_tool(tool)
        self.__works_check()

        if not tool.status:
            raise ToolBroken

        elif self.constr_crud.get_responsible(self.constr.id) is None:
            raise ResponsibleAbsent

        result = self.tool_crud.add(tool, self.constr)
        
        return result


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
        if self.constr_crud.get_tools(self.constr.id): 
            raise ImpossibleCloseConstruction
        
        self.constr_crud.modify_status(self.constr.id, False)
    


    def open_construction(self):
        '''
        Возобновление строительства
        '''
        self.constr_crud.modify_status(self.constr.id, True)
    


    def __works_check(self) -> None:
        '''
        Проверка на работоспособность объекта
        
        Если объект закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.constr.status is ConstructionStatus.finished:
            raise ConstructionClosed
