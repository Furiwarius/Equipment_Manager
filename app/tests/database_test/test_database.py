from app.tests.fake_data import DataGenerator
from app.database.database import Database
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.workerCRUD import WorkerCRUD
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



class TestDatabase():
    '''
    Класс для тестирования БД
    '''

    generator = DataGenerator()
    
    constr_crud = ConstructionCRUD()
    stor_crud = StorageCRUD()
    work_crud = WorkerCRUD()
    tool_crud = ToolCRUD()

    cruds = (work_crud, tool_crud, constr_crud, stor_crud)


    firm_id = create_firm()


    def test_add_construction(self):
        '''
        Тест метода по добавлению сущности (ConstructionCRUD.add())
        '''

        constr = self.generator.constr_generator(firm_id=self.firm_id)
        constr_db = self.constr_crud.add(constr)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert constr_db.name==constr.name



    def test_add_storage(self):
        '''
        Тест метода по добавлению склада (StorageCRUD.add())
        '''

        storage = self.generator.storage_generator(firm_id=self.firm_id)
        storage_db = self.stor_crud.add(storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert storage_db.name==storage.name



    def test_add_worker(self):
        '''
        Тест метода по добавлению работника (WorkerCRUD.add())
        '''

        worker = self.generator.worker_generator(firm_id=self.firm_id)
        worker_db = self.work_crud.add(worker)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert worker_db.name==worker.name



    def test_add_tool(self):
        '''
        Тест метода по добавлению инструмента (ToolCRUD.add())
        '''
        # Тк до этого добавляли склад, он есть в бд
        storage = self.stor_crud.get_by_id(id=1)
        tool = self.generator.tool_generator(firm_id=self.firm_id)
        tool_db = self.tool_crud.add(tool=tool, where=storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert tool_db.name==tool.name
        
        # Находится ли инструмент на складе (таблица tools_on_storage)
        assert tool_db.id in self.stor_crud.get_tools(storage.id)



    def test_get_by_id(self):
        '''
        Тест метода по получению сущности по id (Base.get_by_id())
        '''
        
        # В предыдущем тесте добавлен инструмент
        assert self.tool_crud.get_by_id(id=1) is not None
        


    def test_get_all_item(self):
        '''
        Тест метода по получению всех сущностей (Base.get_all())
        '''

        # Тк предыдущие тесты добавляли сущности, их и будем получать
        workers = self.work_crud.get_all(self.firm_id)   
        constructions = self.constr_crud.get_all(self.firm_id)
        tools = self.tool_crud.get_all(self.firm_id)
        storages = self.stor_crud.get_all(self.firm_id)

        assert workers and constructions and tools and storages
        


    def test_downgrade(self):
        '''
        Тестирование метода по изменению статуса на False (Base.modify_status(False))
        '''

        items = [crud.get_by_id(id=1) for crud in self.cruds]
        
        self.__status_operations(items=items, mode=False)

        for crud in self.cruds:
            # Если статус сущности не False, тест провален
            assert not crud.get_by_id(id=1).status
    


    def test_increase(self):
        '''
        Тестирование метода по изменению статуса на True (Base.modify_status(True))
        '''

        items = [crud.get_by_id(id=1) for crud in self.cruds]
        
        self.__status_operations(items=items)

        for crud in self.cruds:
            # Если статус сущности не True, тест провален
            assert crud.get_by_id(id=1).status
            


    def __status_operations(self, items:list, mode=True):
        '''
        Операции по изменению статуса у списка сущностей
        '''

        # Изменяем статус каждой сущности в зависимости от mode
        [crud.modify_status(obj_id=item.id, status=mode) for item, crud in zip(items, self.cruds)]



    def test_get_tools(self):
        '''
        Тестирование метода по получению инструмента с места хранения
        (StorageCRUD.get_tools() | ConstructionCRUD.get_tools())
        '''

        new_constr = self.generator.constr_generator(firm_id=self.firm_id)
        constr = self.constr_crud.add(new_constr)
        
        tools_on_stor = self.stor_crud.get_tools(self.stor_crud.get_by_id(id=1).id)
        tools_on_constr = self.constr_crud.get_tools(self.constr_crud.get_by_id(constr.id))

        assert tools_on_stor and not tools_on_constr
        


    def test_transfer_worker(self):
        '''
        Тестирование метода по переводу работника на объект 
        (ConstructionCRUD.transfer_worker(brigadir=False))
        '''
        new_worker = self.generator.worker_generator(firm_id=self.firm_id)
        worker = self.work_crud.add(new_worker)    
        constr = self.constr_crud.get_last_one()

        assert not self.constr_crud.get_workers(constr.id) and not self.work_crud.get_construction(worker.id)

        # Перевод работника на объект
        self.constr_crud.transfer_worker(constr_id=constr.id, worker_id=worker.id)

        assert self.constr_crud.get_workers(constr.id) or not self.constr_crud.get_responsible(constr.id)
        
        assert self.work_crud.get_construction(worker.id).id==constr.id or not self.work_crud.is_brigadir(worker.id)



    def test_transfer_brigadir(self):
        '''
        Тестирование метода по назначению ответственного лица на объект 
        (ConstructionCRUD.transfer_worker(brigadir=True))
        '''
        # Генерация нового работника
        new_worker = self.generator.worker_generator(firm_id=self.firm_id)    
        new_worker = self.work_crud.add(new_worker)

        constr = self.constr_crud.get_by_id(id=1)

        assert not self.constr_crud.get_responsible(constr.id) or not self.work_crud.is_brigadir(new_worker.id)

        # Перевод работника на объект как ответственного
        self.constr_crud.transfer_worker(constr.id, new_worker.id, brigadir=True)

        assert self.constr_crud.get_responsible(constr.id)

        assert new_worker.id in self.constr_crud.get_workers(constr.id)

        assert self.work_crud.is_brigadir(new_worker.id).id==constr.id
    


    def test_move_tool(self):
        '''
        Тестирование метода по перемещению инструмента
        (ToolCRUD.move_to())
        '''
        tool = self.tool_crud.get_by_id(id=1)
        old_constr = self.tool_crud.get_construction(tool.id)

        assert old_constr

        new_constr = self.generator.constr_generator(firm_id=self.firm_id)
        new_constr = self.constr_crud.add(new_constr)


        assert not self.constr_crud.get_tools(new_constr.id)
        
        self.tool_crud.move_to(tool=tool, where=new_constr)

        assert self.tool_crud.get_construction(tool.id).id!=old_constr.id
        
        assert tool.id in self.constr_crud.get_tools(new_constr.id)