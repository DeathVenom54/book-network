from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from api_routers.auth.auth import CurrentUserDep

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get('/register')
def login(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.get('/logout')
def login(response: Response):
    response.delete_cookie(key='token', httponly=True)
    return RedirectResponse(url='/login')

@router.get("/")
def root(request: Request, user: CurrentUserDep):
    print(user)
    return templates.TemplateResponse('home.html', {'request': request})