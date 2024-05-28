import pytest
from datetime import datetime
from app.service.essence.managers import Storekeeper
from app.tests.service_tests.fake_data import DataGenerator

# TestStorekeeper
class TestSK():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''

    generator = DataGenerator()
    stock = Storekeeper(user_id=1)


    def test_add_storage(self):
        '''
        Тестрирование метода по добавлению склада
        '''
        storage = self.generator.storage_generator()
        self.stock.add_storage(storage=storage)

        assert storage.get_id() in self.stock.storages.keys()
    
    
    def test_add_tool(self):
        '''
        Тестирование метода по добавлению инструмента
        '''
        storage = self.generator.storage_generator()
        self.stock.add_storage(storage=storage)
        
        tool = self.generator.tool_generator()
        self.stock.add_tool(tool=tool, storage=storage)
        assert tool.get_construction()==storage.get_id()
        assert tool.get_id() in storage.get_tools() and tool.get_id() in self.stock.get_id_tools()
        assert datetime.now()==tool.get_import_date()

    
    def test_add_worker(self):
        '''
        Тестирование метода по добавлению работника
        '''
        worker = self.generator.worker_generator()
        self.stock.add_worker(worker=worker)
        
        assert worker.get_id() in self.stock.get_id_workers()
    

    def test_add_construction(self):
        '''
        Тестирование метода по добавлению объекта строительства
        '''
        construction = self.generator.constr_generator()
        self.stock.add_construction(construction=construction)

        assert construction.get_id() in self.stock.get_id_construction()
    

    def test_appointment_healthy_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])
        worker = self.stock.get_worker_by_id(self.stock.get_id_workers()[0])
        
        self.stock.appointment_responsible(worker=worker, construction=construction)

        assert worker.get_id()==construction.get_worker() and worker.get_construction()==construction.get_id()
        assert datetime.now()==worker.get_date_work()
    

    def test_appointment_sick_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''
        sick_worker = self.generator.worker_generator()
        sick_worker.get_sick()
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])
        
        self.stock.appointment_responsible(worker=sick_worker, construction=construction)

        assert sick_worker.get_id()!=construction.get_worker()
        assert sick_worker.get_construction()!=construction.get_id()

    
    def test_appointment_engaged_responsible(self):
        '''
        Тестирование метода по назначению на объект ответственного 
        лица с уже имеющимся объектом и инструментами на нем
        '''
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])
        worker = self.stock.get_worker_by_id(construction.get_worker())

        new_constr = self.generator.constr_generator()
        self.stock.appointment_responsible(worker=worker,construction=new_constr)

        assert construction.get_worker()==worker.get_id()
        assert worker.get_construction()==construction.get_id()
        assert new_constr.get_worker()!=worker.get_id()
    

    def test_move_tool(self):
        '''
        Тестирование метода по перемещению работающего 
        инструмента со склада на объект
        '''
        tool = self.stock.get_tool_by_id(self.stock.get_id_tools()[0])
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])
        storage = self.stock.get_storage_by_id(tool.get_construction())

        self.stock.move_tool(tool=tool, where=construction)

        assert tool.get_construction()==construction.get_id()
        assert tool.get_id() in construction.get_tools()
        assert tool.get_id() not in storage.get_tools()
        assert datetime.now()==tool.get_import_date()
    

    def test_move_broken_tool(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со склада на объект
        '''
        broken_tool = self.generator.tool_generator()
        broken_tool.break_tool()
        
        storage = self.stock.get_storage_by_id(self.stock.get_id_storages()[0])
        self.stock.add_tool(tool=broken_tool, storage=storage)
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])

        self.stock.move_tool(tool=broken_tool, where=construction)

        assert broken_tool.get_id() in storage.get_tools()
        assert broken_tool.get_id() not in construction.get_tools()
        assert broken_tool.get_construction()==storage.get_id()


    def test_move_broken_tool_to_storage(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со объекта на склад
        '''
        construction = self.stock.get_construction_by_id(self.stock.get_id_construction()[0])
        tool = self.stock.get_tool_by_id(construction.get_tools()[0])
        tool.break_tool()
        storage = self.stock.get_storage_by_id(self.stock.get_id_storages()[0])
        
        self.stock.move_tool(tool=tool, where=storage)

        assert tool.get_id() in storage.get_tools() and tool.get_construction() is storage.get_id()
        assert tool.get_id() not in construction.get_tools()
        assert tool.get_import_date()==datetime.now()


    def test_remove_tool_from_stock(self):
        '''
        Удаление инструмента со склада
        '''
        tool = self.generator.tool_generator()
        storage = self.generator.storage_generator()
        self.stock.add_storage(storage)
        self.stock.add_tool(tool=tool, storage=storage)

        assert tool.get_id() in self.stock.get_id_tools() 
        assert storage.get_id() is tool.get_construction()

        self.stock.delete_tool(tool)

        assert tool.get_id() not in storage.get_tools()
        assert tool.get_id() not in self.stock.get_id_tools()

    
    def test_remove_tool_from_construction(self):
        '''
        Удаление инструмента с объекта строительства
        '''
        constr = self.stock.get_construction_by_id((self.stock.get_id_construction()[0]))
        tool = self.stock.get_tool_by_id(self.stock.get_id_tools()[0])
        self.stock.move_tool(tool=tool, where=constr)
        
        try:
            self.stock.delete_tool(tool)
        except AttributeError: 
            assert True