from app.entities.tool import Tool
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import StorageTable
from app.database.tables.essence import ToolTable
from app.database.tables.summary import ToolsOnStorage
from sqlalchemy.orm import Session


class StorageCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=StorageTable)


    @BaseCRUD.logger.info
    def get_tools(self, storage:Storage) -> dict:
        '''
        Получить инструменты на складе 


        Выдает словарь в виде id: Tool 
        '''
        
        with Session(autoflush=False, bind=self.engine) as db:

            tools_id = db.query(ToolsOnStorage.tool_id).filter(ToolsOnStorage.place_id==storage.id).all()
            result = {item[0]: self.coverter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result