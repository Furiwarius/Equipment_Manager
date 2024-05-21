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
        
        tool = TestSK.generator.tool_renerator()
        TestSK.storekeeper.add_tool(tool=tool, storage=storage)
        assert tool.get_construction()
        assert tool.get_id() in storage.get_tools() and tool.get_id() in TestSK.storekeeper.get_id_tools()