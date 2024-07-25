from app.entities.account import Account
from app.loggers.database_logger.db_logger import DatabaseLogger
from app.database.tables.essence import Base, AccountTable
from app.database.database import Database
from app.database.converter import Converter
from app.database.crud.baseCRUD import BaseCRUD
from app.errors.service_error.account_error import LoginExists, EmailExists



class AccountCRUD(BaseCRUD):
    '''
    Класс управления бд
    '''
    
    
    def __init__(self) -> None:
        super().__init__(table=AccountTable)



    def __repr__(self) -> str:
        return f"{__class__.__name__}"



    @BaseCRUD.logger.info
    def add(self, account:Account) -> Account:
        '''
        Добавить сущности
        '''
        account = self.converter.conversion_to_table(account)
        with Database() as db:

            db.add(account)     # добавляем в бд
            db.commit()     # сохраняем изменения
            
            result = db.query(AccountTable).order_by(AccountTable.id.desc()).first()

        return self.converter.conversion_to_data(result)



    @BaseCRUD.logger.info
    def get_account_by_login(self, login:str) -> Account|None:
        '''
        Получение данных об аккаунте по логину

        login передаются в виде hash
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.login==login).all()

        if account:
            return self.converter.conversion_to_data(account[0])



    @BaseCRUD.logger.info
    def get_account_by_email(self, email:str) -> Account|None:
        '''
        Получение данных лю аккаунте по адресу почты
        '''
        with Database() as db:
            account = db.query(self.table).filter(AccountTable.email==email).all()
            
        if account:
            return self.converter.conversion_to_data(account[0])



    @BaseCRUD.logger.info
    def get_all(self) -> list:
        '''
        Получить id сущностей

        Метод смотрит поле table,
        и по нему ищет данные в БД
        '''

        with Database() as db:
            result = db.query(self.table.id).all()
            result = [item[0] for item in result]

        return list(result)

    

    @BaseCRUD.logger.info
    def modify_status(self, account_id:int) -> None:
        '''
        Подтвердить аккаунт
        '''
        with Database() as db:
            db.query(self.table).filter(self.table.id == account_id).update({self.table.confirmation_status:True}, synchronize_session = False)
            db.commit()


    
    @BaseCRUD.logger.info
    def check_data(self, email:str, login:str) -> None:
        '''
        Проверка логина и адреса почты на уникальность

        Делается это в одном методе
        '''
        with Database() as db:
            account = db.query(AccountTable).filter(AccountTable.email==email).all()
            if account: 
                raise EmailExists
            
            account = db.query(AccountTable).filter(AccountTable.login==login).all()
            if account:
                raise LoginExists
            


    def retire(self) -> None:
        '''
        AccountCRUD наследует от BaseCRUD этот метод,
        но не использует его
        '''
