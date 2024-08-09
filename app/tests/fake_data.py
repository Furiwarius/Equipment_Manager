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
from app.database.crud.accountCRUD import AccountCRUD
from app.database.crud.firmCRUD import FirmCRUD



def create_firm() -> int:
    '''
    Создает фирму для тестов
    '''
    new_account = DataGenerator().account_generate()
    new_firm = DataGenerator().firm_generate()

    account = AccountCRUD().add(new_account)
    firm = FirmCRUD().add(account_id=account.id, 
                          new_firm=new_firm)
    
    return firm.id



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



    def worker_generator(self, firm_id:int=None, status=True) -> Worker:
        '''
        Генератор работников
        '''

        new_worker = Worker(name=self.fake.first_name(),
                            surname=self.fake.last_name(),
                            phone_number=''.join(list(filter(str.isdigit, list(self.fake.phone_number())))),
                            job_title=self.fake.job(),
                            status=status)
        if firm_id:
            new_worker.firm_id = firm_id

        return new_worker
    


    def tool_generator(self, firm_id:int=None, status=True) -> Tool:
        '''
        Генератор инструментов
        '''
        random_number = self.__generate_number()

        new_tool = Tool(name=f"tool{random_number}",
                        factory_number=self.fake.vin(),
                        status=status,)
        if firm_id:
            new_tool.firm_id = firm_id

        return new_tool
    


    def constr_generator(self, firm_id:int=None, status=True) -> Construction:
        '''
        Генератор объектов
        '''
        random_number = self.__generate_number()

        new_construction = Construction(name=self.fake.company(),
                                        project=f"project №{random_number}",
                                        address=self.fake.address(),
                                        status=status)
        if firm_id:
            new_construction.firm_id = firm_id

        return new_construction



    def storage_generator(self, firm_id:int=None, status=True) -> Storage:
        '''
        Генератор данных склада
        '''
        random_number = f"S{self.__generate_number()}"

        new_storage = Storage(name=f"storage №{random_number}",
                              address=self.fake.address(),
                              status=status)
        if firm_id:
            new_storage.firm_id = firm_id

        return new_storage



    def firm_generate(self, status=True) -> Firm:
        '''
        Генератор данных фирмы
        '''

        new_firm = Firm(name=self.fake.company(),
                        status=status)

        return new_firm



    def account_generate(self, status=True) -> Account:
        '''
        Генератор данных аккаунта
        '''
        random_number = f"S{self.__generate_number()}"

        new_account = Account(login=f"login{random_number}",
                              password=self.password.run_generation(size=16),
                              email=self.fake.email(),
                              confirmation_status=status,
                              timezone=get_random_timezone())

        return new_account