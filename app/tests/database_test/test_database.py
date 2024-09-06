from app.entities import Construction, Storage, Tool, Worker
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.workerCRUD import WorkerCRUD
from typing import Tuple


class TestDatabase():
    '''
    Класс для тестирования БД
    '''

    def test_add_construction(self, constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тест метода по добавлению сущности (ConstructionCRUD.add())
        '''

        constr_db:Construction = constr_crud.add(constr)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert constr_db.name==constr.name



    def test_add_storage(self, storage:Storage, stor_crud:StorageCRUD):
        '''
        Тест метода по добавлению склада (StorageCRUD.add())
        '''

        storage_db:Storage = stor_crud.add(storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert storage_db.name==storage.name



    def test_add_worker(self, worker:Worker, work_crud:WorkerCRUD):
        '''
        Тест метода по добавлению работника (WorkerCRUD.add())
        '''

        worker_db:Worker = work_crud.add(worker)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert worker_db.name==worker.name



    def test_add_tool_for_storage(self, tool:Tool, exist_storage:Storage, tool_crud:ToolCRUD, stor_crud:StorageCRUD):
        '''
        Тест метода по добавлению инструмента на склад (ToolCRUD.add())
        '''
        tool_db:Tool = tool_crud.add(tool=tool, where=exist_storage)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert tool_db.name==tool.name
        
        # Находится ли инструмент на складе (таблица tools_on_storage)
        assert tool_db.id in stor_crud.get_tools(exist_storage.id)

    

    def test_add_tool_for_construction(self, tool:Tool, exist_constr:Construction, tool_crud:ToolCRUD, constr_crud:ConstructionCRUD):
        '''
        Тест метода по добавлению инструмента на объект (ToolCRUD.add())
        '''
        tool_db:Tool = tool_crud.add(tool=tool, where=exist_constr)

        # Данные генерируются уникальные, поэтому хватит одной проверки
        assert tool_db.name==tool.name
        
        # Находится ли инструмент на складе (таблица tools_on_storage)
        assert tool_db.id in constr_crud.get_tools(exist_constr.id)



    def test_get_by_id(self, exist_storage:Storage, stor_crud:StorageCRUD):
        '''
        Тест метода по получению сущности по id
        '''
        
        storage_in_db:Storage = stor_crud.get_by_id(exist_storage.id)
        assert storage_in_db.name == exist_storage.name



    def test_get_all_item(self, exist_storage:Storage, stor_crud:StorageCRUD):
        '''
        Тест метода по получению всех сущностей
        '''

        assert stor_crud.get_all(exist_storage.firm_id)
        


    def test_downgrade(self, item_cruds:Tuple[ConstructionCRUD, StorageCRUD, ToolCRUD, WorkerCRUD]):
        '''
        Тестирование метода по изменению статуса на False
        '''

        items = [crud.get_by_id(id=1) for crud in item_cruds]
        
        self.__status_operations(cruds=item_cruds, items=items, mode=False)

        for crud in item_cruds:
            # Если статус сущности не False, тест провален
            assert not crud.get_by_id(id=1).status
    


    def test_increase(self, item_cruds:Tuple[ConstructionCRUD, StorageCRUD, ToolCRUD, WorkerCRUD]):
        '''
        Тестирование метода по изменению статуса на True (Base.modify_status(True))
        '''

        items = [crud.get_by_id(id=1) for crud in item_cruds]
        
        self.__status_operations(cruds=item_cruds, items=items)

        for crud in item_cruds:
            # Если статус сущности не True, тест провален
            assert crud.get_by_id(id=1).status
            


    def __status_operations(self, cruds:Tuple[ConstructionCRUD, StorageCRUD, ToolCRUD, WorkerCRUD], items:list, mode=True):
        '''
        Операции по изменению статуса у списка сущностей
        '''

        # Изменяем статус каждой сущности в зависимости от mode
        [crud.modify_status(obj_id=item.id, status=mode) for item, crud in zip(items, cruds)]



    def test_get_tools_from_storage(self, exist_storage:Storage, stor_crud:StorageCRUD, tool:Tool, tool_crud:ToolCRUD):
        '''
        Тестирование метода по получению инструмента со склада
        (StorageCRUD.get_tools())
        '''

        new_tool:Tool = tool_crud.add(tool=tool, where=exist_storage)

        tools_on_stor = stor_crud.get_tools(exist_storage.id)

        assert tools_on_stor and new_tool.id in tools_on_stor



    def test_get_tools_from_construction(self, exist_constr:Construction, constr_crud:ConstructionCRUD, tool:Tool, tool_crud:ToolCRUD):
        '''
        Тестирование метода по получению инструмента с объекта строительства
        (ConstructionCRUD.get_tools())
        '''

        new_tool:Tool = tool_crud.add(tool=tool, where=exist_constr)

        tools_on_constr = constr_crud.get_tools(exist_constr.id)

        assert tools_on_constr and new_tool.id in tools_on_constr



    def test_transfer_worker(self, exist_constr:Construction, exist_worker:Worker, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по переводу работника на объект 
        (ConstructionCRUD.transfer_worker(brigadir=False))
        '''
        
        assert not constr_crud.get_workers(exist_constr.id) and not work_crud.get_construction(exist_worker.id)

        # Перевод работника на объект
        constr_crud.transfer_worker(constr_id=exist_constr.id, worker_id=exist_worker.id)

        assert constr_crud.get_workers(exist_constr.id) or not constr_crud.get_responsible(exist_constr.id)
        assert work_crud.get_construction(exist_worker.id).id==exist_constr.id or not work_crud.is_brigadir(exist_worker.id)



    def test_transfer_brigadir(self, exist_constr:Construction, exist_worker:Worker, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект 
        (ConstructionCRUD.transfer_worker(brigadir=True))
        '''

        assert not constr_crud.get_responsible(exist_constr.id) or not work_crud.is_brigadir(exist_worker.id)

        # Перевод работника на объект как ответственного
        constr_crud.transfer_worker(exist_constr.id, exist_worker.id, brigadir=True)

        assert constr_crud.get_responsible(exist_constr.id)

        assert exist_worker.id in constr_crud.get_workers(exist_constr.id)

        assert work_crud.is_brigadir(exist_worker.id).id==exist_constr.id
    


    def test_move_tool(self, exist_constr:Construction, exist_tool:Tool, tool_crud:ToolCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по перемещению инструмента
        (ToolCRUD.move_to())
        '''

        old_constr:Construction|Storage = tool_crud.get_construction(exist_tool.id)

        assert old_constr

        assert not constr_crud.get_tools(exist_constr.id)
        
        tool_crud.move_to(tool=exist_tool, where=exist_constr)

        assert type(tool_crud.get_construction(exist_tool.id)) is type(exist_constr) or tool_crud.get_construction(exist_tool.id).id!=old_constr.id
        
        assert exist_tool.id in constr_crud.get_tools(exist_constr.id)