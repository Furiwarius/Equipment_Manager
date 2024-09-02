import pytest
from app.service.construction.construction import ConstructionManager as ConstrM
from app.service.storage.storage import StorageManager as StorM
from app.service.worker.worker import WorkerManager as WorkM
from app.service.tool.tool import ToolManager as ToolM
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.workerCRUD import WorkerCRUD
from app.errors.service_error.validator_error import BaseValidatorException
from app.errors.service_error.construction_error import ResponsibleAbsent
from app.errors.service_error.worker_error import WorkerDoesntWork
from app.errors.service_error.tool_error import ToolBroken
from app.entities import Construction, Storage, Tool, Worker


class TestBusinessLogic():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''


    def test_add_storage(self, storage:Storage, stor_crud:StorageCRUD):
        '''
        Тестрирование метода по добавлению склада
        '''

        storage_manager = StorM(storage)

        assert stor_crud.get_last_one().id is storage_manager.storage.id


    
    def test_add_broken_storage(self, storage:Storage, stor_crud:StorageCRUD):
        '''
        Тестирование исключений выпадающих 
        при добавлении склада с неправильными атрибутами
        '''

        with pytest.raises(BaseValidatorException):
            storage.name = "   "

            StorM(storage)
        
        assert stor_crud.get_last_one().name != storage.name     



    def test_add_tool_in_storage(self, tool:Tool, exist_storage:Storage, stor_crud:StorageCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на склад
        '''
        
        stor_manager:StorM = StorM(exist_storage)
        
        tool:Tool = stor_manager.add_tool(tool)      

        assert tool.id in stor_crud.get_tools(exist_storage.id) 



    def test_add_construction(self, constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению объекта строительства
        ''' 

        constr_manager:ConstrM = ConstrM(constr)

        assert constr_crud.get_last_one().id is constr_manager.constr.id



    def test_add_tool_in_construction_without_responsible(self, tool:Tool, exist_constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        без ответственного лица
        '''

        with pytest.raises(ResponsibleAbsent):
            
            constr_m:ConstrM = ConstrM(exist_constr)
            constr_m.add_tool(tool)


    
    def test_add_worker(self, worker:Worker, work_crud:WorkerCRUD):
        '''
        Тестирование метода по добавлению работника
        '''

        worker_manager:WorkM = WorkM(worker)

        assert work_crud.get_last_one().id is worker_manager.worker.id



    def test_appointment_healthy_responsible(self, exist_worker:Worker, exist_constr:Construction, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''

        assert exist_worker.status

        assert not constr_crud.get_responsible(exist_constr.id)

        constr_m:ConstrM = ConstrM(exist_constr)
        constr_m.appointment_responsible(exist_worker)
        
        assert work_crud.is_brigadir(exist_worker.id).id is exist_constr.id
        assert constr_crud.get_responsible(exist_constr.id).id is exist_worker.id
    


    def test_add_tool_in_construction_with_responsible(self, tool:Tool, constr_with_responsible:Construction, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        с имеющимся ответственным лицом
        '''
     
        assert constr_crud.get_responsible(constr_with_responsible.id)

        constr_m = ConstrM(constr_with_responsible)
        assert constr_m.constr.id is constr_with_responsible.id

        tool:Tool = constr_m.add_tool(tool)
        
        assert tool.id in constr_crud.get_tools(constr_m.constr.id)



    def test_appointment_sick_responsible(self, exist_worker:Worker, exist_constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''

        assert not constr_crud.get_responsible(exist_constr.id)

        worker_m:WorkM = WorkM(exist_worker)
        worker_m.get_sick() 
        
        assert not worker_m.worker.status

        constr_m:ConstrM = ConstrM(exist_constr)

        with pytest.raises(WorkerDoesntWork):
            constr_m.appointment_responsible(worker_m.worker)
        
        assert not constr_crud.get_responsible(constr_m.constr.id)


    
    def test_appointment_engaged_responsible(self, constr:Construction, constr_with_responsible:Construction, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению на объект ответственного 
        лица с уже имеющимся объектом и инструментами на нем
        '''
        
        responsible:Worker = constr_crud.get_responsible(constr_with_responsible.id)
        assert responsible

        constr_m = ConstrM(constr)
        constr_m.appointment_responsible(responsible)

        assert constr_crud.get_responsible(constr_m.constr.id).id is responsible.id
        assert not constr_crud.get_responsible(constr_with_responsible.id)
        assert work_crud.is_brigadir(responsible.id).id is constr_m.constr.id



    def test_move_tool(self, storage_with_tool:Storage, exist_tool:Tool, constr_with_responsible:Construction, stor_crud:StorageCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по перемещению работающего 
        инструмента со склада на объект
        '''

        assert stor_crud.get_tools(storage_with_tool.id)

        tool_m:ToolM = ToolM(exist_tool)
        tool_m.move_tool_to_construction(constr_with_responsible)
        
        assert tool_m.tool.id in constr_crud.get_tools(constr_with_responsible.id)    
        assert tool_m.tool.id not in stor_crud.get_tools(storage_with_tool.id)

        

    def test_move_broken_tool(self, exist_tool:Tool, storage_with_tool:Storage, constr_with_responsible:Construction, constr_crud:ConstructionCRUD, tool_crud:ToolCRUD):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со склада на объект
        '''

        tool_m:ToolM = ToolM(exist_tool)
        tool_m.break_tool()

        assert not tool_m.tool.status

        with pytest.raises(ToolBroken):
            StorM(storage_with_tool).move_tool_to_construction(tool_crud.get_by_id(exist_tool.id), constr_with_responsible)

        assert exist_tool.id not in constr_crud.get_tools(constr_with_responsible.id)



    def test_move_broken_tool_to_storage(self, exist_tool:Tool, constr_with_tool:Construction, exist_storage:Storage, constr_crud:ConstructionCRUD, stor_crud:StorageCRUD):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со объекта на склад
        '''
        tool_m:ToolM = ToolM(exist_tool)
        tool_m.break_tool()

        ConstrM(constr_with_tool).move_tool_to_storage(exist_tool, exist_storage)

        assert exist_tool.id not in constr_crud.get_tools(constr_with_tool.id)
        assert exist_tool.id in stor_crud.get_tools(exist_storage.id)



    def test_remove_tool_from_stock(self, tool:Tool, exist_storage:Storage, stor_crud:StorageCRUD):
        '''
        Удаление инструмента со склада
        '''
        stor_m = StorM(exist_storage)

        tool:Tool = stor_m.add_tool(tool)

        stor_m.delete_tool(tool)

        assert tool.id not in stor_crud.get_tools(exist_storage.id)
