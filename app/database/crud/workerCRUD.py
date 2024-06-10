from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import WorkerTable
from app.database.tables.essence import ConstructionTable as ConstrTable
from sqlalchemy.orm import Session
from app.database.tables.summary import WorksOnConstructions as WorkOnConstr


class WorkerCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=WorkerTable)
       
    
    def get_construction(self, worker:Worker) -> Construction|None:
        '''
        Получить объект, на котором
        находится работник
        ''' 

        with Session(autoflush=False, bind=self.engine) as db:
            place = db.get(WorkOnConstr, worker.id)

            if place:
                constr = db.get(ConstrTable, place.construction_id)
                return self.coverter.conversion_to_data(constr)

    

    def is_brigadir(self, worker:Worker) -> Construction:
        '''
        Метод, возвращающий объект, на котором 
        работник является ответственным.
        '''

        with Session(autoflush=False, bind=self.engine) as db:
            place = db.query(WorkOnConstr.construction_id).filter(WorkOnConstr.worker_id==worker.id, 
                                                                  WorkOnConstr.DT_end==None,
                                                                  WorkOnConstr.is_brigadir==True).all()
            
            if place: 
                constr = db.get(ConstrTable, place[0])
                return self.coverter.conversion_to_data(constr)
