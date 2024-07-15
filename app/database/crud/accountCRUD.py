from app.entities.account import Account
from app.loggers.database_logger.db_logger import DatabaseLogger
from app.database.tables.essence import Base, AccountTable
from app.database.database import Database




class AccountCRUD():
    '''
    Класс управления бд
    '''

    logger = DatabaseLogger()
    logger.get_logger()
    
    
    
    def __init__(self) -> None:
        self.table = AccountTable



    def __repr__(self) -> str:
        return f"{__class__.__name__}"



    @logger.info
    def get_account(self, login:str, password:str) -> Account:
        '''
        Получение данных об аккаунте по логину

        login и password передаются в виде hash
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.login==login, 
                                                                  AccountTable.password==password).all()
            
        return account[0]



    @logger.info
    def add_account(self, login:str, password:str, email:str, timezone:str) -> Account:
        '''
        Добавить аккаунт в БД

        login и password приходят в виде hash
        timezone приходит в виде строки Europe/Moscow
        '''

        with Database() as db:
            new_account = AccountTable(login=login,
                                       password=password,
                                       email=email,
                                       timezone=timezone)
            db.add(new_account)
            db.commit()

    

    @logger.info
    def confirm(self, account_id:int) -> None:
        '''
        Подтвердить аккаунт
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == account_id).update({self.table.confirmation_status:True}, synchronize_session = False)
            db.commit()
