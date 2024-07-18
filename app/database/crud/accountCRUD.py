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
    def get_account_by_login(self, login:str) -> Account:
        '''
        Получение данных об аккаунте по логину

        login передаются в виде hash
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.login==login).all()
            
        return account[0]


    @logger.info
    def get_account_by_email(self, email:str) -> Account:
        '''
        Получение данных лю аккаунте по адресу почты
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.email==email).all()
            
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

            result = db.query(self.table).order_by(self.table.id.desc()).first()
        
        return result

    

    @logger.info
    def confirm(self, account_id:int) -> None:
        '''
        Подтвердить аккаунт
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == account_id).update({self.table.confirmation_status:True}, synchronize_session = False)
            db.commit()
