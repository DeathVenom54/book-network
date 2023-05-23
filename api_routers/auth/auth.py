from fastapi import APIRouter, Form, Response, Request, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated

router = APIRouter(prefix='/api/auth')

class RequiresLoginException(Exception):
    pass

async def current_user(req: Request):
    token = req.cookies.get('token')
    if token == 'fake-cookie-token':
        return 'dv'
    else:
        raise RequiresLoginException()

CurrentUserDep = Annotated[str, Depends(current_user)]

@router.post('/login')
async def login(response: Response, username: str = Form(), password: str = Form()):
    # TODO replace with actual auth at some point
    if username == 'dv' and password == 'dv':
        res = RedirectResponse(url='/', status_code=302)
        res.set_cookie(key='token', value='fake-cookie-token')
        return res
    else:
        return RedirectResponse(url='/login')