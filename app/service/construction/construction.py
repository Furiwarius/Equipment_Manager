import enum
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.tool import Tool
from app.entities.storage import Storage


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
            # Если работник не работает,
            # вызывает исключение
            pass

        constructionCRUD.add_worker(construction=self.constr, worker=worker, brigadir=True)
    

    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''

        self.__works_check()

        if not worker.status:
            # Если работник не работает,
            # вызывает исключение
            pass

        constructionCRUD.add_worker(construction=self.constr, worker=worker, brigadir=False)


    def add_tool(self, tool:Tool) -> None:
        '''
        Добавить инструмент на объект
        '''

        self.__works_check()

        if not tool.status:
            # Если инструмент не рабочий,
            # то вызываем исключение
            pass

        if constructionCRUD.get_responsible(self.constr) is None:
            # Если не назначен ответственный,
            # то вызываем исключение 
            pass

        constructionCRUD.add_tool(self.constr, tool)
        

    def move_tool_to_storage(self, tool:Tool, where:Storage) -> None:
        '''
        Перевезти инструмент с объекта на склад
        '''
        if not where.status:
            # Если склад закрыт,
            # вызывает исключение.
            pass

        toolCRUD.move_to_storage(tool, where)
    

    def move_tool_to_construction(self, tool:Tool, where:Construction) -> None:
        '''
        Перевезти инструмент с объекта на объект
        '''
        if not where.status:
            # Кастомное исключение
            # Если объект не рабочий
            pass

        toolCRUD.move_to_construction(tool, where)


    def close_construction(self) -> None:
        '''
        Закрытие объекта строительства
        '''
        if constructionCRUD.get_tools(): 
            # Если на объекте есть инструмент,
            # то вызывается кастомное исключение
            pass
        
        constructionCRUD.close_construction(self.constr)
    

    def open_construction(self):
        '''
        Возобновление строительства
        '''
        constructionCRUD.open_construction(self.constr)
    

    def __works_check(self) -> None:
        '''
        Проверка на работоспособность объекта
        
        Если объект закрыт, то вызывает исключение,
        если работает, то ничего не происходит
        '''
        
        if self.constr.status is ConstructionStatus.finished:
            # КАСТОМНОЕ ИСКЛЮЧЕНИЕ
            pass

