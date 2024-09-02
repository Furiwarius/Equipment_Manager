from app.entities import Construction, Storage, Tool, Worker
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.workerCRUD import WorkerCRUD



class TestDatabase():
    '''
    Класс для тестирования БД
    '''

    def test_add_construction(self, constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тест метода по добавлению сущности (ConstructionCRUD.add())
        '''

        constr_db = constr_crud.add(constr)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert constr_db.name==constr.name



    def test_add_storage(self, storage:Storage, stor_crud:StorageCRUD):
        '''
        Тест метода по добавлению склада (StorageCRUD.add())
        '''

        storage_db = stor_crud.add(storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert storage_db.name==storage.name



    def test_add_worker(self, worker:Worker, work_crud:WorkerCRUD):
        '''
        Тест метода по добавлению работника (WorkerCRUD.add())
        '''

        worker_db = work_crud.add(worker)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert worker_db.name==worker.name



    def test_add_tool(self, tool:Tool, storage:Storage, tool_crud:ToolCRUD, stor_crud:StorageCRUD):
        '''
        Тест метода по добавлению инструмента (ToolCRUD.add())
        '''
        # Тк до этого добавляли склад, он есть в бд
        new_storage = stor_crud.add(storage)
        tool_db = tool_crud.add(tool=tool, where=new_storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert tool_db.name==tool.name
        
        # Находится ли инструмент на складе (таблица tools_on_storage)
        assert tool_db.id in stor_crud.get_tools(new_storage.id)



    def test_get_by_id(self, item_cruds:tuple):
        '''
        Тест метода по получению сущности по id (Base.get_by_id())
        '''
        
        # В предыдущих тестах были добавлены элементы
        for crud in item_cruds:

            assert crud.get_by_id(id=1) is not None
        


    def test_get_all_item(self, constr_crud:ConstructionCRUD, tool_crud:ToolCRUD, work_crud:WorkerCRUD, stor_crud:StorageCRUD, firm_id:int):
        '''
        Тест метода по получению всех сущностей (Base.get_all())
        '''

        # Тк предыдущие тесты добавляли сущности, их и будем получать
        workers = work_crud.get_all(firm_id)   
        constructions = constr_crud.get_all(firm_id)
        tools = tool_crud.get_all(firm_id)
        storages = stor_crud.get_all(firm_id)

        assert workers 
        assert constructions 
        assert tools 
        assert storages
        


    def test_downgrade(self, item_cruds:tuple):
        '''
        Тестирование метода по изменению статуса на False (Base.modify_status(False))
        '''

        items = [crud.get_by_id(id=1) for crud in item_cruds]
        
        self.__status_operations(cruds=item_cruds, items=items, mode=False)

        for crud in item_cruds:
            # Если статус сущности не False, тест провален
            assert not crud.get_by_id(id=1).status
    


    def test_increase(self, item_cruds:tuple):
        '''
        Тестирование метода по изменению статуса на True (Base.modify_status(True))
        '''

        items = [crud.get_by_id(id=1) for crud in item_cruds]
        
        self.__status_operations(cruds=item_cruds, items=items)

        for crud in item_cruds:
            # Если статус сущности не True, тест провален
            assert crud.get_by_id(id=1).status
            


    def __status_operations(self, cruds:tuple, items:list, mode=True):
        '''
        Операции по изменению статуса у списка сущностей
        '''

        # Изменяем статус каждой сущности в зависимости от mode
        [crud.modify_status(obj_id=item.id, status=mode) for item, crud in zip(items, cruds)]



    def test_get_tools(self, constr:Construction, storage:Storage, constr_crud:ConstructionCRUD, stor_crud:StorageCRUD, tool:Tool, tool_crud:ToolCRUD):
        '''
        Тестирование метода по получению инструмента с места хранения
        (StorageCRUD.get_tools() | ConstructionCRUD.get_tools())
        '''

        constr = constr_crud.add(constr)
        
        storage = stor_crud.add(storage)
        tool_crud.add(tool=tool, where=storage)

        tools_on_stor = stor_crud.get_tools(stor_crud.get_by_id(storage.id).id)
        tools_on_constr = constr_crud.get_tools(constr_crud.get_by_id(constr.id).id)


        assert tools_on_stor and not tools_on_constr
        


    def test_transfer_worker(self, worker:Worker, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по переводу работника на объект 
        (ConstructionCRUD.transfer_worker(brigadir=False))
        '''
        
        worker = work_crud.add(worker)    
        constr = constr_crud.get_last_one()

        assert not constr_crud.get_workers(constr.id) and not work_crud.get_construction(worker.id)

        # Перевод работника на объект
        constr_crud.transfer_worker(constr_id=constr.id, worker_id=worker.id)

        assert constr_crud.get_workers(constr.id) or not constr_crud.get_responsible(constr.id)
        assert work_crud.get_construction(worker.id).id==constr.id or not work_crud.is_brigadir(worker.id)



    def test_transfer_brigadir(self, worker:Worker, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект 
        (ConstructionCRUD.transfer_worker(brigadir=True))
        '''
        # Генерация нового работника
        new_worker = work_crud.add(worker)

        constr = constr_crud.get_by_id(id=1)

        assert not constr_crud.get_responsible(constr.id) or not work_crud.is_brigadir(new_worker.id)

        # Перевод работника на объект как ответственного
        constr_crud.transfer_worker(constr.id, new_worker.id, brigadir=True)

        assert constr_crud.get_responsible(constr.id)

        assert new_worker.id in constr_crud.get_workers(constr.id)

        assert work_crud.is_brigadir(new_worker.id).id==constr.id
    


    def test_move_tool(self, constr:Construction, tool_crud:ToolCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по перемещению инструмента
        (ToolCRUD.move_to())
        '''
        tool = tool_crud.get_by_id(id=1)
        old_constr = tool_crud.get_construction(tool.id)

        assert old_constr

        new_constr = constr_crud.add(constr)


        assert not constr_crud.get_tools(new_constr.id)
        
        tool_crud.move_to(tool=tool, where=new_constr)

        assert tool_crud.get_construction(tool.id).id!=old_constr.id
        
        assert tool.id in constr_crud.get_tools(new_constr.id)