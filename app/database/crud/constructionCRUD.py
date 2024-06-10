from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ConstructionTable


class ConstructionCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=ConstructionTable)
    

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


    def transfer_worker(self,  constr:Construction, worker:Worker, brigadir:bool) -> None:
        '''
        Перевести работника на объект
        

        Если параметр brigadir=True, то этот работник
        будет ответственным на объекте 
        '''
