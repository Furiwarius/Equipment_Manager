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
            broken_storage = storage
            broken_storage.name = "   "

            StorM(broken_storage)
        
        assert stor_crud.get_last_one().name != broken_storage.name     



    def test_add_tool_in_storage(self, tool:Tool, stor_crud:StorageCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на склад
        '''
        
        storage = stor_crud.get_last_one()
        stor_manager = StorM(storage)
        
        tool = stor_manager.add_tool(tool)      

        assert tool.id in stor_crud.get_tools(storage.id) 



    def test_add_construction(self, constr:Construction, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению объекта строительства
        ''' 

        constr_manager = ConstrM(constr)

        assert constr_crud.get_last_one().id is constr_manager.constr.id



    def test_add_tool_in_construction_without_responsible(self, tool:Tool, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        без ответственного лица
        '''

        with pytest.raises(ResponsibleAbsent):
            
            constr = constr_crud.get_last_one()
            
            constr_m = ConstrM(constr)
            constr_m.add_tool(tool)


    
    def test_add_worker(self, worker:Worker, work_crud:WorkerCRUD):
        '''
        Тестирование метода по добавлению работника
        '''

        worker_manager = WorkM(worker)

        assert work_crud.get_last_one().id is worker_manager.worker.id



    def test_appointment_healthy_responsible(self, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''

        worker = work_crud.get_last_one()
        assert worker.status

        constr = constr_crud.get_last_one()
        assert not constr_crud.get_responsible(constr.id)

        constr_m = ConstrM(constr)
        constr_m.appointment_responsible(worker)
        
        assert work_crud.is_brigadir(worker.id).id is constr.id
        assert constr_crud.get_responsible(constr.id).id is worker.id
    


    def test_add_tool_in_construction_with_responsible(self, tool:Tool, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        с имеющимся ответственным лицом
        '''

        constr = constr_crud.get_last_one()
        
        assert constr_crud.get_responsible(constr.id)

        constr_m = ConstrM(constr)
        assert constr_m.constr.id is constr.id

        tool = constr_m.add_tool(tool)
        
        assert tool.id in constr_crud.get_tools(constr_m.constr.id)



    def test_appointment_sick_responsible(self, worker:Worker, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''

        constr = constr_crud.get_last_one()
        assert constr_crud.get_responsible(constr.id)

        worker_m = WorkM(worker)
        worker_m.get_sick() 
        
        assert not worker_m.worker.status

        constr_m = ConstrM(constr)

        with pytest.raises(WorkerDoesntWork):
            constr_m.appointment_responsible(worker_m.worker)
        
        assert constr_crud.get_responsible(constr_m.constr.id).id!=worker_m.worker.id


    
    def test_appointment_engaged_responsible(self, constr:Construction, work_crud:WorkerCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по назначению на объект ответственного 
        лица с уже имеющимся объектом и инструментами на нем
        '''
        
        old_constr = constr_crud.get_last_one()
        responsible = constr_crud.get_responsible(old_constr.id)
        assert responsible

        constr_m = ConstrM(constr)
        constr_m.appointment_responsible(responsible)

        assert constr_crud.get_responsible(constr_m.constr.id).id is responsible.id
        assert not constr_crud.get_responsible(old_constr.id)
        assert work_crud.is_brigadir(responsible.id).id is constr_m.constr.id



    def test_move_tool(self, storage:Storage, constr:Construction, worker:Worker, tool:Tool, stor_crud:StorageCRUD, constr_crud:ConstructionCRUD):
        '''
        Тестирование метода по перемещению работающего 
        инструмента со склада на объект
        '''

        stor_m = StorM(storage)

        # Создаем объект строительства
        constr_m = ConstrM(constr)

        # Создаем работника и назначаем его ответственным на объекте
        constr_m.appointment_responsible(WorkM(worker).worker)

        # Помещаем инструмент на склад
        tool = stor_m.add_tool(tool)

        assert tool.id in stor_crud.get_tools(stor_m.storage.id)

        tool_m = ToolM(tool)
        tool_m.move_tool_to_construction(constr_m.constr)
        
        assert tool.id in constr_crud.get_tools(constr_m.constr.id)    
        assert tool.id not in stor_crud.get_tools(stor_m.storage.id)

        

    def test_move_broken_tool(self, tool:Tool, stor_crud:StorageCRUD, constr_crud:ConstructionCRUD, tool_crud:ToolCRUD):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со склада на объект
        '''
        storage = stor_crud.get_last_one()
        stor_m = StorM(storage)

        tool = stor_m.add_tool(tool)

        tool_m = ToolM(tool)
        tool_m.break_tool()

        assert not tool_m.tool.status

        constr = constr_crud.get_last_one()
        assert constr_crud.get_responsible(constr.id)

        with pytest.raises(ToolBroken):
            stor_m.move_tool_to_construction(tool_crud.get_by_id(tool.id), constr)

        assert tool.id not in constr_crud.get_tools(constr.id)



    def test_move_broken_tool_to_storage(self, tool:Tool, constr_crud:ConstructionCRUD, stor_crud:StorageCRUD):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со объекта на склад
        '''

        constr = constr_crud.get_last_one()
        constr_m = ConstrM(constr)

        tool:Tool = constr_m.add_tool(tool)

        tool_m:ToolM = ToolM(tool)
        tool_m.break_tool()

        storage:Storage = stor_crud.get_last_one()

        constr_m.move_tool_to_storage(tool, storage)

        assert tool.id not in constr_crud.get_tools(constr.id)
        assert tool.id in stor_crud.get_tools(storage.id)



    def test_remove_tool_from_stock(self, tool:Tool, stor_crud:StorageCRUD):
        '''
        Удаление инструмента со склада
        '''
        stor:Storage = stor_crud.get_last_one()
        stor_m = StorM(stor)

        tool:Tool = stor_m.add_tool(tool)

        stor_m.delete_tool(tool)

        assert tool.id not in stor_crud.get_tools(stor.id)
