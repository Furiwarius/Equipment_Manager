import pytest
from app.service.essence.managers import Storekeeper
from app.tests.service_tests.fake_data import DataGenerator

# TestStorekeeper
class TestSK():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''

    generator = DataGenerator()
    storekeeper = Storekeeper(user_id=1)


    def test_add_storage(self):
        '''
        Тестрирование метода по добавлению склада
        '''
        storage = TestSK.generator.storage_generator()
        TestSK.storekeeper.add_storage(storage=storage)

        assert storage.get_id() in TestSK.storekeeper.storages.keys()
    
    
    def test_add_tool(self):
        '''
        Тестирование метода по добавлению инструмента
        '''
        storage = TestSK.generator.storage_generator()
        TestSK.storekeeper.add_storage(storage=storage)
        
        tool = TestSK.generator.tool_generator()
        TestSK.storekeeper.add_tool(tool=tool, storage=storage)
        assert tool.get_construction()==storage.get_id()
        assert tool.get_id() in storage.get_tools() and tool.get_id() in TestSK.storekeeper.get_id_tools()

    
    def test_add_worker(self):
        '''
        Тестирование метода по добавлению работника
        '''
        worker = TestSK.generator.worker_generator()
        TestSK.storekeeper.add_worker(worker=worker)
        
        assert worker.get_id() in TestSK.storekeeper.get_id_workers()
    

    def test_add_construction(self):
        '''
        Тестирование метода по добавлению объекта строительства
        '''
        construction = TestSK.generator.constr_generator()
        TestSK.storekeeper.add_construction(construction=construction)

        assert construction.get_id() in TestSK.storekeeper.get_id_construction()
    

    def test_appointment_healthy_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''
        construction = TestSK.storekeeper.get_construction_by_id(TestSK.storekeeper.get_id_construction()[0])
        worker = TestSK.storekeeper.get_worker_by_id(TestSK.storekeeper.get_id_workers()[0])
        
        TestSK.storekeeper.appointment_responsible(worker=worker, construction=construction)

        assert worker.get_id()==construction.get_worker() and worker.get_construction()==construction.get_id()
    

    def test_appointment_sick_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''
        sick_worker = TestSK.generator.worker_generator()
        sick_worker.get_sick()
        construction = TestSK.storekeeper.get_construction_by_id(TestSK.storekeeper.get_id_construction()[0])
        
        TestSK.storekeeper.appointment_responsible(worker=sick_worker, construction=construction)

        assert sick_worker.get_id()!=construction.get_worker()
        assert sick_worker.get_construction()!=construction.get_id()
    

    def test_move_tool(self):
        '''
        Тестирование метода по перемещению инструмента
        '''
        tool = TestSK.storekeeper.get_tool_by_id(TestSK.storekeeper.get_id_tools()[0])
        construction = TestSK.storekeeper.get_construction_by_id(TestSK.storekeeper.get_id_construction()[0])

        TestSK.storekeeper.move_tool(tool=tool, where=construction)

        assert tool.get_construction()==construction.get_id()
        assert tool.get_id() in construction.get_tools()