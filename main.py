from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from constants import DB_HOST, DB_USER, DB_PASSWORD
from models.Database import Database
from routers.api.auth import router as auth_router, RequiresLoginException
from routers.api.books import router as api_books_router
from routers.books import router as books_router
from routers.main import router as main_router

app = FastAPI()

db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
db.connect()
print('Connected to database')

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.exception_handler(RequiresLoginException)
async def requires_login_handler(request: Request, e: RequiresLoginException):
    return RedirectResponse(url='/login')

app.include_router(main_router)
app.include_router(auth_router)
app.include_router(api_books_router)
app.include_router(books_router)