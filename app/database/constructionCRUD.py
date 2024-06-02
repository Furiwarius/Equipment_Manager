from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction

class ConstructionCRUD():
    '''
    Класс для взаимодействия с БД
    '''


    def add_construction(self, construction:Construction) -> None:
        '''
        Добавить объект строительства
        '''


    def get_tools(self, constr:Construction) -> dict:
        '''
        Получить инструменты на объекте 


        Выдает словарь в виде id: Tool 
        '''
        
        return {Tool.id: Tool}
    

    def get_workers(self, constr:Construction) -> dict:
        '''
        Получить работников на объекте


        Выдает словарь в виде id: Worker
        '''

        return {Worker.id: Worker}
    
    
    def get_responsible(self, constr:Construction) -> Worker:
        '''
        Получить ответственного на объекте
        '''

        return Worker


    def add_tool(self,  constr:Construction, tool:Tool) -> None:
        '''
        Перевезти инструмент на этот объект
        '''


    def add_worker(self,  constr:Construction, worker:Worker, brigadir:bool) -> None:
        '''
        Перевести работника на этот объект
        

        Если параметр brigadir=True, то этот работник
        будет ответственным на объекте 
        '''


    def close_construction(self, constr:Construction) -> None:
        '''
        Закрыть объект
        '''


    def open_construction(self, constr:Construction) -> None:
        '''
        Возобновить работу
        '''