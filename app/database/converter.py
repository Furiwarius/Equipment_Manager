from app.entities.tool import Tool
from app.entities.worker import Worker as Work
from app.entities.construction import Construction as Constr
from app.entities.storage import Storage as Stor
from app.database.tables.essence import ConstructionTable as ConstrT
from app.database.tables.essence import WorkerTable as WorkT
from app.database.tables.essence import ToolTable as ToolT
from app.database.tables.essence import StorageTable as StorT

class Converter():
    '''
    Конвертиртер

    Переводит данные из классов таблиц
    в классы с голыми данными для слоя бизнес-логики
    '''

    def conversion_to_data(self, obj:ConstrT|WorkT|ToolT|StorT) -> Tool|Work|Constr|Stor:
        '''
        Конвертация из объекта Table
        в класс в голыми данными
        '''
        if isinstance(obj, ConstrT):
            return self.__conversion_to_constr(obj)
        elif isinstance(obj, StorT):
            return self.__conversion_to_stor(obj)
        elif isinstance(obj, WorkT):
            return self.__conversion_to_work(obj)
        elif isinstance(obj, ToolT):
            return self.__conversion_to_tool(obj)
    

    def __conversion_to_tool(self, tool:ToolT) -> Tool:
        '''
        Переводит данные из класса ToolTable в Tool
        '''
        
        result = Tool(id=tool.id, name=tool.name,
                      status=tool.status, factory_number=tool.factory_number)

        return result


    def __conversion_to_work(self, worker:WorkT) -> Work:
        '''
        Переводит данные из класса WorkerTable в Worker
        '''

        result = Work(id=worker.id, name=worker.name,
                      surname=worker.surname,
                      phone_number=worker.phone_number,
                      job_title=worker.job_title,
                      start_work=worker.start_work,
                      dismissal_work=worker.dismissal_work,
                      status=worker.status)

        return result


    def __conversion_to_constr(self, constr:ConstrT) -> Constr:
        '''
        Переводит данные из класса ConstructionTable в Construction
        '''

        result = Constr(id=constr.id, name=constr.name,
                        project=constr.project,
                        address=constr.address,
                        status=constr.status,
                        start_date=constr.start_date,
                        end_date=constr.end_date)
        
        return result


    def __conversion_to_stor(self, storage:StorT) -> Stor:
        '''
        Переводит данные из класса StorageTable в Storage
        '''
        
        result = Stor(id=storage.id, name=storage.name,
                        address=storage.address,
                        status=storage.status,
                        start_date=storage.start_date,
                        end_date=storage.end_date)
        
        return result
