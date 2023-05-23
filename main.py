from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from api_routers.auth.auth import router as auth_router, RequiresLoginException
from routers.main import router as main_router

app = FastAPI()

# non_auth_routes = ['/login', '/register', '/api/auth/login', '/api/auth/register']

# @app.middleware('http')
# async def auth_middleware(request: Request, call_next):
#     if request.url.path in non_auth_routes:
#         return await call_next(request)
#     token = request.cookies.get('token')
#     if token:
#         return await call_next(request)
#     else:
#         print(f'no token found for {request.url.path}')
#         return RedirectResponse(url='/login')

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.exception_handler(RequiresLoginException)
async def requires_login_handler(request: Request, e: RequiresLoginException):
    return RedirectResponse(url='/login')

app.include_router(main_router)
app.include_router(auth_router)
