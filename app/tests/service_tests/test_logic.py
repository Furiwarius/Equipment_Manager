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

    
    def test_add_tool(self):
        '''
        Тестирование метода по добавлению инструмента
        '''
        

    
    def test_add_worker(self):
        '''
        Тестирование метода по добавлению работника
        '''
        
    

    def test_add_construction(self):
        '''
        Тестирование метода по добавлению объекта строительства
        '''
        

    def test_appointment_healthy_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник здоров)
        '''
        
    

    def test_appointment_sick_responsible(self):
        '''
        Тестирование метода по назначению ответственного лица на объект (Работник болен)
        '''
        

    
    def test_appointment_engaged_responsible(self):
        '''
        Тестирование метода по назначению на объект ответственного 
        лица с уже имеющимся объектом и инструментами на нем
        '''
        
    

    def test_move_tool(self):
        '''
        Тестирование метода по перемещению работающего 
        инструмента со склада на объект
        '''
        
    

    def test_move_broken_tool(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со склада на объект
        '''


    def test_move_broken_tool_to_storage(self):
        '''
        Тестирование метода по перемещению сломанного
        инструмента со объекта на склад
        '''
        


    def test_remove_tool_from_stock(self):
        '''
        Удаление инструмента со склада
        '''
        

    
    def test_remove_tool_from_construction(self):
        '''
        Удаление инструмента с объекта строительства
        '''
        