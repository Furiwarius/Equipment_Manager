from fastapi import FastAPI
from app.api.routes.login_account import login_account


class Application():
    '''
    Приложение
    '''

    def create_app(self) -> FastAPI:
        '''
        Создание приложения
        '''
        self.app = FastAPI()
        self.app.include_router(login_account)

        return self.app