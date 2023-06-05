from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from models.Book import UserBook
from routers.api.auth import CurrentUserDep

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
    userbooks = UserBook.get_books_for_user(user.username)
    print(userbooks)
    return templates.TemplateResponse('home.html', {'request': request, 'user': user.__dict__})