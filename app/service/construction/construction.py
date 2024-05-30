import enum
from app.entities.construction import ConstructionTable
from app.entities.worker import WorkerTable
from app.entities.tool import ToolTable
from app.entities.storage import StorageTable


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
    
    def __init__(self, constr:ConstructionTable) -> None:

        self.constr = constr
        self.responsible: int
        self.workers = []
        self.tools = []
       

    def appointment_responsible(self, worker:WorkerTable) -> None:
        '''
        Назначить ответственного

        Идет в бд в таблицу works_on_constructions.
        Если этот работник уже является ответственным
        на другом объекте, то бросает исключение.
        Если нет, то создает новую запись
        с полем is_brigadir = True
        '''
        self.__works_check()
        self.responsible = worker.id
    

    def add_warker(self, worker:WorkerTable) -> None:
        '''
        Добавить работника

        Идет в бд в таблицу works_on_constructions.
        Если у последней записи с этим работником
        в пункте DT_end стоит None, то ставим текущую дату.
        После чего создаем новую запись с текущим объектом
        и работником с полем is_brigadir = False.
        '''
        self.__works_check()
        self.workers.append(worker.id)



    def add_tool(self, tool:ToolTable) -> None:
        '''
        Добавить инструмент на объект
        '''

        self.__works_check()
        if not tool.status:
            # Если инструмент не рабочий,
            # то вызываем исключение
            pass

        if not self.responsible:
            # Если не назначен ответственный,
            # то вызываем исключение 
            pass

        self.tools.append(tool.id)
        

    def move_tool_to_storage(self, tool:ToolTable, where:StorageTable) -> None:
        '''
        Перевезти инструмент с объекта на склад

        Идет в бд и в таблице tool_on_constructions 
        меняет DT_end на текущую. После чего, в таблице
        tools_on_storage  создает новую запись.
        '''
        self.tools.remove(tool.id)
    

    def move_tool_to_construction(self, tool:ToolTable, where:ConstructionTable) -> None:
        '''
        Перевезти инструмент с объекта на объект

        Идет в бд и в таблице tool_on_constructions 
        меняет DT_end на текущую. После чего, в этой же
        таблице создает новую запись с новым объектом.
        '''
        if where.status:
            self.tools.remove(tool.id)
        else:
            # Кастомное исключение
            # Если объект не рабочий
            pass


    def close_construction(self) -> None:
        '''
        Закрытие объекта строительства
        '''
        if self.tools: 
            # Если на объекте есть инструмент,
            # то вызывается кастомное исключение
            pass
        
        self.constr.status= ConstructionStatus.finished
    

    def open_construction(self):
        '''
        Возобновление строительства
        '''
        self.constr.status = ConstructionStatus.works
    

    def __works_check(self) -> None:
        '''
        Проверка на работоспособность объекта
        
        Если объект закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.constr.status is ConstructionStatus.finished:
            # КАСТОМНОЕ ИСКЛЮЧЕНИЕ
            pass

