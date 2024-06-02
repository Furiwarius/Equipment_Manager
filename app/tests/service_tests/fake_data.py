from app.service.construction.construction import ConstructionManager, ConstructionStatus
from app.service.worker.worker import StatusWorker, Worker
from app.service.tool.tool import  Tool, ToolStatus
from app.service.storage.storage import  Storage
from datetime import datetime
from random import randrange


class DataGenerator():
    '''
    Генератор данных
    '''
    # набор цифр, которые будут использоваться как id
    id = set([number for number in range(1000)])


    def __generate_id(self) -> int:
        '''
        Генерация уникального id
        '''
        value = tuple(self.id)[randrange(0, len(self.id)-1)]
        self.id.discard(value)
        return value


    def worker_generator(self) -> Worker:
        '''
        Генератор работников
        '''
        random_id = self.__generate_id()
        name = f"name{random_id}"
        surname = f"surname{random_id}"
        phone = randrange(89000000000, 89999999999)
        job_title = f"jobtitle{random_id}"
        date = datetime.now()
        status = StatusWorker.works
        construction = None

        new_worker = Worker(id=random_id,
                                name=name,
                                surname=surname,
                                phone_number=phone,
                                job_title=job_title,
                                start_work=date,
                                status=status,
                                construction=construction)
        return new_worker
    

    def tool_generator(self) -> Tool:
        '''
        Генератор инструментов
        '''
        random_id = self.__generate_id()
        name = f"tool{random_id}"
        date = datetime.now()
        status = ToolStatus.works
        construction = None

        new_tool = Tool(id=random_id,
                             name=name,
                             import_date=date,
                             status=status,
                             construction=construction)
        return new_tool
    

    def constr_generator(self) -> ConstructionManager:
        '''
        Генератор объектов
        '''
        random_id = f"C{self.__generate_id()}"
        name = f"construction{random_id}"
        project = f"project{random_id}"
        status = ConstructionStatus.works
        date = datetime.now()
        worker = None
        tools = dict()

        new_construction = ConstructionManager(id=random_id,
                                        name=name,
                                        project=project,
                                        status=status,
                                        date_creation=date,
                                        worker=worker,
                                        tools=tools)
        return new_construction


    def storage_generator(self) -> Storage:
        '''
        Генератор данных склада
        '''
        random_id = f"S{self.__generate_id()}"
        name = f"storage{random_id}"
        tools = dict()

        new_storage = Storage(id=random_id,
                              name=name,
                              tools=tools)
        return new_storage