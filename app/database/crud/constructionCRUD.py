from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import ConstructionTable
from app.database.tables.essence import ToolTable
from app.database.tables.essence import WorkerTable
from sqlalchemy.orm import Session
from app.database.tables.summary import ToolsOnConstructions as ToolOnConstr
from app.database.tables.summary import WorksOnConstructions as WorkOnConstr
from datetime import datetime
from app.database.database import Database


class ConstructionCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=ConstructionTable)
    


    def __repr__(self) -> str:
        return f"{__class__.__name__}"
    


    @BaseCRUD.logger.info
    def get_tools(self, constr_id:int) -> dict:
        '''
        Получить инструменты на объекте 


        Выдает словарь в виде id: Tool 
        '''

        with Database() as db:

            tools_id = db.query(ToolOnConstr.tool_id).filter(ToolOnConstr.place_id==constr_id, ToolOnConstr.end_date==None).all()
            result = {item[0]: self.converter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result
    

    @BaseCRUD.logger.info
    def get_workers(self, constr_id:int) -> dict:
        '''
        Получить работников на объекте


        Выдает словарь в виде id: Worker
        '''

        with Database() as db:

            works_id = db.query(WorkOnConstr.worker_id).filter(WorkOnConstr.construction_id==constr_id, WorkOnConstr.end_date==None).all()
            result = {item[0]: self.converter.conversion_to_data(db.get(WorkerTable, item)) for item in works_id}

        return result
    
    
    @BaseCRUD.logger.info
    def get_responsible(self, constr_id:int) -> Worker:
        '''
        Получить ответственного на объекте
        '''
        
        with Database() as db:
            place = db.query(WorkOnConstr.worker_id).filter(WorkOnConstr.construction_id==constr_id, 
                                                                    WorkOnConstr.end_date==None,
                                                                    WorkOnConstr.is_brigadir==True).all()
            
            if place: 
                constr_id = db.get(WorkerTable, place[0])
                return self.converter.conversion_to_data(constr_id)

              
              
    @BaseCRUD.logger.info
    def transfer_worker(self,  constr_id:int, worker_id:int, brigadir:bool=False) -> None:
        '''
        Перевести работника на объект
        

        Если параметр brigadir=True, то этот работник
        будет ответственным на объекте 
        '''

        with Database() as db:
            
            location = self.__locate(db, worker_id)
            if location:
                self.__close_post(db, location)

            work_on_constr = WorkOnConstr(worker_id=worker_id,
                        construction_id=constr_id,
                        is_brigadir=brigadir)

            db.add(work_on_constr)
            db.commit()

    
    @BaseCRUD.logger.info
    def __locate(self, db:Session, worker_id:int) -> WorkOnConstr:
        '''
        Определить местоположение работника
        '''

        constr = db.query(WorkOnConstr).filter(WorkOnConstr.worker_id==worker_id,
                                                WorkOnConstr.end_date==None).all()

        if constr:
            return constr[0]
    

    @BaseCRUD.logger.info
    def __close_post(self, db:Session, location:WorkOnConstr) -> None:
        '''
        Записывает дату окончания работы 
        на объекте строительства
        '''

        db.query(WorkOnConstr).filter(WorkOnConstr.id == location.id
                                           ).update({WorkOnConstr.end_date:datetime.now()}, synchronize_session = False)