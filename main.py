from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from api_routers.auth.auth import router as auth_router, RequiresLoginException
from database.Database import Database
from database.db import connect_to_db
from routers.main import router as main_router

app = FastAPI()
connect_to_db()

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.exception_handler(RequiresLoginException)
async def requires_login_handler(request: Request, e: RequiresLoginException):
    return RedirectResponse(url='/login')

app.include_router(main_router)
app.include_router(auth_router)
