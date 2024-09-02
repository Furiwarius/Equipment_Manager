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
from app.database.crud.firmCRUD import FirmCRUD
from app.database.crud.accountCRUD import AccountCRUD
from typing import AsyncGenerator, Generator
from app import app
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.utilities.hashing import to_hash
from copy import copy
from app.service.construction.construction import ConstructionManager
from app.service.storage.storage import StorageManager



# набор уникальных цифр
numbers = set([number for number in range(1000)])



@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"



@pytest_asyncio.fixture(scope="session")
def client() -> Generator:
    yield TestClient(app)



@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client.base_url) as ac:
        yield ac
        


@pytest_asyncio.fixture(scope="session")
def fake() -> Faker:
    return Faker(locale="ru")



@pytest_asyncio.fixture(scope="function")
def password() -> str:
    return PasswordGenerator().run_generation(size=16)



@pytest_asyncio.fixture(scope="function")
def generate_number() -> int:
        '''
        Генерация уникальной цифры
        '''
        value = tuple(numbers)[randrange(0, len(numbers)-1)]
        numbers.discard(value)

        return value



@pytest_asyncio.fixture(scope="function")
def account(fake:Faker, generate_number:int, password:str) -> Account:
    '''
    Генератор данных аккаунта
    '''

    new_account = Account(login=f"{fake.first_name()}{generate_number}",
                              password=password,
                              email=fake.email(),
                              confirmation_status=False,
                              timezone=get_random_timezone())

    return new_account



@pytest_asyncio.fixture(scope="function")
def firm(fake:Faker) -> Firm:
    '''
    Генератор данных фирмы
    '''

    new_firm = Firm(name=fake.company(),
                        status=True)

    return new_firm



@pytest_asyncio.fixture(scope="function")
def firm_id(fake:Faker, account:Account) -> int:
    '''
    Создает фирму для тестов
    '''

    account = AccountCRUD().add(account)
    firm:Firm = FirmCRUD().add(account_id=account.id, 
                          new_firm=Firm(name=fake.company(), status=True))
    
    return firm.id



@pytest_asyncio.fixture(scope="function")
def storage(firm_id:int, generate_number:int, fake:Faker) -> Storage:
    '''
    Генератор данных склада
    '''

    new_storage = Storage(name=f"storage №{generate_number}",
                              address=fake.address(),
                              status=True,
                              firm_id=firm_id)
    
    return new_storage



@pytest_asyncio.fixture(scope="function")
def constr(firm_id:int, generate_number:int, fake:Faker) -> Construction:
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
def tool(firm_id:int, generate_number:int, fake:Faker) -> Tool:
    '''
    Генератор инструментов
    '''

    new_tool = Tool(name=f"tool{generate_number}",
                        factory_number=fake.vin(),
                        status=True,
                        firm_id=firm_id)
        
    return new_tool



@pytest_asyncio.fixture(scope="function")
def worker(firm_id:int, fake:Faker) -> Worker:
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



@pytest_asyncio.fixture(scope="function")
def exist_worker(worker:Worker, work_crud:WorkerCRUD) -> Worker:
    '''
    Генератор работника занесенного в бд
    '''
    return work_crud.add(worker)



@pytest_asyncio.fixture(scope="function")
def exist_constr(constr:Construction, constr_crud:ConstructionCRUD) -> Construction:
    '''
    Генератор конструкции занесенного в бд
    '''
    return constr_crud.add(constr)



@pytest_asyncio.fixture(scope="function")
def exist_storage(storage:Storage, stor_crud:StorageCRUD) -> Storage:
    '''
    Генератор склада занесенного в бд
    '''
    return stor_crud.add(storage)



@pytest_asyncio.fixture(scope="function")
def exist_tool(tool:Tool, tool_crud:ToolCRUD, exist_storage:Storage) -> Tool:
    '''
    Генератор инструмента занесенного в бд
    '''
    return tool_crud.add(tool, exist_storage)



@pytest_asyncio.fixture(scope="function")
def constr_with_responsible(exist_constr:Construction, exist_worker:Worker) -> Construction:
    '''
    Генератор конструкции занесенной в бд с назначенным ответственным
    '''

    ConstructionManager(exist_constr).appointment_responsible(exist_worker)

    return exist_constr


@pytest_asyncio.fixture(scope="function")
def storage_with_tool(exist_storage:Storage, tool:Tool) -> Storage:
    '''
    Генератор склада занесенного в бд с инструментами в нем
    '''

    StorageManager(exist_storage).add_tool(tool)

    return exist_storage



@pytest_asyncio.fixture(scope="function")
def constr_with_tool(constr_with_responsible:Construction, tool:Tool) -> Storage:
    '''
    Генератор склада занесенного в бд с инструментами в нем
    '''

    ConstructionManager(constr_with_responsible).add_tool(tool)

    return constr_with_responsible



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
def firm_crud() -> FirmCRUD:
     
    return FirmCRUD()



@pytest_asyncio.fixture(scope="session")
def acc_crud() -> AccountCRUD:
     
    return AccountCRUD()


@pytest_asyncio.fixture(scope="function")
def exist_account(account:Account, acc_crud:AccountCRUD) -> Account:
    '''
    Генератор данных аккаунта добавленного в бд
    '''
    new_account = copy(account)
    new_account.login = to_hash(new_account.login)
    new_account.password = to_hash(new_account.password)
    
    new_account:Account = acc_crud.add(new_account)
    account.id = new_account.id

    return account


@pytest_asyncio.fixture(scope="function")
def exist_firm(firm:Firm, exist_account:Account, firm_crud:FirmCRUD) -> Firm:
    '''
    Генератор данных фирмы добавленной в бд
    '''
    return firm_crud.add(exist_account.id, firm)



@pytest_asyncio.fixture(scope="session")
def item_cruds(constr_crud:ConstructionCRUD, stor_crud:StorageCRUD, tool_crud:ToolCRUD, work_crud:WorkerCRUD) -> tuple:
     
    return (constr_crud, stor_crud, tool_crud, work_crud)