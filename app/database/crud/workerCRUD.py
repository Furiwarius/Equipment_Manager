from app.entities.worker import Worker
from app.entities.construction import Construction
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import WorkerTable
from app.database.tables.essence import ConstructionTable as ConstrTable
from sqlalchemy.orm import Session
from app.database.tables.summary import WorksOnConstructions as WorkOnConstr
from app.database.database import Database
from app.utilities.converter import convertertation



class WorkerCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=WorkerTable)



    def __repr__(self) -> str:
        return f"{__class__.__name__}"       



    @convertertation
    @BaseCRUD.logger.info
    def get_construction(self, worker_id:int) -> Construction|None:
        '''
        Получить объект, на котором
        находится работник
        ''' 

        with Database() as db:
            place = db.query(WorkOnConstr.construction_id).filter(WorkOnConstr.worker_id==worker_id, 
                                                                  WorkOnConstr.end_date==None).all()

            if place:
                return db.get(ConstrTable, place[0])
                    


    @convertertation
    @BaseCRUD.logger.info
    def is_brigadir(self, worker_id:int) -> Construction:
        '''
        Метод, возвращающий объект, на котором 
        работник является ответственным.
        '''

        with Database() as db:
            place = db.query(WorkOnConstr.construction_id).filter(WorkOnConstr.worker_id==worker_id, 
                                                                  WorkOnConstr.end_date==None,
                                                                  WorkOnConstr.is_brigadir==True).all()
            
            if place: 
                return db.get(ConstrTable, place[0])
                
