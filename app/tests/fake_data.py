from app.entities.tool import Tool
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.storage import Storage
from datetime import datetime, timezone
from app.entities.firm import Firm
from app.entities.account import Account
from random import randrange
from faker import Faker
from app.service.password.password_generator.password_generator import PasswordGenerator
from app.utilities.random_timezone import get_random_timezone



class DataGenerator():
    '''
    Генератор данных
    '''

    # набор уникальных цифр
    numbers = set([number for number in range(1000)])

    fake = Faker("ru_RU")
    
    password = PasswordGenerator()



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

        new_worker = Worker(name=self.fake.first_name(),
                            surname=self.fake.last_name(),
                            phone_number=self.fake.phone_number(),
                            job_title=self.fake.job(),
                            start_date=datetime.now(timezone.utc),
                            status=status)
        
        return new_worker
    


    def tool_generator(self, status=True) -> Tool:
        '''
        Генератор инструментов
        '''
        random_number = self.__generate_number()

        new_tool = Tool(name=f"tool{random_number}",
                        factory_number=self.fake.vin(),
                        status=status,
                        start_date=datetime.now(timezone.utc))
        
        return new_tool
    


    def constr_generator(self, status=True) -> Construction:
        '''
        Генератор объектов
        '''
        random_number = self.__generate_number()

        new_construction = Construction(name=self.fake.company(),
                                        project=f"project №{random_number}",
                                        address=self.fake.address(),
                                        status=status,
                                        start_date=datetime.now(timezone.utc))
        
        return new_construction



    def storage_generator(self, status=True) -> Storage:
        '''
        Генератор данных склада
        '''
        random_number = f"S{self.__generate_number()}"

        new_storage = Storage(name=f"storage №{random_number}",
                              address=self.fake.address(),
                              status=status,
                              start_date=datetime.now(timezone.utc))
        
        return new_storage



    def firm_generate(self, status=True) -> Firm:
        '''
        Генератор данных фирмы
        '''

        new_firm = Firm(name=self.fake.company(),
                        status=status,
                        start_date=datetime.now(timezone.utc))

        return new_firm



    def account_generate(self, status=True) -> Account:
        '''
        Генератор данных аккаунта
        '''

        new_account = Account(login=self.fake.first_name(),
                              password=self.password.run_generation(size=16),
                              email=self.fake.email(),
                              confirmation_status=status,
                              timezone=get_random_timezone())

        return new_account