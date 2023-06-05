from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Form, Response, Request, Depends
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from passlib.context import CryptContext

from models.Database import UserExistsException, Database


class StatusCode:
    UserExists = 600
    IncorrectCredentials = 601

router = APIRouter(prefix='/api/auth')

SECRET_KEY = "f1d704df981cf3bfe15e6fd5204697f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 week

class RequiresLoginException(Exception): ...

async def current_user(req: Request):
    db = Database()
    token = req.cookies.get('token')
    if token is None:
        raise RequiresLoginException()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        if username is None:
            raise RequiresLoginException()
        user = db.get_user(username)
        if user is None:
            raise RequiresLoginException()
        if payload.get('last_ip') != req.client.host:
            raise RequiresLoginException()
        return user
    except JWTError:
        raise RequiresLoginException()

CurrentUserDep = Annotated[str, Depends(current_user)]

@router.post('/login')
async def login(req: Request, username: str = Form(), password: str = Form()):
    db = Database()
    user = db.get_user(username)
    if user and pwd_context.verify(password, user.password):
        res = RedirectResponse(url='/', status_code=302)
        res.set_cookie(key='token', value=create_token(username, req.client.host))
        return res
    else:
        return RedirectResponse(url='/login', status_code=302)

@router.post('/register')
async def login(req: Request, username= Form(), password= Form(), display_name = Form(default=None), bio = Form(default=None)):
    try:
        db = Database()
        print(id(db.db))
        db.create_user(username, hash_password(password), display_name, bio)
        res = RedirectResponse(url='/', status_code=302)
        res.set_cookie(key='token', value=create_token(username, req.client.host))
    except UserExistsException:
        return RedirectResponse(url='/register', status_code=302)

def create_token(username, ip):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({'username': username, 'last_ip': ip, 'exp': expires}, SECRET_KEY, algorithm=ALGORITHM)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password):
    return str(pwd_context.hash(password))