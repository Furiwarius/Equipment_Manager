from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.service.user_account.account import AccountManager, Account
from app.api.dependencies import create_jwt_token


login_account = APIRouter()
templates = Jinja2Templates(directory="app/templates")
staticfiles = StaticFiles(directory="app")
login_account.mount("/static", staticfiles, name="static")



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
async def new_user(login: str = Form(min_length=6, max_length=20),
                   password: str = Form(min_length=6, max_length=20),
                   email: str = Form(min_length=6, max_length=60),
                   timezone: str = Form()):
    '''
    Регистрация пользователя
    '''
    account_manager = AccountManager(Account(login=login,
                                             password=password,
                                             email=email,
                                             timezone=timezone),
                                    new=True,
                                    send_code=False)
    
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
async def login(login: str = Form(min_length=6, max_length=20),
                password: str = Form(min_length=6, max_length=20)):
    '''
    Вход
    '''
    account_manager = AccountManager(Account(login=login,
                                             password=password))
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}