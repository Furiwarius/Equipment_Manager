from fastapi import APIRouter, Depends,  Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


login_account = APIRouter()
templates = Jinja2Templates(directory="app/templates")
staticfiles = StaticFiles(directory="app")
login_account.mount("/static", staticfiles, name="static")


@login_account.get("/")
async def index(request:Request):

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "page_name":"Сервис EquipmentManager"})