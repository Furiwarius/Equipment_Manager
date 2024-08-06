from fastapi.staticfiles import StaticFiles
from app.api import app

app.mount("/static", StaticFiles(directory="app/static"))