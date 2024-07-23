from app.entities.account import Account
from app.loggers.database_logger.db_logger import DatabaseLogger
from app.database.tables.essence import Base, AccountTable
from app.database.database import Database
from app.database.converter import Converter
from app.database.crud.baseCRUD import BaseCRUD



class AccountCRUD(BaseCRUD):
    '''
    Класс управления бд
    '''
    
    
    def __init__(self) -> None:
        super().__init__(table=AccountTable)



    def __repr__(self) -> str:
        return f"{__class__.__name__}"



    @BaseCRUD.logger.info
    def get_account_by_login(self, login:str) -> Account:
        '''
        Получение данных об аккаунте по логину

        login передаются в виде hash
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.login==login).all()
            
        return self.converter.conversion_to_data(account[0])


    @BaseCRUD.logger.info
    def get_account_by_email(self, email:str) -> Account:
        '''
        Получение данных лю аккаунте по адресу почты
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.email==email).all()
            
        return self.converter.conversion_to_data(account[0])

    

    @BaseCRUD.logger.info
    def modify_status(self, account_id:int) -> None:
        '''
        Подтвердить аккаунт
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == account_id).update({self.table.confirmation_status:True}, synchronize_session = False)
            db.commit()

    

    def retire(self) -> None:
        '''
        AccountCRUD наследует от BaseCRUD этот метод,
        но не использует его
        '''
