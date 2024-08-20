import pytest_asyncio
from faker import Faker
from app.entities.account import Account
from random import randrange
from app.service.password.password_generator.password_generator import PasswordGenerator
from app.utilities.random_timezone import get_random_timezone
from app.entities.firm import Firm
from app.entities.tool import Tool
from app.entities.construction import Construction
from app.entities.worker import Worker
from app.entities.storage import Storage
from app.database.crud.accountCRUD import AccountCRUD
from app.database.crud.firmCRUD import FirmCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.workerCRUD import WorkerCRUD




# набор уникальных цифр
numbers = set([number for number in range(1000)])



@pytest_asyncio.fixture(scope="session")
def fake():
    return Faker(locale="ru")



@pytest_asyncio.fixture(scope="session")
def password():
    return PasswordGenerator().run_generation(size=16)



@pytest_asyncio.fixture(scope="session")
def generate_number() -> int:
        '''
        Генерация уникальной цифры
        '''
        value = tuple(numbers)[randrange(0, len(numbers)-1)]
        numbers.discard(value)

        return value



@pytest_asyncio.fixture(scope="session")
def account_generate(fake, generate_number, password) -> Account:
    '''
    Генератор данных аккаунта
    '''

    new_account = Account(login=f"login{generate_number}",
                              password=password,
                              email=fake.email(),
                              confirmation_status=True,
                              timezone=get_random_timezone())

    return new_account



@pytest_asyncio.fixture(scope="session")
def firm_generate(fake) -> Firm:
    '''
    Генератор данных фирмы
    '''

    new_firm = Firm(name=fake.company(),
                        status=True)

    return new_firm



@pytest_asyncio.fixture(scope="class")
def firm_id(account_generate, firm_generate) -> int:
    '''
    Создает фирму для тестов
    '''

    account = AccountCRUD().add(account_generate)
    firm = FirmCRUD().add(account_id=account.id, 
                          new_firm=firm_generate)
    
    return firm.id



@pytest_asyncio.fixture(scope="function")
def storage(firm_id, generate_number, fake) -> Storage:
    '''
    Генератор данных склада
    '''

    new_storage = Storage(name=f"storage №{generate_number}",
                              address=fake.address(),
                              status=True,
                              firm_id=firm_id)
    
    return new_storage



@pytest_asyncio.fixture(scope="function")
def constr(firm_id, generate_number, fake) -> Construction:
    '''
    Генератор объектов
    '''

    new_construction = Construction(name=fake.company(),
                                        project=f"project №{generate_number}",
                                        address=fake.address(),
                                        status=True,
                                        firm_id=firm_id)

    return new_construction



@pytest_asyncio.fixture(scope="function")
def tool(firm_id, generate_number, fake) -> Tool:
    '''
    Генератор инструментов
    '''

    new_tool = Tool(name=f"tool{generate_number}",
                        factory_number=fake.vin(),
                        status=True,
                        firm_id=firm_id)
        
    return new_tool



@pytest_asyncio.fixture(scope="function")
def worker(firm_id, fake) -> Worker:
    '''
    Генератор работников
    '''

    new_worker = Worker(name=fake.first_name(),
                            surname=fake.last_name(),
                            phone_number=''.join(list(filter(str.isdigit, list(fake.phone_number())))),
                            job_title=fake.job(),
                            status=True,
                            firm_id=firm_id)

    return new_worker



@pytest_asyncio.fixture(scope="session")
def constr_crud() -> ConstructionCRUD:
    return ConstructionCRUD()



@pytest_asyncio.fixture(scope="session")
def stor_crud() -> StorageCRUD:
    return StorageCRUD()



@pytest_asyncio.fixture(scope="session")
def tool_crud() -> ToolCRUD:
     
    return ToolCRUD()



@pytest_asyncio.fixture(scope="session")
def work_crud() -> WorkerCRUD:
     
    return WorkerCRUD()



@pytest_asyncio.fixture(scope="session")
def item_cruds(constr_crud, stor_crud, tool_crud, work_crud) -> tuple:
     
    return (constr_crud, stor_crud, tool_crud, work_crud)