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


    def test_get_by_id():
        '''
        Тест метода по получению сущности по id (Base.get_by_id())
        '''


    def test_add_construction():
        '''
        Тест метода по добавлению сущности (ConstructionCRUD.add())
        '''
    

    def test_add_storage():
        '''
        Тест метода по добавлению склада (StorageCRUD.add())
        '''

    
    def test_add_worker():
        '''
        Тест метода по добавлению работника (WorkerCRUD.add())
        '''
    

    def test_add_tool():
        '''
        Тест метода по добавлению инструмента (ToolCRUD.add())
        '''


    def test_get_all_item():
        '''
        Тест метода по получению всех сущностей (Base.get_all())
        '''
    

    def test_downgrade():
        '''
        Тестирование метода по изменению статуса на False (Base.downgrade())
        '''

    
    def test_increase():
        '''
        Тестирование метода по изменению статуса на True (Base.increase())
        '''