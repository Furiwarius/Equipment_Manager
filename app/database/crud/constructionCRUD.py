from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ConstructionTable
from app.database.tables.essence import ToolTable
from sqlalchemy.orm import Session
from app.database.tables.summary import ToolsOnConstructions as ToolOnConstr
from app.database.tables.summary import WorksOnConstructions as WorkOnConstr

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

        with Session(autoflush=False, bind=self.engine) as db:

            tools_id = db.query(ToolOnConstr.tool_id).filter(ToolOnConstr.construction_id==constr.id).all()
            result = {item[0]: self.coverter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result
    

    def get_workers(self, constr:Construction) -> dict:
        '''
        Получить работников на объекте


        Выдает словарь в виде id: Worker
        '''

        with Session(autoflush=False, bind=self.engine) as db:

            tools_id = db.query(WorkOnConstr.worker_id).filter(WorkOnConstr.construction_id==constr.id).all()
            result = {item[0]: self.coverter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result
    
    
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
