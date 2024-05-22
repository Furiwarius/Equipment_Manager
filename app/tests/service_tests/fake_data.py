from app.service.essence.fields.construction import Construction, ConstructionStatus
from app.service.essence.fields.worker import StatusWorker, Worker
from app.service.essence.fields.tool import  Tool, ToolStatus
from app.service.essence.fields.warehouse import  Storage
from datetime import datetime
from random import randrange


class DataGenerator():
    '''
    Генератор данных
    '''

    def worker_generator(self) -> Worker:
        '''
        Генератор работников
        '''
        random_id = randrange(1, 100)
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
    

    def tool_renerator(self) -> Tool:
        '''
        Генератор инструментов
        '''
        random_id = randrange(1, 100)
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
    

    def constr_generator(self) -> Construction:
        '''
        Генератор объектов
        '''
        random_id = randrange(1, 100)
        name = f"construction{random_id}"
        project = f"project{random_id}"
        status = ConstructionStatus.under_construction
        date = datetime.now()
        worker = None
        tools = dict()

        new_construction = Construction(id=random_id,
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
        random_id = randrange(1, 100)
        name = f"storage{random_id}"
        tools = dict()

        new_storage = Storage(id=random_id,
                              name=name,
                              tools=tools)
        return new_storage