from app.entities.tool import Tool
from app.entities.storage import Storage
from app.database.crud.baseCRUD import BaseCRUD
from app.database.tables.essence import StorageTable
from app.database.tables.essence import ToolTable
from app.database.tables.summary import ToolsOnStorage
from sqlalchemy.orm import Session
from app.database.database import Database


class StorageCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с БД
    '''

    def __init__(self) -> None:
        
        super().__init__(table=StorageTable)


        
    def __repr__(self) -> str:
        return f"{__class__.__name__}"



    @BaseCRUD.logger.info
    def get_tools(self, storage_id:int) -> dict:
        '''
        Получить инструменты на складе 


        Выдает словарь в виде id: Tool 
        '''
        
        with Database() as db:

            tools_id = db.query(ToolsOnStorage.tool_id).filter(ToolsOnStorage.place_id==storage_id, ToolsOnStorage.DT_end==None).all()
            result = {item[0]: self.converter.conversion_to_data(db.get(ToolTable, item)) for item in tools_id}

        return result