import pytest
from datetime import datetime
from app.service.construction.construction import Construction as Constr
from app.service.storage.storage import Storage
from app.service.worker.worker import Worker
from app.service.tool.tool import Tool
from app.tests.fake_data import DataGenerator


class TestBusinessLogic():
    '''
    Тестовый класс для Storekeeper и управляемых объектов
    '''

    generator = DataGenerator()


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
        