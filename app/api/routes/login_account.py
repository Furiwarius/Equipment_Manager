from fastapi import APIRouter, Depends,  Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.service.user_account.account import AccountManager, Account
from app.database.crud.accountCRUD import AccountCRUD
from app.api.models.models import User, NewUser, Code
from app.utilities.hashing import to_hash
from app.api.dependencies import create_jwt_token, verify_jwt_token


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
async def new_user(user:NewUser, timezone:str):
    '''
    Регистрация пользователя
    '''
    account_manager = AccountManager(Account(login=user.login,
                                             password=user.password,
                                             email=user.email,
                                             timezone=timezone),
                                    new=True)
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}



@login_account.post("/confirmation-code") 
async def confirmation_code(code:Code):
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
async def login(user:User):
    '''
    Вход
    '''
    login, password = to_hash(user.login), to_hash(user.password)
    account_manager = AccountManager(Account(login=login,
                                             password=password))
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}