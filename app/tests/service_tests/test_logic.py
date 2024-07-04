import pytest
from datetime import datetime
from app.service.construction.construction import ConstructionManager as ConstrM
from app.service.storage.storage import StorageManager as StorM
from app.service.worker.worker import WorkerManager as WorkM
from app.service.tool.tool import ToolManager as ToolM
from app.tests.fake_data import DataGenerator
from app.database.database import Database
from app.database.crud.toolCRUD import ToolCRUD
from app.database.crud.storageCRUD import StorageCRUD
from app.database.crud.constructionCRUD import ConstructionCRUD
from app.database.crud.workerCRUD import WorkerCRUD
from app.errors.service_error.validator_error import BaseValidatorException
from app.errors.service_error.construction_error import ResponsibleAbsent
from app.errors.service_error.worker_error import WorkerDoesntWork
from app.errors.service_error.tool_error import ToolBroken


class TestBusinessLogic():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''

    generator = DataGenerator()

    db = Database()
    # Пересоздаем бд
    db.delete_database()
    db.create_database()

    # круды
    constr_crud = ConstructionCRUD()
    stor_crud = StorageCRUD()
    work_crud = WorkerCRUD()
    tool_crud = ToolCRUD()


    def test_add_storage(self):
        '''
        Тестрирование метода по добавлению склада
        '''
        new_storage = self.generator.storage_generator()

        storage_manager = StorM(new_storage)

        assert self.stor_crud.get_all()[-1].id is storage_manager.storage.id


    
    def test_add_broken_storage(self):
        '''
        Тестирование исключений выпадающих 
        при добавлении склада с неправильными атрибутами
        '''

        with pytest.raises(BaseValidatorException):
            broken_storage = self.generator.storage_generator()
            broken_storage.name = "   "

            StorM(broken_storage)
        
        assert self.stor_crud.get_all()[-1].name != broken_storage.name     



    def test_add_tool_in_storage(self):
        '''
        Тестирование метода по добавлению 
        инструмента на склад
        '''

        new_tool = self.generator.tool_generator()  
        
        storage = self.stor_crud.get_all()[-1]
        stor_manager = StorM(storage)
        
        stor_manager.add_tool(new_tool)      

        assert self.tool_crud.get_all()[-1].id in self.stor_crud.get_tools(storage) 



    def test_add_construction(self):
        '''
        Тестирование метода по добавлению объекта строительства
        '''

        new_constr = self.generator.constr_generator()
        constr_manager = ConstrM(new_constr)

        assert self.constr_crud.get_all()[-1].id is constr_manager.constr.id



    def test_add_tool_in_construction_without_responsible(self):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        без ответственного лица
        '''

        with pytest.raises(ResponsibleAbsent):
            
            new_tool = self.generator.tool_generator()
            constr = self.constr_crud.get_all()[-1]
            
            constr_m = ConstrM(constr)
            constr_m.add_tool(new_tool)


    
    def test_add_worker(self):
        '''
        Тестирование метода по добавлению работника
        '''

        new_worker = self.generator.worker_generator()
        worker_manager = WorkM(new_worker)

        assert self.work_crud.get_all()[-1].id is worker_manager.worker.id



    def test_appointment_healthy_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''

        worker = self.work_crud.get_all()[-1]
        assert worker.status

        constr = self.constr_crud.get_all()[-1]
        assert not self.constr_crud.get_responsible(constr)

        constr_m = ConstrM(constr)
        constr_m.appointment_responsible(worker)
        
        assert self.work_crud.is_brigadir(worker).id is constr.id
        assert self.constr_crud.get_responsible(constr).id is worker.id
    


    def test_add_tool_in_construction_with_responsible(self):
        '''
        Тестирование метода по добавлению 
        инструмента на объект строительства
        без с имеющимся ответственным лицом
        '''

        new_tool = self.generator.tool_generator()
        constr = self.constr_crud.get_all()[-1]
            
        constr_m = ConstrM(constr)
        constr_m.add_tool(new_tool)

        tool = self.tool_crud.get_all()[-1]
        
        assert tool.id in self.constr_crud.get_tools(constr_m.constr)



    def test_appointment_sick_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''

        constr = self.constr_crud.get_all()[-1]
        assert self.constr_crud.get_responsible(constr)

        worker = self.generator.worker_generator()
        worker_m = WorkM(worker)
        worker_m.get_sick() 
        
        sick_worker = self.work_crud.get_by_id(id=worker_m.worker.id)
        assert not sick_worker.status

        constr_m = ConstrM(constr)

        with pytest.raises(WorkerDoesntWork):
            constr_m.appointment_responsible(sick_worker)
        
        assert self.constr_crud.get_responsible(constr_m.constr).id!=sick_worker.id


    
    def test_appointment_engaged_responsible(self):
        '''
        Тестирование метода по назначению на объект ответственного 
        лица с уже имеющимся объектом и инструментами на нем
        '''
        
        old_constr = self.constr_crud.get_all()[-1]
        responsible = self.constr_crud.get_responsible(old_constr)
        assert responsible

        new_constr = self.generator.constr_generator()
        constr_m = ConstrM(new_constr)
        constr_m.appointment_responsible(responsible)

        assert self.constr_crud.get_responsible(constr_m.constr).id is responsible.id
        assert not self.constr_crud.get_responsible(old_constr)
        assert self.work_crud.is_brigadir(responsible).id is constr_m.constr.id



    def test_move_tool(self):
        '''
        Тестирование метода по перемещению работающего 
        инструмента со склада на объект
        '''

        new_storage = self.generator.storage_generator()
        stor_m = StorM(new_storage)

        # Создаем объект строительства
        new_constr = self.generator.constr_generator()
        constr_m = ConstrM(new_constr)

        # Создаем работника и назначаем его ответственным на объекте
        new_worker = self.generator.worker_generator()
        constr_m.appointment_responsible(WorkM(new_worker).worker)

        new_tool = self.generator.tool_generator()
        # Помещаем инструмент на склад
        stor_m.add_tool(new_tool)
        tool = self.tool_crud.get_all()[-1]

        assert tool.id in self.stor_crud.get_tools(stor_m.storage)

        tool_m = ToolM(tool)
        tool_m.move_tool_to_construction(constr_m.constr)
        
        assert tool.id in self.constr_crud.get_tools(constr_m.constr)    
        assert tool.id not in self.stor_crud.get_tools(stor_m.storage)

        

    def test_move_broken_tool(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со склада на объект
        '''
        storage = self.stor_crud.get_all()[-1]
        stor_m = StorM(storage)

        new_tool = self.generator.tool_generator()
        stor_m.add_tool(new_tool)

        tool = self.tool_crud.get_all()[-1]
        tool_m = ToolM(tool)
        tool_m.break_tool()

        assert not self.tool_crud.get_by_id(id=tool_m.tool.id).status

        constr = self.constr_crud.get_all()[-1]
        assert self.constr_crud.get_responsible(constr)

        with pytest.raises(ToolBroken):
            stor_m.move_tool_to_construction(self.tool_crud.get_by_id(tool.id), constr)

        assert tool.id not in self.constr_crud.get_tools(constr)



    def test_move_broken_tool_to_storage(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со объекта на склад
        '''

        constr = self.constr_crud.get_all()[-1]
        constr_m = ConstrM(constr)

        new_tool = self.generator.tool_generator()
        constr_m.add_tool(new_tool)

        tool = self.tool_crud.get_all()[-1]
        tool_m = ToolM(tool)
        tool_m.break_tool()

        storage = self.stor_crud.get_all()[-1]

        constr_m.move_tool_to_storage(tool, storage)

        assert tool.id not in self.constr_crud.get_tools(constr)
        assert tool.id in self.stor_crud.get_tools(storage)



    def test_remove_tool_from_stock(self):
        '''
        Удаление инструмента со склада
        '''
        

    
    def test_remove_tool_from_construction(self):
        '''
        Удаление инструмента с объекта строительства
        '''
        