from fastapi import APIRouter, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from app.service.user_account.account import AccountManager, Account
from app.api.dependencies import create_jwt_token, verify_jwt_token
from app.settings.settings import app_settings
from app.api.models.models import NewUser, User, UserEmail, Code
from app.errors.service_error.account_error import (IncorrectLogin, IncorrectPassword, 
                                                    LoginExists, CodeDoesntMatch, EmailExists)
from app.service.verification_code.code import SenderCode
from time import time



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
    return templates.TemplateResponse(request, "index.html", {"page_name":"Сервис EquipmentManager"})



@login_account.get("/registr")
async def registr(request:Request):
    '''
    Страница с полями для регистрации
    '''
    return templates.TemplateResponse(request, "registr.html", {"page_name":"Регистрация в EquipmentManager"})



@login_account.post("/registr")
async def new_user(new_user: NewUser):
    '''
    Регистрация пользователя
    '''
    try:
        account_manager = AccountManager(Account(login=new_user.login,
                                                password=new_user.password,
                                                email=new_user.email,
                                                timezone=new_user.timezone), new=True)
    
    except EmailExists as err:
        raise HTTPException(status_code=422, detail="This email is already in use") from err
    except LoginExists as err:
        raise HTTPException(status_code=422, detail="This login is already taken") from err
    
    return {"message": "Accaunt created"}



@login_account.get("/authorization")
async def authorization(request:Request):
    '''
    Страница с полями для входа
    '''
    return templates.TemplateResponse(request, "authorization.html", {"page_name":"Вход в EquipmentManager"})



@login_account.post("/login")
async def login(user: User):
    '''
    Вход
    '''
    try:
        account_manager = AccountManager(Account(login=user.login,
                                                password=user.password))
    except IncorrectPassword as err:
        raise HTTPException(status_code=401, detail="Wrong password") from err
    except IncorrectLogin as err:
        raise HTTPException(status_code=401, detail="Wrong login") from err
    
    token = create_jwt_token({"user_id": account_manager.account.id})
    return {"token": token}



@login_account.post("/confirmation_code")
async def confirmation_code(email: UserEmail, sender:SenderCode = Depends(SenderCode)):
    '''
    При регистрации на сайте, будет отпревлен пятизначный код
    на почту, которую указал пользователь.
    '''
    confirmation_code = sender.send_code(email.email)

    code_token = create_jwt_token({"code": confirmation_code.code, "lifetime": confirmation_code.lifetime, "start_time": time()})
    
    return {"code": code_token}



@login_account.post("/check_confirmation_code")
async def check_confirmation_code(data:Code):
    '''
    Проверка кода подтверждения аккаунта
    '''
    
    try:
        jwt_data = verify_jwt_token(data.jwt)
    except HTTPException:
        raise HTTPException(status_code=419, detail="Incorrect token with source code")

    # Если истекло время ожидания кода
    if time()-int(jwt_data["start_time"])>int(jwt_data["lifetime"]):
        raise HTTPException(status_code=419, detail="Code lifetime has expired")
    
    # Если код неверный
    elif int(jwt_data["code"])!=int(data.code):
        raise HTTPException(status_code=419, detail="Wrong code")

    return {"message": "Email has been successfully verified"}