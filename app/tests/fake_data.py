from app.entities.tool import Tool
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.storage import Storage
from datetime import datetime
from random import randrange


class DataGenerator():
    '''
    Генератор данных
    '''
    # набор уникальных цифр
    numbers = set([number for number in range(1000)])


    def __generate_number(self) -> int:
        '''
        Генерация уникальной цифры
        '''
        value = tuple(self.numbers)[randrange(0, len(self.numbers)-1)]
        self.numbers.discard(value)
        return value


    def worker_generator(self, status=True) -> Worker:
        '''
        Генератор работников
        '''
        
        random_number = self.__generate_number()

        new_worker = Worker(id=None,
                            account_id=None,
                            name=f"name{random_number}",
                            surname=f"surname{random_number}",
                            phone_number=randrange(89000000000, 89999999999),
                            job_title=f"jobtitle{random_number}",
                            start_date=datetime.now(),
                            end_date=None,
                            status=status)
        
        return new_worker
    

    def tool_generator(self, status=True) -> Tool:
        '''
        Генератор инструментов
        '''
        random_number = self.__generate_number()

        new_tool = Tool(id=None,
                             name=f"tool{random_number}",
                             factory_number=f"factory_number{random_number}",
                             status=status,
                             start_date=datetime.now(),
                             end_date=None)
        
        return new_tool
    

    def constr_generator(self, status=True) -> Construction:
        '''
        Генератор объектов
        '''
        random_number = self.__generate_number()

        new_construction = Construction(id=None,
                                        name=f"construction{random_number}",
                                        project=f"project{random_number}",
                                        address=f"address{random_number}",
                                        status=status,
                                        start_date=datetime.now(),
                                        end_date=None)
        
        return new_construction


    def storage_generator(self, status=True) -> Storage:
        '''
        Генератор данных склада
        '''
        random_number = f"S{self.__generate_number()}"

        new_storage = Storage(id=None,
                              name=f"storage{random_number}",
                              address=f"address{random_number}",
                              status=status,
                              start_date=datetime.now(),
                              end_date=None)
        
        return new_storage