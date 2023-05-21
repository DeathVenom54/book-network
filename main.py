from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from handlers.auth import verify_token

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.middleware('http')
def auth_middleware(request: Request, call_next):
    token = request.cookies.get('token')
    if verify_token(token):
        return call_next(request)
    else:
        return RedirectResponse(url='/login')

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})