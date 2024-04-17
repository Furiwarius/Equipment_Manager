from tool import Tool
from construction import Construction
from worker import Worker
from my_exception import NonWorkingComponent, checking_incoming_objects


class ToolManager():
    '''
    Менеджер инструмента
    '''

    def __init__(self, tool: Tool) -> None:
        if type(tool)!=Tool:
            raise TypeError("Передан неиспользуемый класс")
        self.tool = tool
    

    def filling_fields (self, construction:Construction, responsible:Worker) -> None:
        '''
        Первоначальное заполненние полей инструмента
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.filling_fields.__annotations__, [construction, responsible])
        
        self.tool.change_construction(construction)
        self.tool.change_responsible(responsible)
        

    def set_construction(self, new_construction:Construction) -> None:
        '''
        Изменение объекта,
        на котором находится инструмент
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.set_construction.__annotations__, [new_construction])
        
        self.tool.change_construction(new_construction)
        

    def set_responsible(self, new_responsible:Worker) -> None:
        '''
        Изменение ответственного,
        в подчинении у которого
        находится инструмент
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.set_responsible.__annotations__, [new_responsible])

        self.tool.change_responsible(new_responsible)


class WorkerManager():
    '''
    Менеджер работников
    '''

    def __init__(self, worker: Worker) -> None:
        if type(worker)!=Worker:
            raise TypeError("Передан неиспользуемый класс")
        self.worker = worker


    def set_construction(self, construction:Construction) -> None:
        '''
        Изменение поля с объектом
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.set_construction.__annotations__, [construction])

        self.worker.change_construction(construction)


class ConstructionManager():
    '''
    Менеджер работников
    '''

    def __init__(self, construction: Construction) -> None:
        if type(construction)!=Construction:
            raise TypeError("Передан неиспользуемый класс")
        self.construction = construction


    def set_responsible(self, responsible:Worker) -> None:
        '''
        Изменение поля с ответственным
        '''

        # Проверка передаваемых значений
        checking_incoming_objects(self.set_responsible.__annotations__, [responsible])

        self.construction.change_responsible(responsible)
        
