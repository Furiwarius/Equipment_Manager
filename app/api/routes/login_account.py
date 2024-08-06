from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from app.service.user_account.account import AccountManager, Account
from app.api.dependencies import create_jwt_token
from app.settings.settings import app_settings
from app.api.models.models import NewUser, User


login_account = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@login_account.get('/favicon.ico', include_in_schema=False)
async def favicon():
    '''
    Возвращает иконку сайта
    '''
    return FileResponse(app_settings.favicon_path)



@login_account.get("/")
async def index(request:Request):
    '''
    Главная страница
    '''
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "page_name":"Сервис EquipmentManager"})



@login_account.get("/registr")
async def registr(request:Request):
    '''
    Страница с полями для регистрации
    '''
    return templates.TemplateResponse("registr.html", {"request": request,
                                                     "page_name":"Регистрация в EquipmentManager"})



@login_account.post("/registr")
async def new_user(new_user: NewUser):
    '''
    Регистрация пользователя
    '''
    account_manager = AccountManager(Account(login=new_user.login,
                                             password=new_user.password,
                                             email=new_user.email,
                                             timezone=new_user.timezone),
                                    new=True,
                                    send_code=False) #После разработки метода confirmation_code станет True
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}



@login_account.post("/confirmation-code") 
async def confirmation_code(code: int = Form(length=5)):
    '''
    Получение кода подтверждения
    '''
    # ПОКА В РАЗРАБОТКЕ!
    


@login_account.get("/authorization")
async def authorization(request:Request):
    '''
    Страница с полями для входа
    '''
    return templates.TemplateResponse("authorization.html", {"request": request,
                                                     "page_name":"Вход в EquipmentManager"})



@login_account.post("/login")
async def login(user: User):
    '''
    Вход
    '''
    account_manager = AccountManager(Account(login=user.login,
                                             password=user.password))
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}