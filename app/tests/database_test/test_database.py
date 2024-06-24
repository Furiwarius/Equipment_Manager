from app.tests.service_tests.fake_data import DataGenerator
from app.database.database import Database
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.workerCRUD import WorkerCRUD


class TestDatabase():
    '''
    Класс для тестирования БД
    '''

    generator = DataGenerator()

    db = Database()
    # Пересоздаем бд
    db.delete_database()
    db.create_database()

    constr_crud = ConstructionCRUD()
    stor_crud = StorageCRUD()
    work_crud = WorkerCRUD()
    tool_crud = ToolCRUD()

    cruds = (work_crud, tool_crud, constr_crud, stor_crud)


    def test_add_construction(self):
        '''
        Тест метода по добавлению сущности (ConstructionCRUD.add())
        '''

        constr = self.generator.constr_generator()
        self.constr_crud.add(constr)

        # Бд была пуста, поэтому мы точно знаем с каким id добавлен элемент
        constr_db = self.constr_crud.get_by_id(id=1)
        # Данные генерируются уникальные, поэтому хватит одной проверки
        if constr_db.name!=constr.name:
            assert False


    def test_add_storage(self):
        '''
        Тест метода по добавлению склада (StorageCRUD.add())
        '''

        storage = self.generator.storage_generator()
        self.stor_crud.add(storage)

        # Бд была пуста, поэтому мы точно знаем с каким id добавлен элемент
        storage_db = self.stor_crud.get_by_id(id=1)
        # Данные генерируются уникальные, поэтому хватит одной проверки
        if storage_db.name!=storage.name:
            assert False


    def test_add_worker(self):
        '''
        Тест метода по добавлению работника (WorkerCRUD.add())
        '''

        worker = self.generator.worker_generator()
        self.work_crud.add(worker)

        # Бд была пуста, поэтому мы точно знаем с каким id добавлен элемент
        worker_db = self.work_crud.get_by_id(id=1)
        # Данные генерируются уникальные, поэтому хватит одной проверки
        if worker_db.name!=worker.name:
            assert False


    def test_add_tool(self):
        '''
        Тест метода по добавлению инструмента (ToolCRUD.add())
        '''
        # Тк до этого добавляли склад, он есть в бд
        storage = self.stor_crud.get_by_id(id=1)
        tool = self.generator.tool_generator()
        self.tool_crud.add(tool=tool, where=storage)

        # Бд была пуста, поэтому мы точно знаем с каким id добавлен элемент
        tool_db = self.tool_crud.get_by_id(id=1)
        # Данные генерируются уникальные, поэтому хватит одной проверки
        if tool_db.name!=tool.name: 
            assert False
        
        # Находится ли инструмент на складе (таблица tools_on_storage)
        if tool_db.id not in self.stor_crud.get_tools(storage=storage):
            assert False


    def test_get_by_id(self):
        '''
        Тест метода по получению сущности по id (Base.get_by_id())
        '''

        if self.tool_crud.get_by_id(id=100) is None:
            assert True
        
        # В предыдущем тесте добавлен инструмент
        if self.tool_crud.get_by_id(id=1) is None:
            assert False
        

    def test_get_all_item(self):
        '''
        Тест метода по получению всех сущностей (Base.get_all())
        '''

        # Тк предыдущие тесты добавляли сущности, их и будем получать
        workers = self.work_crud.get_all()   
        constructions = self.constr_crud.get_all()
        tools = self.tool_crud.get_all()
        storages = self.stor_crud.get_all()

        if workers and constructions and tools and storages:
            assert True
        else:
            assert False
        

    def test_downgrade(self):
        '''
        Тестирование метода по изменению статуса на False (Base.downgrade())
        '''

        items = [crud.get_by_id(id=1) for crud in self.cruds]
        
        self.__status_operations(items=items, mode=False)

        for crud in self.cruds:
            # Если статус сущности не False, тест провален
            if crud.get_by_id(id=1).status:
                assert False
    

    def test_increase(self):
        '''
        Тестирование метода по изменению статуса на True (Base.increase())
        '''

        items = [crud.get_by_id(id=1) for crud in self.cruds]
        
        self.__status_operations(items=items)

        for crud in self.cruds:
            # Если статус сущности не True, тест провален
            if not crud.get_by_id(id=1).status:
                assert False


    def __status_operations(self, items:list, mode=True):
        '''
        Операции по изменению статуса у списка сущностей
        '''

        # Изменяем статус каждой сущности в зависимости от mode
        if mode: 
            # Выставляем статус True
            [crud.increase(item) for item, crud in zip(items, self.cruds)]
        else: 
            # Выставляем статус False
            [crud.downgrade(item) for item, crud in zip(items, self.cruds)]


    def test_get_tools(self):
        '''
        Тестирование метода по получению инструмента с места хранения
        (StorageCRUD.get_tools() | ConstructionCRUD.get_tools())
        '''

        # Инструмент с id=1 был добавлен на склад с id 1
        # На стройке с id=1 не должно быть инструмента вообще
        tools_on_stor = self.stor_crud.get_tools(self.stor_crud.get_by_id(id=1))
        tools_on_constr = self.constr_crud.get_tools(self.constr_crud.get_by_id(id=1))

        if not tools_on_stor and tools_on_constr:
            assert False
        

    def test_transfer_worker(self):
        '''
        Тестирование метода по переводу работника на объект 
        (ConstructionCRUD.transfer_worker(brigadir=False))
        '''

        worker = self.work_crud.get_by_id(id=1)    
        constr = self.constr_crud.get_by_id(id=1)

        if self.constr_crud.get_workers(constr) and self.work_crud.get_construction(worker):
            assert False

        # Перевод работника на объект
        self.constr_crud.transfer_worker(constr=constr, worker=worker)

        if not self.constr_crud.get_workers(constr) or self.constr_crud.get_responsible(constr):
            assert False
        
        if self.work_crud.get_construction(worker).id!=constr.id or self.work_crud.is_brigadir(worker):
            assert False


    def test_transfer_brigadir(self):
        '''
        Тестирование метода по назначению ответственного лица на объект 
        (ConstructionCRUD.transfer_worker(brigadir=True))
        '''
        # Генерация нового работника
        new_worker = self.generator.worker_generator()    
        self.work_crud.add(new_worker)

        # Получение данных из таблиц
        new_worker = self.work_crud.get_by_id(id=2)
        constr = self.constr_crud.get_by_id(id=1)

        if self.constr_crud.get_responsible(constr) or self.work_crud.is_brigadir(new_worker):
            assert False

        # Перевод работника на объект как ответственного
        self.constr_crud.transfer_worker(constr, new_worker, brigadir=True)

        if not self.constr_crud.get_responsible(constr):
            assert False

        if new_worker.id not in self.constr_crud.get_workers(constr):
            assert False

        if self.work_crud.is_brigadir(new_worker).id!=constr.id:
            assert False