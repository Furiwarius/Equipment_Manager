import pytest
from app.service.essence.managers import Storekeeper
from app.tests.service_tests.fake_data import DataGenerator


class TestClass():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''

    generator = DataGenerator()


    def test_add_storage(self):
        '''
        Тестрирование метода по добавлению склада
        '''
        storekeeper = Storekeeper(user_id=1)
        storage = TestClass.generator.storage_generator()
        storekeeper.add_storage(storage=storage)
        assert storage.get_id() in storekeeper.storages.keys()