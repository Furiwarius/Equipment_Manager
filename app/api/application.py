from fastapi import FastAPI
from app.api.routes.login_account import login_account
from app.api.routes.work_with_firm import work_with_firm
from app.api.errors.api_errors import api_errors


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
        self.app.include_router(work_with_firm)
        self.app.include_router(api_errors)

        return self.app