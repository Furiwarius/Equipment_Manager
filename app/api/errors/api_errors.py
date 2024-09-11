from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


api_errors = APIRouter()
templates = Jinja2Templates(directory="app/templates")
staticfiles = StaticFiles(directory="app")
api_errors.mount("/static", staticfiles, name="static")



@api_errors.get("/notfound", status_code=404)
def not_found(request:Request):
    return  templates.TemplateResponse("error404.html", {"request": request,
                                                    "page_name": "Страница не найдена"})



@api_errors.get("/server_error", status_code=500)
def server_error(request:Request):
    return  templates.TemplateResponse("error500.html", {"request": request,
                                                    "page_name": "Ошибка сервера"})