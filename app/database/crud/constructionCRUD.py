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


class ConstructionCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=ConstructionTable)
    

    @BaseCRUD.logger.info
    def get_tools(self, constr:Construction) -> dict:
        '''
        Получить инструменты на объекте 


        Выдает словарь в виде id: Tool 
        '''

        with Session(autoflush=False, bind=self.engine) as db:

            tools_id = db.query(ToolOnConstr.tool_id).filter(ToolOnConstr.place_id==constr.id, ToolOnConstr.DT_end==None).all()
            result = {item[0]: self.coverter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result
    

    @BaseCRUD.logger.info
    def get_workers(self, constr:Construction) -> dict:
        '''
        Получить работников на объекте


        Выдает словарь в виде id: Worker
        '''

        with Session(autoflush=False, bind=self.engine) as db:

            tools_id = db.query(WorkOnConstr.worker_id).filter(WorkOnConstr.construction_id==constr.id, WorkOnConstr.DT_end==None).all()
            result = {item[0]: self.coverter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result
    
    
    @BaseCRUD.logger.info
    def get_responsible(self, constr:Construction) -> Worker:
        '''
        Получить ответственного на объекте
        '''
        
        with Session(autoflush=False, bind=self.engine) as db:
            place = db.query(WorkOnConstr.worker_id).filter(WorkOnConstr.construction_id==constr.id, 
                                                                    WorkOnConstr.DT_end==None,
                                                                    WorkOnConstr.is_brigadir==True).all()
            
            if place: 
                constr = db.get(WorkerTable, place[0])
                return self.coverter.conversion_to_data(constr)


    @BaseCRUD.logger.info
    def transfer_worker(self,  constr:Construction, worker:Worker, brigadir:bool=False) -> None:
        '''
        Перевести работника на объект
        

        Если параметр brigadir=True, то этот работник
        будет ответственным на объекте 
        '''

        with Session(autoflush=False, bind=self.engine) as db:
            
            location = self.__locate(db, worker)
            if location:
                self.__close_post(db, location)

            work_on_constr = WorkOnConstr(worker_id=worker.id,
                        construction_id=constr.id,
                        is_brigadir=brigadir,
                        DT_start=datetime.now(),
                        DT_end=None)

            db.add(work_on_constr)
            db.commit()

    
    @BaseCRUD.logger.info
    def __locate(self, db:Session, worker:Worker) -> WorkOnConstr:
        '''
        Определить местоположение работника
        '''

        constr = db.query(WorkOnConstr).filter(WorkOnConstr.worker_id==worker.id,
                                                WorkOnConstr.DT_end==None).all()

        if constr:
            return constr[0]
    

    @BaseCRUD.logger.info
    def __close_post(self, db:Session, location:WorkOnConstr) -> None:
        '''
        Записывает дату окончания работы 
        на объекте строительства
        '''

        db.query(WorkOnConstr).filter(WorkOnConstr.id == location.id
                                           ).update({WorkOnConstr.DT_end:datetime.now()}, synchronize_session = False)